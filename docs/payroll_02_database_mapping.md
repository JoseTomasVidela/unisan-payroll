# Payroll Module - Database Mapping

Versión: 1.0

---

# Objetivo

Este documento define la relación exacta entre:

- Base de datos
- Pantalla de liquidaciones
- Importaciones Excel
- Cálculos

El objetivo es evitar que la lógica de negocio quede implícita o sea interpretada por el desarrollador.

---

# Fuente Oficial de Datos

Una vez realizada la importación:

- Los archivos Excel dejan de ser utilizados.
- La base de datos pasa a ser la única fuente oficial.
- Todas las modificaciones posteriores se realizan directamente sobre la base de datos.

---

# Tabla Principal

## payroll_records

Esta tabla almacena toda la producción diaria.

Cada fila representa:

```text
Trabajador
+
Fecha
+
Centro de costo
+
Cargo
+
Conceptos realizados ese día
```

---

# Identificación

## employee_id

Relación:

```text
payroll_employees.id
```

---

## source_employee_name

Nombre del trabajador proveniente del Excel.

Se utiliza para:

- validación
- auditoría
- troubleshooting

---

## role_type

Valores:

```text
DRIVER
ASSISTANT
```

---

## cost_center

Valores:

```text
DR
SERVICES
```

---

## work_date

Fecha de producción.

Ejemplo:

```text
2026-05-22
```

---

# Conceptos D&R

## Despacho

Campo:

```text
dispatch_flag
```

Liquidación:

```text
Despacho / Retiro
```

---

`Despacho / Retiro` es un único concepto y utiliza solamente `dispatch_flag`.
La columna `retrieval_flag` queda reservada para una evolución futura y no
participa en importaciones, liquidaciones ni cálculos actuales.

---

## Entrada antes de 19:30

Campo:

```text
entry_before_1930_qty
```

Liquidación:

```text
Entrada < 19:30
```

---

## Entrada antes de 07:30

Campo:

```text
entry_before_0730_qty
```

Liquidación:

```text
Entrada < 07:30
```

---

## Salida después de 19:30

Campo:

```text
exit_after_1930_qty
```

Liquidación:

```text
Salida > 19:30
```

---

## Feria Semana 01

Campo:

```text
fair_week_1_flag
```

Liquidación:

```text
Feria Semana 01
```

---

## Feria Semana 02

Campo:

```text
fair_week_2_flag
```

Liquidación:

```text
Feria Semana 02
```

---

## Fuera Radio Normal

Campo:

```text
outside_radius_flag
```

Liquidación:

```text
Fuera Radio Normal
```

---

## Fuera Radio V Región

Campo:

```text
outside_radius_v_region_qty
```

Liquidación:

```text
Fuera Radio V Región
```

---

## Sábado Semana 01

Campo:

```text
saturday_week_1_qty
```

Liquidación:

```text
Sábado Semana 01
```

---

## Domingo Semana 01

Campo:

```text
sunday_week_1_qty
```

Liquidación:

```text
Domingo Semana 01
```

---

## Sábado Semana 02

Campo:

```text
saturday_week_2_qty
```

Liquidación:

```text
Sábado Semana 02
```

---

## Domingo Semana 02

Campo:

```text
sunday_week_2_qty
```

Liquidación:

```text
Domingo Semana 02
```

---

## Viajes por Cliente

Campo:

```text
client_trips_qty
```

Liquidación:

```text
Viajes por Cliente
```

---

## Sábado después de las 16:00

Campo:

```text
saturday_after_1600_qty
```

Liquidación:

```text
Sábado > 16:00
```

---

## Domingo después de las 16:00

Campo:

```text
sunday_after_1600_qty
```

Liquidación:

```text
Domingo > 16:00
```

---

## Evento

Campo:

```text
event_flag
```

Liquidación:

```text
Evento
```

---

# Conceptos Servicios

## Lavado

Campo:

```text
cleaning_flag
```

---

## Secado

Campo:

```text
drying_flag
```

---

## Secado Fin de Semana

Campo:

```text
weekend_drying_qty
```

Liquidación:

```text
Secado Fin de Semana
```

---

## Punto de Agua

Campo:

```text
water_point_flag
```

Liquidación:

```text
Punto de Agua
```

---

## Entrega de Kit

Campo:

```text
kit_delivery_flag
```

Liquidación:

```text
Entrega Kit
```

---

## Carga Baño

Campo:

```text
lavatory_load_flag
```

Liquidación:

```text
Carga Baño
```

---

## Succión Riles

Campo:

```text
riles_suction_flag
```

Tipo lógico:

```text
cantidad decimal en m³
```

No interpretar este campo como booleano.

Liquidación:

```text
Succión Riles
```

---

## Fosa

Campo:

```text
fosa_qty
```

Liquidación:

```text
Fosa
```

---

## Basurero Grande

Campo:

```text
large_trash_bin_qty
```

Liquidación:

```text
Basurero Grande
```

---

## Basurero Chico

Campo:

```text
small_trash_bin_qty
```

Liquidación:

```text
Basurero Chico
```

---

# Construcción de la Pantalla

Para cada fila de liquidación:

## Unidades

Calcular:

```sql
SUM(campo_concepto)
```

Filtrado por:

```sql
employee_id
cycle_id
cost_center
role_type
```

Cada liquidación corresponde exclusivamente a ese `cost_center` y
`role_type`. No consolidar centros de costo ni cargos distintos.

---

## Valor Unitario

Obtener desde:

```text
payroll_concept_rates.amount
```

---

## Total

Calcular:

```text
Unidades * Valor Unitario
```

---

# Construcción de las Columnas Diarias

Cada columna corresponde a:

```text
1 día del ciclo
```

Ejemplo:

```text
22-05
23-05
24-05
...
21-06
```

---

Cada celda diaria debe mostrar:

```sql
SUM(campo_concepto)
```

Filtrado por:

```sql
employee_id
cycle_id
cost_center
role_type
work_date
```

---

# Edición

Sólo ADMIN.

---

Modo normal:

```text
Sólo lectura
```

---

Modo edición:

```text
Botón Editar
```

Permite modificar:

```text
Celdas diarias
```

---

No permite modificar:

```text
Unidades
Valor Unitario
Totales
Semana Corrida
Producción Total
```

---

Al editar una celda diaria:

1. Obtener todos los registros asociados a la celda.
2. Mostrar el detalle de esos registros.
3. Permitir seleccionar y editar un registro específico.
4. Guardar el cambio en ese registro.
5. Recalcular la liquidación.

Nunca actualizar automáticamente el primer registro encontrado.

Generar registro:

```text
payroll_audit_log
```

---

# Recalcular

Después de guardar:

1. Recalcular unidades.
2. Recalcular totales.
3. Recalcular total a pagar.
4. Recalcular semana corrida.
5. Recalcular producción total.

Siempre en backend.

Nunca en frontend.
