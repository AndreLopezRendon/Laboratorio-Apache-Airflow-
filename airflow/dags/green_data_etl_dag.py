from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

from airflow.sdk import DAG, task

PROJECT_DIR = Path("/opt/airflow/green-data-etl")

sys.path.insert(0, str(PROJECT_DIR))

from src.extract.extract_api import extract_api
from src.transform.silver_transform import transform_to_silver
from src.transform.gold_integration import build_gold


with DAG(
    dag_id="green_data_etl",
    description="Green Data ETL - Medallion Architecture",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["etl", "green-data", "medallion"],
) as dag:

    @task
    def generar_bronze():

        print("Generando Bronze...")

        extract_api(
            "/opt/airflow/green-data-etl/data/bronze/countries_raw.csv"
        )

        print("Bronze generado correctamente")


    @task
    def generar_silver():

        print("Generando Silver...")

        transform_to_silver()

        print("Silver generado correctamente")


    @task
    def generar_gold():

        print("Generando Gold...")

        build_gold()

        print("Gold generado correctamente")


    bronze = generar_bronze()
    silver = generar_silver()
    gold = generar_gold()

    bronze >> silver >> gold