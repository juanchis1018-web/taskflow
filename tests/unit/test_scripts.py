"""CP-U: pruebas de los scripts de carga de datos y export de la base de datos."""
import sqlite3

import pytest

from scripts import export_db, seed_demo

pytestmark = pytest.mark.unit


def test_cp_u17_seed_y_export(tmp_path, monkeypatch):
    db = tmp_path / "demo.sqlite"
    monkeypatch.setenv("DATABASE_PATH", str(db))
    monkeypatch.setattr(export_db, "OUT", str(tmp_path / "database"))
    seed_demo.seed(reset=True)
    export_db.export()

    dump = (tmp_path / "database" / "taskflow_export.sql").read_text(encoding="utf-8")
    assert "CREATE TABLE users" in dump and "INSERT INTO" in dump
    mysql = (tmp_path / "database" / "taskflow_export_mysql.sql").read_text(encoding="utf-8")
    assert "ENGINE=InnoDB" in mysql and "INSERT INTO tasks" in mysql

    # El volcado se puede restaurar en una base nueva con los mismos datos
    nueva = sqlite3.connect(":memory:")
    nueva.executescript(dump)
    assert nueva.execute("SELECT COUNT(*) FROM users").fetchone()[0] == len(seed_demo.USUARIOS)
    assert nueva.execute("SELECT COUNT(*) FROM tasks").fetchone()[0] == sum(len(t) for t in seed_demo.TAREAS.values())
    nueva.close()
