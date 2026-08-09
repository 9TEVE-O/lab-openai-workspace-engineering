import json
import os
import resource
import sqlite3
import subprocess
import time
from pathlib import Path

from click.testing import CliRunner

from sqlite_utils.cli import cli


def _write_defs(path: Path):
    path.write_text(
        "from sqlite_utils import Migrations\n"
        "core=Migrations('core')\n"
        "@core()\n"
        "def c1(db): raise RuntimeError('must not execute')\n"
        "app=Migrations('app', depends_on=('core',))\n"
        "@app()\n"
        "def a1(db): raise RuntimeError('must not execute')\n",
        encoding='utf-8',
    )


def _verify(db, defs, *extra):
    result = CliRunner().invoke(cli, ['migrate', str(db), str(defs), '--verify-json', *extra])
    assert result.output.strip(), result.exception
    return result, json.loads(result.output)


def test_missing_database_is_valid_pending_and_not_created(tmp_path):
    defs = tmp_path / 'migrations.py'
    _write_defs(defs)
    db = tmp_path / 'missing.db'
    result, data = _verify(db, defs)
    assert result.exit_code == 0
    assert data['valid'] is True
    assert data['applied'] == 0
    assert data['pending'] == 2
    assert not db.exists()


def test_unknown_applied_and_dependency_violation_are_reported(tmp_path):
    defs = tmp_path / 'migrations.py'
    _write_defs(defs)
    db = tmp_path / 'x.db'
    conn = sqlite3.connect(db)
    conn.executescript("create table _sqlite_migrations(id integer primary key, migration_set text, name text, applied_at text); create unique index idx_m on _sqlite_migrations(migration_set,name);")
    conn.execute("insert into _sqlite_migrations(migration_set,name,applied_at) values ('app','a1','x')")
    conn.execute("insert into _sqlite_migrations(migration_set,name,applied_at) values ('gone','old','x')")
    conn.commit(); conn.close()
    before = db.read_bytes()
    _, data = _verify(db, defs)
    assert data['valid'] is False
    assert ['gone', 'old'] in data['unknown_applied'] or {'migration_set':'gone','migration_name':'old'} in data['unknown_applied']
    assert data['dependency_violations']
    assert db.read_bytes() == before


def test_consistent_partial_state_can_be_valid(tmp_path):
    defs = tmp_path / 'migrations.py'
    _write_defs(defs)
    db = tmp_path / 'x.db'
    conn = sqlite3.connect(db)
    conn.executescript("create table _sqlite_migrations(id integer primary key, migration_set text, name text, applied_at text); create unique index idx_m on _sqlite_migrations(migration_set,name);")
    conn.execute("insert into _sqlite_migrations(migration_set,name,applied_at) values ('core','c1','x')")
    conn.commit(); conn.close()
    _, data = _verify(db, defs)
    assert data['valid'] is True
    assert data['applied'] == 1 and data['pending'] == 1


def test_duplicate_sets_and_cycles_are_machine_readable(tmp_path):
    for name, body, field in [
        ('dup', "a=Migrations('x')\nb=Migrations('x')\n", 'duplicate_sets'),
        ('cycle', "a=Migrations('a', depends_on=('b',))\nb=Migrations('b', depends_on=('a',))\n", 'cycles'),
    ]:
        defs = tmp_path / f'{name}.py'
        defs.write_text('from sqlite_utils import Migrations\n' + body, encoding='utf-8')
        result = CliRunner().invoke(cli, ['migrate', str(tmp_path / f'{name}.db'), str(defs), '--verify-json'])
        assert result.output.strip()
        data = json.loads(result.output)
        assert data['valid'] is False and data[field]


def test_10k_verification_within_committed_time_and_rss(tmp_path):
    defs = tmp_path / 'large.py'
    defs.write_text(
        "from sqlite_utils import Migrations\n"
        "for i in range(100):\n"
        "    m=Migrations(f's{i:03}')\n"
        "    globals()[f'set_{i:03}']=m\n"
        "    for j in range(100):\n"
        "        def fn(db): pass\n"
        "        fn.__name__=f'm{j:03}'\n"
        "        m(name=f'm{j:03}')(fn)\n",
        encoding='utf-8',
    )
    db = tmp_path / 'large.db'
    conn = sqlite3.connect(db)
    conn.executescript("create table _sqlite_migrations(id integer primary key, migration_set text, name text, applied_at text); create unique index idx_m on _sqlite_migrations(migration_set,name);")
    rows = [(f's{i:03}', f'm{j:03}', 'x') for i in range(50) for j in range(100)]
    conn.executemany("insert into _sqlite_migrations(migration_set,name,applied_at) values (?,?,?)", rows)
    conn.commit(); conn.close()
    exe = os.environ.get('SQLITE_UTILS_EXE', 'sqlite-utils')
    before = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    started = time.monotonic()
    proc = subprocess.run([exe, 'migrate', str(db), str(defs), '--verify-json'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=8)
    elapsed = time.monotonic() - started
    after = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    assert proc.returncode == 0, proc.stdout + proc.stderr
    data = json.loads(proc.stdout)
    assert data['applied'] == 5000 and data['pending'] == 5000
    assert elapsed <= 5.0
    assert max(before, after) / 1024 <= 256
