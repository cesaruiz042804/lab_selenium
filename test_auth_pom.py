from selenium import webdriver
from login_page import LoginPage
import time


# Inicializar navegador
driver = webdriver.Chrome()

# Crear objeto LoginPage
login = LoginPage(driver)

try:

    # ======================================================
    # CASO 1 - LOGIN EXITOSO
    # ======================================================

    print("Ejecutando Login Exitoso...")

    login.open()

    login.login(
        "standard_user",
        "secret_sauce"
    )

    assert "inventory.html" in driver.current_url

    print("✅ Login exitoso validado")


    # ======================================================
    # CASO 2 - LOGIN FALLIDO
    # ======================================================

    print("Ejecutando Login Fallido...")

    driver.delete_all_cookies()

    login.open()

    login.login(
        "locked_out_user",
        "secret_sauce"
    )

    error = login.get_error_message()

    assert "locked out" in error

    print("✅ Login fallido validado")


except Exception as e:

    print(f"❌ Error detectado: {e}")

    driver.save_screenshot("screenshots/error.png")


finally:

    time.sleep(3)
    driver.quit()