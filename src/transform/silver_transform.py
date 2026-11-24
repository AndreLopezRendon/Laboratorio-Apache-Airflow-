"""Capa Silver: limpieza, estandarización e integración por código ISO."""

import pandas as pd

from src.config import bronze_dir, silver_dir

TEXT_COLUMNS = ["Country", "Country_Code", "Capital_City", "Region", "Income_Level"]


def _strip_text(df: pd.DataFrame) -> pd.DataFrame:
    for col in TEXT_COLUMNS:
        if col in df.columns:
            df[col] = df[col].astype("string").str.strip()
    return df


def transform_to_silver(base_dir=None) -> pd.DataFrame:
    countries = pd.read_csv(bronze_dir(base_dir) / "countries_raw.csv")
    energy = pd.read_csv(bronze_dir(base_dir) / "energy_raw.csv")

    countries = _strip_text(countries.drop_duplicates())
    energy = _strip_text(energy.drop_duplicates())

    # Los agregados del World Bank (World, regiones, grupos de ingreso) no son países.
    countries = countries[countries["Region"] != "Aggregates"]
    countries["Income_Level"] = countries["Income_Level"].fillna("Unknown")

    # Valor no numérico => faltante (NaN); no se inventa un 0.
    for col in ["Energy_Consumption", "Renewable_Energy"]:
        energy[col] = pd.to_numeric(energy[col], errors="coerce")

    # El nombre de país difiere entre fuentes; se une por código ISO.
    energy = energy.drop(columns=["Country"])
    silver = pd.merge(countries, energy, on="Country_Code", how="inner")

    silver = silver.dropna(axis=1, how="all").sort_values(by="Country")

    out_dir = silver_dir(base_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    silver.to_csv(out_dir / "silver_green_data.csv", index=False)

    return silver


if __name__ == "__main__":
    print(transform_to_silver().head())
