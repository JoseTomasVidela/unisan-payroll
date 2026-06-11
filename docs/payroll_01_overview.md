# Sistema de Liquidaciones - Overview

Versión: 1.0

---

# Objetivo

Construir un módulo de liquidaciones para UNISAN utilizando:

- Frontend Web
- Backend Python
- Base de datos MySQL Azure existente

El sistema reemplazará parcialmente el proceso manual realizado actualmente mediante planillas Excel.

---

# Contexto de Negocio

Actualmente existen dos planillas operacionales:

1. Base Producciones D&R
2. Base Producción Servicios

Estas planillas son mantenidas por el área de Operaciones.

El proceso operacional actual NO debe modificarse.

Operaciones continuará utilizando exactamente los mismos archivos Excel.

---

# Problema Actual

Las planillas Excel:

- contienen miles de registros
- son lentas de abrir
- son lentas de procesar
- requieren correcciones manuales

Cuando Administración detecta diferencias:

1. debe volver a las planillas operacionales
2. modificar información manualmente
3. recalcular liquidaciones

Esto genera:

- pérdida de tiempo
- errores operativos
- falta de trazabilidad

---

# Solución

Crear un sistema web que:

1. importe los Excel operacionales
2. almacene la información en MySQL Azure
3. genere liquidaciones automáticamente
4. permita correcciones desde la aplicación
5. mantenga trazabilidad completa

---

# Principio Fundamental

Después de importar:

```text
Excel = Fuente de carga
Base de datos = Fuente oficial
```

Las correcciones posteriores NO se realizan en Excel.

Las correcciones se realizan únicamente en la aplicación.

---

# Arquitectura

Frontend

```text
HTML
CSS
JavaScript
```

Backend

```text
Python
```

Base de Datos

```text
Azure MySQL
```

---

# Base de Datos

Todas las tablas del módulo utilizan el prefijo:

```text
payroll_
```

Motivo:

La base de datos pertenece a un ERP existente.

No modificar tablas del ERP.

Mantener aislamiento funcional.

---

# Tablas Principales

```text
payroll_cycles

payroll_roles

payroll_users

payroll_employees

payroll_imports

payroll_records

payroll_concepts

payroll_concept_rates

payroll_manual_adjustments

payroll_audit_log

payroll_export_logs
```

---

# Centros de Costo

Valores válidos:

```text
DR

SERVICES
```

---

# Roles Operacionales

Valores válidos:

```text
DRIVER

ASSISTANT
```

---

# Perfiles de Usuario

## ADMIN

Puede:

```text
Importar

Editar

Exportar

Administrar Usuarios
```

---

## USER

Puede:

```text
Consultar

Exportar
```

No puede editar.

---

# Ciclos

Los ciclos NO corresponden a meses calendario.

Ejemplo:

```text
22 Mayo
al
21 Junio
```

Nombre:

```text
Ciclo Junio
```

---

# Módulos del Sistema

## Dashboard

Permite:

```text
Importar Excel D&R

Importar Excel Servicios

Ver historial de importaciones
```

---

## Liquidaciones D&R Choferes

Muestra:

```text
Centro de costo DR

Cargo DRIVER
```

---

## Liquidaciones D&R Auxiliares

Muestra:

```text
Centro de costo DR

Cargo ASSISTANT
```

---

## Liquidaciones Servicios Choferes

Muestra:

```text
Centro de costo SERVICES

Cargo DRIVER
```

---

## Liquidaciones Servicios Auxiliares

Muestra:

```text
Centro de costo SERVICES

Cargo ASSISTANT
```

---

## Búsqueda

Permite consultar:

```text
Histórico de ciclos

Histórico de trabajadores

Histórico de liquidaciones
```

---

## Usuarios

Administración de usuarios.

Disponible sólo para ADMIN.

---

# Liquidación

La liquidación debe replicar visualmente la planilla Excel actual.

La estructura ya fue aprobada.

No modificar:

```text
Layout

Sidebar

Dashboard

Tabla principal

Filtros

Navegación
```

---

# Filosofía de Desarrollo

El frontend ya se encuentra aprobado.

La prioridad es:

```text
Backend

Importación

Persistencia

Cálculos

Auditoría
```

No rediseñar la interfaz.

El backend debe adaptarse al frontend existente.

---

# Orden de Implementación

## Etapa 1

Conexión a MySQL Azure.

---

## Etapa 2

Login.

---

## Etapa 3

Dashboard e importaciones.

---

## Etapa 4

Carga de payroll_records.

---

## Etapa 5

Renderizado de liquidaciones.

---

## Etapa 6

Edición y auditoría.

---

## Etapa 7

Exportación Excel y CSV.

---

## Etapa 8

Búsqueda histórica.

---

# Documentos Relacionados

Leer obligatoriamente:

```text
payroll_00_clarifications.md

payroll_02_database_mapping.md

payroll_03_import_rules.md

payroll_04_calculation_rules.md

payroll_05_frontend_integration.md

payroll_06_queries_and_views.md
```

Antes de implementar cualquier funcionalidad.
