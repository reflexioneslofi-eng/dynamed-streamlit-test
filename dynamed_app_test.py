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
    "Email de DynaMed",
    type="default"
)

if st.button("🚀 Probar acceso"):

    if not email:
        st.warning("Introduce primero tu email.")
        st.stop()

    options = Options()

    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)

    try:

        # --------------------------------------------------
        # 1. Abrir DynaMed
        # --------------------------------------------------

        driver.get("https://www.dynamed.com")

        time.sleep(5)

        # --------------------------------------------------
        # 2. Pulsar Sign In
        # --------------------------------------------------

        links = driver.find_elements(By.TAG_NAME, "a")

        for link in links:

            if "Sign In" in link.text.strip():

                driver.execute_script(
                    "arguments[0].click();",
                    link
                )

                break

        time.sleep(5)

        # --------------------------------------------------
        # 3. Aceptar cookies si aparecen
        # --------------------------------------------------

        buttons = driver.find_elements(
            By.TAG_NAME,
            "button"
        )

        for button in buttons:

            try:

                text = button.text.strip()

                if text == "Accept":

                    driver.execute_script(
                        "arguments[0].click();",
                        button
                    )

                    time.sleep(2)

                    break

            except Exception:
                pass

        # --------------------------------------------------
        # 4. Introducir email
        # --------------------------------------------------

        username = driver.find_element(
            By.ID,
            "username"
        )

        username.clear()

        username.send_keys(email)

        # --------------------------------------------------
        # 5. Buscar Continue
        # --------------------------------------------------

        continue_button = None

        buttons = driver.find_elements(
            By.TAG_NAME,
            "button"
        )

        for button in buttons:

            try:

                if button.text.strip() == "Continue":

                    continue_button = button
                    break

            except Exception:
                pass

        if continue_button is None:

            st.error(
                "No se encontró el botón Continue."
            )

            st.stop()

        # --------------------------------------------------
        # 6. Pulsar Continue mediante JavaScript
        # --------------------------------------------------

        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            continue_button
        )

        time.sleep(1)

        driver.execute_script(
            "arguments[0].click();",
            continue_button
        )

        time.sleep(5)

        # --------------------------------------------------
        # 7. Mostrar resultado
        # --------------------------------------------------

        st.success(
            "Email enviado. Selenium ha pulsado Continue."
        )

        st.write("URL después de Continue:")

        st.code(
            driver.current_url
        )

        st.write("Título:")

        st.code(
            driver.title
        )

        # --------------------------------------------------
        # 8. Captura
        # --------------------------------------------------

        screenshot_path = "/tmp/after_continue.png"

        driver.save_screenshot(
            screenshot_path
        )

        st.write(
            "Pantalla después de Continue:"
        )

        st.image(
            screenshot_path,
            use_container_width=True
        )

        # --------------------------------------------------
        # 9. Texto visible
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
