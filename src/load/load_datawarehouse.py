"""Carga del Gold y los KPIs al Data Warehouse (Postgres) con respaldo CSV."""

import logging

import pandas as pd

from src.config import reports_dir, warehouse_dir

logger = logging.getLogger(__name__)


def _csv_fallback(df: pd.DataFrame, base_dir=None):
    out = warehouse_dir(base_dir)
    out.mkdir(parents=True, exist_ok=True)
    df.to_csv(out / "green_data_warehouse.csv", index=False)


def cargar_datos(df: pd.DataFrame, table="gold_green_data", conn_id="green_dw", base_dir=None):
    """Carga idempotente (replace). Siempre deja también el respaldo CSV."""
    _csv_fallback(df, base_dir)

    try:
        from airflow.providers.postgres.hooks.postgres import PostgresHook
    except ImportError:
        logger.warning("Provider de Postgres no disponible; solo se escribió el CSV.")
        return

    engine = PostgresHook(postgres_conn_id=conn_id).get_sqlalchemy_engine()
    df.to_sql(table, engine, if_exists="replace", index=False)

    kpis_file = reports_dir(base_dir) / "kpis.csv"
    if kpis_file.exists():
        pd.read_csv(kpis_file).to_sql("kpis", engine, if_exists="replace", index=False)
    logger.info("Cargadas %s filas en %s", len(df), table)
