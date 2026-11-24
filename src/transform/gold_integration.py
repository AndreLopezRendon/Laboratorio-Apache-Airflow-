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

import numpy as np
import pandas as pd

from src.config import gold_dir, reports_dir, silver_dir

def classify_environment(score: float) -> str:
    """Clasifica por proporción de energía renovable (más renovable = mejor)."""

    if pd.isna(score):
        return "Unknown"

    if score >= 0.30:
        return "Green"

    if score >= 0.10:
        return "Moderate"

    return "Critical"


def build_gold(base_dir=None) -> pd.DataFrame:
    """Construye Gold y KPIs. El warehouse se carga en la tarea de Load."""

    df = pd.read_csv(silver_dir(base_dir) / "silver_green_data.csv")

    df["Energy_per_Renewable_Unit"] = (
        df["Energy_Consumption"] / (df["Renewable_Energy"] + 1)
    )

    # Consumo 0 => proporción indefinida (NaN), nunca inf.
    consumption = df["Energy_Consumption"].replace(0, np.nan)
    df["Renewable_Share"] = df["Renewable_Energy"] / consumption
    df["Environmental_Status"] = df["Renewable_Share"].apply(classify_environment)

    gold_out = gold_dir(base_dir)
    gold_out.mkdir(parents=True, exist_ok=True)
    df.to_csv(gold_out / "gold_final.csv", index=False)

    status = df["Environmental_Status"]
    kpis = pd.DataFrame(
        {
            "KPI": [
                "Total Countries",
                "Average Energy Consumption",
                "Average Renewable Energy",
                "Max Energy Consumption",
                "Min Energy Consumption",
                "Green Countries",
                "Critical Countries",
            ],
            "Value": [
                float(len(df)),
                round(float(df["Energy_Consumption"].mean()), 2),
                round(float(df["Renewable_Energy"].mean()), 2),
                float(df["Energy_Consumption"].max()),
                float(df["Energy_Consumption"].min()),
                float((status == "Green").sum()),
                float((status == "Critical").sum()),
            ],
        }
    )

    reports_out = reports_dir(base_dir)
    reports_out.mkdir(parents=True, exist_ok=True)
    kpis.to_csv(reports_out / "kpis.csv", index=False)

    return df


if __name__ == "__main__":
    print(build_gold())
