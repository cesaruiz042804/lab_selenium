import pytest
import os
from datetime import datetime


# ======================================================
# HOOK PARA CAPTURAR SCREENSHOTS EN FALLOS
# ======================================================

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()

    # Solo cuando falla el test
    if report.when == "call" and report.failed:

        driver = item.funcargs.get("driver", None)

        if driver:

            # Crear carpeta screenshots
            os.makedirs("screenshots", exist_ok=True)

            # Nombre único del archivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            screenshot_file = (
                f"screenshots/{item.name}_{timestamp}.png"
            )

            # Guardar screenshot
            driver.save_screenshot(screenshot_file)

            # Adjuntar al reporte HTML
            if hasattr(report, "extra"):

                from pytest_html import extras

                report.extra.append(
                    extras.image(screenshot_file)
                )