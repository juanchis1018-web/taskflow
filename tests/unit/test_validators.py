"""CP-U: pruebas unitarias de las reglas de validación."""
import pytest

from app.validators import (
    ValidationError,
    validate_email,
    validate_password,
    validate_task,
    validate_username,
)

pytestmark = pytest.mark.unit


@pytest.mark.parametrize("name", ["abc", "juan_sebastian", "User2026"])
def test_cp_u01_usuario_valido(name):
    assert validate_username(f"  {name} ") == name


@pytest.mark.parametrize("name", ["", "ab", "x" * 21, "juan perez", "juan-perez", "ñandú"])
def test_cp_u02_usuario_invalido(name):
    with pytest.raises(ValidationError):
        validate_username(name)


def test_cp_u03_correo_normalizado():
    assert validate_email("  Juan.Munoz@Example.COM ") == "juan.munoz@example.com"


@pytest.mark.parametrize("email", ["", "juan", "juan@", "@x.com", "juan@x", "a b@x.com"])
def test_cp_u04_correo_invalido(email):
    with pytest.raises(ValidationError):
        validate_email(email)


@pytest.mark.parametrize(
    "pwd,msg",
    [
        ("Ab1", "mínimo 8"),
        ("abcdefg1", "mayúscula"),
        ("ABCDEFG1", "minúscula"),
        ("Abcdefgh", "número"),
    ],
)
def test_cp_u05_contrasena_debil(pwd, msg):
    with pytest.raises(ValidationError, match=msg):
        validate_password(pwd)


def test_cp_u06_contrasena_fuerte():
    assert validate_password("Segura2026") == "Segura2026"


def test_cp_u07_tarea_valida():
    assert validate_task("  Estudiar ISO 25010 ", "alta", "2026-11-01") == (
        "Estudiar ISO 25010",
        "alta",
        "2026-11-01",
    )


@pytest.mark.parametrize(
    "title,priority,due",
    [("", "media", None), ("x" * 101, "media", None), ("Ok", "urgente", None), ("Ok", "baja", "01/11/2026")],
)
def test_cp_u08_tarea_invalida(title, priority, due):
    with pytest.raises(ValidationError):
        validate_task(title, priority, due)


def test_cp_u09_valor_limite_titulo():
    assert validate_task("x" * 100)[0] == "x" * 100
    assert validate_task("x")[0] == "x"
