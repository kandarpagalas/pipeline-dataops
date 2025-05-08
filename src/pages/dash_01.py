import os
import pandas as pd
from sqlalchemy import create_engine
import streamlit as st

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
st.dataframe(df)
# st.dataframe(df1)
# st.dataframe(df2)
