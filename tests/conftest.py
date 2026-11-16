import pytest

from app import create_app, services
from app.db import init_db


@pytest.fixture
def app(tmp_path):
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "test.sqlite"), "SECRET_KEY": "test"})
    with app.app_context():
        init_db()
        services.register_user("juan", "juan@example.com", "Clave1234")
        services.register_user("maria", "maria@example.com", "Clave1234")
        services.register_user("admin", "admin@example.com", "Admin1234", role="admin")
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


class Auth:
    def __init__(self, client):
        self.client = client

    def login(self, username="juan", password="Clave1234"):
        return self.client.post("/login", data={"username": username, "password": password})

    def logout(self):
        return self.client.get("/logout")


@pytest.fixture
def auth(client):
    return Auth(client)


def pytest_metadata(metadata):
    """Deja en el reporte HTML solo la información relevante del entorno."""
    for key in list(metadata):
        if key not in ("Python", "Platform", "Packages", "Plugins"):
            metadata.pop(key)


def pytest_html_report_title(report):
    report.title = "Reporte de pruebas – TaskFlow (Juan Sebastián Muñoz Melo)"
