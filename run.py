"""Punto de entrada: python run.py  (crea la BD y un administrador de ejemplo si no existen)."""
import os

from app import create_app, services
from app.db import init_db

app = create_app()

with app.app_context():
    if not os.path.exists(app.config["DATABASE"]):
        init_db()
        services.register_user("admin", "admin@taskflow.local", "Admin1234", role="admin")
        print("BD creada. Administrador: admin / Admin1234")

if __name__ == "__main__":
    app.run(debug=False, port=5000)
