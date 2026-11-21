"""
Extracción de datos desde la API de World Bank.

Autor: Andrés
Proyecto: Green Data ETL
Python: 3.12
"""

from pathlib import Path
import requests
import pandas as pd


WORLD_BANK_URL = (
    "https://api.worldbank.org/v2/country"
    "?format=json"
    "&per_page=400"
)


def extract_api(output_file: str) -> pd.DataFrame:
    """
    Extrae información de países desde World Bank
    y guarda el resultado en CSV.

    Parameters
    ----------
    output_file : str
        Ruta del CSV de salida.

    Returns
    -------
    pd.DataFrame
    """

    print("Extrayendo datos desde World Bank...")

    response = requests.get(
        WORLD_BANK_URL,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    if not isinstance(data, list) or len(data) < 2:
        raise ValueError(
            f"Respuesta inesperada de la API: {data}"
        )

    countries = []

    for country in data[1]:

        countries.append(
            {
                "Country": country.get("name"),
                "Country_Code": country.get("id"),
                "Capital_City": country.get("capitalCity"),
                "Region": (
                    country.get("region", {})
                    .get("value")
                ),
                "Income_Level": (
                    country.get("incomeLevel", {})
                    .get("value")
                ),
                "Longitude": country.get("longitude"),
                "Latitude": country.get("latitude")
            }
        )

    df = pd.DataFrame(countries)

    Path(output_file).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        output_file,
        index=False
    )

    print(
        f"Extracción completada. "
        f"Registros: {len(df)}"
    )

    return df


if __name__ == "__main__":

    extract_api(
        "data/bronze/countries_raw.csv"
    )