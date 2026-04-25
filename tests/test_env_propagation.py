import os
import unittest
from unittest.mock import patch

import server


class ChildEnvPropagationTests(unittest.TestCase):
    def test_build_child_env_propagates_github_tokens_from_runtime_env(self):
        fake_env = {
            "PATH": "/usr/bin",
            "GITHUB_TOKEN": "runtime-ghp-token",
            "GH_TOKEN": "runtime-gh-token",
            "UNRELATED_SECRET": "should-not-pass",
        }

        with patch.dict(os.environ, fake_env, clear=True):
            child_env = server.build_child_env({})

        self.assertIn("GITHUB_TOKEN", child_env)
        self.assertIn("GH_TOKEN", child_env)
        self.assertNotIn("UNRELATED_SECRET", child_env)

    def test_build_child_env_prefers_env_file_values(self):
        fake_env = {
            "PATH": "/usr/bin",
            "GITHUB_TOKEN": "runtime-value",
            "GH_TOKEN": "runtime-value",
        }
        file_env = {
            "GITHUB_TOKEN": "file-value",
            "GH_TOKEN": "file-value",
        }

        with patch.dict(os.environ, fake_env, clear=True):
            child_env = server.build_child_env(file_env)

        self.assertEqual(child_env["GITHUB_TOKEN"], "file-value")
        self.assertEqual(child_env["GH_TOKEN"], "file-value")

    def test_token_presence_diagnostic_reports_booleans_only(self):
        status = server.token_presence_diagnostic({
            "GITHUB_TOKEN": "present",
            "GH_TOKEN": "",
        })
        self.assertEqual(status, {"GITHUB_TOKEN": True, "GH_TOKEN": False})


if __name__ == "__main__":
    unittest.main()
