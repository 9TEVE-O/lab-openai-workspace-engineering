import json
from pathlib import Path

from click.testing import CliRunner

from sqlite_utils import Database, Migrations
from sqlite_utils.cli import cli


def _entry(entry):
    if hasattr(entry, "__dict__"):
        return dict(entry.__dict__)
    if hasattr(entry, "_asdict"):
        return dict(entry._asdict())
    return dict(entry)


def _migrations(executed=None):
    executed = executed if executed is not None else []
    m = Migrations("alpha")

    @m()
    def one(db):
        executed.append("one")
        db["effects"].insert({"name": "one"})

    @m(transactional=False)
    def two(db):
        executed.append("two")
        db["effects"].insert({"name": "two"})

    @m()
    def three(db):
        executed.append("three")
        db["effects"].insert({"name": "three"})

    return m


def test_public_type_and_empty_plan_is_read_only(tmp_path):
    from sqlite_utils import MigrationPlanEntry

    assert MigrationPlanEntry is not None
    path = tmp_path / "missing.db"
    m = _migrations()
    entries = [_entry(e) for e in m.plan(Database(memory=True))]
    assert [e["status"] for e in entries] == ["pending", "pending", "pending"]
    assert [e["migration_set"] for e in entries] == ["alpha"] * 3
    assert [e["migration_name"] for e in entries] == ["one", "two", "three"]
    assert [e["position"] for e in entries] == [0, 1, 2]
    assert [e["transactional"] for e in entries] == [True, False, True]
    assert not path.exists()


def test_plan_partial_and_stop_before_without_execution(tmp_path):
    path = tmp_path / "db.sqlite"
    m = _migrations()
    db = Database(path)
    m.apply(db, stop_before="two")
    before = path.read_bytes()
    executed = []
    m2 = _migrations(executed)
    entries = [_entry(e) for e in m2.plan(db, stop_before="three")]
    assert [e["status"] for e in entries] == ["applied", "pending", "stopped"]
    assert executed == []
    db.close()
    assert path.read_bytes() == before


def test_plan_does_not_upgrade_legacy_history(tmp_path):
    path = tmp_path / "legacy.db"
    db = Database(path)
    db["_sqlite_migrations"].create(
        {"migration_set": str, "name": str, "applied_at": str},
        pk=("migration_set", "name"),
    )
    db["_sqlite_migrations"].insert(
        {"migration_set": "alpha", "name": "one", "applied_at": "x"}
    )
    db.close()
    before = path.read_bytes()
    db = Database(path)
    _migrations().plan(db)
    db.close()
    assert path.read_bytes() == before


def _write_file(path: Path):
    path.write_text(
        "from sqlite_utils import Migrations\n"
        "m = Migrations('alpha')\n"
        "@m()\n"
        "def one(db): db['effects'].insert({'name': 'one'})\n"
        "@m(transactional=False)\n"
        "def two(db): db['effects'].insert({'name': 'two'})\n"
        "@m()\n"
        "def three(db): db['effects'].insert({'name': 'three'})\n",
        encoding="utf-8",
    )


def test_cli_plan_json_missing_db_and_stop_semantics(tmp_path):
    migrations = tmp_path / "migrations.py"
    _write_file(migrations)
    db_path = tmp_path / "missing.db"
    result = CliRunner().invoke(
        cli,
        ["migrate", str(db_path), str(migrations), "--plan-json", "--stop-before", "two"],
    )
    assert result.exit_code == 0, result.output
    data = json.loads(result.output)
    assert [(x["migration_name"], x["status"]) for x in data] == [
        ("one", "pending"),
        ("two", "stopped"),
        ("three", "stopped"),
    ]
    assert not db_path.exists()


def test_plan_json_is_byte_deterministic_for_identical_state(tmp_path):
    migrations = tmp_path / "migrations.py"
    _write_file(migrations)
    db_path = tmp_path / "missing.db"
    args = ["migrate", str(db_path), str(migrations), "--plan-json"]
    first = CliRunner().invoke(cli, args)
    second = CliRunner().invoke(cli, args)
    assert first.exit_code == second.exit_code == 0
    assert first.output.encode("utf-8") == second.output.encode("utf-8")
    assert not db_path.exists()


def test_cli_plan_json_unknown_stop_before_errors(tmp_path):
    migrations = tmp_path / "migrations.py"
    _write_file(migrations)
    result = CliRunner().invoke(
        cli,
        ["migrate", str(tmp_path / "x.db"), str(migrations), "--plan-json", "--stop-before", "missing"],
    )
    assert result.exit_code != 0


def test_existing_migrate_behaviour_smoke(tmp_path):
    migrations = tmp_path / "migrations.py"
    _write_file(migrations)
    db_path = tmp_path / "x.db"
    applied = CliRunner().invoke(cli, ["migrate", str(db_path), str(migrations)])
    assert applied.exit_code == 0, applied.output
    listed = CliRunner().invoke(cli, ["migrate", str(db_path), str(migrations), "--list"])
    assert listed.exit_code == 0
    assert "one" in listed.output and "three" in listed.output
