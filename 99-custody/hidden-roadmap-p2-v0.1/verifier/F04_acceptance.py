import json
from pathlib import Path

from click.testing import CliRunner

from sqlite_utils import Database, Migrations, hookimpl, plugins
from sqlite_utils.cli import cli


def test_dependency_order_overrides_discovery_order(tmp_path):
    path = tmp_path / 'migrations.py'
    path.write_text(
        "from sqlite_utils import Migrations\n"
        "dependent=Migrations('dependent', depends_on=('prereq',))\n"
        "@dependent()\n"
        "def d(db): db['order'].insert({'name':'dependent'})\n"
        "prereq=Migrations('prereq')\n"
        "@prereq()\n"
        "def p(db): db['order'].insert({'name':'prereq'})\n",
        encoding='utf-8',
    )
    db_path = tmp_path / 'x.db'
    result = CliRunner().invoke(cli, ['migrate', str(db_path), str(path)])
    assert result.exit_code == 0, result.output
    db = Database(db_path)
    assert [r['name'] for r in db['order'].rows] == ['prereq', 'dependent']
    db.close()


def test_missing_dependency_cycle_and_duplicate_fail_before_apply(tmp_path):
    cases = {
        'missing': "a=Migrations('a', depends_on=('missing',))\n@a()\ndef one(db): db['effects'].insert({'x':1})\n",
        'cycle': "a=Migrations('a', depends_on=('b',))\nb=Migrations('b', depends_on=('a',))\n@a()\ndef one(db): db['effects'].insert({'x':1})\n@b()\ndef two(db): db['effects'].insert({'x':2})\n",
        'duplicate': "a=Migrations('dup')\nb=Migrations('dup')\n@a()\ndef one(db): db['effects'].insert({'x':1})\n@b()\ndef two(db): db['effects'].insert({'x':2})\n",
    }
    for name, body in cases.items():
        path = tmp_path / f'{name}.py'
        path.write_text('from sqlite_utils import Migrations\n' + body, encoding='utf-8')
        db_path = tmp_path / f'{name}.db'
        result = CliRunner().invoke(cli, ['migrate', str(db_path), str(path)])
        assert result.exit_code != 0
        if db_path.exists():
            db = Database(db_path)
            assert 'effects' not in db.table_names()
            db.close()


def test_dependency_order_used_by_plan_and_list_without_mutation(tmp_path):
    path = tmp_path / 'migrations.py'
    path.write_text(
        "from sqlite_utils import Migrations\n"
        "b=Migrations('b', depends_on=('a',))\n"
        "@b()\n"
        "def two(db): pass\n"
        "a=Migrations('a')\n"
        "@a()\n"
        "def one(db): pass\n",
        encoding='utf-8',
    )
    db_path = tmp_path / 'missing.db'
    plan = CliRunner().invoke(cli, ['migrate', str(db_path), str(path), '--plan-json'])
    assert plan.exit_code == 0, plan.output
    data = json.loads(plan.output)
    assert [x['migration_set'] for x in data] == ['a', 'b']
    assert data[1]['depends_on'] == ['a'] or data[1]['depends_on'] == ('a',)
    assert not db_path.exists()
    listed = CliRunner().invoke(cli, ['migrate', str(db_path), str(path), '--list'])
    assert listed.exit_code == 0
    assert not db_path.exists()


def test_dependency_can_cross_file_and_plugin_source(tmp_path):
    plugin_set = Migrations('plugin_core')

    @plugin_set()
    def p(db):
        db['order'].insert({'name':'plugin'})

    class Plugin:
        __name__ = 'DependencyVerifierPlugin'

        @hookimpl
        def register_migrations(self):
            return plugin_set

    plugins.pm.register(Plugin(), name='DependencyVerifierPlugin')
    try:
        path = tmp_path / 'migrations.py'
        path.write_text(
            "from sqlite_utils import Migrations\n"
            "m=Migrations('file_app', depends_on=('plugin_core',))\n"
            "@m()\n"
            "def f(db): db['order'].insert({'name':'file'})\n",
            encoding='utf-8',
        )
        db_path = tmp_path / 'x.db'
        result = CliRunner().invoke(cli, ['migrate', str(db_path), str(path), '--include-plugin-migrations'])
        assert result.exit_code == 0, result.output
        db = Database(db_path)
        assert [r['name'] for r in db['order'].rows] == ['plugin', 'file']
        db.close()
    finally:
        plugins.pm.unregister(name='DependencyVerifierPlugin')
