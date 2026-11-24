from __future__ import annotations

import logging
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

from airflow.sdk import DAG, task

# Ruta DENTRO del contenedor (volumen ..:/opt/airflow/green-data-etl), no de Windows.
PROJECT_DIR = Path(os.getenv("PROJECT_DIR", "/opt/airflow/green-data-etl"))
sys.path.insert(0, str(PROJECT_DIR))

log = logging.getLogger(__name__)

default_args = {
    "owner": "green-data",
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="green_data_etl",
    description="Green Data ETL - Medallion: Bronze -> Silver -> Gold -> Load",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",  # validado con disparo manual (schedule=None)
    catchup=False,
    default_args=default_args,
    tags=["etl", "green-data", "medallion"],
) as dag:

    @task
    def extraer_fuentes():
        from src.extract.extract_api import extract_api
        from src.extract.extract_csv import extract_csv

        extract_api(PROJECT_DIR / "data" / "bronze" / "countries_raw.csv")
        extract_csv(PROJECT_DIR)
        log.info("Fuentes extraídas hacia Bronze")

    @task
    def validar_bronze():
        from src.transform.bronze_validation import validate_bronze

        log.info("Bronze validado: %s", validate_bronze(PROJECT_DIR))

    @task
    def transformar_a_silver():
        from src.transform.silver_transform import transform_to_silver

        silver = transform_to_silver(PROJECT_DIR)
        log.info("Silver generado: %s", silver.shape)

    @task
    def integrar_a_gold():
        from src.transform.gold_integration import build_gold

        gold = build_gold(PROJECT_DIR)
        log.info("Gold generado: %s", gold.shape)

    @task
    def cargar_datawarehouse():
        import pandas as pd

        from src.load.load_datawarehouse import cargar_datos

        gold = pd.read_csv(PROJECT_DIR / "data" / "gold" / "gold_final.csv")
        cargar_datos(gold, base_dir=PROJECT_DIR)
        log.info("Carga terminada: %s filas", len(gold))

    (
        extraer_fuentes()
        >> validar_bronze()
        >> transformar_a_silver()
        >> integrar_a_gold()
        >> cargar_datawarehouse()
    )
