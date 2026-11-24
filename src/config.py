"""Rutas del proyecto, independientes del sistema operativo.

En Docker se define PROJECT_DIR=/opt/airflow/green-data-etl; en local se
resuelve desde la ubicación de este archivo.
"""

import os
from pathlib import Path


def get_base_dir(base_dir=None) -> Path:
    if base_dir is not None:
        return Path(base_dir)
    env = os.getenv("PROJECT_DIR")
    if env:
        return Path(env)
    return Path(__file__).resolve().parents[1]


def bronze_dir(base_dir=None) -> Path:
    return get_base_dir(base_dir) / "data" / "bronze"


def silver_dir(base_dir=None) -> Path:
    return get_base_dir(base_dir) / "data" / "silver"


def gold_dir(base_dir=None) -> Path:
    return get_base_dir(base_dir) / "data" / "gold"


def reports_dir(base_dir=None) -> Path:
    return get_base_dir(base_dir) / "reports"


def warehouse_dir(base_dir=None) -> Path:
    return get_base_dir(base_dir) / "warehouse"
