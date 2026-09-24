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

if st.button("🚀 Abrir DynaMed"):

    st.info("Iniciando Chromium en el servidor...")

    options = Options()

    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)

    try:

        # Abrir DynaMed
        driver.get("https://www.dynamed.com")

        time.sleep(5)

        st.success("DynaMed abierto correctamente.")

        st.write("URL inicial:")
        st.code(driver.current_url)

        st.write("Título:")
        st.code(driver.title)

        # Buscar enlaces que contengan "Sign In"
        links = driver.find_elements(By.TAG_NAME, "a")

        sign_in_found = False

        for link in links:

            text = link.text.strip()

            if "Sign In" in text:

                st.info(f"Encontrado: {text}")

                link.click()

                sign_in_found = True

                break

        if not sign_in_found:

            st.warning("No se encontró automáticamente el enlace Sign In.")

        else:

            time.sleep(5)

            st.write("URL después de pulsar Sign In:")
            st.code(driver.current_url)

            st.write("Título:")
            st.code(driver.title)

            # Captura
            screenshot_path = "/tmp/dynamed_login.png"

            driver.save_screenshot(screenshot_path)

            st.write("Pantalla que está viendo Selenium:")

            st.image(
                screenshot_path,
                use_container_width=True
            )

            # Texto
            body_text = driver.find_element(
                By.TAG_NAME,
                "body"
            ).text

            st.write("Texto visible:")

            st.text(body_text[:5000])

    finally:

        driver.quit()
