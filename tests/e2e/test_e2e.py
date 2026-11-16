"""CP-E: pruebas de sistema (extremo a extremo) con navegador real usando Playwright."""
import threading

import pytest
from werkzeug.serving import make_server

pytestmark = pytest.mark.e2e
playwright_api = pytest.importorskip("playwright.sync_api")


@pytest.fixture
def live_server(app):
    server = make_server("127.0.0.1", 5055, app)
    hilo = threading.Thread(target=server.serve_forever, daemon=True)
    hilo.start()
    yield "http://127.0.0.1:5055"
    server.shutdown()


@pytest.fixture
def page():
    with playwright_api.sync_playwright() as p:
        browser = p.chromium.launch()
        pg = browser.new_page(viewport={"width": 1100, "height": 760})
        yield pg
        browser.close()


def test_cp_e01_flujo_completo_usuario(live_server, page):
    expect = playwright_api.expect
    # Registro
    page.goto(f"{live_server}/register")
    page.fill("#username", "sebastian")
    page.fill("#email", "sebastian@example.com")
    page.fill("#password", "Calidad2026")
    page.click("#btn-register")
    expect(page.get_by_role("alert")).to_contain_text("Registro exitoso")
    # Inicio de sesión
    page.fill("#username", "sebastian")
    page.fill("#password", "Calidad2026")
    page.click("#btn-login")
    expect(page.locator("#who")).to_have_text("sebastian")
    # Crear dos tareas
    for titulo, prioridad in [("Informe ISO 9000", "alta"), ("Grabar video", "media")]:
        page.fill("#title", titulo)
        page.select_option("#priority", prioridad)
        page.click("#btn-add")
    expect(page.locator("#st-total")).to_have_text("2")
    # Completar una
    page.locator("tr", has_text="Informe ISO 9000").locator("button.toggle").click()
    expect(page.locator("#st-pct")).to_have_text("50.0%")
    # Cerrar sesión
    page.click("#logout")
    expect(page).to_have_url(f"{live_server}/login")


def test_cp_e02_login_fallido_muestra_mensaje(live_server, page):
    page.goto(f"{live_server}/login")
    page.fill("#username", "juan")
    page.fill("#password", "mala")
    page.click("#btn-login")
    playwright_api.expect(page.get_by_role("alert")).to_contain_text("incorrectos")
