"""Offline tests for the Codex project skill importer. No external services."""
from pathlib import Path
import stat
import sys
import tempfile
import unittest
from zipfile import ZipFile, ZipInfo

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from import_codex_skill_bridge import EXPECTED, ImportErrorSafe, import_bridge


def make_zip(target, missing=None, malicious=None):
    with ZipFile(target, 'w') as z:
        for name in sorted(EXPECTED):
            if name == missing:
                continue
            data = f'---\nname: {name}\ndescription: "Use for {name}."\n---\n\nInstructions\n'
            z.writestr(f'private-bundle/skills/{name}/SKILL.md', data)
            z.writestr(f'private-bundle/skills/{name}/references/example.md', 'Example')
        if malicious:
            if malicious == 'symlink':
                i = ZipInfo('private-bundle/skills/role-evaluation/scripts/malicious')
                i.create_system = 3
                i.external_attr = (stat.S_IFLNK | 0o777) << 16
                z.writestr(i, '../../../../../secret')
            else:
                z.writestr(malicious, 'bad')


class ImporterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'project'
        self.root.mkdir()
        self.archive = Path(self.temp.name) / 'bridge.zip'
        make_zip(self.archive)

    def test_dry_run_does_not_write(self):
        data = import_bridge(self.archive, self.root, 'dry-run')
        self.assertEqual(data['status'], 'dry_run')
        self.assertFalse((self.root / '.agents').exists())

    def test_install_and_readback(self):
        data = import_bridge(self.archive, self.root, 'install')
        self.assertTrue(data['all_six_present'])
        self.assertEqual(len(list((self.root / '.agents' / 'skills').glob('*/SKILL.md'))), 6)
        confirm = import_bridge(self.archive, self.root, 'verify')
        self.assertTrue(all(v == 'unchanged' for v in confirm['skills'].values()))

    def test_conflict_preflight_prevents_partial_write(self):
        existing = self.root / '.agents' / 'skills' / 'role-evaluation'
        existing.mkdir(parents=True)
        (existing / 'SKILL.md').write_text('not the supplied skill')
        with self.assertRaisesRegex(ImportErrorSafe, 'refusing overwrite'):
            import_bridge(self.archive, self.root, 'install')
        self.assertFalse((self.root / '.agents' / 'skills' / 'engineering-closure').exists())

    def test_missing_skill_is_rejected(self):
        make_zip(self.archive, missing='verified-deliverable')
        with self.assertRaisesRegex(ImportErrorSafe, 'Skill mismatch'):
            import_bridge(self.archive, self.root, 'install')

    def test_path_traversal_is_rejected(self):
        make_zip(self.archive, malicious='../escape')
        with self.assertRaisesRegex(ImportErrorSafe, 'Unsafe'):
            import_bridge(self.archive, self.root, 'install')

    def test_symlink_archive_member_is_rejected(self):
        make_zip(self.archive, malicious='symlink')
        with self.assertRaisesRegex(ImportErrorSafe, 'symbolic link'):
            import_bridge(self.archive, self.root, 'install')

    def test_verify_absent_fails(self):
        with self.assertRaisesRegex(ImportErrorSafe, 'Missing installed'):
            import_bridge(self.archive, self.root, 'verify')

    def test_tampering_detected(self):
        import_bridge(self.archive, self.root, 'install')
        file = self.root / '.agents' / 'skills' / 'role-evaluation' / 'SKILL.md'
        file.write_text(file.read_text() + 'changed')
        with self.assertRaisesRegex(ImportErrorSafe, 'refusing overwrite'):
            import_bridge(self.archive, self.root, 'verify')


if __name__ == '__main__':
    unittest.main()
