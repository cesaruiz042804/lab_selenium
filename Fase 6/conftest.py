import pytest
import os

from datetime import datetime

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
# SCREENSHOTS AUTOMÁTICOS
# ======================================================

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:

        driver = item.funcargs.get("driver", None)

        if driver:

            os.makedirs("screenshots", exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            screenshot_file = (
                f"screenshots/{item.name}_{timestamp}.png"
            )

            driver.save_screenshot(screenshot_file)

            report.extras = getattr(report, "extras", [])

            report.extras.append(
                extras.image(screenshot_file)
            )