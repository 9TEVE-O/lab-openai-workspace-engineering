"""Stdlib-only adversarial tests for the evidence publishing gate."""
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

MODULE = Path(__file__).with_name("check_evidence_publication.py")
spec = importlib.util.spec_from_file_location("gate", MODULE)
gate = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(gate)


class EvidenceGateTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "results"
        self.root.mkdir()

    def file(self, name):
        p = self.root / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("synthetic test content", encoding="utf8")
        return p

    def test_clean_browser_report_passes(self):
        for name in gate.ALLOWED_VAULT_FILES:
            self.file(name)
        self.assertEqual(gate.check_tree(self.root, "browser"), [])

    def test_green_browser_test_with_cookie_exposure_fails(self):
        # Test result remains nominally green while evidence includes a cookie DB.
        self.file("prompt-vault-import-report.json")
        self.file("01-before-import.png")
        self.file("isolated-browser-profile/Default/Cookies")
        self.assertTrue(gate.check_tree(self.root, "browser"))

    def test_extra_file_fails(self):
        self.file("prompt-vault-import-report.json")
        self.file("debug-dump.txt")
        self.assertTrue(gate.check_tree(self.root, "browser"))

    def test_symlink_rejected(self):
        self.file("prompt-vault-import-report.json")
        (self.root / "shortcut").symlink_to(self.root / "prompt-vault-import-report.json")
        self.assertTrue(gate.check_tree(self.root, "browser"))

    def test_missing_report_fails(self):
        self.file("01-before-import.png")
        self.assertTrue(gate.check_tree(self.root, "browser"))

    def test_clean_collected_model_and_browser_passes(self):
        self.file("prompt-vault-import/prompt-vault-import-report.json")
        self.file("prompt-vault-import/02-after-import.png")
        self.file("model-qwen/result.json")
        self.assertEqual(gate.check_tree(self.root, "collected"), [])

    def test_unsafe_collected_profile_fails(self):
        self.file("prompt-vault-import/prompt-vault-import-report.json")
        self.file("prompt-vault-import/isolated-browser-profile/Default/Cookies")
        self.assertTrue(gate.check_tree(self.root, "collected"))

    def test_unsafe_profile_hidden_in_model_fails(self):
        self.file("model-qwen/session storage/leveldb/000003.log")
        self.assertTrue(gate.check_tree(self.root, "collected"))

    def test_collected_without_vault_preserves_model_failure_evidence(self):
        self.file("model-qwen/result.json")
        self.assertEqual(gate.check_tree(self.root, "collected"), [])

    def test_unrecognised_namespace_fails(self):
        self.file("other-artifact/secret.txt")
        self.assertTrue(gate.check_tree(self.root, "collected"))

    def test_symlink_root_fails(self):
        link = Path(self.temp.name) / "linked"
        link.symlink_to(self.root, target_is_directory=True)
        self.assertTrue(gate.check_tree(link, "browser"))


if __name__ == "__main__":
    unittest.main()
