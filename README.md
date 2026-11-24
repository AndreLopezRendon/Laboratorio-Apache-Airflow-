# Green Data ETL

Laboratorio 2 de MLOps: ETL con **Arquitectura Medallion** (Bronze → Silver → Gold → Data Warehouse),
orquestado con **Apache Airflow 3.3.2** sobre **WSL2 + Docker Desktop**.

## Fuentes
- API REST: World Bank `https://api.worldbank.org/v2/country`
- CSV: `data/energy_consumption.csv` (20 países con `Country_Code` ISO; datos de laboratorio, no estadísticas oficiales)

## Pipeline (DAG `green_data_etl`)
```text
extraer_fuentes → validar_bronze → transformar_a_silver → integrar_a_gold → cargar_datawarehouse
```
| Tarea | Qué hace |
|---|---|
| extraer_fuentes | API → `bronze/countries_raw.csv`; CSV → `bronze/energy_raw.csv` |
| validar_bronze | Falla (`FileNotFoundError`/`ValueError`) si falta un archivo/columna o hay 0 filas |
| transformar_a_silver | Quita agregados del World Bank, limpia texto, une por `Country_Code` |
| integrar_a_gold | `Renewable_Share`, `Environmental_Status` (≥30 % Green, ≥10 % Moderate, resto Critical) y KPIs |
| cargar_datawarehouse | Tablas `gold_green_data` y `kpis` en Postgres (`warehouse-db`), con respaldo CSV |

El DAG tiene `retries=2`, `catchup=False` y `schedule="@daily"`. Si una tarea falla, las siguientes quedan `upstream_failed`.

## Estructura
```text
airflow/            docker-compose.yaml (oficial 3.3.2 + build + warehouse-db), Dockerfile, dags/, logs/, plugins/, config/
data/               bronze/ silver/ gold/ + energy_consumption.csv
src/                config.py (rutas), extract/, transform/, load/, utils/
tests/              pytest (clasificación, Silver, Gold/KPIs, validar_bronze, DagBag)
main.py             versión monolítica local (sin Docker)
```
`airflow/` monta el proyecto completo en el contenedor: `..:/opt/airflow/green-data-etl` (`PROJECT_DIR`).
Las rutas nunca son de Windows; se resuelven en `src/config.py`.

## Requisitos
Windows 10 2004+ / 11, WSL2, Docker Desktop (integración WSL), 4 GB de RAM mínimo (8–16 GB recomendado).

## Ejecución con Airflow (PowerShell, desde `airflow/`)
```powershell
cd airflow
Copy-Item .env.example .env      # y completa FERNET_KEY (ver comentario del archivo)
docker compose build
docker compose up airflow-init   # debe terminar: airflow-init exited with code 0
docker compose up -d
docker ps                        # 8 servicios healthy (incl. warehouse-db)
```
UI: http://localhost:8080 (usuario/clave por defecto `airflow` / `airflow`).

### Verificación
```powershell
docker compose exec airflow-scheduler airflow dags list
docker compose exec airflow-scheduler airflow dags list-import-errors     # "No data found" = sin errores
docker compose exec airflow-scheduler ls /opt/airflow/dags
docker compose exec airflow-scheduler airflow dags unpause green_data_etl
docker compose exec airflow-scheduler airflow dags trigger green_data_etl
docker compose exec airflow-scheduler airflow dags list-runs green_data_etl
docker compose exec warehouse-db psql -U dw -d green_dw -c "select count(*) from gold_green_data"
docker compose logs -f airflow-scheduler
```
Logs por tarea: UI → `green_data_etl` → tarea → Logs. Detener: `docker compose down`.

## Ejecución local (sin Docker)
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
python -m pytest
```
El test del DAG (`tests/test_dag.py`) se omite si Airflow no está instalado; corre dentro del contenedor:
`docker compose exec airflow-scheduler sh -c "pip install pytest && cd /opt/airflow/green-data-etl && python -m pytest"`.

## KPIs (`reports/kpis.csv`)
Total Countries, Average/Max/Min Energy Consumption, Average Renewable Energy, Green Countries, Critical Countries.

## Autor
Maestría en Ciencia de Datos e Inteligencia Artificial
