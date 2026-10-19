"""CP-I: pruebas de integración de la API REST /api/tasks."""
import pytest

pytestmark = pytest.mark.integration


def test_cp_i11_api_requiere_autenticacion(client):
    assert client.get("/api/tasks").status_code == 401


def test_cp_i12_api_crud_completo(client, auth):
    auth.login()
    r = client.post("/api/tasks", json={"title": "API task", "priority": "baja", "due_date": "2026-12-01"})
    assert r.status_code == 201
    tid = r.get_json()["id"]

    assert client.get(f"/api/tasks/{tid}").get_json()["title"] == "API task"

    r = client.put(f"/api/tasks/{tid}", json={"title": "API task editada", "priority": "alta", "done": True})
    assert r.status_code == 200
    assert r.get_json()["done"] == 1 and r.get_json()["priority"] == "alta"

    assert len(client.get("/api/tasks").get_json()) == 1
    assert client.get("/api/stats").get_json()["percent"] == 100.0

    assert client.delete(f"/api/tasks/{tid}").status_code == 204
    assert client.get(f"/api/tasks/{tid}").status_code == 404


def test_cp_i13_api_datos_invalidos(client, auth):
    auth.login()
    r = client.post("/api/tasks", json={"title": "", "priority": "media"})
    assert r.status_code == 400 and "obligatorio" in r.get_json()["error"]
    r = client.post("/api/tasks", data="no es json", content_type="text/plain")
    assert r.status_code == 400


def test_cp_i14_api_recurso_inexistente(client, auth):
    auth.login()
    assert client.put("/api/tasks/999", json={"title": "x"}).status_code == 404
    assert client.delete("/api/tasks/999").status_code == 404
