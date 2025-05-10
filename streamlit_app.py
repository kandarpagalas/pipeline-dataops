import streamlit as st
from src.helpers.setup import load_env

load_env()


st.set_page_config(layout="wide")

dash_01 = st.Page(
    title="QUANTIDADE DE VENDAS",
    icon=":material/shopping_cart:",
    page="src/pages/dash_01.py",
)
dash_02 = st.Page(
    title="VALOR DE VENDAS",
    icon=":material/payments:",
    page="src/pages/dash_02.py",
)

pg = st.navigation(
    {
        "Dashboards": [dash_01, dash_02],
    }
)
pg.run()
