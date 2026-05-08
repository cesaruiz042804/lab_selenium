from login_page import LoginPage


# ======================================================
# LOGIN EXITOSO
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
# LOGIN FALLIDO
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