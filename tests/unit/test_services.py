"""CP-U: pruebas unitarias de la capa de servicios (con BD temporal)."""
import pytest

from app import services
from app.validators import ValidationError

pytestmark = pytest.mark.unit


def test_cp_u10_registro_guarda_hash(app):
    with app.app_context():
        uid = services.register_user("nuevo", "nuevo@example.com", "Clave1234")
        user = services.get_user(uid)
        assert user["password_hash"] != "Clave1234"
        assert user["role"] == "user"


def test_cp_u11_registro_duplicado(app):
    with app.app_context():
        with pytest.raises(ValidationError, match="ya están registrados"):
            services.register_user("juan", "otro@example.com", "Clave1234")
        with pytest.raises(ValidationError):
            services.register_user("otro", "JUAN@example.com", "Clave1234")


def test_cp_u12_autenticacion(app):
    with app.app_context():
        assert services.authenticate("juan", "Clave1234")["username"] == "juan"
        assert services.authenticate("juan", "incorrecta") is None
        assert services.authenticate("noexiste", "Clave1234") is None


def test_cp_u13_estadisticas(app):
    with app.app_context():
        assert services.task_stats(1) == {"total": 0, "completed": 0, "pending": 0, "percent": 0.0}
        a = services.create_task(1, "A")
        services.create_task(1, "B")
        services.create_task(1, "C")
        services.toggle_task(a, 1)
        assert services.task_stats(1) == {"total": 3, "completed": 1, "pending": 2, "percent": 33.3}


def test_cp_u14_orden_por_prioridad(app):
    with app.app_context():
        services.create_task(1, "baja", priority="baja")
        services.create_task(1, "alta", priority="alta")
        services.create_task(1, "media", priority="media")
        assert [t["title"] for t in services.list_tasks(1)] == ["alta", "media", "baja"]


def test_cp_u15_eliminar_usuario_elimina_tareas(app):
    with app.app_context():
        services.create_task(1, "Tarea de juan")
        services.delete_user(1)
        assert services.list_tasks(1) == []
        assert services.get_user(1) is None


def test_cp_u16_actualizar_perfil(app):
    with app.app_context():
        services.update_profile(1, "juan.nuevo@example.com", "NuevaClave9")
        assert services.get_user(1)["email"] == "juan.nuevo@example.com"
        assert services.authenticate("juan", "NuevaClave9") is not None
        with pytest.raises(ValidationError, match="en uso"):
            services.update_profile(1, "maria@example.com")
