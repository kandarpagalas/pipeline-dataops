from __future__ import annotations

import sys
from pendulum import datetime, duration
from airflow import DAG
from airflow.decorators import dag, task

# from airflow.sdk import DAG, dag, task

# from airflow.models import Variable


sys.path.append("/opt/airflow/dags")


default_args = {
    "owner": "DataOps",
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "contato@kandarpagalas.com",
    "retries": 1,
    "retry_delay": duration(minutes=1),
}


with DAG(
    dag_id="PIPELINE_DE_DADOS",
    schedule="10 5 * * *",  # Todo dia as 5h
    start_date=datetime(2025, 5, 1, tz="America/Fortaleza"),
    dagrun_timeout=duration(minutes=60),
    params={"dag_id": "__template_dag__"},
    tags=["MinIO", "Postgres"],
    default_args=default_args,
    catchup=False,
) as dag:

    @task
    def data_ingestion():
        from ingest import get_json_data_from_minio

        raw_data = get_json_data_from_minio()
        return raw_data

    @task
    def data_transformation(raw_data):
        from transform import transform

        df = transform(raw_data)
        return df

    @task
    def data_load(df):
        from load import load_to_postgres

        load_to_postgres(df)

    raw_data = data_ingestion()
    df = data_transformation(raw_data)
    data_load(df)


if __name__ == "__main__":
    run = dag.test(mark_success_pattern="wait_for_.*|cleanup")
