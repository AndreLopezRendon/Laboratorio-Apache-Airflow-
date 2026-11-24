"""Extracción del CSV de energía hacia Bronze."""

import shutil

from src.config import bronze_dir, get_base_dir


def extract_csv(base_dir=None):
    source = get_base_dir(base_dir) / "data" / "energy_consumption.csv"
    target_dir = bronze_dir(base_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "energy_raw.csv"
    shutil.copy(source, target)
    return target
