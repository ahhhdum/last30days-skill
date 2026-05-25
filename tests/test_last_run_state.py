import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LAST30DAYS_SCRIPT = REPO_ROOT / "skills" / "last30days" / "scripts" / "last30days.py"


def run_last30days(topic: str, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(LAST30DAYS_SCRIPT), topic, "--mock", "--emit=json"],
        cwd=REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


class LastRunStateTests(unittest.TestCase):
    def test_empty_config_override_disables_last_run_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            env = os.environ.copy()
            env["HOME"] = str(home)
            env["LAST30DAYS_CONFIG_DIR"] = ""

            result = run_last30days("synthetic eval query", env)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse((home / ".config" / "last30days" / "last-run.json").exists())

    def test_custom_config_override_writes_last_run_to_custom_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            config_dir = Path(tmp) / "custom-config"
            env = os.environ.copy()
            env["HOME"] = str(Path(tmp) / "home")
            env["LAST30DAYS_CONFIG_DIR"] = str(config_dir)

            result = run_last30days("custom config query", env)

            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads((config_dir / "last-run.json").read_text())
            self.assertEqual(payload["topic"], "custom config query")
            self.assertGreaterEqual(payload["total"], 0)

    def test_hook_exits_zero_when_configured_without_last_run(self):
        # Regression: prior to fix, the trailing `[[ -n "$LAST_RUN_LINE" ]] && echo`
        # in the HAS_SCRAPECREATORS branch was the last command before EOF. When
        # last-run.json did not exist, the test returned 1, the && short-circuited,
        # and the script exited 1 (set -e does not trip on the left of &&). Claude
        # Code reported "SessionStart:startup hook error / No stderr output".
        with tempfile.TemporaryDirectory() as tmp:
            env = os.environ.copy()
            env["HOME"] = str(Path(tmp) / "home")
            env["LAST30DAYS_CONFIG_DIR"] = str(Path(tmp) / "empty-config")
            env["SCRAPECREATORS_API_KEY"] = "dummy"

            result = subprocess.run(
                ["bash", "hooks/scripts/check-config.sh"],
                cwd=REPO_ROOT,
                env=env,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Ready", result.stdout)
            self.assertNotIn("Last run", result.stdout)

    def test_hook_reads_last_run_from_custom_config_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            config_dir = Path(tmp) / "custom-config"
            config_dir.mkdir()
            (config_dir / "last-run.json").write_text(
                json.dumps(
                    {
                        "topic": "custom hook query",
                        "timestamp": "2026-04-30T00:00:00+00:00",
                        "sources": {"reddit": 2},
                        "total": 2,
                    }
                )
            )
            env = os.environ.copy()
            env["HOME"] = str(Path(tmp) / "home")
            env["LAST30DAYS_CONFIG_DIR"] = str(config_dir)

            result = subprocess.run(
                ["bash", "hooks/scripts/check-config.sh"],
                cwd=REPO_ROOT,
                env=env,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('Last run: "custom hook query"', result.stdout)


if __name__ == "__main__":
    unittest.main()
