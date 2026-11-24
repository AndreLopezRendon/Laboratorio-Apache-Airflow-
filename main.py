"""Green Data ETL - Arquitectura Medallion (ejecución local).

El DAG de Airflow (airflow/dags/green_data_etl_dag.py) orquesta estas mismas
funciones; main.py es la versión monolítica para correr sin Docker.
"""

from src.config import bronze_dir, get_base_dir
from src.extract.extract_api import extract_api
from src.extract.extract_csv import extract_csv
from src.load.load_datawarehouse import cargar_datos
from src.transform.bronze_validation import validate_bronze
from src.transform.gold_integration import build_gold
from src.transform.silver_transform import transform_to_silver
from src.utils.logger import get_logger

logger = get_logger()

OUTPUTS = [
    "data/bronze/countries_raw.csv",
    "data/bronze/energy_raw.csv",
    "data/silver/silver_green_data.csv",
    "data/gold/gold_final.csv",
    "reports/kpis.csv",
    "warehouse/green_data_warehouse.csv",
]


def validate_outputs():
    missing = [f for f in OUTPUTS if not (get_base_dir() / f).exists()]
    if missing:
        raise FileNotFoundError(f"Archivos faltantes: {missing}")
    for f in OUTPUTS:
        logger.info("Validación exitosa: %s", f)


def main():
    logger.info("Inicio ejecución Green Data ETL")
    try:
        extract_api(bronze_dir() / "countries_raw.csv")
        extract_csv()
        logger.info("Bronze: %s", validate_bronze())
        transform_to_silver()
        gold = build_gold()
        cargar_datos(gold)
        validate_outputs()
    except Exception:
        logger.exception("Error durante la ejecución del pipeline")
        raise
    logger.info("Pipeline ejecutado correctamente (Gold: %s)", gold.shape)
    print(f"Pipeline OK. Gold: {gold.shape}")
    print(gold["Environmental_Status"].value_counts())


if __name__ == "__main__":
    main()
