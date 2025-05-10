import os
import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
import matplotlib.pyplot as plt

st.title("dash_01")

# # 🔧 Configurações de conexão
# usuario = os.getenv("POSTGRES_USERs", "postgres")
# senha = os.getenv("POSTGRES_PASSWORDs", "z111pass")
# host = os.getenv("POSTGRES_HOSTs", "localhost")
# porta = os.getenv("POSTGRES_PORTs", "35432")
# banco = os.getenv("POSTGRES_DBs", "z111")

# # 🛠️ Criação da string de conexão
# conn_str = f"postgresql+psycopg2://{usuario}:{senha}@{host}:{porta}/{banco}"
# engine = create_engine(conn_str)

# tabela = "ORDERS"
# df = pd.read_sql(f"SELECT * FROM {tabela}", engine)
# st.write(f"Dados da tabela '{tabela}' lidos com sucesso:")


# Inicializa a conexão
conn = st.connection("postgresql", type="sql")

# Consulta SQL
query = """SELECT * FROM "ORDERS";"""

# Executa e converte em DataFrame
df = conn.query(query, ttl="10m")  # usa cache por 10 minutos
# df2 = pd.read_sql(query, conn.engine)

# Mostra os dados
# st.dataframe(df)
# st.dataframe(df1)
# st.dataframe(df2)
# Agrupamento por shipping_region_code e contagem de order_id
agrupado = df.groupby("shipping_region_code")["order_id"].count().reset_index()

# Renomear a coluna para melhor legenda no gráfico
agrupado.columns = ["shipping_region_code", "total_orders"]

st.header("Total de Pedidos por Região de Envio")
# Criação da figura
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(agrupado["shipping_region_code"], agrupado["total_orders"], color="skyblue")
ax.set_xlabel("Shipping Region Code")
ax.set_ylabel("Total de Pedidos (order_id)")
ax.set_title("Total de Pedidos por Região de Envio")
plt.xticks(rotation=45)
plt.tight_layout()

# Exibição no Streamlit
st.pyplot(fig)

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
# Criar a figura e os eixos
fig, ax = plt.subplots(figsize=(12, 6))

# Plotar o gráfico no eixo
pivotado.plot(kind="bar", ax=ax)

# Personalizações
ax.set_xlabel("Shipping Region Code")
ax.set_ylabel("Total de Pedidos (order_id)")
ax.set_title("Total de Pedidos por Região de Envio e Método de Pagamento")
ax.tick_params(axis="x", rotation=45)
ax.legend(title="Método de Pagamento")
plt.tight_layout()

# Exibir no Streamlit
st.pyplot(fig)


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

# Criar a figura
fig, ax = plt.subplots(figsize=(12, 6))

# Plotar a linha
ax.plot(
    agrupado["Mês"],
    agrupado["Total de Pedidos"],
    marker="o",
    linestyle="-",
    color="teal",
)

# Personalizações
ax.set_xlabel("Mês")
ax.set_ylabel("Total de Pedidos (order_id)")
ax.set_title("Total de Pedidos por Mês")
ax.tick_params(axis="x", rotation=45)
ax.grid(True)
plt.tight_layout()

# Exibir no Streamlit
st.pyplot(fig)


# Garantir que 'item_qtd' seja numérico
df["item_qtd"] = pd.to_numeric(df["item_qtd"], errors="coerce")

# Agrupar por item_id e somar as quantidades vendidas
agrupado = df.groupby("item_categoria")["item_qtd"].sum().reset_index()
agrupado.columns = ["Item ID", "Total de Itens Vendidos"]

# Ordenar por quantidade de itens vendidos
agrupado = agrupado.sort_values(by="Total de Itens Vendidos", ascending=False)


st.header("Total de Itens Vendidos por Categoria")

# Criar a figura
fig, ax = plt.subplots(figsize=(12, 6))

# Plotar as barras
ax.bar(agrupado["Item ID"], agrupado["Total de Itens Vendidos"], color="steelblue")

# Personalizações
ax.set_xlabel("Item Categoria")
ax.set_ylabel("Total de Itens Vendidos")
ax.set_title("Total de Itens Vendidos por Categoria")
ax.tick_params(axis="x", rotation=45)
plt.tight_layout()

# Exibir no Streamlit
st.pyplot(fig)
