import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time


st.set_page_config(
    page_title="DynaMed Test",
    page_icon="📚"
)

st.title("📚 Prueba DynaMed + Selenium")

email = st.text_input(
    "Email de DynaMed"
)

password = st.text_input(
    "Contraseña de DynaMed",
    type="password"
)

if st.button("🚀 Iniciar sesión"):

    if not email or not password:
        st.warning(
            "Introduce email y contraseña."
        )
        st.stop()

    options = Options()

    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        options=options
    )

    try:

        # --------------------------------------------------
        # 1. Abrir DynaMed
        # --------------------------------------------------

        driver.get(
            "https://www.dynamed.com"
        )

        time.sleep(5)

        # --------------------------------------------------
        # 2. Sign In
        # --------------------------------------------------

        links = driver.find_elements(
            By.TAG_NAME,
            "a"
        )

        for link in links:

            if "Sign In" in link.text.strip():

                driver.execute_script(
                    "arguments[0].click();",
                    link
                )

                break

        time.sleep(5)

        # --------------------------------------------------
        # 3. Cookies
        # --------------------------------------------------

        buttons = driver.find_elements(
            By.TAG_NAME,
            "button"
        )

        for button in buttons:

            try:

                if button.text.strip() == "Accept":

                    driver.execute_script(
                        "arguments[0].click();",
                        button
                    )

                    time.sleep(2)

                    break

            except Exception:
                pass

        # --------------------------------------------------
        # 4. Email
        # --------------------------------------------------

        username = driver.find_element(
            By.ID,
            "username"
        )

        username.clear()

        username.send_keys(
            email
        )

        # --------------------------------------------------
        # 5. Continue
        # --------------------------------------------------

        buttons = driver.find_elements(
            By.TAG_NAME,
            "button"
        )

        for button in buttons:

            try:

                if button.text.strip() == "Continue":

                    driver.execute_script(
                        "arguments[0].click();",
                        button
                    )

                    break

            except Exception:
                pass

        time.sleep(5)

        # --------------------------------------------------
        # 6. Contraseña
        # --------------------------------------------------

        password_field = driver.find_element(
            By.ID,
            "password"
        )

        password_field.clear()

        password_field.send_keys(
            password
        )

        # --------------------------------------------------
        # 7. Login
        # --------------------------------------------------

        buttons = driver.find_elements(
            By.TAG_NAME,
            "button"
        )

        login_button = None

        for button in buttons:

            try:

                if button.text.strip() == "Continue":

                    login_button = button
                    break

            except Exception:
                pass

        if login_button is None:

            st.error(
                "No se encontró el botón Continue después de introducir la contraseña."
            )

            st.stop()

        driver.execute_script(
            "arguments[0].click();",
            login_button
        )

        # --------------------------------------------------
        # 8. Esperar login
        # --------------------------------------------------

        time.sleep(8)

        # --------------------------------------------------
        # 9. Resultado
        # --------------------------------------------------

        st.write(
            "URL después del login:"
        )

        st.code(
            driver.current_url
        )

        st.write(
            "Título:"
        )

        st.code(
            driver.title
        )

        # --------------------------------------------------
        # 10. Captura
        # --------------------------------------------------

        screenshot_path = (
            "/tmp/after_login.png"
        )

        driver.save_screenshot(
            screenshot_path
        )

        st.write(
            "Pantalla después del login:"
        )

        st.image(
            screenshot_path,
            use_container_width=True
        )

        # --------------------------------------------------
        # 11. Texto
        # --------------------------------------------------

        body_text = driver.find_element(
            By.TAG_NAME,
            "body"
        ).text

        st.write(
            "Texto visible:"
        )

        st.text(
            body_text[:5000]
        )

    finally:

        driver.quit()
