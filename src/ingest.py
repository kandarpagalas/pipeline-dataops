import os
import json
import boto3
from botocore.client import Config
import pandas as pd


def get_json_data_from_minio():
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

    prefix = ""  # "diretório" no bucket, use '' para a raiz

    # Listar objetos no bucket/prefixo
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

    # Obter as chaves dos arquivos JSON
    order_files = [
        obj for obj in response.get("Contents", []) if obj["Key"].endswith(".json")
    ]

    full_dataset = []

    print(f"{len(order_files)} Arquivos JSON encontrados:")
    orders_dataset = []
    for order in order_files[:50]:
        key = order.get("Key", "")

        # lastMod = order.get("LastModified", "")
        # print(f"{lastMod.date()} {lastMod.strftime('%H:%M:%S')} - {key}")

        # Coletar dados do arquivo
        obj = s3.get_object(Bucket=bucket_name, Key=key)
        json_bytes = obj["Body"].read()
        json_data = json.loads(json_bytes.decode("utf-8"))
        orders_dataset.append(json_data)

        # print(json_data.keys())

        customer = json_data.get("customer", "")
        charges = json_data.get("charges", "")
        items = json_data.get("items", "")
        shipping = json_data.get("shipping", "")

        charge = charges[0]
        # Transformar cada item em uma linha
        for item in items:

            data = {
                "obj_key": key,
                "order_id": json_data["id"],
                "customer_id": customer["id"],
                "charge_id": charge["id"],
                "item_id": item["reference_id"],
                "item_price": item["unit_price"],
                "item_qtd": item["quantity"],
                "shipping_region_code": shipping["region_code"],
                "charge_paid": round(charge["amount"]["summary"]["paid"], 2),
                "charge_payment_method": charge["payment_method"]["type"],
            }

            full_dataset.append(data)
    return orders_dataset

    return pd.DataFrame(full_dataset)


if __name__ == "__main__":
    df = get_json_data_from_minio()
    print(df)
