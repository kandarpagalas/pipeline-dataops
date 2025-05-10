import pandas as pd
import os
import json
import boto3
from botocore.client import Config
import io
from datetime import datetime


def transform(file_key):
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
    json_bytes = obj["Body"].read()
    json_data = json.loads(json_bytes.decode("utf-8"))

    full_dataset = []
    for order in json_data:
        customer = order.get("customer", "")
        charges = order.get("charges", "")
        items = order.get("items", "")
        shipping = order.get("shipping", "")

        charge = charges[0]
        # Transformar cada item em uma linha
        for item in items:

            data = {
                # "obj_key": key,
                "order_id": order["id"],
                "created_at": datetime.fromisoformat(order["created_at"]),
                "customer_id": customer["id"],
                "charge_id": charge["id"],
                "item_id": item["reference_id"],
                "item_price": item["unit_price"],
                "item_qtd": item["quantity"],
                "item_categoria": item["categoria"],
                "shipping_region_code": shipping["region_code"],
                "charge_paid": round(charge["amount"]["summary"]["paid"], 2),
                "charge_payment_method": charge["payment_method"]["type"],
            }

            full_dataset.append(data)

    df = pd.DataFrame(full_dataset)
    # 2. Salvar o DataFrame em um buffer em formato Parquet
    buffer = io.BytesIO()
    df.to_parquet(buffer, engine="pyarrow", index=False)
    buffer.seek(0)

    output_key = file_key.replace("ingest", "transform").replace("json", "parquet")
    # 5. Fazer upload do arquivo para o MinIO
    s3.upload_fileobj(buffer, bucket_name, output_key)

    return output_key
