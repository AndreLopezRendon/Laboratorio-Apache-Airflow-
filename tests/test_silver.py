import pandas as pd

from src.transform.silver_transform import transform_to_silver


def _write_bronze(base, countries, energy):
    bronze = base / "data" / "bronze"
    bronze.mkdir(parents=True)
    pd.DataFrame(countries).to_csv(bronze / "countries_raw.csv", index=False)
    pd.DataFrame(energy).to_csv(bronze / "energy_raw.csv", index=False)


COUNTRIES = [
    {"Country": "Colombia", "Country_Code": "COL", "Capital_City": "Bogota",
     "Region": "Latin America & Caribbean ", "Income_Level": "Upper middle income",
     "Longitude": -74.0, "Latitude": 4.6},
    {"Country": "Bolivia", "Country_Code": "BOL", "Capital_City": "La Paz",
     "Region": "Latin America & Caribbean", "Income_Level": "Lower middle income",
     "Longitude": -68.1, "Latitude": -16.5},
    {"Country": "World", "Country_Code": "WLD", "Capital_City": None,
     "Region": "Aggregates", "Income_Level": "Aggregates",
     "Longitude": None, "Latitude": None},
]
ENERGY = [
    {"Country": "Colombia", "Country_Code": "COL", "Energy_Consumption": 250, "Renewable_Energy": 35},
    {"Country": "Bolivia (Plurinational State of)", "Country_Code": "BOL",
     "Energy_Consumption": 100, "Renewable_Energy": "n/a"},
    {"Country": "World", "Country_Code": "WLD", "Energy_Consumption": 9999, "Renewable_Energy": 999},
]


def test_silver_excludes_aggregates_and_joins_by_iso_code(tmp_path):
    _write_bronze(tmp_path, COUNTRIES, ENERGY)

    silver = transform_to_silver(base_dir=tmp_path)

    assert sorted(silver["Country_Code"]) == ["BOL", "COL"]
    assert "Aggregates" not in set(silver["Region"])


def test_silver_strips_text_and_writes_csv(tmp_path):
    _write_bronze(tmp_path, COUNTRIES, ENERGY)

    transform_to_silver(base_dir=tmp_path)

    out = pd.read_csv(tmp_path / "data" / "silver" / "silver_green_data.csv")
    assert set(out["Region"]) == {"Latin America & Caribbean"}


def test_silver_keeps_unparseable_energy_as_missing_not_zero(tmp_path):
    _write_bronze(tmp_path, COUNTRIES, ENERGY)

    silver = transform_to_silver(base_dir=tmp_path).set_index("Country_Code")

    assert pd.isna(silver.loc["BOL", "Renewable_Energy"])
    assert silver.loc["COL", "Renewable_Energy"] == 35
