import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


st.set_page_config(
    page_title="DynaMed Test",
    page_icon="📚"
)

st.title("📚 DynaMed + Selenium")


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


if st.button("🚀 Login + buscar topic"):

    if not email or not password or not topic:
        st.warning("Introduce email, contraseña y topic.")
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


    # =========================================================
    # 1. DYNAMED
    # =========================================================

    st.info("Abriendo DynaMed...")

    driver.get(
        "https://www.dynamed.com"
    )

    time.sleep(5)


    # =========================================================
    # 2. SIGN IN
    # =========================================================

    st.info("Buscando Sign In...")

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


    # =========================================================
    # 3. COOKIES
    # =========================================================

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


    # =========================================================
    # 4. EMAIL
    # =========================================================

    st.info("Introduciendo email...")

    username = driver.find_element(
        By.ID,
        "username"
    )

    username.clear()

    username.send_keys(
        email
    )


    # =========================================================
    # 5. CONTINUE
    # =========================================================

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


    # =========================================================
    # 6. PASSWORD
    # =========================================================

    st.info("Introduciendo contraseña...")

    password_field = driver.find_element(
        By.ID,
        "password"
    )

    password_field.clear()

    password_field.send_keys(
        password
    )


    # =========================================================
    # 7. LOGIN
    # =========================================================

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


    # =========================================================
    # 8. BUSCAR TOPIC
    # =========================================================

    st.info(
        f'Buscando "{topic}"...'
    )

    search_box = driver.find_element(
        By.ID,
        "autosuggest"
    )

    search_box.clear()

    search_box.send_keys(
        topic
    )

    time.sleep(2)


    # =========================================================
    # 9. ENTER
    # =========================================================

    st.info(
        "Enviando búsqueda con ENTER..."
    )

    search_box.send_keys(
        Keys.ENTER
    )

    time.sleep(8)


    # =========================================================
    # 10. RESULTADO
    # =========================================================

    st.success(
        "Búsqueda enviada."
    )

    st.write(
        "### URL actual"
    )

    st.code(
        driver.current_url
    )


    st.write(
        "### Título"
    )

    st.code(
        driver.title
    )


       # =========================================================
    # 11. ENCONTRAR Y ABRIR EL RESULTADO EXACTO
    # =========================================================

    st.info(
        "Buscando el resultado exacto..."
    )

    links = driver.find_elements(
        By.TAG_NAME,
        "a"
    )

    target_link = None

    for link in links:

        try:

            text = link.text.strip()

            href = link.get_attribute(
                "href"
            )

            if (
                text.lower() == topic.lower()
                and href
                and "/condition/" in href
            ):

                target_link = link

                break

        except Exception:
            pass


    if target_link is None:

        st.error(
            "No se encontró el resultado exacto."
        )

        driver.quit()
        st.stop()


    target_href = target_link.get_attribute(
        "href"
    )

    target_text = target_link.text.strip()


    st.success(
        f"Resultado encontrado: {target_text}"
    )

    st.code(
        target_href
    )


    # =========================================================
    # ABRIR RESULTADO
    # =========================================================

    st.info(
        "Abriendo el resultado..."
    )

    driver.execute_script(
        "arguments[0].click();",
        target_link
    )

    time.sleep(8)


    # =========================================================
    # COMPROBAR PÁGINA FINAL
    # =========================================================

    st.success(
        "Resultado abierto."
    )

    st.write(
        "### URL final"
    )

    st.code(
        driver.current_url
    )

    st.write(
        "### Título final"
    )

    st.code(
        driver.title
    )

    # =========================================================
    # 12. TEXTO DE LA PÁGINA
    # =========================================================

    body_text = driver.find_element(
        By.TAG_NAME,
        "body"
    ).text


    st.write(
        "### Texto visible de la página"
    )

    st.text(
        body_text[:12000]
    )


    # =========================================================
    # 13. SCREENSHOT
    # =========================================================

    screenshot_path = (
        "/tmp/search_results.png"
    )

    driver.save_screenshot(
        screenshot_path
    )

    st.image(
        screenshot_path,
        caption="Página de resultados",
        use_container_width=True
    )


    # =========================================================
    # 14. CERRAR CHROME
    # =========================================================

    driver.quit()
