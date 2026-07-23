import os
import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

def pytest_addoption(parser):
    """Agrega opciones de línea de comandos personalizadas a pytest."""
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Ejecutar las pruebas en modo con interfaz gráfica (sin headless)."
    )
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Navegador a utilizar: chrome (por defecto)"
    )

@pytest.fixture(scope="function")
def driver(request):
    """Fixture de PyTest para inicializar y cerrar Selenium WebDriver."""
    is_headed = request.config.getoption("--headed")
    browser_name = request.config.getoption("--browser")

    if browser_name.lower() == "chrome":
        chrome_options = ChromeOptions()
        if not is_headed:
            chrome_options.add_argument("--headless=new")
        
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--allow-file-access-from-files")
        chrome_options.add_argument("--allow-file-access")
        chrome_options.add_argument("--log-level=3")

        try:
            driver = webdriver.Chrome(options=chrome_options)
        except Exception:
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)

    yield driver

    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook para capturar pantalla en caso de fallo en una prueba y adjuntarla al reporte HTML."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshots_dir = os.path.join(os.getcwd(), "reports", "screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshots_dir, f"{item.name}_{int(time.time())}.png")
            driver.save_screenshot(screenshot_path)
            
            # Integrar captura de pantalla en reportes de pytest-html si está disponible
            pytest_html = item.config.pluginmanager.getplugin("html")
            if pytest_html:
                extra = getattr(report, "extra", [])
                extra.append(pytest_html.extras.image(screenshot_path))
                report.extra = extra
