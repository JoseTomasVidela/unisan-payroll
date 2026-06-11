Sí. Aquí tienes el nuevo documento:

````markdown
# docs/payroll_03A_excel_source_mapping.md

# Mapping Exacto Excel Fuente → Base de Datos

Versión: 1.0

---

# Objetivo

Este documento define la estructura exacta de los archivos Excel fuente y cómo deben mapearse hacia `payroll_records`.

Este documento tiene prioridad sobre `payroll_03_import_rules.md` cuando exista conflicto.

---

# Regla General

Usar únicamente la hoja:

`Base Datos`

No usar hojas resumen como:

- Conductor
- Conductores
- Auxiliar
- Auxiliares
- Hoja2

La fila de encabezados es siempre la fila 1.

Los datos comienzan en la fila 2.

---

# Archivo D&R

Archivo:

`Base Producciones D&R.xlsx`

Hoja:

`Base Datos`

Cantidad detectada:

- 4.438 filas
- 28 columnas

---

## Columnas D&R

| Columna | Encabezado Excel | Destino DB |
|---|---|---|
| A | Operador | source_employee_name |
| B | Auxiliar | source_employee_name para registro ASSISTANT |
| C | Cod. Usuario | source_employee_code |
| D | Fecha Inicial | work_date |
| E | Fecha Final | no importar |
| F | Duración | duration_minutes |
| G | Estado | status |
| H | Despacho / Retiro | dispatch_flag |
| I | Entrada < 19:30 | entry_before_1930_qty |
| J | Salida > 19:30 | exit_after_1930_qty |
| K | Feria Semana 01 | fair_week_1_flag |
| L | Feria Semana 02 | fair_week_2_flag |
| M | Fuera Radio Normal | outside_radius_flag |
| N | Fuera Radio V Región | outside_radius_v_region_qty |
| O | Sabado | saturday_week_1_qty |
| P | Domingo | sunday_week_1_qty |
| Q | Viajes Por Cliente | client_trips_qty |
| R | Sábado > 16:00 | saturday_after_1600_qty |
| S | Domingo > 16:00 | sunday_after_1600_qty |
| T | URL | no importar |
| U | Secado | weekend_drying_qty |
| V | Evento | event_flag |
| W | Punto de Agua | water_point_flag |
| X | Basurero Grande | large_trash_bin_qty |
| Y | Basurero chico | small_trash_bin_qty |
| Z | Fosa | fosa_qty |
| AA | Aux Sabado Semana 02 | saturday_week_2_qty, solo auxiliares |
| AB | Aux Domingo Semana 02 | sunday_week_2_qty, solo auxiliares |

---

## D&R Choferes

Por cada fila crear un registro para:

`Operador`

Valores fijos:

```text
source_type = DR
cost_center = DR
role_type = DRIVER
````

Usar:

```text
source_employee_name = Operador
source_employee_code = Cod. Usuario
```

---

## D&R Auxiliares

Por cada fila crear un segundo registro si `Auxiliar` tiene valor válido.

Valores inválidos:

```text
N/A
Sin Auxiliar
0
vacío
```

Valores fijos:

```text
source_type = DR
cost_center = DR
role_type = ASSISTANT
```

Usar:

```text
source_employee_name = Auxiliar
source_employee_code = NULL
```

---

# Archivo Servicios

Archivo:

`Base Producción Servicios.xlsx`

Hoja:

`Base Datos`

Cantidad detectada:

* 5.610 filas
* 26 columnas

---

## Columnas Servicios

| Columna | Encabezado Excel     | Destino DB                                   |
| ------- | -------------------- | -------------------------------------------- |
| A       | Operador             | source_employee_name                         |
| B       | Codigo de Usuario    | source_employee_code                         |
| C       | Auxiliar1            | source_employee_name para registro ASSISTANT |
| D       | Auxiliar2            | source_employee_name para registro ASSISTANT |
| E       | Fecha Inicial        | work_date                                    |
| F       | Fecha Final          | no importar                                  |
| G       | Duracion             | duration_minutes                             |
| H       | Estado               | status                                       |
| I       | Aseo                 | cleaning_flag                                |
| J       | Secado               | drying_flag                                  |
| K       | Despacho / Retiro    | dispatch_flag                                |
| L       | Entrada < 07:30      | entry_before_0730_qty                        |
| M       | Salida > 19:30       | exit_after_1930_qty                          |
| N       | Fuera Radio Normal   | outside_radius_flag                          |
| O       | Fuera Radio V Región | outside_radius_v_region_qty                  |
| P       | Entrega Kit          | kit_delivery_flag                            |
| Q       | Carga Lavamanos      | lavatory_load_flag                           |
| R       | Sabado               | saturday_week_1_qty                          |
| S       | Domingo              | sunday_week_1_qty                            |
| T       | Aseo Fin de Semana   | weekend_cleaning_qty                         |
| U       | Secado Fin de Semana | weekend_drying_qty                           |
| V       | Sabado > 16:00       | saturday_after_1600_qty                      |
| W       | Domingo > 16:00      | sunday_after_1600_qty                        |
| X       | Succión Riles (M3)   | riles_suction_flag                           |
| Y       | URL                  | no importar                                  |
| Z       | sin encabezado       | ignorar                                      |

---

## Servicios Choferes

Por cada fila crear un registro para:

`Operador`

Valores fijos:

```text
source_type = SERVICES
cost_center = SERVICES
role_type = DRIVER
```

Usar:

```text
source_employee_name = Operador
source_employee_code = Codigo de Usuario
```

---

## Servicios Auxiliares

Por cada fila crear registros independientes para:

```text
Auxiliar1
Auxiliar2
```

Solo crear registro si el valor es válido.

Valores inválidos:

```text
Sin Auxiliar
N/A
0
vacío
```

Valores fijos:

```text
source_type = SERVICES
cost_center = SERVICES
role_type = ASSISTANT
```

Usar:

```text
source_employee_name = Auxiliar1 o Auxiliar2
source_employee_code = NULL
```

---

# Conversión de Datos

## Fechas

Las columnas `Fecha Inicial` y `Fecha Final` pueden venir como fecha Excel.

Guardar:

```text
work_date = Fecha Inicial
```

Formato destino:

```text
YYYY-MM-DD
```

`Fecha Final` no se importa en esta versión.

---

## Duración

Guardar en:

```text
duration_minutes
```

Si viene vacío o inválido:

```text
NULL
```

---

## Conceptos Numéricos

Todos los conceptos deben convertirse a decimal.

Si el valor viene:

```text
vacío
NULL
texto no numérico
```

guardar:

```text
0
```

---

# Reglas Importantes

## Despacho / Retiro

Usar solo:

```text
dispatch_flag
```

No usar `retrieval_flag` en esta versión.

---

## Fosa

Usar solo:

```text
fosa_qty
```

No usar `septic_tank_flag`.

---

## Succión Riles

Aunque el campo se llama:

```text
riles_suction_flag
```

debe tratarse como cantidad decimal, no como booleano.

---

# Control de Ciclo

Solo importar filas donde:

```text
Fecha Inicial >= payroll_cycles.start_date
Fecha Inicial <= payroll_cycles.end_date
```

---

# Control de Duplicados

No usar `import_id` para detectar duplicados.

Criterio mínimo:

```text
cycle_id
source_type
cost_center
role_type
source_employee_name
work_date
```

Si se detectan registros existentes para el mismo criterio, advertir antes de insertar.

No borrar automáticamente datos existentes.

---

# Resultado Esperado de Importación

Después de importar, mostrar:

* archivo procesado
* tipo: DR o SERVICES
* ciclo
* registros leídos
* registros insertados
* trabajadores creados
* registros omitidos
* errores detectados

---

# Restricción

No modificar `frontend/approved_ui`.

La importación debe alimentar las pantallas existentes en `frontend/working_ui`.

```
```
