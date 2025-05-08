from ingest import get_json_data_from_minio
from transform import transform
from load import load_to_postgres

if __name__ == "__main__":
    raw_data = get_json_data_from_minio()
    df = transform(raw_data)
    load_to_postgres(df)

    # print(df)
