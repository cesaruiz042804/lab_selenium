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

    # ERROR INTENCIONAL PARA PROBAR SCREENSHOT
    login.login(
        "usuario_incorrecto",
        "password_incorrecto"
    )

    assert "inventory.html" in driver.current_url