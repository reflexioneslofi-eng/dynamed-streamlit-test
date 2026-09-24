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

topic = st.text_input(
    "Topic a buscar",
    value="hip fracture"
)


if st.button("🚀 Login + inspeccionar topic"):

    if not email or not password or not topic:

        st.warning(
            "Introduce email, contraseña y topic."
        )

        st.stop()


    # =========================================================
    # CHROME
    # =========================================================

    options = Options()

    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        options=options
    )


    try:

        # =====================================================
        # 1. ABRIR DYNAMED
        # =====================================================

        st.info("Abriendo DynaMed...")

        driver.get(
            "https://www.dynamed.com"
        )

        time.sleep(5)


        # =====================================================
        # 2. SIGN IN
        # =====================================================

        st.info("Accediendo al login...")

        links = driver.find_elements(
            By.TAG_NAME,
            "a"
        )

        for link in links:

            try:

                if "Sign In" in link.text.strip():

                    driver.execute_script(
                        "arguments[0].click();",
                        link
                    )

                    break

            except Exception:
                pass


        time.sleep(5)


        # =====================================================
        # 3. COOKIES
        # =====================================================

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


        # =====================================================
        # 4. EMAIL
        # =====================================================

        username = driver.find_element(
            By.ID,
            "username"
        )

        username.clear()

        username.send_keys(
            email
        )


        # =====================================================
        # 5. CONTINUE
        # =====================================================

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


        # =====================================================
        # 6. PASSWORD
        # =====================================================

        password_field = driver.find_element(
            By.ID,
            "password"
        )

        password_field.clear()

        password_field.send_keys(
            password
        )


        # =====================================================
        # 7. LOGIN
        # =====================================================

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
                "No se encontró el botón Continue."
            )

            st.stop()


        driver.execute_script(
            "arguments[0].click();",
            login_button
        )


        time.sleep(8)


        st.success(
            "Login realizado correctamente."
        )


        # =====================================================
        # 8. BUSCAR TOPIC
        # =====================================================

        st.info(
            f"Buscando: {topic}"
        )


        search_box = driver.find_element(
            By.ID,
            "autosuggest"
        )

        search_box.clear()

        search_box.send_keys(
            topic
        )


        time.sleep(4)


# =====================================================
# 9. COMPROBAR PÁGINA DE RESULTADOS
# =====================================================

st.success(
    "Búsqueda enviada."
)

st.write("URL de búsqueda:")

st.code(
    driver.current_url
)

st.write("Título:")

st.code(
    driver.title
)


# =====================================================
# 10. BUSCAR ENLACES DE RESULTADOS
# =====================================================

st.info(
    "Buscando resultados reales..."
)

links = driver.find_elements(
    By.TAG_NAME,
    "a"
)


results = []

for link in links:

    try:

        text = link.text.strip()

        href = link.get_attribute("href")

        if text and href:

            results.append(
                (
                    text,
                    href
                )
            )

    except Exception:
        pass


st.write(
    f"Enlaces encontrados: {len(results)}"
)


# =====================================================
# 11. MOSTRAR RESULTADOS
# =====================================================

for text, href in results:

    if (
        "hip fracture" in text.lower()
        or "hip-fracture" in href.lower()
    ):

        st.write(
            f"**{text}**"
        )

        st.code(
            href
        )


# =====================================================
# 12. CAPTURA
# =====================================================

screenshot_path = "/tmp/search_results.png"

driver.save_screenshot(
    screenshot_path
)

st.image(
    screenshot_path,
    caption="Página completa de resultados",
    use_container_width=True
)


# =====================================================
# 13. TEXTO VISIBLE
# =====================================================

body_text = driver.find_element(
    By.TAG_NAME,
    "body"
).text


st.write(
    "Texto visible:"
)

st.text(
    body_text[:12000]
)


    finally:

        driver.quit()
