from sqlite_utils import Database, Migrations


def test_existing_migration_path_executes_in_frozen_environment():
    migrations = Migrations("synthetic")

    @migrations()
    def one(db):
        db["items"].insert({"name": "ok"})

    db = Database(memory=True)
    migrations.apply(db)
    assert list(db["items"].rows) == [{"name": "ok"}]
    assert [m.name for m in migrations.applied(db)] == ["one"]
