import os
import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
import matplotlib.pyplot as plt

st.title("QUANTIDADE DE VENDAS")

# Inicializa a conexão
conn = st.connection("postgresql", type="sql")

# Consulta SQL
query = """SELECT * FROM "ORDERS";"""

# Executa e converte em DataFrame
df = conn.query(query, ttl="10m")  # usa cache por 10 minutos
# df2 = pd.read_sql(query, conn.engine)

# Agrupamento por shipping_region_code e contagem de order_id
agrupado = df.groupby("shipping_region_code")["order_id"].count().reset_index()

# Renomear a coluna para melhor legenda no gráfico
agrupado.columns = ["shipping_region_code", "total_orders"]

st.header("Total de Pedidos por Região de Envio")
st.bar_chart(
    data=agrupado,
    x="shipping_region_code",
    y="total_orders",
    x_label="Shipping Region Code",
    y_label="Total de Pedidos (order_id)",
    color=None,
    horizontal=False,
    stack=None,
    width=None,
    height=None,
    use_container_width=True,
)


# Agrupamento por shipping_region_code e charge_payment_method, contando os order_id
agrupado = (
    df.groupby(["shipping_region_code", "charge_payment_method"])["order_id"]
    .count()
    .reset_index()
)

# Pivotar para formato de tabela com métodos de pagamento como colunas
pivotado = agrupado.pivot(
    index="shipping_region_code", columns="charge_payment_method", values="order_id"
).fillna(0)


st.header("Total de Pedidos por Região de Envio e Método de Pagamento")
st.bar_chart(
    data=pivotado,
    # x="shipping_region_code",
    # y="total_orders",
    x_label="Shipping Region Code",
    y_label="Total de Pedidos (order_id)",
    color=None,
    horizontal=False,
    stack=None,
    width=None,
    height=None,
    use_container_width=True,
)


# Converter 'created_at' para datetime, considerando fuso horário
df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")

# Criar uma nova coluna com o mês e ano no formato 'YYYY-MM'
df["mes"] = df["created_at"].dt.to_period("M").astype(str)

# Agrupar por mês e contar order_id
agrupado = df.groupby("mes")["order_id"].count().reset_index()
agrupado.columns = ["Mês", "Total de Pedidos"]

# Ordenar os meses cronologicamente
agrupado = agrupado.sort_values(by="Mês")

st.header("Total de Pedidos por Mês")
st.line_chart(
    data=agrupado,
    x="Mês",
    y="Total de Pedidos",
    x_label="Mês",
    y_label="Total de Pedidos (order_id)",
    color=None,
    width=None,
    height=None,
    use_container_width=True,
)


# Garantir que 'item_qtd' seja numérico
df["item_qtd"] = pd.to_numeric(df["item_qtd"], errors="coerce")

# Agrupar por item_id e somar as quantidades vendidas
agrupado = df.groupby("item_categoria")["item_qtd"].sum().reset_index()
agrupado.columns = ["Item ID", "Total de Itens Vendidos"]

# Ordenar por quantidade de itens vendidos
agrupado = agrupado.sort_values(by="Total de Itens Vendidos", ascending=False)


st.header("Total de Itens Vendidos por Categoria")
st.bar_chart(
    data=agrupado,
    x="Item ID",
    y="Total de Itens Vendidos",
    x_label="Item Categoria",
    y_label="Total de Itens Vendidos",
    color=None,
    horizontal=False,
    stack=None,
    width=None,
    height=None,
    use_container_width=True,
)
