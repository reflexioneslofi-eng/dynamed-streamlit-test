#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

st.set_page_config(
    page_title="DynaMed Test",
    page_icon="📚"
)

st.title("📚 Prueba DynaMed + Selenium")

st.write(
    "Esta aplicación comprobará si Selenium puede "
    "abrir Chrome desde el servidor."
)

if st.button("🚀 Abrir DynaMed"):

    st.info("Iniciando Chrome...")

    options = Options()

    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        options=options
    )

    driver.get("https://www.dynamed.com")

    st.success("Chrome ha abierto DynaMed correctamente.")

    st.write("URL actual:")
    st.code(driver.current_url)

    st.write("Título:")
    st.code(driver.title)

    driver.quit()


# In[ ]:
