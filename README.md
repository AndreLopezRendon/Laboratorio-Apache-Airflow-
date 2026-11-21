# Green Data ETL

## Descripción

Proyecto desarrollado para el Laboratorio 2 de MLOps.

El objetivo es implementar un proceso ETL utilizando Arquitectura Medallion (Bronze, Silver y Gold), integrando datos provenientes de una API REST y un archivo CSV.

El pipeline realiza:

- Extracción de datos desde World Bank API.
- Lectura de datos energéticos desde CSV.
- Limpieza y transformación de datos.
- Integración de fuentes.
- Generación de indicadores de negocio.
- Construcción de un Data Warehouse.
- Supervisión mediante logs.
- Orquestación mediante Apache Airflow.

---

# Arquitectura Medallion

```text
API World Bank
       +
CSV Energy Consumption
       ↓

    BRONZE
       ↓

    SILVER
       ↓

     GOLD
       ↓

 DATA WAREHOUSE
```

---

# Tecnologías Utilizadas

- Python 3.12.10
- Apache Airflow 3.3.2
- Pandas 2.3.2
- NumPy 2.3.2
- Requests 2.32.5
- OpenPyXL 3.1.5
- Docker Desktop
- WSL2
- Visual Studio Code

---
# Estructura del Proyecto

green-data-etl/
│
├── airflow/
│   ├── dags/
│   ├── logs/
│   ├── plugins/
│   ├── config/
│   ├── Dockerfile
│   └── docker-compose.yaml
│
├── data/
│   ├── bronze/
│   ├── silver/
│   └── gold/
│
├── reports/
│
├── warehouse/
│
├── src/
│   ├── extract/
│   ├── transform/
│   ├── load/
│   └── utils/
│
├── logs/
│
├── main.py
├── requirements.txt
└── README.md

# Fuentes de Datos

## API REST

World Bank API

https://api.worldbank.org/v2/country

## Dataset CSV

energy_consumption.csv

---

# Capas Medallion

## Bronze
- countries_raw.csv
- energy_raw.csv

## Silver
- silver_green_data.csv

## Gold
- gold_final.csv

---

# KPIs

- Total Countries
- Average Energy Consumption
- Average Renewable Energy
- Max Energy Consumption
- Min Energy Consumption
- Green Countries
- Critical Countries

Archivo generado:

reports/kpis.csv

---

# Logging

Archivo:

logs/etl.log

---

# Ejecución

```bash
python -m venv .venv
.venv\Scriptsctivate
pip install -r requirements.txt
python main.py
```

---

# Autor

Andrés

Maestría en Ciencia de Datos e Inteligencia Artificial
