# Propuesta de Solución

## Elaborado por

**Andrés Fernando López Rendón**

**Rol:** Product Owner

**Proyecto:** Green Data ETL

**Fecha:** Noviembre 2026

---

# Objetivo General

Desarrollar una plataforma automatizada de integración y procesamiento de datos ambientales que consolide información proveniente de fuentes heterogéneas, aplicando una arquitectura Medallion y procesos ETL orquestados mediante Apache Airflow para generar indicadores estratégicos y alimentar un Data Warehouse orientado al análisis y la toma de decisiones.

---

# Objetivos Específicos

1. Extraer datos desde una API REST del Banco Mundial y fuentes CSV.

2. Garantizar la calidad de los datos mediante validaciones automáticas.

3. Transformar e integrar la información en capas Silver y Gold.

4. Automatizar el pipeline mediante Apache Airflow.

5. Facilitar el monitoreo y trazabilidad mediante logs y dashboards operativos.

---

# Propuesta Técnica

La solución será implementada bajo una Arquitectura Medallion:

## Capa Bronze

- Extracción desde World Bank API.
- Extracción desde archivos CSV.
- Almacenamiento de datos sin transformación.

## Capa Silver

- Limpieza de datos.
- Estandarización.
- Integración de fuentes.

## Capa Gold

- Cálculo de indicadores ambientales.
- Clasificación ambiental.
- Generación de métricas de negocio.

## Data Warehouse

- Persistencia histórica.
- Consulta analítica.
- Soporte para futuras visualizaciones.

---

# Arquitectura Propuesta

World Bank API + CSV

↓

Bronze

↓

Silver

↓

Gold

↓

Data Warehouse

↓

KPIs Ambientales

---

# Beneficios Esperados

- Automatización de procesos ETL.
- Reducción de errores manuales.
- Mejora de calidad de datos.
- Disponibilidad de indicadores ambientales.
- Escalabilidad para nuevas fuentes de información.
- Trazabilidad y monitoreo completo.

---

# Concepto del Product Owner

Se recomienda aprobar el inicio y ejecución de esta iniciativa debido a su alineación con los objetivos de automatización y explotación de datos de la organización.

---

Atentamente,

**Andrés Fernando López Rendón**

**Product Owner**