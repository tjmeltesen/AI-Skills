"""Offline behavioral checks for installation planning and failure handling."""

import subprocess
import json
import sys
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch

# Ensure the scripts directory is on sys.path for direct or discovered test runs.
SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import bootstrap


class BootstrapTests(unittest.TestCase):
    def test_project_plan_targets_all_four_hosts(self):
        manifest = bootstrap.load_manifest()
        commands = bootstrap.install_commands(manifest, "npx", manifest["agents"])
        self.assertEqual(len(commands), 2)
        self.assertEqual(commands[0][4], str(bootstrap.ROOT))
        for agent in manifest["agents"]:
            self.assertIn(agent, commands[0])
        self.assertNotIn("cursor", commands[1])
        self.assertIn("--copy", commands[0])
        self.assertNotIn("--global", commands[0])

    def test_filtered_global_plan_only_installs_selected_agent(self):
        commands = bootstrap.install_commands(bootstrap.load_manifest(), "npx", ["gemini-cli"], True)
        self.assertEqual(len(commands), 2)
        for command in commands:
            self.assertIn("gemini-cli", command)
            self.assertIn("--global", command)
            self.assertNotIn("claude-code", command)
            self.assertNotIn("cursor", command)
            self.assertNotIn("codex", command)

    def test_bad_manifest_fails_before_execution(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "skills.yaml"
            path.write_text("version: 2\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                bootstrap.load_manifest(path)

    def test_lock_normalization_preserves_remote_dependencies(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "skills-lock.json"
            remote = {"source": "cursor/plugins", "sourceType": "github", "computedHash": "abc"}
            path.write_text(json.dumps({"version": 1, "skills": {
                "ponytail": {"source": str(bootstrap.ROOT), "sourceType": "local"},
                "poteto-mode": remote,
            }}), encoding="utf-8")
            bootstrap.normalize_local_lock(path)
            data = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(data["skills"]["ponytail"]["source"], ".")
            self.assertEqual(data["skills"]["poteto-mode"], remote)

    def test_dry_run_never_executes(self):
        with patch.object(sys, "argv", ["bootstrap.py", "--dry-run"]), \
                patch.object(bootstrap.subprocess, "run") as run:
            self.assertEqual(bootstrap.main(), 0)
            run.assert_not_called()

    def test_failed_install_stops_remaining_commands(self):
        failure = subprocess.CalledProcessError(1, ["npx"])
        with patch.object(sys, "argv", ["bootstrap.py"]), \
                patch.object(bootstrap.shutil, "which", return_value="npx"), \
                patch.object(bootstrap.subprocess, "run", side_effect=failure) as run:
            self.assertEqual(bootstrap.main(), 1)
            self.assertEqual(run.call_count, 1)


if __name__ == "__main__":
    unittest.main()
