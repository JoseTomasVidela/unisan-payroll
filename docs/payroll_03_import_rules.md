# Especificación de Importación - Módulo Liquidaciones

Versión: 1.0

---

# Objetivo

Definir cómo importar los archivos Excel fuente hacia la tabla `payroll_records`.

El frontend ya está definido y aprobado.  
No modificar la estructura visual del frontend.

El backend debe alimentar el frontend usando los datos importados desde la base de datos.

---

# Regla General

Los Excel son solo fuente de carga.

Después de importar:

- No se vuelve a consultar el Excel.
- No se sincronizan cambios hacia el Excel.
- Toda corrección posterior se realiza en la aplicación.
- La base de datos es la fuente oficial.

---

# Ciclo de Liquidación

Toda importación debe asociarse a un ciclo existente en:

`payroll_cycles`

Ejemplo:

```text
Ciclo Junio 2026
start_date = 2026-05-22
end_date   = 2026-06-21
```

Solo deben importarse registros cuya fecha esté dentro del rango del ciclo seleccionado.

---

# Archivos Fuente

Existen dos archivos fuente:

1. Base Producciones D&R.xlsx
2. Base Producción Servicios.xlsx

Ambos contienen una hoja llamada:

`Base Datos`

Esa es la única hoja que debe usarse para importar.

No usar hojas resumen como:

- Conductor
- Conductores
- Auxiliar
- Auxiliares

---

# Tabla Principal de Destino

Toda la información operacional debe insertarse en:

`payroll_records`

Cada fila de `payroll_records` representa un registro diario de producción asociado a:

- trabajador
- fecha
- centro de costo
- cargo
- importación
- ciclo

---

# Registro de Importación

Antes de insertar registros en `payroll_records`, crear un registro en:

`payroll_imports`

Campos:

- `cycle_id`
- `source_type`
- `cost_center`
- `file_name`
- `imported_by`
- `rows_imported`

Valores:

Para archivo D&R:

```text
source_type = DR
cost_center = DR
```

Para archivo Servicios:

```text
source_type = SERVICES
cost_center = SERVICES
```

---

# Creación de Trabajadores

Si un trabajador no existe en `payroll_employees`, debe crearse automáticamente.

Comparar por:

- `employee_name`
- `role_type`

No exigir RUT ni código interno.

Valores permitidos de `role_type`:

```text
DRIVER
ASSISTANT
```

---

# Importación D&R

Archivo:

`Base Producciones D&R.xlsx`

Hoja:

`Base Datos`

## Columnas fuente

| Columna Excel | Nombre | Uso |
|---|---|---|
| A | Operador | Chofer |
| B | Auxiliar | Auxiliar |
| C | Cod. Usuario | Código original |
| D | Fecha Inicial | Fecha de trabajo |
| E | Fecha Final | Referencia |
| F | Duración | Duración |
| G | Estado | Estado |
| H | Despacho / Retiro | Concepto |
| I | Entrada < 19:30 | Concepto |
| J | Salida > 19:30 | Concepto |
| K | Feria Semana 01 | Concepto |
| L | Feria Semana 02 | Concepto |
| M | Fuera Radio Normal | Concepto |
| N | Fuera Radio V Región | Concepto |
| O | Sabado | Concepto |
| P | Domingo | Concepto |
| Q | Viajes Por Cliente | Concepto |
| R | Sábado > 16:00 | Concepto |
| S | Domingo > 16:00 | Concepto |
| U | Secado | Concepto |
| V | Evento | Concepto |
| W | Punto de Agua | Concepto |
| X | Basurero Grande | Concepto |
| Y | Basurero Chico | Concepto |
| Z | Fosa | Concepto |
| AA | Aux Sabado Semana 02 | Concepto auxiliar |
| AB | Aux Domingo Semana 02 | Concepto auxiliar |

---

## D&R Choferes

Por cada fila del Excel, crear un registro para el operador.

Valores fijos:

```text
source_type = DR
cost_center = DR
role_type   = DRIVER
```

Mapeo:

| payroll_records | Origen Excel |
|---|---|
| source_employee_name | Operador |
| source_employee_code | Cod. Usuario |
| work_date | Fecha Inicial |
| duration_minutes | Duración |
| status | Estado |
| dispatch_flag | Despacho / Retiro |
| entry_before_1930_qty | Entrada < 19:30 |
| exit_after_1930_qty | Salida > 19:30 |
| fair_week_1_flag | Feria Semana 01 |
| fair_week_2_flag | Feria Semana 02 |
| outside_radius_flag | Fuera Radio Normal |
| outside_radius_v_region_qty | Fuera Radio V Región |
| saturday_week_1_qty | Sabado |
| sunday_week_1_qty | Domingo |
| client_trips_qty | Viajes Por Cliente |
| saturday_after_1600_qty | Sábado > 16:00 |
| sunday_after_1600_qty | Domingo > 16:00 |
| weekend_drying_qty | Secado |
| event_flag | Evento |
| water_point_flag | Punto de Agua |
| large_trash_bin_qty | Basurero Grande |
| small_trash_bin_qty | Basurero Chico |
| fosa_qty | Fosa |

---

## D&R Auxiliares

Por cada fila del Excel, si existe valor en `Auxiliar`, crear un segundo registro para el auxiliar.

Valores fijos:

```text
source_type = DR
cost_center = DR
role_type   = ASSISTANT
```

Mapeo:

| payroll_records | Origen Excel |
|---|---|
| source_employee_name | Auxiliar |
| source_employee_code | NULL |
| work_date | Fecha Inicial |
| duration_minutes | Duración |
| status | Estado |
| dispatch_flag | Despacho / Retiro |
| entry_before_1930_qty | Entrada < 19:30 |
| exit_after_1930_qty | Salida > 19:30 |
| fair_week_1_flag | Feria Semana 01 |
| fair_week_2_flag | Feria Semana 02 |
| outside_radius_flag | Fuera Radio Normal |
| outside_radius_v_region_qty | Fuera Radio V Región |
| saturday_week_1_qty | Sabado |
| sunday_week_1_qty | Domingo |
| saturday_week_2_qty | Aux Sabado Semana 02 |
| sunday_week_2_qty | Aux Domingo Semana 02 |
| client_trips_qty | Viajes Por Cliente |
| saturday_after_1600_qty | Sábado > 16:00 |
| sunday_after_1600_qty | Domingo > 16:00 |
| weekend_drying_qty | Secado |
| event_flag | Evento |
| water_point_flag | Punto de Agua |
| large_trash_bin_qty | Basurero Grande |
| small_trash_bin_qty | Basurero Chico |
| fosa_qty | Fosa |

---

# Importación Servicios

Archivo:

`Base Producción Servicios.xlsx`

Hoja:

`Base Datos`

## Columnas fuente

| Columna Excel | Nombre | Uso |
|---|---|---|
| A | Operador | Chofer |
| B | Codigo de Usuario | Código original |
| C | Auxiliar1 | Auxiliar |
| D | Auxiliar2 | Auxiliar |
| E | Fecha Inicial | Fecha de trabajo |
| F | Fecha Final | Referencia |
| G | Duracion | Duración |
| H | Estado | Estado |
| I | Aseo | Concepto |
| J | Secado | Concepto |
| K | Despacho / Retiro | Concepto |
| L | Entrada < 07:30 | Concepto |
| M | Salida > 19:30 | Concepto |
| N | Fuera Radio Normal | Concepto |
| O | Fuera Radio V Región | Concepto |
| P | Entrega Kit | Concepto |
| Q | Carga Lavamanos | Concepto |
| R | Sabado | Concepto |
| S | Domingo | Concepto |
| T | Aseo Fin de Semana | Concepto |
| U | Secado Fin de Semana | Concepto |
| V | Sabado > 16:00 | Concepto |
| W | Domingo > 16:00 | Concepto |
| X | Succión Riles (M3) | Concepto |

---

## Servicios Choferes

Por cada fila del Excel, crear un registro para el operador.

Valores fijos:

```text
source_type = SERVICES
cost_center = SERVICES
role_type   = DRIVER
```

Mapeo:

| payroll_records | Origen Excel |
|---|---|
| source_employee_name | Operador |
| source_employee_code | Codigo de Usuario |
| work_date | Fecha Inicial |
| duration_minutes | Duracion |
| status | Estado |
| cleaning_flag | Aseo |
| drying_flag | Secado |
| dispatch_flag | Despacho / Retiro |
| entry_before_0730_qty | Entrada < 07:30 |
| exit_after_1930_qty | Salida > 19:30 |
| outside_radius_flag | Fuera Radio Normal |
| outside_radius_v_region_qty | Fuera Radio V Región |
| kit_delivery_flag | Entrega Kit |
| lavatory_load_flag | Carga Lavamanos |
| saturday_week_1_qty | Sabado |
| sunday_week_1_qty | Domingo |
| weekend_cleaning_qty | Aseo Fin de Semana |
| weekend_drying_qty | Secado Fin de Semana |
| saturday_after_1600_qty | Sabado > 16:00 |
| sunday_after_1600_qty | Domingo > 16:00 |
| riles_suction_flag | Succión Riles (M3) |

`riles_suction_flag` debe importarse como cantidad decimal en m³, no como
bandera booleana.

---

## Servicios Auxiliares

Por cada fila del Excel, crear registros separados para:

- Auxiliar1
- Auxiliar2

Solo crear registro si el valor no está vacío y no es:

```text
Sin Auxiliar
```

Valores fijos:

```text
source_type = SERVICES
cost_center = SERVICES
role_type   = ASSISTANT
```

Mapeo:

| payroll_records | Origen Excel |
|---|---|
| source_employee_name | Auxiliar1 o Auxiliar2 |
| source_employee_code | NULL |
| work_date | Fecha Inicial |
| duration_minutes | Duracion |
| status | Estado |
| cleaning_flag | Aseo |
| drying_flag | Secado |
| dispatch_flag | Despacho / Retiro |
| entry_before_0730_qty | Entrada < 07:30 |
| exit_after_1930_qty | Salida > 19:30 |
| outside_radius_flag | Fuera Radio Normal |
| outside_radius_v_region_qty | Fuera Radio V Región |
| kit_delivery_flag | Entrega Kit |
| lavatory_load_flag | Carga Lavamanos |
| saturday_week_1_qty | Sabado |
| sunday_week_1_qty | Domingo |
| weekend_cleaning_qty | Aseo Fin de Semana |
| weekend_drying_qty | Secado Fin de Semana |
| saturday_after_1600_qty | Sabado > 16:00 |
| sunday_after_1600_qty | Domingo > 16:00 |
| riles_suction_flag | Succión Riles (M3) |

`riles_suction_flag` debe importarse como cantidad decimal en m³, no como
bandera booleana.

---

# Conversión de Fechas

Las fechas pueden venir como número serial Excel.

Ejemplo:

```text
45799
```

El sistema debe convertirlas a formato fecha MySQL:

```text
YYYY-MM-DD
```

Guardar en:

```text
work_date
```

---

# Conversión de Valores Numéricos

Todos los campos de conceptos deben guardarse como número decimal.

Si el valor viene vacío, nulo o no numérico:

```text
guardar 0
```

No guardar texto en columnas numéricas.

---

# Control de Duplicados

En esta primera versión, evitar duplicar registros cuando se importe nuevamente el mismo archivo para el mismo ciclo.

Criterio mínimo de duplicado:

```text
cycle_id
source_employee_name
role_type
cost_center
work_date
source_type
```

No utilizar `import_id` para detectar duplicados.

Si se reimporta un archivo del mismo ciclo, el sistema debe advertir al usuario antes de insertar registros duplicados.

No borrar registros existentes automáticamente.

---

# Resultado de Importación

Después de importar, mostrar resumen:

- archivo procesado
- ciclo
- centro de costo
- registros leídos
- registros insertados
- trabajadores creados
- registros omitidos
- errores detectados

---

# Restricción Importante

No modificar el frontend aprobado.

El frontend debe recibir datos desde el backend en el mismo layout definido:

- Dashboard
- Liquidaciones D&R Choferes
- Liquidaciones D&R Auxiliares
- Liquidaciones Servicios Choferes
- Liquidaciones Servicios Auxiliares
- Búsqueda
- Usuarios

La importación debe alimentar esas pantallas usando `payroll_records`.
