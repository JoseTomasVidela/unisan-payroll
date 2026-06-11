# Consultas y Vistas - Módulo Liquidaciones

Versión: 1.0

---

# Objetivo

Definir qué información debe consultar el backend para alimentar cada pantalla del frontend aprobado.

Este documento reemplaza un plan de API formal.

El objetivo es alinear:

```text
Frontend aprobado
+
Base de datos
+
Backend Python
```

---

# Regla General

No modificar el frontend aprobado.

El backend debe entregar los datos necesarios para poblar:

```text
Dashboard

Liquidaciones D&R Choferes

Liquidaciones D&R Auxiliares

Liquidaciones Servicios Choferes

Liquidaciones Servicios Auxiliares

Búsqueda

Usuarios
```

---

# Dashboard

## Historial de Importaciones

Tabla:

```text
payroll_imports
```

Consulta conceptual:

```sql
SELECT
    imported_at,
    file_name,
    source_type,
    rows_imported,
    imported_by
FROM payroll_imports
ORDER BY imported_at DESC;
```

Mostrar columnas:

```text
Fecha

Archivo

Tipo

Registros

Usuario
```

---

# Selector de Ciclos

Utilizado en:

```text
Dashboard

Liquidaciones

Búsqueda
```

Tabla:

```text
payroll_cycles
```

Consulta conceptual:

```sql
SELECT
    id,
    cycle_name,
    start_date,
    end_date
FROM payroll_cycles
ORDER BY start_date DESC;
```

Mostrar:

```text
cycle_name
```

---

# Selector de Trabajadores

Utilizado en pantallas de liquidación.

Tabla:

```text
payroll_employees
+
payroll_records
```

La lista debe filtrarse según la pantalla.

---

## D&R Choferes

Filtros:

```text
cost_center = DR
role_type = DRIVER
```

---

## D&R Auxiliares

Filtros:

```text
cost_center = DR
role_type = ASSISTANT
```

---

## Servicios Choferes

Filtros:

```text
cost_center = SERVICES
role_type = DRIVER
```

---

## Servicios Auxiliares

Filtros:

```text
cost_center = SERVICES
role_type = ASSISTANT
```

---

Consulta conceptual:

```sql
SELECT DISTINCT
    e.id,
    e.employee_name
FROM payroll_employees e
JOIN payroll_records r
    ON r.employee_id = e.id
WHERE r.cycle_id = :cycle_id
AND r.cost_center = :cost_center
AND r.role_type = :role_type
ORDER BY e.employee_name;
```

---

# Pantallas de Liquidación

Las cuatro pantallas usan el mismo componente visual.

Sólo cambian:

```text
cost_center

role_type
```

---

## Parámetros

El backend debe recibir:

```text
cycle_id

employee_id

cost_center

role_type
```

---

# Datos Base para Liquidación

Tabla principal:

```text
payroll_records
```

Filtro base:

```sql
WHERE cycle_id = :cycle_id
AND employee_id = :employee_id
AND cost_center = :cost_center
AND role_type = :role_type
```

---

# Fechas del Ciclo

Las columnas del frontend se generan desde:

```text
payroll_cycles.start_date

payroll_cycles.end_date
```

Ejemplo:

```text
22-05

23-05

...

21-06
```

---

# Estado Diario

Fila:

```text
Estado
```

Fuente:

```text
payroll_records.status
```

Consulta conceptual:

```sql
SELECT
    work_date,
    status
FROM payroll_records
WHERE cycle_id = :cycle_id
AND employee_id = :employee_id
AND cost_center = :cost_center
AND role_type = :role_type;
```

Si hay múltiples registros en el mismo día:

- Priorizar estados no vacíos.
- Si hay más de un estado distinto, mostrar el primero no vacío.
- En backend se puede resolver como valor agregado.

---

# Filas de Conceptos

Cada fila de concepto se construye desde una columna de:

```text
payroll_records
```

---

## Estructura esperada por el frontend

El backend debe entregar cada fila así:

```json
{
  "row_type": "concept",
  "concept_code": "EVENT",
  "concept_name": "Evento",
  "db_field": "event_flag",
  "units": 0,
  "rate": 0,
  "total": 0,
  "editable": true,
  "daily_values": [
    {
      "date": "2026-05-22",
      "value": 0,
      "editable": true
    }
  ]
}
```

---

# Cálculo Diario de Conceptos

Para cada fecha:

```sql
SUM(db_field)
```

Filtro:

```sql
cycle_id
employee_id
cost_center
role_type
work_date
```

---

# Cálculo de Unidades

```text
units = SUM(daily_values.value)
```

---

# Cálculo de Total

```text
total = units * rate
```

---

# Tarifas

Tabla:

```text
payroll_concept_rates
+
payroll_concepts
```

Consulta conceptual:

```sql
SELECT
    c.concept_code,
    c.concept_name,
    cr.amount
FROM payroll_concepts c
JOIN payroll_concept_rates cr
    ON cr.concept_id = c.id
WHERE c.cost_center = :cost_center
AND c.role_type = :role_type
AND c.active = 1
AND cr.active = 1;
```

La lista de conceptos debe provenir exclusivamente de `payroll_concepts`; no
hardcodearla en frontend ni backend.

Las tarifas actuales son fijas. El acceso a `payroll_concept_rates` debe quedar
encapsulado para permitir histórico en el futuro, sin implementar todavía
campos como `effective_from`, `effective_to` o `cycle_id`.

---

# Mapping de Conceptos a Campos

El backend debe mapear cada concepto a una columna de `payroll_records`.

Ejemplos:

```text
DISPATCH_RETRIEVAL
→ dispatch_flag

EVENT
→ event_flag

ENTRY_BEFORE_1930
→ entry_before_1930_qty

EXIT_AFTER_1930
→ exit_after_1930_qty

FAIR_WEEK_1
→ fair_week_1_flag

FAIR_WEEK_2
→ fair_week_2_flag

OUTSIDE_RADIUS
→ outside_radius_flag

OUTSIDE_RADIUS_V_REGION
→ outside_radius_v_region_qty

SATURDAY_WEEK_1
→ saturday_week_1_qty

SUNDAY_WEEK_1
→ sunday_week_1_qty

SATURDAY_WEEK_2
→ saturday_week_2_qty

SUNDAY_WEEK_2
→ sunday_week_2_qty

CLIENT_TRIPS
→ client_trips_qty

SATURDAY_AFTER_1600
→ saturday_after_1600_qty

SUNDAY_AFTER_1600
→ sunday_after_1600_qty

WEEKEND_DRYING
→ weekend_drying_qty

WATER_POINT
→ water_point_flag

KIT_DELIVERY
→ kit_delivery_flag

LAVATORY_LOAD
→ lavatory_load_flag

RILES_SUCTION
→ riles_suction_flag

LARGE_TRASH_BIN
→ large_trash_bin_qty

SMALL_TRASH_BIN
→ small_trash_bin_qty

FOSA
→ fosa_qty
```

`retrieval_flag` y `septic_tank_flag` quedan reservados y no participan en la
liquidación actual. `riles_suction_flag` representa una cantidad decimal en m³,
no un booleano.

---

# Filas Calculadas

Estas filas no se leen directamente desde una columna de `payroll_records`.

Deben calcularse en backend:

```text
TOTAL A PAGAR

VARIABLE DIARIO

DIA TRABAJADO

SEMANA CORRIDA

VACACIONES

BONO FUERA PRODUCCION

PRODUCCION TOTAL
```

Todos estos cálculos deben limitarse al `cost_center` y `role_type` de la
liquidación actual. No consolidar automáticamente múltiples centros de costo.

---

# Ajustes Manuales

Tabla:

```text
payroll_manual_adjustments
```

Consulta conceptual:

```sql
SELECT
    adjustment_type,
    adjustment_name,
    adjustment_date,
    units,
    amount,
    notes
FROM payroll_manual_adjustments
WHERE cycle_id = :cycle_id
AND employee_id = :employee_id
AND cost_center = :cost_center
AND role_type = :role_type;
```

`amount` representa el monto total del ajuste. `units` es opcional e
informativo.

---

# Vacaciones

Fuente:

```text
payroll_manual_adjustments
```

Filtro:

```text
adjustment_type = VACATION
```

---

# Bono Fuera Producción

Fuente:

```text
payroll_manual_adjustments
```

Filtro:

```text
adjustment_type = OUT_OF_PRODUCTION_BONUS
```

---

# Otros Ajustes

Fuente:

```text
payroll_manual_adjustments
```

Tipos:

```text
BONUS

MANUAL_ADJUSTMENT

DISCOUNT
```

---

# Edición de Celdas Diarias

Cuando ADMIN solicita editar una celda diaria, el backend debe obtener todos
los registros asociados y devolver su detalle. Una celda agregada puede
representar múltiples filas de `payroll_records`.

Para guardar una edición, el backend debe identificar:

```text
employee_id

cycle_id

cost_center

role_type

work_date

concept_code

record_id

nuevo_valor
```

---

# Actualización en DB

Convertir `concept_code` a campo físico de `payroll_records`.

Ejemplo:

```text
EVENT
→ event_flag
```

Actualizar registros correspondientes al día.

---

El backend debe exigir `record_id` y actualizar únicamente el registro
seleccionado en el detalle. Nunca actualizar el primer registro encontrado como
comportamiento por defecto.

Después de guardar debe registrar auditoría y recalcular la liquidación.

---

# Auditoría

Toda edición debe registrar:

```text
payroll_audit_log
```

Información mínima:

```text
user_id

action_type = UPDATE_DAILY_CELL

table_name = payroll_records

record_id

field_name

old_value

new_value

action_date
```

---

# Usuarios

Pantalla:

```text
Usuarios
```

Tablas:

```text
payroll_users

payroll_roles
```

Consulta conceptual:

```sql
SELECT
    u.id,
    u.username,
    r.role_name,
    u.active
FROM payroll_users u
JOIN payroll_roles r
    ON r.id = u.role_id
ORDER BY u.username;
```

---

# Búsqueda

Filtros:

```text
cycle_from

cycle_to

cost_center

role_type

employee_id
```

---

La búsqueda debe reutilizar el mismo motor de liquidación.

No crear un layout distinto.

---

# Exportaciones

Toda exportación debe registrar en:

```text
payroll_export_logs
```

Campos:

```text
user_id

export_type

cycle_id

employee_id

cost_center

exported_at
```

---

# Regla Crítica

El backend debe adaptarse al frontend aprobado.

No modificar:

```text
sidebar

login

dashboard

tabla tipo Excel

búsqueda

usuarios

modal de confirmación
```

---

# Resultado Esperado

Cuando el usuario abra una liquidación, el backend debe devolver todos los datos necesarios para renderizar:

```text
Cabecera

Fechas del ciclo

Estado diario

Conceptos

Unidades

Tarifas

Totales

Variable diario

Día trabajado

Semana corrida

Ajustes

Producción total
```

en el mismo layout visual aprobado.
