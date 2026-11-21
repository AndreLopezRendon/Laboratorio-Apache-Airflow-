"""
Gold Layer

Proyecto: Green Data ETL
Python 3.12

Responsabilidades:
- Construir métricas de negocio
- Clasificación ambiental
- Generar KPIs
- Crear Gold Dataset
- Simular Data Warehouse
"""

from pathlib import Path

import pandas as pd


SILVER_FILE = "data/silver/silver_green_data.csv"

GOLD_FILE = "data/gold/gold_final.csv"

KPI_FILE = "reports/kpis.csv"

WAREHOUSE_FILE = (
    "warehouse/green_data_warehouse.csv"
)


def classify_environment(score: float) -> str:

    if score < 0.05:
        return "Green"

    if score < 0.10:
        return "Moderate"

    return "Critical"


def build_gold():

    print("Construyendo capa Gold...")

    df = pd.read_csv(SILVER_FILE)

    # ==================================
    # KPI DERIVADO
    # ==================================

    df["Emission_Efficiency"] = (
        df["Energy_Consumption"]
        /
        (df["Renewable_Energy"] + 1)
    )

    # ==================================
    # CLASIFICACIÓN
    # ==================================

    df["Environmental_Status"] = (
        df["Renewable_Energy"]
        /
        df["Energy_Consumption"]
    )

    df["Environmental_Status"] = (
        df["Environmental_Status"]
        .apply(classify_environment)
    )

    # ==================================
    # CREAR FOLDERS
    # ==================================

    Path("data/gold").mkdir(
        parents=True,
        exist_ok=True
    )

    Path("reports").mkdir(
        parents=True,
        exist_ok=True
    )

    Path("warehouse").mkdir(
        parents=True,
        exist_ok=True
    )

    # ==================================
    # GUARDAR GOLD
    # ==================================

    df.to_csv(
        GOLD_FILE,
        index=False
    )

    # ==================================
    # KPIs
    # ==================================

    kpis = pd.DataFrame(
        {
            "KPI": [
                "Total Countries",
                "Average Energy Consumption",
                "Average Renewable Energy",
                "Max Energy Consumption",
                "Min Energy Consumption",
                "Green Countries",
                "Critical Countries"
            ],
            "Value": [
                len(df),
                round(
                    df["Energy_Consumption"]
                    .mean(),
                    2
                ),
                round(
                    df["Renewable_Energy"]
                    .mean(),
                    2
                ),
                df["Energy_Consumption"]
                .max(),
                df["Energy_Consumption"]
                .min(),
                len(
                    df[
                        df[
                            "Environmental_Status"
                        ] == "Green"
                    ]
                ),
                len(
                    df[
                        df[
                            "Environmental_Status"
                        ] == "Critical"
                    ]
                )
            ]
        }
    )

    kpis.to_csv(
        KPI_FILE,
        index=False
    )

    # ==================================
    # WAREHOUSE
    # ==================================

    df.to_csv(
        WAREHOUSE_FILE,
        index=False
    )

    print("Gold generado correctamente")

    print(df.shape)

    print("\nKPIs:")

    print(kpis)

    return df


if __name__ == "__main__":

    build_gold()