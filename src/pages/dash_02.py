import os
import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
import matplotlib.pyplot as plt

st.title("dash_02")

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
# Criar a figura
fig, ax = plt.subplots(figsize=(10, 6))

# Plotar as barras
ax.bar(
    agrupado["shipping_region_code"], agrupado["charge_paid"], color="cornflowerblue"
)

# Personalizações
ax.set_xlabel("Shipping Region Code")
ax.set_ylabel("Total Pago (charge_paid)")
ax.set_title("Total de Vendas por Região de Envio")
ax.tick_params(axis="x", rotation=45)
plt.tight_layout()

# Exibir no Streamlit
st.pyplot(fig)


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
# Criar a figura e o eixo
fig, ax = plt.subplots(figsize=(12, 6))

# Plotar gráfico de barras agrupadas
pivotado.plot(kind="bar", ax=ax)

# Personalizações
ax.set_xlabel("Shipping Region Code")
ax.set_ylabel("Total Pago (charge_paid)")
ax.set_title("Total de Vendas por Região de Envio e Método de Pagamento")
ax.tick_params(axis="x", rotation=45)
ax.legend(title="Método de Pagamento")
plt.tight_layout()

# Exibir no Streamlit
st.pyplot(fig)


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

# Criar a figura e o eixo
fig, ax = plt.subplots(figsize=(12, 6))

# Plotar gráfico de linha
ax.plot(
    agrupado["Mês"], agrupado["Total Pago"], marker="o", linestyle="-", color="orange"
)

# Personalizações
ax.set_xlabel("Mês")
ax.set_ylabel("Total de Vendas (charge_paid)")
ax.set_title("Total de Vendas por Mês")
ax.tick_params(axis="x", rotation=45)
ax.grid(True)
plt.tight_layout()

# Exibir no Streamlit
st.pyplot(fig)


# Agrupar por item_categoria e somar charge_paid
agrupado = df.groupby("item_categoria")["charge_paid"].sum().reset_index()

# Renomear as colunas para facilitar
agrupado.columns = ["Item Categoria", "Total Pago (charge_paid)"]

# Ordenar para facilitar a visualização
agrupado = agrupado.sort_values(by="Total Pago (charge_paid)", ascending=False)

st.header("Total Pago por Categoria de Item")

# Criar a figura e o eixo
fig, ax = plt.subplots(figsize=(12, 6))

# Plotar gráfico de barras
ax.bar(
    agrupado["Item Categoria"], agrupado["Total Pago (charge_paid)"], color="seagreen"
)

# Personalizações
ax.set_xlabel("Item Categoria")
ax.set_ylabel("Total Pago (charge_paid)")
ax.set_title("Total Pago por Categoria de Item")
ax.tick_params(axis="x", rotation=45)
plt.tight_layout()

# Exibir no Streamlit
st.pyplot(fig)
