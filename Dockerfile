# Imagen de producción de TaskFlow: Python 3.12 + Gunicorn
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DATABASE_PATH=/data/taskflow.sqlite

WORKDIR /srv/taskflow
COPY requirements-prod.txt .
RUN pip install --no-cache-dir -r requirements-prod.txt

COPY app ./app
COPY run.py wsgi.py ./

RUN useradd --create-home taskflow && mkdir -p /data && chown taskflow /data
USER taskflow
VOLUME ["/data"]
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request;urllib.request.urlopen('http://127.0.0.1:8000/health')"
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "--access-logfile", "-", "wsgi:app"]
