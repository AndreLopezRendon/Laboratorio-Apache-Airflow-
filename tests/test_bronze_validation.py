import pandas as pd
import pytest

from src.transform.bronze_validation import validate_bronze


def _bronze(base, countries=True, energy=True, energy_df=None):
    d = base / "data" / "bronze"
    d.mkdir(parents=True, exist_ok=True)
    if countries:
        pd.DataFrame([{"Country": "Colombia", "Country_Code": "COL", "Region": "LAC",
                       "Income_Level": "UMIC"}]).to_csv(d / "countries_raw.csv", index=False)
    if energy:
        df = energy_df if energy_df is not None else pd.DataFrame(
            [{"Country": "Colombia", "Country_Code": "COL",
              "Energy_Consumption": 250, "Renewable_Energy": 35}])
        df.to_csv(d / "energy_raw.csv", index=False)


def test_valid_bronze_returns_row_counts(tmp_path):
    _bronze(tmp_path)

    assert validate_bronze(base_dir=tmp_path) == {"countries": 1, "energy": 1}


def test_missing_file_raises_file_not_found(tmp_path):
    _bronze(tmp_path, energy=False)

    with pytest.raises(FileNotFoundError, match="energy_raw.csv"):
        validate_bronze(base_dir=tmp_path)


def test_missing_expected_column_raises_value_error(tmp_path):
    _bronze(tmp_path, energy_df=pd.DataFrame([{"Country": "Colombia", "Country_Code": "COL"}]))

    with pytest.raises(ValueError, match="Renewable_Energy"):
        validate_bronze(base_dir=tmp_path)


def test_empty_file_raises_value_error(tmp_path):
    cols = ["Country", "Country_Code", "Energy_Consumption", "Renewable_Energy"]
    _bronze(tmp_path, energy_df=pd.DataFrame(columns=cols))

    with pytest.raises(ValueError, match="vac"):
        validate_bronze(base_dir=tmp_path)
