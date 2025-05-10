import os
import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
import matplotlib.pyplot as plt

st.title("VALOR DE VENDAS")

# Inicializa a conexão
conn = st.connection("postgresql", type="sql")

# Consulta SQL
query = """SELECT * FROM "ORDERS";"""

# Executa e converte em DataFrame
df = conn.query(query, ttl="10m")  # usa cache por 10 minutos
# df2 = pd.read_sql(query, conn.engine)


# Agrupar e somar o valor de charge_paid por shipping_region_code
agrupado = df.groupby("shipping_region_code")["charge_paid"].sum().reset_index()

# Ordenar do maior para o menor
agrupado = agrupado.sort_values(by="charge_paid", ascending=False)

st.header(("Total de Vendas por Região de Envio"))
st.bar_chart(
    data=agrupado,
    x="shipping_region_code",
    y="charge_paid",
    x_label="Código de Região",
    y_label="Total Pago (charge_paid)",
    color=None,
    horizontal=False,
    stack=None,
    width=None,
    height=None,
    use_container_width=True,
)


# Garantir que charge_paid seja numérico (caso necessário)
df["charge_paid"] = pd.to_numeric(df["charge_paid"], errors="coerce")

# Agrupamento por região e método de pagamento, somando charge_paid
agrupado = (
    df.groupby(["shipping_region_code", "charge_payment_method"])["charge_paid"]
    .sum()
    .reset_index()
)

# Pivotar para ter métodos de pagamento como colunas
pivotado = agrupado.pivot(
    index="shipping_region_code", columns="charge_payment_method", values="charge_paid"
).fillna(0)


st.header("Total de Vendas por Região de Envio e Método de Pagamento")
st.bar_chart(
    data=pivotado,
    # x="shipping_region_code",
    # y="total_orders",
    x_label="Código de Região",
    y_label="Total Pago (charge_paid)",
    color=None,
    horizontal=False,
    stack=None,
    width=None,
    height=None,
    use_container_width=True,
)


# Converter 'created_at' para datetime
df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")

# Converter 'charge_paid' para numérico (caso necessário)
df["charge_paid"] = pd.to_numeric(df["charge_paid"], errors="coerce")

# Criar coluna com mês e ano no formato 'YYYY-MM'
df["mes"] = df["created_at"].dt.to_period("M").astype(str)

# Agrupar por mês e somar charge_paid
agrupado = df.groupby("mes")["charge_paid"].sum().reset_index()
agrupado.columns = ["Mês", "Total Pago"]

# Ordenar os meses cronologicamente
agrupado = agrupado.sort_values(by="Mês")

st.header("Total de Vendas por Mês")
st.line_chart(
    data=agrupado,
    x="Mês",
    y="Total Pago",
    x_label="Mês",
    y_label="Total de Vendas (charge_paid)",
    color=None,
    width=None,
    height=None,
    use_container_width=True,
)


# Agrupar por item_categoria e somar charge_paid
agrupado = df.groupby("item_categoria")["charge_paid"].sum().reset_index()

# Renomear as colunas para facilitar
agrupado.columns = ["Item Categoria", "Total Pago (charge_paid)"]

# Ordenar para facilitar a visualização
agrupado = agrupado.sort_values(by="Total Pago (charge_paid)", ascending=False)

st.header("Total Pago por Categoria de Item")
st.bar_chart(
    data=agrupado,
    x="Item Categoria",
    y="Total Pago (charge_paid)",
    x_label="Item Categoria",
    y_label="Total Pago (charge_paid)",
    color=None,
    horizontal=False,
    stack=None,
    width=None,
    height=None,
    use_container_width=True,
)
