import json
from pathlib import Path

from click.testing import CliRunner

from sqlite_utils import Migrations, hookimpl, plugins
from sqlite_utils.cli import cli


def _file_migrations(path: Path):
    path.write_text(
        "from sqlite_utils import Migrations\n"
        "m = Migrations('file_set')\n"
        "@m()\n"
        "def file_one(db): db['order'].insert({'name': 'file'})\n",
        encoding="utf-8",
    )


def _plugin(calls):
    m1 = Migrations("plugin_one")

    @m1()
    def p1(db):
        db["order"].insert({"name": "plugin_one"})

    m2 = Migrations("plugin_two")

    @m2()
    def p2(db):
        db["order"].insert({"name": "plugin_two"})

    class Plugin:
        __name__ = "VerifierMigrationPlugin"

        @hookimpl
        def register_migrations(self):
            calls.append("register")
            return [m1, m2]

    return Plugin()


def test_plugin_migrations_are_opt_in_and_called_once(tmp_path):
    calls = []
    plugin = _plugin(calls)
    plugins.pm.register(plugin, name="VerifierMigrationPlugin")
    try:
        path = tmp_path / "migrations.py"
        _file_migrations(path)
        db = tmp_path / "x.db"
        result = CliRunner().invoke(cli, ["migrate", str(db), str(path)])
        assert result.exit_code == 0, result.output
        assert calls == []

        result = CliRunner().invoke(
            cli,
            ["migrate", str(db), str(path), "--include-plugin-migrations", "--plan-json"],
        )
        assert result.exit_code == 0, result.output
        assert calls == ["register"]
        data = json.loads(result.output)
        assert [x["migration_set"] for x in data] == [
            "file_set",
            "plugin_one",
            "plugin_two",
        ]
        plugin_rows = [x for x in data if x["migration_set"].startswith("plugin_")]
        assert all(x["source"].startswith("plugin:") for x in plugin_rows)
    finally:
        plugins.pm.unregister(name="VerifierMigrationPlugin")


def test_plugin_migrations_apply_in_declared_order(tmp_path):
    calls = []
    plugin = _plugin(calls)
    plugins.pm.register(plugin, name="VerifierMigrationPlugin")
    try:
        path = tmp_path / "migrations.py"
        _file_migrations(path)
        db_path = tmp_path / "x.db"
        result = CliRunner().invoke(
            cli,
            ["migrate", str(db_path), str(path), "--include-plugin-migrations"],
        )
        assert result.exit_code == 0, result.output
        from sqlite_utils import Database

        db = Database(db_path)
        assert [r["name"] for r in db["order"].rows] == [
            "file",
            "plugin_one",
            "plugin_two",
        ]
        db.close()
        assert calls == ["register"]
    finally:
        plugins.pm.unregister(name="VerifierMigrationPlugin")


def test_stop_before_targets_plugin_migration(tmp_path):
    calls = []
    plugin = _plugin(calls)
    plugins.pm.register(plugin, name="VerifierMigrationPlugin")
    try:
        path = tmp_path / "migrations.py"
        _file_migrations(path)
        db_path = tmp_path / "x.db"
        result = CliRunner().invoke(
            cli,
            [
                "migrate",
                str(db_path),
                str(path),
                "--include-plugin-migrations",
                "--stop-before",
                "plugin_one:p1",
            ],
        )
        assert result.exit_code == 0, result.output
        from sqlite_utils import Database

        db = Database(db_path)
        assert [r["name"] for r in db["order"].rows] == ["file"]
        db.close()
    finally:
        plugins.pm.unregister(name="VerifierMigrationPlugin")


def test_plugin_hook_failure_happens_before_migration_application(tmp_path):
    class Broken:
        __name__ = "BrokenMigrationPlugin"

        @hookimpl
        def register_migrations(self):
            raise RuntimeError("expected verifier plugin failure")

    plugins.pm.register(Broken(), name="BrokenMigrationPlugin")
    try:
        path = tmp_path / "migrations.py"
        _file_migrations(path)
        db_path = tmp_path / "x.db"
        result = CliRunner().invoke(
            cli,
            ["migrate", str(db_path), str(path), "--include-plugin-migrations"],
        )
        assert result.exit_code != 0
        if db_path.exists():
            from sqlite_utils import Database

            db = Database(db_path)
            assert "order" not in db.table_names()
            db.close()
    finally:
        plugins.pm.unregister(name="BrokenMigrationPlugin")
