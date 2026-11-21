"""
Green Data ETL Pipeline

Laboratorio MLOps - Arquitectura Medallion

Pipeline:

API World Bank
     +
CSV Energía
     ↓
BRONZE
     ↓
SILVER
     ↓
GOLD
     ↓
KPIs
     ↓
WAREHOUSE

Python 3.12
"""

from pathlib import Path
import shutil
import logging
import pandas as pd

from src.extract.extract_api import extract_api
from src.transform.silver_transform import transform_to_silver
from src.transform.gold_integration import build_gold


# ====================================================
# CONFIGURACIÓN DE LOGS
# ====================================================

Path("logs").mkdir(
    parents=True,
    exist_ok=True
)

logging.basicConfig(
    filename="logs/etl.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def generate_bronze():
    """
    Genera la capa Bronze.
    """

    print("\n" + "=" * 60)
    print("BRONZE LAYER")
    print("=" * 60)

    logger.info("Inicio capa Bronze")

    extract_api(
        "data/bronze/countries_raw.csv"
    )

    source_file = Path(
        "data/energy_consumption.csv"
    )

    target_file = Path(
        "data/bronze/energy_raw.csv"
    )

    shutil.copy(
        source_file,
        target_file
    )

    print("energy_raw.csv generado")

    logger.info(
        "Archivo energy_raw.csv generado correctamente"
    )

    logger.info(
        "Capa Bronze completada correctamente"
    )


def generate_silver():
    """
    Genera la capa Silver.
    """

    print("\n" + "=" * 60)
    print("SILVER LAYER")
    print("=" * 60)

    logger.info("Inicio capa Silver")

    transform_to_silver()

    logger.info(
        "Capa Silver completada correctamente"
    )


def generate_gold():
    """
    Genera la capa Gold.
    """

    print("\n" + "=" * 60)
    print("GOLD LAYER")
    print("=" * 60)

    logger.info("Inicio capa Gold")

    build_gold()

    logger.info(
        "Capa Gold completada correctamente"
    )


def validate_outputs():
    """
    Verifica archivos generados.
    """

    print("\n" + "=" * 60)
    print("VALIDACIÓN")
    print("=" * 60)

    files = [
        "data/bronze/countries_raw.csv",
        "data/bronze/energy_raw.csv",
        "data/silver/silver_green_data.csv",
        "data/gold/gold_final.csv",
        "reports/kpis.csv",
        "warehouse/green_data_warehouse.csv"
    ]

    for file in files:

        exists = Path(file).exists()

        status = "OK" if exists else "ERROR"

        print(f"[{status}] {file}")

        if exists:
            logger.info(
                f"Validación exitosa: {file}"
            )
        else:
            logger.error(
                f"Archivo faltante: {file}"
            )


def show_summary():
    """
    Muestra resumen final.
    """

    print("\n" + "=" * 60)
    print("RESUMEN DEL PIPELINE")
    print("=" * 60)

    gold = pd.read_csv(
        "data/gold/gold_final.csv"
    )

    kpis = pd.read_csv(
        "reports/kpis.csv"
    )

    print("\nDataset GOLD")

    print(gold.shape)

    print("\nPrimeros registros")

    print(gold.head())

    print("\nKPIs")

    print(kpis)

    logger.info(
        f"Dataset GOLD generado con dimensión {gold.shape}"
    )

    logger.info(
        "Resumen de KPIs generado correctamente"
    )


def main():

    logger.info(
        "============================================="
    )
    logger.info(
        "Inicio ejecución Green Data ETL"
    )
    logger.info(
        "============================================="
    )

    print("\n")
    print("=" * 60)
    print("GREEN DATA ETL")
    print("=" * 60)

    try:

        generate_bronze()

        generate_silver()

        generate_gold()

        validate_outputs()

        show_summary()

        logger.info(
            "Pipeline ejecutado correctamente"
        )

        print("\n")
        print("=" * 60)
        print("PIPELINE EJECUTADO CORRECTAMENTE")
        print("=" * 60)

    except Exception as e:

        logger.exception(
            f"Error durante la ejecución del pipeline: {e}"
        )

        print("\nERROR EN EL PIPELINE")
        print(str(e))

        raise


if __name__ == "__main__":
    main()