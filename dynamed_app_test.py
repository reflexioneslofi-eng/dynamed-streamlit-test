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

N_TOPICS_TEST = 3


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


        search_box.clear()


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
        # BUSCAR CONDITION
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


                if (
                    text.lower() == topic.lower()
                    and href
                    and "/condition/" in href
                ):

                    target_link = link

                    break


            except Exception:

                pass


        # =================================================
        # ABRIR CONDITION
        # =================================================

        if target_link is None:

            st.error(
                f"No se encontró Condition para: {topic}"
            )

            continue


        target_href = target_link.get_attribute(
            "href"
        )


        st.success(
            f"Condition encontrado: {target_href}"
        )


        driver.execute_script(
            "arguments[0].click();",
            target_link
        )


        time.sleep(6)


        st.write(
            f"URL final: {driver.current_url}"
        )


        # =================================================
        # COMPROBAR QUE ESTAMOS EN EL TOPIC
        # =================================================

        if "/condition/" in driver.current_url:

            st.success(
                "✓ Topic abierto correctamente."
            )

        else:

            st.warning(
                "La URL final no parece corresponder "
                "a un Condition."
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
