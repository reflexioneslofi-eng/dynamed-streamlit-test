import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="Pregunteitor",
    page_icon="📚"
)

st.title("📚 Pregunteitor")


# =========================================================
# CARGAR CSV
# =========================================================

TOPICS_FILE = "topics_1.csv"


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


# =========================================================
# COMPROBAR COLUMNA
# =========================================================

if "topic" not in df.columns:

    st.error(
        f"No se encontró la columna 'topic'. "
        f"Columnas encontradas: {list(df.columns)}"
    )

    st.stop()


# =========================================================
# MOSTRAR INFORMACIÓN
# =========================================================

st.success(
    f"{TOPICS_FILE} cargado correctamente."
)

st.write(
    f"Topics encontrados: **{len(df)}**"
)


st.write(
    "### Primeros 10 topics"
)


for i, topic in enumerate(
    df["topic"].head(10),
    start=1
):

    st.write(
        f"{i}. {topic}"
    )
