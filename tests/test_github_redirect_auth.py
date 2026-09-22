"""Modules that build their own Request must not leak credentials on redirect.

``lib/http.py`` installs a redirect handler that drops credential headers when a
3xx changes origin, but that only protects callers that go through it. Several
modules build a ``urllib.request.Request`` themselves; ``github.py`` and
``transcribe.py`` attach a bearer token to theirs, so they must use
``http.open_request`` rather than ``urllib.request.urlopen``.
"""

import http.server
import socketserver
import threading
from urllib.request import Request

from lib import http as l30d_http


class _CaptureHandler(http.server.BaseHTTPRequestHandler):
    captured: dict = {}

    def do_GET(self):
        type(self).captured = {k.lower(): v for k, v in self.headers.items()}
        body = b'{"ok":true}'
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *_args):
        pass


def _serve(handler):
    httpd = socketserver.TCPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def test_open_request_strips_bearer_across_origin():
    attacker = _serve(_CaptureHandler)
    _CaptureHandler.captured = {}

    class Victim(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(302)
            self.send_header(
                "Location", f"http://127.0.0.1:{attacker.server_address[1]}/steal"
            )
            self.send_header("Content-Length", "0")
            self.end_headers()

        def log_message(self, *_args):
            pass

    victim = _serve(Victim)
    req = Request(
        f"http://127.0.0.1:{victim.server_address[1]}/start",
        headers={"Authorization": "Bearer ghp_sentinel_token"},
    )
    try:
        with l30d_http.open_request(req, 10) as resp:
            resp.read()
    finally:
        victim.shutdown()
        attacker.shutdown()

    assert "authorization" not in _CaptureHandler.captured, (
        "bearer token survived a cross-origin redirect: "
        f"{_CaptureHandler.captured.get('authorization')!r}"
    )


def test_credential_bearing_modules_do_not_call_urlopen_directly():
    """Regression guard: these modules attach a bearer token to their Request."""
    import pathlib

    lib = pathlib.Path(l30d_http.__file__).parent
    for name in ("github.py", "transcribe.py"):
        source = (lib / name).read_text(encoding="utf-8")
        assert "urllib.request.urlopen(" not in source, (
            f"{name} calls urllib.request.urlopen directly, bypassing the "
            "cross-origin credential strip"
        )
