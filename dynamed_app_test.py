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

if st.button("🚀 Probar acceso"):

    options = Options()

    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)

    try:

        # --------------------------------------------------
        # 1. DynaMed
        # --------------------------------------------------

        driver.get("https://www.dynamed.com")

        time.sleep(5)

        st.write("DynaMed:")
        st.code(driver.current_url)

        # --------------------------------------------------
        # 2. Sign In
        # --------------------------------------------------

        links = driver.find_elements(By.TAG_NAME, "a")

        for link in links:

            if "Sign In" in link.text.strip():

                link.click()
                break

        time.sleep(5)

        st.write("Login:")
        st.code(driver.current_url)

        st.write("Título:")
        st.code(driver.title)

        # --------------------------------------------------
        # 3. Buscar campos del formulario
        # --------------------------------------------------

        inputs = driver.find_elements(By.TAG_NAME, "input")

        st.write(f"Campos input encontrados: {len(inputs)}")

        for i, element in enumerate(inputs):

            try:

                st.write(
                    f"Input {i}: "
                    f"type={element.get_attribute('type')} | "
                    f"name={element.get_attribute('name')} | "
                    f"id={element.get_attribute('id')} | "
                    f"placeholder={element.get_attribute('placeholder')}"
                )

            except Exception:
                pass

        # --------------------------------------------------
        # 4. Buscar botones
        # --------------------------------------------------

        buttons = driver.find_elements(By.TAG_NAME, "button")

        st.write(f"Botones encontrados: {len(buttons)}")

        for i, button in enumerate(buttons):

            try:

                st.write(
                    f"Botón {i}: "
                    f"text='{button.text}' | "
                    f"type={button.get_attribute('type')}"
                )

            except Exception:
                pass

        # --------------------------------------------------
        # 5. Captura
        # --------------------------------------------------

        screenshot_path = "/tmp/login.png"

        driver.save_screenshot(screenshot_path)

        st.image(
            screenshot_path,
            use_container_width=True
        )

    finally:

        driver.quit()
