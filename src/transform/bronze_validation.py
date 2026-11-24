"""Validación de la capa Bronze (tarea validar_bronze del DAG)."""

import pandas as pd

from src.config import bronze_dir

EXPECTED = {
    "countries_raw.csv": ["Country", "Country_Code", "Region", "Income_Level"],
    "energy_raw.csv": ["Country", "Country_Code", "Energy_Consumption", "Renewable_Energy"],
}


def validate_bronze(base_dir=None) -> dict:
    counts = {}
    for filename, columns in EXPECTED.items():
        path = bronze_dir(base_dir) / filename
        if not path.exists():
            raise FileNotFoundError(f"No existe {path}")

        df = pd.read_csv(path)
        missing = [c for c in columns if c not in df.columns]
        if missing:
            raise ValueError(f"{filename}: faltan columnas {missing}")
        if df.empty:
            raise ValueError(f"{filename}: archivo vacío (0 filas)")

        counts[filename.split("_")[0]] = len(df)
    return counts
