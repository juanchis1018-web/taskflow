"""Exporta la base de datos de TaskFlow a archivos .sql.

Uso (desde la carpeta del proyecto):
    python -m scripts.export_db

Genera en la carpeta database/:
    taskflow_export.sql        volcado completo para SQLite (estructura + datos)
    taskflow_export_mysql.sql  mismo contenido adaptado a MySQL / MariaDB
    schema.sql                 solo la estructura
"""
import os
import sqlite3
from datetime import datetime

from app import create_app

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database")

MYSQL_SCHEMA = """CREATE DATABASE IF NOT EXISTS taskflow CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE taskflow;

DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    username      VARCHAR(20)  NOT NULL UNIQUE,
    email         VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role          ENUM('user','admin') NOT NULL DEFAULT 'user',
    created_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE tasks (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT NOT NULL,
    title       VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    priority    ENUM('baja','media','alta') NOT NULL DEFAULT 'media',
    done        TINYINT(1) NOT NULL DEFAULT 0,
    due_date    DATE NULL,
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_tasks_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_tasks_user (user_id)
) ENGINE=InnoDB;
"""


def _mysql_value(v):
    if v is None:
        return "NULL"
    if isinstance(v, (int, float)):
        return str(v)
    return "'" + str(v).replace("\\", "\\\\").replace("'", "''") + "'"


def export():
    app = create_app()
    db_path = app.config["DATABASE"]
    if not os.path.exists(db_path):
        raise SystemExit(f"No existe la base de datos {db_path}. Ejecute primero: python run.py")
    os.makedirs(OUT, exist_ok=True)
    con = sqlite3.connect(db_path)
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = (f"-- TaskFlow - export de la base de datos\n-- Generado: {stamp}\n"
              f"-- Origen: {os.path.basename(db_path)}\n\n")

    with open(os.path.join(OUT, "taskflow_export.sql"), "w", encoding="utf-8") as f:
        f.write(header + "PRAGMA foreign_keys=OFF;\n")
        for line in con.iterdump():
            f.write(line + "\n")

    with open(os.path.join(OUT, "schema.sql"), "w", encoding="utf-8") as f:
        f.write(header)
        for (sql,) in con.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"):
            f.write(sql + ";\n\n")

    with open(os.path.join(OUT, "taskflow_export_mysql.sql"), "w", encoding="utf-8") as f:
        f.write(header + MYSQL_SCHEMA + "\n")
        for table, cols in (("users", "id, username, email, password_hash, role, created_at"),
                            ("tasks", "id, user_id, title, description, priority, done, due_date, created_at")):
            rows = con.execute(f"SELECT {cols} FROM {table} ORDER BY id").fetchall()
            if rows:
                f.write(f"INSERT INTO {table} ({cols}) VALUES\n")
                f.write(",\n".join("  (" + ", ".join(_mysql_value(v) for v in r) + ")" for r in rows) + ";\n\n")

    counts = {t: con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in ("users", "tasks")}
    con.close()
    print(f"Export listo en {OUT}: {counts['users']} usuarios, {counts['tasks']} tareas")


if __name__ == "__main__":
    export()
