"""
Silver Layer Transformation

Proyecto: Green Data ETL
Autor: Andrés
Python: 3.12

Responsabilidades:
- Leer archivos Bronze
- Limpiar datos
- Estandarizar formatos
- Realizar integración (JOIN)
- Generar Silver Dataset
"""

from pathlib import Path

import pandas as pd


BRONZE_COUNTRIES = "data/bronze/countries_raw.csv"
BRONZE_ENERGY = "data/bronze/energy_raw.csv"

SILVER_OUTPUT = "data/silver/silver_green_data.csv"


def transform_to_silver() -> pd.DataFrame:
    """
    Construye la capa Silver.
    """

    print("Iniciando transformación Silver...")

    countries = pd.read_csv(BRONZE_COUNTRIES)
    energy = pd.read_csv(BRONZE_ENERGY)

    print(f"Countries: {countries.shape}")
    print(f"Energy: {energy.shape}")

    # ==========================
    # ELIMINAR DUPLICADOS
    # ==========================

    countries = countries.drop_duplicates()

    energy = energy.drop_duplicates()

    # ==========================
    # TRATAMIENTO DE NULOS
    # ==========================

    countries["Region"] = (
        countries["Region"]
        .fillna("Unknown")
    )

    countries["Income_Level"] = (
        countries["Income_Level"]
        .fillna("Unknown")
    )

    energy["Energy_Consumption"] = (
        pd.to_numeric(
            energy["Energy_Consumption"],
            errors="coerce"
        )
        .fillna(0)
    )

    energy["Renewable_Energy"] = (
        pd.to_numeric(
            energy["Renewable_Energy"],
            errors="coerce"
        )
        .fillna(0)
    )

    # ==========================
    # NORMALIZACIÓN DE STRINGS
    # ==========================

    countries["Country"] = (
        countries["Country"]
        .astype(str)
        .str.strip()
    )

    energy["Country"] = (
        energy["Country"]
        .astype(str)
        .str.strip()
    )

    # ==========================
    # JOIN
    # ==========================

    silver = pd.merge(
        countries,
        energy,
        on="Country",
        how="inner"
    )

    # ==========================
    # ELIMINAR COLUMNAS VACÍAS
    # ==========================

    silver = silver.dropna(
        axis=1,
        how="all"
    )

    # ==========================
    # ORDENAR DATOS
    # ==========================

    silver = silver.sort_values(
        by="Country"
    )

    # ==========================
    # CREAR DIRECTORIO
    # ==========================

    Path(
        "data/silver"
    ).mkdir(
        parents=True,
        exist_ok=True
    )

    # ==========================
    # GUARDAR RESULTADO
    # ==========================

    silver.to_csv(
        SILVER_OUTPUT,
        index=False
    )

    print(
        f"Silver generado correctamente: "
        f"{silver.shape}"
    )

    return silver


if __name__ == "__main__":

    df_silver = transform_to_silver()

    print(df_silver.head())