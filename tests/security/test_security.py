"""CP-S: pruebas de seguridad (autorización, inyección, XSS, cabeceras)."""
import pytest

from app import services

pytestmark = pytest.mark.security


def test_cp_s01_usuario_no_accede_a_tareas_ajenas(client, auth, app):
    with app.app_context():
        tid = services.create_task(2, "Secreto de maria")  # tarea de maria
    auth.login("juan")
    assert client.get(f"/api/tasks/{tid}").status_code == 404
    assert client.delete(f"/api/tasks/{tid}").status_code == 404
    assert client.post(f"/tasks/{tid}/delete").status_code == 404
    with app.app_context():
        assert services.get_task(tid, 2) is not None


def test_cp_s02_usuario_estandar_no_entra_a_admin(client, auth):
    auth.login("juan")
    assert client.get("/admin/users").status_code == 403


def test_cp_s03_admin_si_entra(client, auth):
    auth.login("admin", "Admin1234")
    r = client.get("/admin/users")
    assert r.status_code == 200 and b"maria@example.com" in r.data


def test_cp_s04_inyeccion_sql_en_login(auth):
    r = auth.login(username="juan' OR '1'='1", password="x' OR '1'='1")
    assert r.status_code == 401


def test_cp_s05_inyeccion_sql_en_busqueda(client, auth, app):
    auth.login()
    client.post("/tasks/new", data={"title": "normal"})
    r = client.get("/dashboard?q=%' OR 1=1 --")
    assert r.status_code == 200 and b"normal" not in r.data
    with app.app_context():
        assert len(services.list_users()) == 3  # la tabla sigue intacta


def test_cp_s06_xss_escapado(client, auth):
    auth.login()
    client.post("/tasks/new", data={"title": "<script>alert(1)</script>"})
    r = client.get("/dashboard")
    assert b"<script>alert(1)</script>" not in r.data
    assert b"&lt;script&gt;" in r.data


def test_cp_s07_contrasena_no_se_guarda_en_claro(app):
    with app.app_context():
        for u in services.list_users():
            full = services.get_user(u["id"])
            assert "Clave1234" not in full["password_hash"]
            assert full["password_hash"].startswith(("scrypt:", "pbkdf2:"))


def test_cp_s08_cabeceras_y_cookie(client, auth):
    r = auth.login()
    assert "HttpOnly" in r.headers["Set-Cookie"]
    assert r.headers["X-Frame-Options"] == "DENY"
    assert r.headers["X-Content-Type-Options"] == "nosniff"
