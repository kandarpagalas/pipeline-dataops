import os
import pandas as pd
import boto3
from botocore.client import Config
from sqlalchemy import create_engine
import io


def load_to_postgres(file_key):

    # Configurações do banco de dados
    POSTGRES_HOST = os.getenv("POSTGRES_HOSTs", "postgres_z:5432")
    POSTGRES_USER = os.getenv("POSTGRES_USERs", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORDs", "z111pass")
    POSTGRES_DB = os.getenv("POSTGRES_DBs", "z111")

    # Configurações do MinIO
    MINIO_ENDPOINT = os.getenv(
        "MINIO_ENDPOINTs", "http://minio:9000"
    )  # ou o IP/host do seu servidor MinIO

    # Deve gerar uma nova Cresencial no 1o acesso ao minio
    MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEYs", "h31kVG1KwaTvywDIajQd")
    MINIO_SECRET_KEY = os.getenv(
        "MINIO_SECRET_KEYs", "DT6Oy2nbumi6LEtIA4tRWB3AV5n4P0YWVO2D3ctD"
    )
    bucket_name = "staging"

    # Conexão com o MinIO
    s3 = boto3.client(
        "s3",
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
        config=Config(signature_version="s3v4"),
        region_name="us-east-1",  # Pode ser qualquer coisa no caso do MinIO
    )

    # Coletar dados do arquivo
    obj = s3.get_object(Bucket=bucket_name, Key=file_key)

    # Ler o conteúdo do arquivo em memória
    file_content = obj["Body"].read()

    # Usar BytesIO para criar um objeto em memória que pandas pode ler
    parquet_file = io.BytesIO(file_content)

    # Ler o arquivo Parquet diretamente de memória
    df = pd.read_parquet(parquet_file, engine="pyarrow")  # Ou use 'fastparquet'

    # Criar engine de conexão com o PostgreSQL
    engine = create_engine(
        f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"
    )

    tabela_destino = "ORDERS"
    # Inserir dados no PostgreSQL (substitui a tabela, se existir)
    df.to_sql(tabela_destino, engine, if_exists="replace", index=False)

    print("Carga de dados concluída com sucesso!")
