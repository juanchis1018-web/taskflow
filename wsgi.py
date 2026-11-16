"""Punto de entrada WSGI para producción (Gunicorn detrás de Nginx).

    gunicorn --workers 3 --bind 0.0.0.0:8000 wsgi:app
"""
from run import app  # noqa: F401  (crea la BD y el administrador si no existen)
