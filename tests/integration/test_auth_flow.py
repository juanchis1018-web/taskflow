"""CP-I: pruebas de integración de rutas web (Flask + SQLite)."""
import pytest

pytestmark = pytest.mark.integration


def test_cp_i01_registro_exitoso(client):
    r = client.post("/register", data={"username": "sebas", "email": "sebas@example.com", "password": "Clave1234"}, follow_redirects=True)
    assert r.status_code == 200
    assert "Registro exitoso".encode() in r.data


def test_cp_i02_registro_con_datos_invalidos(client):
    r = client.post("/register", data={"username": "s", "email": "mal", "password": "123"})
    assert r.status_code == 400
    assert "El usuario debe tener".encode() in r.data


def test_cp_i03_login_correcto_redirige_al_tablero(auth):
    r = auth.login()
    assert r.status_code == 302 and r.headers["Location"].endswith("/dashboard")


def test_cp_i04_login_incorrecto(auth):
    r = auth.login(password="Equivocada1")
    assert r.status_code == 401
    assert "incorrectos".encode() in r.data


def test_cp_i05_ruta_protegida_sin_sesion(client):
    r = client.get("/dashboard")
    assert r.status_code == 302 and "/login" in r.headers["Location"]


def test_cp_i06_crear_completar_eliminar_tarea(client, auth):
    auth.login()
    r = client.post("/tasks/new", data={"title": "Plan de pruebas", "priority": "alta"}, follow_redirects=True)
    assert "Plan de pruebas".encode() in r.data and "Tarea creada".encode() in r.data
    r = client.post("/tasks/1/toggle", follow_redirects=True)
    assert "Completada".encode() in r.data
    r = client.post("/tasks/1/delete", follow_redirects=True)
    assert "No hay tareas registradas".encode() in r.data


def test_cp_i07_buscar_tareas(client, auth):
    auth.login()
    client.post("/tasks/new", data={"title": "Leer ISO 9001"})
    client.post("/tasks/new", data={"title": "Hacer video"})
    r = client.get("/dashboard?q=ISO")
    assert b"Leer ISO 9001" in r.data and b"Hacer video" not in r.data


def test_cp_i08_editar_perfil(client, auth):
    auth.login()
    r = client.post("/profile", data={"email": "juan.sebastian@example.com"}, follow_redirects=True)
    assert "Perfil actualizado".encode() in r.data
    assert b"juan.sebastian@example.com" in r.data


def test_cp_i09_eliminar_cuenta(client, auth):
    auth.login()
    r = client.post("/profile/delete", follow_redirects=True)
    assert "Su cuenta fue eliminada".encode() in r.data
    assert auth.login().status_code == 401


def test_cp_i10_logout(client, auth):
    auth.login()
    auth.logout()
    assert client.get("/dashboard").status_code == 302
