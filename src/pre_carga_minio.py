import os
import json
import tempfile
import boto3
from botocore.client import Config

# Configurações do MinIO
MINIO_ENDPOINT = os.getenv(
    "MINIO_ENDPOINTs", "http://localhost:9000"
)  # ou o IP/host do seu servidor MinIO

# Deve gerar uma nova Cresencial no 1o acesso ao minio
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEYs", "h31kVG1KwaTvywDIajQd")
MINIO_SECRET_KEY = os.getenv(
    "MINIO_SECRET_KEYs", "DT6Oy2nbumi6LEtIA4tRWB3AV5n4P0YWVO2D3ctD"
)
bucket_name = "orders"


# Conexão com o MinIO
s3 = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
    config=Config(signature_version="s3v4"),
    region_name="us-east-1",  # Pode ser qualquer coisa no caso do MinIO
)

origem_json = "data/datasets/orders/0-1000.json"

with open(origem_json, "r") as f:
    orders = json.loads(f.read())


count_insert = 0
for order in orders:
    # Criação do arquivo JSON temporário
    with tempfile.NamedTemporaryFile(
        mode="w+", suffix=".json", delete=True
    ) as temp_json:
        json.dump(order, temp_json, indent=4)
        temp_json.flush()  # Garante que os dados estejam salvos

        order_id = order["id"]
        file_key = f"{order_id}.json"
        temp_json_path = temp_json.name

        try:
            # Upload do arquivo
            s3.upload_file(temp_json_path, bucket_name, file_key)
        except Exception as e:
            print(f"Erro ao enviar o arquivo: {e}")

    count_insert += 1

print(f"Foram enviados {count_insert} arquivo(s)")
