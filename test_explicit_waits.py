from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

# Inicializar navegador
driver = webdriver.Chrome()

# Espera explícita global
wait = WebDriverWait(driver, 10)

try:

    # ======================================================
    # CASO 1 - LOGIN EXITOSO
    # ======================================================

    print("Ejecutando Login Exitoso...")

    driver.get("https://www.saucedemo.com/")

    # Esperar campo usuario
    usuario = wait.until(
        EC.visibility_of_element_located((By.ID, "user-name"))
    )

    usuario.send_keys("standard_user")

    # Esperar campo password
    password = wait.until(
        EC.visibility_of_element_located((By.ID, "password"))
    )

    password.send_keys("secret_sauce")

    # Esperar botón login
    boton_login = wait.until(
        EC.element_to_be_clickable((By.ID, "login-button"))
    )

    boton_login.click()

    # Verificar acceso al inventario
    wait.until(
        EC.url_contains("inventory.html")
    )

    print("✅ Login exitoso validado")


    # ======================================================
    # CASO 2 - AGREGAR PRODUCTO AL CARRITO
    # ======================================================

    print("Agregando producto al carrito...")

    boton_carrito = wait.until(
        EC.element_to_be_clickable(
            (By.ID, "add-to-cart-sauce-labs-backpack")
        )
    )

    boton_carrito.click()

    badge = wait.until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "shopping_cart_badge")
        )
    )

    assert badge.text == "1"

    print("✅ Producto agregado correctamente")


    # ======================================================
    # CASO 3 - LOGIN FALLIDO
    # ======================================================

    print("Probando login fallido...")

    driver.delete_all_cookies()

    driver.get("https://www.saucedemo.com/")

    wait.until(
        EC.visibility_of_element_located((By.ID, "user-name"))
    ).send_keys("locked_out_user")

    wait.until(
        EC.visibility_of_element_located((By.ID, "password"))
    ).send_keys("secret_sauce")

    wait.until(
        EC.element_to_be_clickable((By.ID, "login-button"))
    ).click()

    mensaje_error = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "[data-test='error']")
        )
    )

    assert "locked out" in mensaje_error.text

    print("✅ Login fallido validado")


except TimeoutException:

    print("❌ Tiempo de espera agotado")

    driver.save_screenshot("timeout_error.png")


except Exception as e:

    print(f"❌ Error detectado: {e}")

    driver.save_screenshot("general_error.png")


finally:

    time.sleep(3)
    driver.quit()