"""Contract tests for the /last30days HTML save handoff."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = ROOT / "skills" / "last30days" / "SKILL.md"
SAVE_HTML = ROOT / "skills" / "last30days" / "references" / "save-html-brief.md"


def test_skill_routes_html_to_reference_and_artifact_handoff():
    text = SKILL_MD.read_text(encoding="utf-8")
    start = text.index("## SHAREABLE HTML BRIEF")
    end = text.index("## WAIT FOR USER'S RESPONSE", start)
    section = text[start:end]

    assert "Read `references/save-html-brief.md`" in section
    assert "artifact handoff" in section
    assert "local open/view affordance" in section
    assert "Upload or publish" in section
    assert "Append the confirmation line" not in section


def test_explicit_html_export_is_artifact_first_not_full_markdown_repeat():
    text = SAVE_HTML.read_text(encoding="utf-8")
    assert "**Explicit HTML export**" in text
    assert "the HTML artifact is the primary output" in text
    assert "do **not** paste the full Markdown report back into chat" in text
    assert "The user asked for a file" in text


def test_html_handoff_includes_local_open_commands_without_requiring_success():
    text = SAVE_HTML.read_text(encoding="utf-8")
    for snippet in [
        'open "<absolute HTML path>"',
        'xdg-open "<absolute HTML path>"',
        'start "" "<absolute HTML path>"',
        "If the command fails or the host is headless",
    ]:
        assert snippet in text


def test_html_save_flow_does_not_publish_or_upload():
    text = SAVE_HTML.read_text(encoding="utf-8")
    assert "Do not offer public publishing or upload in this flow" in text
    assert "Do NOT publish, upload, or send the HTML to a third-party service" in text
