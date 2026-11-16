"""Carga datos de demostración en la base de datos de TaskFlow.

Uso (desde la carpeta del proyecto):
    python -m scripts.seed_demo            # agrega datos si la BD está vacía
    python -m scripts.seed_demo --reset    # borra todo y vuelve a cargar
"""
import sys

from app import create_app, services
from app.db import get_db, init_db

USUARIOS = [
    ("admin", "admin@taskflow.local", "Admin1234", "admin"),
    ("jsmunoz", "juan.munoz@taskflow.local", "Calidad2026", "user"),
    ("lgarcia", "laura.garcia@taskflow.local", "Calidad2026", "user"),
    ("cperez", "carlos.perez@taskflow.local", "Calidad2026", "user"),
]

TAREAS = {
    "jsmunoz": [
        ("Especificar requerimientos funcionales", "Documento IEEE 29148 del proyecto", "alta", "2026-10-05", 1),
        ("Diseñar modelo de base de datos", "Tablas users y tasks con integridad referencial", "alta", "2026-10-08", 1),
        ("Implementar API REST de tareas", "Endpoints GET/POST/PUT/DELETE /api/tasks", "alta", "2026-10-15", 1),
        ("Automatizar pruebas con pytest y Playwright", "Unitarias, integración, seguridad y E2E", "media", "2026-10-18", 1),
        ("Elaborar diagrama de despliegue UML", "Nodos cliente, servidor web, aplicación y BD", "media", "2026-11-10", 1),
        ("Configurar despliegue con Docker y Nginx", "docker-compose con proxy inverso", "media", "2026-11-14", 0),
        ("Grabar video de avance del proyecto", "10 minutos en español", "alta", "2026-11-16", 0),
    ],
    "lgarcia": [
        ("Diseñar interfaz gráfica de usuario", "Mapa de navegación y vistas", "alta", "2026-10-10", 1),
        ("Validar diseño adaptable en celular", "Pruebas en 375 px y 768 px de ancho", "media", "2026-11-12", 0),
        ("Revisar accesibilidad de formularios", "Etiquetas, foco visible y contraste", "baja", "2026-11-20", 0),
    ],
    "cperez": [
        ("Medir métricas ISO/IEC 25023", "Cobertura, tiempos de respuesta, defectos", "media", "2026-11-11", 1),
        ("Preparar plan de pruebas de aceptación", "Escenarios con el cliente", "media", "2026-11-18", 0),
    ],
}


def seed(reset=False):
    app = create_app()
    with app.app_context():
        if reset:
            init_db()
        else:
            try:
                if get_db().execute("SELECT COUNT(*) FROM users").fetchone()[0]:
                    print("La base de datos ya tiene datos; use --reset para recargarla.")
                    return
            except Exception:
                init_db()
        ids = {}
        for username, email, pwd, role in USUARIOS:
            ids[username] = services.register_user(username, email, pwd, role=role)
        for username, tareas in TAREAS.items():
            for title, desc, prio, due, done in tareas:
                tid = services.create_task(ids[username], title, desc, prio, due)
                if done:
                    services.toggle_task(tid, ids[username])
        total = sum(len(t) for t in TAREAS.values())
        print(f"Datos cargados: {len(USUARIOS)} usuarios y {total} tareas en {app.config['DATABASE']}")


if __name__ == "__main__":
    seed(reset="--reset" in sys.argv)
