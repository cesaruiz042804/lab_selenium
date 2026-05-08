from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Inicializar navegador
driver = webdriver.Chrome()

# Espera explícita
wait = WebDriverWait(driver, 10)

def ejecutar_pruebas():

    try:

        # ======================================================
        # CASO 1 - LOGIN EXITOSO
        # ======================================================

        print("Ejecutando Caso 1: Login Exitoso")

        driver.get("https://www.saucedemo.com/")

        wait.until(
            EC.visibility_of_element_located((By.ID, "user-name"))
        ).send_keys("standard_user")

        driver.find_element(By.ID, "password").send_keys("secret_sauce")

        driver.find_element(By.ID, "login-button").click()

        # Validar redirección
        assert "inventory.html" in driver.current_url

        print("✅ Login exitoso completado")


        # ======================================================
        # CASO 2 - AGREGAR PRODUCTO AL CARRITO
        # ======================================================

        print("Ejecutando Caso 2: Agregar al carrito")

        boton_agregar = wait.until(
            EC.element_to_be_clickable(
                (By.ID, "add-to-cart-sauce-labs-backpack")
            )
        )

        boton_agregar.click()

        badge_carrito = driver.find_element(
            By.CLASS_NAME,
            "shopping_cart_badge"
        ).text

        assert badge_carrito == "1"

        print("✅ Producto agregado correctamente")


        # ======================================================
        # CASO 3 - LOGIN FALLIDO
        # ======================================================

        print("Ejecutando Caso 3: Login Fallido")

        # Limpiar sesión
        driver.delete_all_cookies()

        driver.get("https://www.saucedemo.com/")

        wait.until(
            EC.visibility_of_element_located((By.ID, "user-name"))
        ).send_keys("locked_out_user")

        driver.find_element(By.ID, "password").send_keys("secret_sauce")

        driver.find_element(By.ID, "login-button").click()

        error_msg = wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "[data-test='error']")
            )
        ).text

        assert "Sorry, this user has been locked out" in error_msg

        print("✅ Login fallido validado correctamente")

    except Exception as e:

        print(f"❌ Error durante la ejecución: {e}")

        # Captura de pantalla automática
        driver.save_screenshot("error_screenshot.png")

    finally:

        time.sleep(3)
        driver.quit()


# Ejecutar pruebas
ejecutar_pruebas()