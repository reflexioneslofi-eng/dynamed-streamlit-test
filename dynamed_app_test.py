import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


st.set_page_config(
    page_title="Pregunteitor",
    page_icon="📚"
)

st.title("📚 Pregunteitor")


# =========================================================
# CONFIGURACIÓN
# =========================================================

TOPICS_FILE = "topics_1.csv"

N_TOPICS_TEST = 99


# =========================================================
# CARGAR CSV
# =========================================================

try:

    df = pd.read_csv(
        TOPICS_FILE,
        sep=";",
        encoding="latin1"
    )

except Exception as e:

    st.error(
        f"No se pudo cargar {TOPICS_FILE}"
    )

    st.exception(e)

    st.stop()


if "topic" not in df.columns:

    st.error(
        f"No se encontró la columna 'topic'. "
        f"Columnas encontradas: {list(df.columns)}"
    )

    st.stop()


topics = (
    df["topic"]
    .dropna()
    .astype(str)
    .tolist()
)


topics_test = topics[:N_TOPICS_TEST]


st.success(
    f"{TOPICS_FILE} cargado correctamente: "
    f"{len(topics)} topics."
)


st.write(
    "### Topics que se van a probar"
)


for i, topic in enumerate(
    topics_test,
    start=1
):

    st.write(
        f"{i}. {topic}"
    )


# =========================================================
# DATOS DE LOGIN
# =========================================================

email = st.text_input(
    "Email de DynaMed"
)

password = st.text_input(
    "Contraseña de DynaMed",
    type="password"
)


# =========================================================
# BOTÓN
# =========================================================

if st.button("🚀 Ejecutar Pregunteitor"):

    if not email or not password:

        st.warning(
            "Introduce email y contraseña."
        )

        st.stop()


    # =====================================================
    # CHROME
    # =====================================================

    options = Options()

    options.add_argument(
        "--headless"
    )

    options.add_argument(
        "--no-sandbox"
    )

    options.add_argument(
        "--disable-dev-shm-usage"
    )

    options.add_argument(
        "--window-size=1920,1080"
    )


    driver = webdriver.Chrome(
        options=options
    )


    # =====================================================
    # LOGIN DYNAMED
    # =====================================================

    st.info(
        "Abriendo DynaMed..."
    )

    driver.get(
        "https://www.dynamed.com"
    )

    time.sleep(5)


    st.info(
        "Buscando Sign In..."
    )


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
    # COOKIES
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
    # EMAIL
    # =====================================================

    st.info(
        "Introduciendo email..."
    )


    username = driver.find_element(
        By.ID,
        "username"
    )


    username.clear()

    username.send_keys(
        email
    )


    # =====================================================
    # CONTINUE EMAIL
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
    # PASSWORD
    # =====================================================

    st.info(
        "Introduciendo contraseña..."
    )


    password_field = driver.find_element(
        By.ID,
        "password"
    )


    password_field.clear()

    password_field.send_keys(
        password
    )


    # =====================================================
    # LOGIN
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

        driver.quit()

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
    # PROCESAR LOS 3 TOPICS
    # =====================================================

    for number, topic in enumerate(
        topics_test,
        start=1
    ):

        st.write(
            "---"
        )

        st.subheader(
            f"Topic {number}/{len(topics_test)}: {topic}"
        )


        # =================================================
        # BUSCADOR
        # =================================================

        st.info(
            f'Buscando "{topic}"...'
        )


        search_box = driver.find_element(
            By.ID,
            "autosuggest"
        )


        # -------------------------------------------------
        # LIMPIAR CORRECTAMENTE EL CAMPO REACT
        # -------------------------------------------------

        search_box.click()

        search_box.send_keys(
            Keys.CONTROL,
            "a"
        )

        search_box.send_keys(
            Keys.BACKSPACE
        )

        time.sleep(1)


        # =================================================
        # ESCRIBIR TOPIC
        # =================================================

        search_box.send_keys(
            topic
        )

        time.sleep(2)


        # =================================================
        # ENTER
        # =================================================

        search_box.send_keys(
            Keys.ENTER
        )

        time.sleep(6)


        st.write(
            f"Resultados: {driver.current_url}"
        )


        # =================================================
        # BUSCAR RESULTADOS DE CONTENIDO
        # =================================================

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


                if not href:
                    continue


                # Solo enlaces que llevan a contenido
                # real de DynaMed.

                is_content = (
                    "/condition/" in href
                    or "/drug-monograph/" in href
                    or "/management/" in href
                    or "/evaluation/" in href
                    or "/prevention/" in href
                    or "/procedure/" in href
                    or "/approach-to/" in href
                )


                if is_content:

                    target_link = link

                    break


            except Exception:

                pass


        # =================================================
        # ABRIR RESULTADO
        # =================================================

        if target_link is None:

            st.warning(
                f"No se encontró un resultado de contenido "
                f"para: {topic}"
            )

            continue


        target_text = target_link.text.strip()

        target_href = target_link.get_attribute(
            "href"
        )


        st.success(
            f"Resultado encontrado: {target_text}"
        )


        st.code(
            target_href
        )


        # =================================================
        # ABRIR
        # =================================================

        driver.execute_script(
            "arguments[0].click();",
            target_link
        )


        time.sleep(6)


        st.write(
            f"URL final: {driver.current_url}"
        )


        # =================================================
        # COMPROBAR
        # =================================================

        if (
            "/condition/" in driver.current_url
            or "/drug-monograph/" in driver.current_url
            or "/management/" in driver.current_url
            or "/evaluation/" in driver.current_url
            or "/prevention/" in driver.current_url
            or "/procedure/" in driver.current_url
            or "/approach-to/" in driver.current_url
        ):

            st.success(
                "✓ Resultado abierto correctamente."
            )

        else:

            st.warning(
                "La URL final no parece corresponder "
                "a contenido de DynaMed."
            )


    # =====================================================
    # FIN
    # =====================================================

    st.write(
        "---"
    )


    st.success(
        "🎉 Prueba de los 3 topics terminada."
    )


    # =====================================================
    # CERRAR CHROME
    # =====================================================

    driver.quit()
