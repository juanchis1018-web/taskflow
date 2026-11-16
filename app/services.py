"""Lógica de negocio de usuarios y tareas."""
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db
from .validators import (
    ValidationError,
    validate_email,
    validate_password,
    validate_task,
    validate_username,
)


# ---------------------------------------------------------------- usuarios
def register_user(username, email, password, role="user"):
    username = validate_username(username)
    email = validate_email(email)
    validate_password(password)
    db = get_db()
    exists = db.execute(
        "SELECT 1 FROM users WHERE username = ? OR email = ?", (username, email)
    ).fetchone()
    if exists:
        raise ValidationError("El usuario o el correo ya están registrados.")
    cur = db.execute(
        "INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)",
        (username, email, generate_password_hash(password), role),
    )
    db.commit()
    return cur.lastrowid


def authenticate(username, password):
    user = get_db().execute(
        "SELECT * FROM users WHERE username = ?", ((username or "").strip(),)
    ).fetchone()
    if user is None or not check_password_hash(user["password_hash"], password or ""):
        return None
    return user


def get_user(user_id):
    return get_db().execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()


def list_users():
    return get_db().execute(
        "SELECT id, username, email, role, created_at FROM users ORDER BY id"
    ).fetchall()


def update_profile(user_id, email, new_password=None):
    email = validate_email(email)
    db = get_db()
    taken = db.execute(
        "SELECT 1 FROM users WHERE email = ? AND id <> ?", (email, user_id)
    ).fetchone()
    if taken:
        raise ValidationError("El correo ya está en uso por otra cuenta.")
    db.execute("UPDATE users SET email = ? WHERE id = ?", (email, user_id))
    if new_password:
        validate_password(new_password)
        db.execute(
            "UPDATE users SET password_hash = ? WHERE id = ?",
            (generate_password_hash(new_password), user_id),
        )
    db.commit()


def delete_user(user_id):
    db = get_db()
    db.execute("DELETE FROM users WHERE id = ?", (user_id,))
    db.commit()


# ------------------------------------------------------------------ tareas
def create_task(user_id, title, description="", priority="media", due_date=None):
    title, priority, due_date = validate_task(title, priority, due_date)
    db = get_db()
    cur = db.execute(
        "INSERT INTO tasks (user_id, title, description, priority, due_date) "
        "VALUES (?, ?, ?, ?, ?)",
        (user_id, title, (description or "").strip(), priority, due_date),
    )
    db.commit()
    return cur.lastrowid


def list_tasks(user_id, search=None):
    sql = "SELECT * FROM tasks WHERE user_id = ?"
    params = [user_id]
    if search:
        sql += " AND title LIKE ?"
        params.append(f"%{search}%")
    sql += " ORDER BY done, CASE priority WHEN 'alta' THEN 0 WHEN 'media' THEN 1 ELSE 2 END, id"
    return get_db().execute(sql, params).fetchall()


def get_task(task_id, user_id):
    return get_db().execute(
        "SELECT * FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id)
    ).fetchone()


def update_task(task_id, user_id, title, description, priority, due_date, done):
    if get_task(task_id, user_id) is None:
        return False
    title, priority, due_date = validate_task(title, priority, due_date)
    db = get_db()
    db.execute(
        "UPDATE tasks SET title = ?, description = ?, priority = ?, due_date = ?, done = ? "
        "WHERE id = ? AND user_id = ?",
        (title, (description or "").strip(), priority, due_date, int(bool(done)), task_id, user_id),
    )
    db.commit()
    return True


def toggle_task(task_id, user_id):
    db = get_db()
    cur = db.execute(
        "UPDATE tasks SET done = 1 - done WHERE id = ? AND user_id = ?", (task_id, user_id)
    )
    db.commit()
    return cur.rowcount == 1


def delete_task(task_id, user_id):
    db = get_db()
    cur = db.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id))
    db.commit()
    return cur.rowcount == 1


def task_stats(user_id):
    row = get_db().execute(
        "SELECT COUNT(*) AS total, COALESCE(SUM(done), 0) AS completed FROM tasks WHERE user_id = ?",
        (user_id,),
    ).fetchone()
    total, completed = row["total"], row["completed"]
    pct = round(completed * 100 / total, 1) if total else 0.0
    return {"total": total, "completed": completed, "pending": total - completed, "percent": pct}
