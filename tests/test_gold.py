import numpy as np
import pandas as pd

from src.transform.gold_integration import build_gold

SILVER = [
    {"Country": "Brazil", "Country_Code": "BRA", "Energy_Consumption": 500.0, "Renewable_Energy": 250.0},
    {"Country": "Colombia", "Country_Code": "COL", "Energy_Consumption": 250.0, "Renewable_Energy": 35.0},
    {"Country": "Chad", "Country_Code": "TCD", "Energy_Consumption": 100.0, "Renewable_Energy": 2.0},
    {"Country": "Nowhere", "Country_Code": "NWH", "Energy_Consumption": 0.0, "Renewable_Energy": 5.0},
    {"Country": "Unmeasured", "Country_Code": "UNM", "Energy_Consumption": 80.0, "Renewable_Energy": np.nan},
]


def _prepare(base):
    silver = base / "data" / "silver"
    silver.mkdir(parents=True)
    pd.DataFrame(SILVER).to_csv(silver / "silver_green_data.csv", index=False)


def _kpis(base):
    df = pd.read_csv(base / "reports" / "kpis.csv")
    return dict(zip(df["KPI"], df["Value"]))


def test_status_follows_renewable_share(tmp_path):
    _prepare(tmp_path)

    gold = build_gold(base_dir=tmp_path).set_index("Country_Code")

    assert gold.loc["BRA", "Environmental_Status"] == "Green"      # 50 %
    assert gold.loc["COL", "Environmental_Status"] == "Moderate"   # 14 %
    assert gold.loc["TCD", "Environmental_Status"] == "Critical"   # 2 %


def test_zero_consumption_or_missing_renewable_is_unknown_without_inf(tmp_path):
    _prepare(tmp_path)

    gold = build_gold(base_dir=tmp_path).set_index("Country_Code")

    assert gold.loc["NWH", "Environmental_Status"] == "Unknown"
    assert gold.loc["UNM", "Environmental_Status"] == "Unknown"
    assert not np.isinf(gold.select_dtypes("number")).any().any()


def test_kpis_are_numeric_and_consistent(tmp_path):
    _prepare(tmp_path)
    build_gold(base_dir=tmp_path)

    kpis = _kpis(tmp_path)

    assert pd.api.types.is_numeric_dtype(pd.read_csv(tmp_path / "reports" / "kpis.csv")["Value"])
    assert kpis["Total Countries"] == 5
    assert kpis["Green Countries"] == 1
    assert kpis["Critical Countries"] == 1
    assert kpis["Max Energy Consumption"] == 500
    assert kpis["Average Energy Consumption"] == 186


def test_gold_is_written_and_efficiency_is_renamed(tmp_path):
    _prepare(tmp_path)

    gold = build_gold(base_dir=tmp_path)

    assert (tmp_path / "data" / "gold" / "gold_final.csv").exists()
    assert "Energy_per_Renewable_Unit" in gold.columns
    assert "Emission_Efficiency" not in gold.columns
