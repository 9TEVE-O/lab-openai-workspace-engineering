import shutil
import sqlite3
import subprocess
import time
from pathlib import Path


def _write_overlap_migration(path: Path):
    path.write_text(
        "from sqlite_utils import Migrations\n"
        "import time\n"
        "m = Migrations('concurrent')\n"
        "@m()\n"
        "def once(db):\n"
        "    db['effects'].insert({'marker': 'x'})\n"
        "    time.sleep(1.5)\n",
        encoding='utf-8',
    )


def test_two_processes_execute_migration_at_most_once(tmp_path):
    exe = shutil.which('sqlite-utils')
    assert exe
    migrations = tmp_path / 'migrations.py'
    _write_overlap_migration(migrations)
    db = tmp_path / 'shared.db'
    p1 = subprocess.Popen([exe, 'migrate', str(db), str(migrations), '--lock-timeout', '5.0'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    time.sleep(0.2)
    p2 = subprocess.Popen([exe, 'migrate', str(db), str(migrations), '--lock-timeout', '5.0'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out1, err1 = p1.communicate(timeout=15)
    out2, err2 = p2.communicate(timeout=15)
    assert p1.returncode == 0, out1 + err1
    assert p2.returncode == 0 or 'lock' in (out2 + err2).lower()
    conn = sqlite3.connect(db)
    assert conn.execute('select count(*) from effects').fetchone()[0] == 1
    assert conn.execute("select count(*) from _sqlite_migrations where migration_set='concurrent' and name='once'").fetchone()[0] == 1
    conn.close()


def test_timeout_process_makes_no_own_migration_change(tmp_path):
    exe = shutil.which('sqlite-utils')
    migrations = tmp_path / 'migrations.py'
    _write_overlap_migration(migrations)
    db = tmp_path / 'shared.db'
    p1 = subprocess.Popen([exe, 'migrate', str(db), str(migrations), '--lock-timeout', '5.0'])
    time.sleep(0.2)
    p2 = subprocess.run([exe, 'migrate', str(db), str(migrations), '--lock-timeout', '0.1'], capture_output=True, text=True, timeout=10)
    p1.wait(timeout=15)
    assert p1.returncode == 0
    assert p2.returncode != 0
    assert 'lock' in (p2.stdout + p2.stderr).lower()
    conn = sqlite3.connect(db)
    assert conn.execute('select count(*) from effects').fetchone()[0] == 1
    conn.close()


def test_failed_transaction_remains_retryable_under_locking(tmp_path):
    exe = shutil.which('sqlite-utils')
    bad = tmp_path / 'bad.py'
    bad.write_text(
        "from sqlite_utils import Migrations\n"
        "m=Migrations('retry')\n"
        "@m()\n"
        "def work(db):\n"
        "    db['effects'].insert({'marker':'bad'})\n"
        "    raise RuntimeError('boom')\n",
        encoding='utf-8',
    )
    good = tmp_path / 'good.py'
    good.write_text(
        "from sqlite_utils import Migrations\n"
        "m=Migrations('retry')\n"
        "@m()\n"
        "def work(db): db['effects'].insert({'marker':'good'})\n",
        encoding='utf-8',
    )
    db = tmp_path / 'retry.db'
    first = subprocess.run([exe, 'migrate', str(db), str(bad), '--lock-timeout', '5.0'])
    assert first.returncode != 0
    second = subprocess.run([exe, 'migrate', str(db), str(good), '--lock-timeout', '5.0'])
    assert second.returncode == 0
    conn = sqlite3.connect(db)
    assert conn.execute('select marker from effects').fetchall() == [('good',)]
    assert conn.execute("select count(*) from _sqlite_migrations where migration_set='retry' and name='work'").fetchone()[0] == 1
    conn.close()
