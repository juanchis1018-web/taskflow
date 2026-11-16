"""CP-R: pruebas de rendimiento básicas (tiempos de respuesta con volumen)."""
import time

import pytest

from app import services

pytestmark = pytest.mark.performance


def test_cp_r01_listado_con_500_tareas_bajo_300ms(client, auth, app):
    with app.app_context():
        for i in range(500):
            services.create_task(1, f"Tarea {i}", priority=("baja", "media", "alta")[i % 3])
    auth.login()
    inicio = time.perf_counter()
    r = client.get("/api/tasks")
    duracion = (time.perf_counter() - inicio) * 1000
    assert r.status_code == 200 and len(r.get_json()) == 500
    assert duracion < 300, f"tardó {duracion:.1f} ms"


def test_cp_r02_100_peticiones_secuenciales(client, auth):
    auth.login()
    inicio = time.perf_counter()
    for i in range(100):
        assert client.post("/api/tasks", json={"title": f"t{i}"}).status_code == 201
    promedio = (time.perf_counter() - inicio) * 1000 / 100
    assert promedio < 50, f"promedio {promedio:.1f} ms"
