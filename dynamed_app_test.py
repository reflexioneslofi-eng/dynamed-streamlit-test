import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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
        driver.get("https://www.dynamed.com")

        time.sleep(5)

        st.success("Chromium ha abierto DynaMed correctamente.")

        st.write("URL actual:")
        st.code(driver.current_url)

        st.write("Título:")
        st.code(driver.title)

        # Captura de pantalla del navegador remoto
        screenshot_path = "/tmp/dynamed.png"
        driver.save_screenshot(screenshot_path)

        st.write("Captura de lo que está viendo Selenium:")

        st.image(
            screenshot_path,
            use_container_width=True
        )

        # Texto visible de la página
        st.write("Texto visible:")

        body_text = driver.find_element("tag name", "body").text

        st.text(body_text[:5000])

    finally:
        driver.quit()
