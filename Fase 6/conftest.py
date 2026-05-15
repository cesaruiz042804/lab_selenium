import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pytest_html import extras


# ======================================================
# FIXTURE DRIVER
# ======================================================

@pytest.fixture
def driver():

    chrome_options = Options()

    # Headless para GitHub Actions
    chrome_options.add_argument("--headless")

    chrome_options.add_argument("--no-sandbox")

    chrome_options.add_argument("--disable-dev-shm-usage")

    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)

    yield driver

    driver.quit()


# ======================================================
# SCREENSHOTS INCRUSTADOS EN EL REPORTE HTML
# ======================================================

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()

    extra = getattr(report, "extra", [])

    if report.when == "call" and report.failed:

        driver = item.funcargs.get("driver", None)

        if driver:

            screenshot = driver.get_screenshot_as_base64()

            html = (
                f'<div>'
                f'<img src="data:image/png;base64,{screenshot}" '
                f'alt="screenshot" style="width:304px;height:228px;" '
                f'onclick="window.open(this.src)" align="right"/>'
                f'</div>'
            )

            extra.append(extras.html(html))

    report.extra = extra