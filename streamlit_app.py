import streamlit as st
from src.helpers.setup import load_env

load_env()

st.set_page_config(layout="wide")

dash_01 = st.Page(
    title="Itens",
    icon=":material/download:",
    page="src/pages/dash_01.py",
)
dash_02 = st.Page(
    title="Vendas",
    icon=":material/publish:",
    page="src/pages/dash_02.py",
)

pg = st.navigation(
    {
        "Dashboards": [dash_01, dash_02],
    }
)
pg.run()
