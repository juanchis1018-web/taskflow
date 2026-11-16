# TaskFlow – Proyecto integrador

**Asignaturas:** Estándares y Métricas de Calidad de Software · Ingeniería Web
**Autor:** Juan Sebastián Muñoz Melo · Código 1034277244
link video youtube: https://youtu.be/ZO2UbT28iIo 

Aplicación web con base de datos para gestionar tareas: registro e inicio de sesión, tareas con
prioridad y fecha límite, indicadores de avance, perfil, roles de usuario y administrador, API REST
y despliegue en contenedores (Nginx + Gunicorn + SQLite).

## Contenido de la entrega

| Carpeta / archivo | Qué contiene |
|---|---|
| `app/` | Código fuente de la aplicación (Flask, patrón MVC) |
| `tests/` | 62 pruebas: unitarias, integración, seguridad, rendimiento y E2E |
| `database/` | **Export de la base de datos**: `taskflow_export.sql` (SQLite), `taskflow_export_mysql.sql` (MySQL/MariaDB), `schema.sql` y la base de demostración `taskflow_demo.sqlite` |
| `scripts/` | `seed_demo.py` (datos de demostración) y `export_db.py` (genera el export) |
| `Dockerfile`, `docker-compose.yml`, `deploy/nginx.conf`, `wsgi.py` | Configuración de despliegue |
| `docs/Avance_Proyecto_TaskFlow.pdf` / `.docx` | Documento de avance: requerimientos, calidad, GUI, BD, API y despliegue |
| `docs/uml/` | Diagramas UML (fuente PlantUML `.puml` e imagen `.png`): casos de uso, componentes, navegación, modelo ER y **despliegue** |
| `docs/capturas/` | Capturas de la interfaz (computador y celular) |
| `docs/evidencias/` | Reporte HTML de pruebas, cobertura y salida de consola |
| `docs/guia6/` | Entrega anterior (Guía 6: estándares ISO y plan de pruebas) |

## Estructura

```
taskflow/
├── app/
│   ├── __init__.py       Rutas web, API REST, sesión y cabeceras de seguridad
│   ├── db.py             Esquema y conexión SQLite
│   ├── services.py       Lógica de negocio (usuarios y tareas)
│   ├── validators.py     Reglas de validación
│   ├── static/           Recursos estáticos
│   └── templates/        Vistas HTML (Jinja2)
├── scripts/              seed_demo.py, export_db.py
├── tests/                unit/ integration/ security/ performance/ e2e/
├── database/             Export de la base de datos
├── deploy/nginx.conf     Proxy inverso
├── docs/                 Documentación, UML, capturas y evidencias
├── Dockerfile · docker-compose.yml · wsgi.py · run.py
└── requirements.txt · requirements-prod.txt · pytest.ini
```

## Ejecutar en el computador (desarrollo)

```bash
python -m pip install -r requirements.txt
python -m playwright install chromium      # solo para las pruebas E2E
python -m scripts.seed_demo --reset        # carga 4 usuarios y 12 tareas de demostración
python run.py                              # http://127.0.0.1:5000
```

Usuarios de demostración: `admin` / `Admin1234` (administrador) y `jsmunoz` / `Calidad2026`.

## Pruebas

```bash
python -m pytest -v                                   # 62 pruebas
python -m pytest -m security                          # solo seguridad (también: unit, integration, e2e, performance)
python -m pytest --cov=app --cov=scripts --cov-report=term-missing
```

Resultado actual: **62 aprobadas, 0 fallidas, 95 % de cobertura.**

## Export de la base de datos

```bash
python -m scripts.export_db
```

Genera en `database/` el volcado de SQLite, la versión para MySQL/MariaDB (importable en phpMyAdmin) y
el esquema. Para restaurar: `sqlite3 nueva.sqlite < database/taskflow_export.sql` o
`mysql -u root -p < database/taskflow_export_mysql.sql`.

## Despliegue con Docker

```bash
export SECRET_KEY="una-clave-larga-y-secreta"
docker compose up -d --build     # Nginx en el puerto 80 -> Gunicorn (8000) -> SQLite en un volumen
curl http://localhost/health     # {"status": "ok", ...}
```

## API REST

| Método | Ruta | Respuestas |
|---|---|---|
| GET | `/api/tasks` | 200, 401 |
| POST | `/api/tasks` | 201, 400, 401 |
| GET | `/api/tasks/{id}` | 200, 401, 404 |
| PUT | `/api/tasks/{id}` | 200, 400, 401, 404 |
| DELETE | `/api/tasks/{id}` | 204, 401, 404 |
| GET | `/api/stats` | 200, 401 |
| GET | `/health` | 200 |
