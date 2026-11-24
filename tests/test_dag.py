from pathlib import Path

import pytest

pytest.importorskip("airflow.models")

from airflow.models import DagBag  # noqa: E402

DAGS = Path(__file__).resolve().parents[1] / "airflow" / "dags"


def test_dag_imports_without_errors_and_has_guide_pipeline():
    bag = DagBag(dag_folder=str(DAGS))

    assert bag.import_errors == {}
    dag = bag.get_dag("green_data_etl")
    assert [t.task_id for t in dag.topological_sort()] == [
        "extraer_fuentes",
        "validar_bronze",
        "transformar_a_silver",
        "integrar_a_gold",
        "cargar_datawarehouse",
    ]
    assert dag.catchup is False
