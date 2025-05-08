import os
import pandas as pd
from sqlalchemy import create_engine


def load_to_postgres(df):

    # Configurações do banco de dados
    POSTGRES_HOST = os.getenv("POSTGRES_HOSTs", "localhost:35432")
    POSTGRES_USER = os.getenv("POSTGRES_USERs", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORDs", "z111pass")
    POSTGRES_DB = os.getenv("POSTGRES_DBs", "z111")

    # Criar engine de conexão com o PostgreSQL
    engine = create_engine(
        f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"
    )

    tabela_destino = "ORDERS"
    # Inserir dados no PostgreSQL (substitui a tabela, se existir)
    df.to_sql(tabela_destino, engine, if_exists="replace", index=False)

    print("Carga de dados concluída com sucesso!")
