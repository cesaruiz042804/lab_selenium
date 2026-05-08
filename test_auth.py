import pytest
from selenium import webdriver
from login_page import LoginPage


# ======================================================
# FIXTURE - Inicializar navegador
# ======================================================

@pytest.fixture
def driver():

    driver = webdriver.Chrome()

    yield driver

    driver.quit()


# ======================================================
# CASO 1 - LOGIN EXITOSO
# ======================================================

def test_login_exitoso(driver):

    login = LoginPage(driver)

    login.open()

    login.login(
        "standard_user",
        "secret_sauce"
    )

    assert "inventory.html" in driver.current_url


# ======================================================
# CASO 2 - LOGIN FALLIDO
# ======================================================

def test_login_fallido(driver):

    login = LoginPage(driver)

    login.open()

    login.login(
        "locked_out_user",
        "secret_sauce"
    )

    error = login.get_error_message()

    assert "locked out" in error