# TaskFlow – Plan de pruebas (Guía 6, Estándares y Métricas de Calidad de Software)

**Autor:** Juan Sebastián Muñoz Melo

Aplicación web de gestión de usuarios y tareas (Python + Flask + SQLite) con su suite de pruebas
automatizadas: unitarias, integración, sistema (E2E con navegador), seguridad y rendimiento.

## Estructura

```
taskflow/
├── app/                  Código de la aplicación
│   ├── __init__.py       Rutas web y API REST
│   ├── db.py             Esquema y conexión SQLite
│   ├── services.py       Lógica de negocio (usuarios y tareas)
│   ├── validators.py     Reglas de validación
│   └── templates/        Vistas HTML
├── tests/
│   ├── unit/             CP-U01 … CP-U16
│   ├── integration/      CP-I01 … CP-I14
│   ├── security/         CP-S01 … CP-S08
│   ├── performance/      CP-R01 … CP-R02
│   └── e2e/              CP-E01 … CP-E02 (Playwright)
├── docs/
│   ├── evidencias/       Reporte HTML de pruebas, cobertura y salida de consola
│   ├── capturas/         Capturas de la aplicación
│   └── *.png / *.dot     Mapas conceptuales
├── run.py                Punto de entrada
└── requirements.txt
```

## Instalación

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium        # solo para las pruebas E2E
```

## Ejecutar la aplicación

```bash
python run.py
```

Abrir http://127.0.0.1:5000 . En el primer arranque se crea la base de datos y el usuario
administrador `admin` / `Admin1234`.

## Ejecutar las pruebas

```bash
python -m pytest -v                                   # toda la suite (60 pruebas)
python -m pytest -m unit                              # solo unitarias
python -m pytest -m integration                       # solo integración
python -m pytest -m security                          # solo seguridad
python -m pytest -m e2e                               # solo sistema (navegador)
python -m pytest -m performance                       # solo rendimiento
python -m pytest --cov=app --cov-report=term-missing  # con cobertura
python -m pytest --html=docs/evidencias/reporte_pruebas.html --self-contained-html
```

## Resultados

60 pruebas ejecutadas, 60 aprobadas, 0 fallidas · cobertura de código 97 %.
