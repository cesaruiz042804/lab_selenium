import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# extras permite adjuntar contenido extra (imágenes, HTML) al reporte HTML
from pytest_html import extras


# ======================================================
# FIXTURE DRIVER
# ======================================================

@pytest.fixture
def driver():

    # Paso 1: Configurar opciones de Chrome para correr sin ventana visible
    chrome_options = Options()

    # Modo headless: el navegador corre en segundo plano sin abrir ventana
    # Obligatorio en servidores CI como GitHub Actions que no tienen monitor
    chrome_options.add_argument("--headless")

    # Desactiva la caja de arena de seguridad de Chrome
    # Necesario en contenedores Linux donde el usuario es root
    chrome_options.add_argument("--no-sandbox")

    # Evita errores de memoria compartida en contenedores Docker/CI
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Define el tamaño de la ventana virtual para que los elementos se rendericen bien
    chrome_options.add_argument("--window-size=1920,1080")

    # Paso 2: Inicializar el driver con las opciones configuradas
    driver = webdriver.Chrome(options=chrome_options)

    # Paso 3: Entregar el driver al test que lo solicite
    yield driver

    # Paso 4: Cerrar el navegador al finalizar cada test (limpieza automática)
    driver.quit()


# ======================================================
# HOOK: SCREENSHOTS INCRUSTADOS EN EL REPORTE HTML
# ======================================================

# hookwrapper=True permite ejecutar código antes Y después del test
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    # Paso 1: Dejar que pytest ejecute el test normalmente
    outcome = yield

    # Paso 2: Obtener el resultado del test (passed, failed, error)
    report = outcome.get_result()

    # Paso 3: Recuperar la lista de extras ya existente en el reporte (o lista vacía)
    extra = getattr(report, "extra", [])

    # Paso 4: Solo actuar cuando el test falla durante su ejecución
    if report.when == "call" and report.failed:

        # Paso 5: Obtener el driver desde los argumentos del test
        driver = item.funcargs.get("driver", None)

        if driver:

            # Paso 6: Capturar la pantalla actual del navegador en formato base64
            # base64 permite incrustar la imagen directamente en el HTML sin archivos externos
            screenshot = driver.get_screenshot_as_base64()

            # Paso 7: Construir el elemento HTML con la imagen incrustada
            # onclick permite ver la imagen en tamaño completo al hacer clic
            html = (
                f'<div>'
                f'<img src="data:image/png;base64,{screenshot}" '
                f'alt="screenshot" style="width:304px;height:228px;" '
                f'onclick="window.open(this.src)" align="right"/>'
                f'</div>'
            )

            # Paso 8: Adjuntar el HTML con la imagen al reporte
            extra.append(extras.html(html))

    # Paso 9: Guardar los extras actualizados en el reporte final
    report.extra = extra