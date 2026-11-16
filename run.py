"""Punto de entrada en desarrollo: python run.py

Crea la base de datos y el usuario administrador la primera vez que se ejecuta.
"""
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
    app.run(host=os.environ.get("HOST", "127.0.0.1"), port=int(os.environ.get("PORT", 5000)), debug=False)
