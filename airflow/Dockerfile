FROM apache/airflow:3.3.2

COPY requirements-airflow.txt /requirements-airflow.txt

# Se fija la versión de Airflow para que pip no la cambie al resolver dependencias.
RUN pip install --no-cache-dir \
    "apache-airflow==${AIRFLOW_VERSION}" \
    -r /requirements-airflow.txt
