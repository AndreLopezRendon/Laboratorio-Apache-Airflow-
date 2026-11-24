# Solicitud del Cliente

## Información General

**Proyecto:** Green Data ETL

**Solicitante:** Área de Análisis Ambiental y Sostenibilidad

**Fecha:** Noviembre 2026

---

# Contexto del Negocio

La organización requiere una solución tecnológica que permita consolidar información ambiental proveniente de diferentes fuentes de datos y generar indicadores estratégicos para apoyar la toma de decisiones.

Actualmente, la información se encuentra distribuida entre fuentes externas y archivos locales, lo que dificulta la integración, validación y explotación eficiente de los datos.

---

# Requerimientos Funcionales

## Fuente Oficial de Información

API REST del Banco Mundial:

https://api.worldbank.org/v2/country

## Fuente Complementaria

Archivo CSV con información de consumo energético por país.

---

# Necesidades del Negocio

Se requiere una solución capaz de:

- Extraer información desde fuentes oficiales internacionales.
- Integrar datos de consumo energético.
- Validar automáticamente la calidad de los datos.
- Transformar datos para análisis ambiental.
- Generar indicadores ambientales y energéticos.
- Almacenar información consolidada para análisis posterior.
- Automatizar completamente el proceso de integración.

---

# Historia de Usuario Principal

## HU-001

### Título

Generación automática de indicadores ambientales

### Historia

**Como** Analista de Datos Ambiental

**Quiero** integrar automáticamente datos de consumo de energía y fuentes oficiales internacionales

**Para** generar indicadores ambientales confiables que apoyen la toma de decisiones estratégicas.

---

# Resultado Esperado

Disponer de una plataforma automatizada que permita consolidar, transformar y analizar información ambiental de manera periódica y confiable.