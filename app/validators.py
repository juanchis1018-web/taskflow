"""Reglas de validación de datos de entrada (lógica pura, sin dependencias)."""
import re
from datetime import date

USERNAME_RE = re.compile(r"^[A-Za-z0-9_]{3,20}$")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[A-Za-z]{2,}$")
PRIORITIES = ("baja", "media", "alta")


class ValidationError(ValueError):
    """Error de validación con mensaje legible para el usuario."""


def validate_username(username: str) -> str:
    username = (username or "").strip()
    if not USERNAME_RE.match(username):
        raise ValidationError(
            "El usuario debe tener entre 3 y 20 caracteres (letras, números o _)."
        )
    return username


def validate_email(email: str) -> str:
    email = (email or "").strip().lower()
    if len(email) > 120 or not EMAIL_RE.match(email):
        raise ValidationError("El correo electrónico no es válido.")
    return email


def validate_password(password: str) -> str:
    password = password or ""
    if len(password) < 8:
        raise ValidationError("La contraseña debe tener mínimo 8 caracteres.")
    if not re.search(r"[A-Z]", password):
        raise ValidationError("La contraseña debe contener al menos una mayúscula.")
    if not re.search(r"[a-z]", password):
        raise ValidationError("La contraseña debe contener al menos una minúscula.")
    if not re.search(r"\d", password):
        raise ValidationError("La contraseña debe contener al menos un número.")
    return password


def validate_task(title: str, priority: str = "media", due_date: str | None = None):
    title = (title or "").strip()
    if not 1 <= len(title) <= 100:
        raise ValidationError("El título es obligatorio (máximo 100 caracteres).")
    if priority not in PRIORITIES:
        raise ValidationError("La prioridad debe ser baja, media o alta.")
    if due_date:
        try:
            date.fromisoformat(due_date)
        except ValueError as exc:
            raise ValidationError("La fecha límite debe tener formato AAAA-MM-DD.") from exc
    return title, priority, (due_date or None)
