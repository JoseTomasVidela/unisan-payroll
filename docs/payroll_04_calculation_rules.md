# Especificación de Cálculo - Módulo Liquidaciones

Versión: 2.0

---

# Objetivo

Definir todas las reglas matemáticas utilizadas para construir la liquidación.

La implementación debe reproducir el comportamiento de la planilla Excel actualmente utilizada por el cliente.

No modificar el frontend aprobado.

Toda la lógica de cálculo debe ejecutarse en backend.

---

# Fuente de Datos

La liquidación se construye utilizando:

```text
payroll_records
+
payroll_concept_rates
+
payroll_manual_adjustments
```

---

# Ciclos

Los ciclos NO corresponden a meses calendario.

Formato:

```text
22 de un mes
hasta
21 del mes siguiente
```

Ejemplo:

```text
22-05-2026
21-06-2026
```

Nombre:

```text
Ciclo Junio 2026
```

---

# Construcción de Calendario

Las columnas del layout deben generarse dinámicamente.

Ejemplo:

```text
22-05
23-05
24-05
...
21-06
```

La cantidad de columnas corresponde al rango inclusivo entre
`payroll_cycles.start_date` y `payroll_cycles.end_date`. No asumir 31 días.

---

# Construcción de Conceptos

Cada fila visible en la liquidación corresponde a un concepto.

La lista debe generarse desde `payroll_concepts`. No hardcodear conceptos en
frontend ni backend.

Ejemplo:

```text
Despacho / Retiro

Entrada < 19:30

Salida > 19:30

Evento

Viajes por Cliente

Punto de Agua

Fosa

Basurero Grande

Basurero Chico

Secado Fin de Semana

etc.
```

---

# Valor Diario

Cada celda diaria debe mostrar:

```sql
SUM(campo_concepto)
```

Filtrado por:

```text
employee_id
cycle_id
work_date
```

---

Ejemplo:

```text
Evento
05-06
```

```sql
SUM(event_flag)
```

---

# Unidades

Columna:

```text
UNIDADES
```

Regla:

```sql
SUM(valor_diario)
```

de todos los días del ciclo.

---

Ejemplo:

```text
1
0
3
2
1
```

Resultado:

```text
7
```

---

# Valor Unitario

Proviene desde:

```text
payroll_concept_rates.amount
```

---

# Total Concepto

Regla:

```text
UNIDADES * VALOR UNITARIO
```

---

Ejemplo:

```text
Unidades = 8

Tarifa = 5.000
```

Resultado:

```text
40.000
```

---

# Total a Pagar

Fila:

```text
TOTAL A PAGAR
```

Regla:

```text
SUMA de todos los totales por concepto
```

Incluye:

```text
Sólo conceptos del cost_center y role_type de la pantalla actual
```

No mezclar `DR` y `SERVICES` ni cargos distintos en una misma liquidación.

No incluye:

```text
Semana Corrida

Vacaciones

Bonos Fuera Producción
```

---

# Variable Diario

Fila:

```text
VARIABLE DIARIO
```

La fórmula observada en el Excel es:

```excel
=SUMPRODUCT(CantidadesDiarias, Tarifas)
```

---

Por cada día:

```text
VARIABLE DIARIO

=

Σ
(
cantidad concepto día
*
tarifa concepto
)
```

---

Ejemplo:

```text
Despacho
2 × 5.000

Evento
1 × 10.000

Viaje Cliente
3 × 2.000
```

Resultado:

```text
26.000
```

---

# Día Trabajado

Fila:

```text
DIA TRABAJADO
```

Valores posibles:

```text
1
0
```

---

Regla observada en Excel:

```excel
IF(
Estado = Sin Producción,
1,
IF(
Estado = Inasistencia,
1,
IF(
VariableDiario < 1,
0,
1
)
)
)
```

---

Por lo tanto:

```text
Día Trabajado = 1
```

si:

- Estado = Sin Producción
- Estado = Inasistencia
- Variable Diario > 0

---

En caso contrario:

```text
Día Trabajado = 0
```

---

# Semana Corrida

Fila:

```text
SEMANA CORRIDA
```

---

Fuente:

```text
VARIABLE DIARIO

+

DIA TRABAJADO
```

---

La implementación debe reproducir exactamente el comportamiento observado en
el Excel original. No utilizar fórmulas genéricas sin validarlas contra casos
reales del Excel.

La lógica debe implementarse como componente aislado, por ejemplo
`WeekCorridaCalculator`, para facilitar su validación y pruebas.

---

# Vacaciones

Las vacaciones NO provienen de payroll_records.

Provienen de:

```text
payroll_manual_adjustments
```

---

Tipos permitidos:

```text
VACATION
```

---

Visualización:

Fila:

```text
VACACIONES
```

---

# Bono Fuera Producción

No proviene de payroll_records.

Proviene de:

```text
payroll_manual_adjustments
```

---

Tipos permitidos:

```text
OUT_OF_PRODUCTION_BONUS
```

---

Visualización:

```text
BONO FUERA PRODUCCION
```

---

Ejemplos:

```text
Marathon Santiago

Bono Especial

Compensación
```

---

# Ajustes Manuales

Provienen de:

```text
payroll_manual_adjustments
```

---

Tipos:

```text
MANUAL_ADJUSTMENT

BONUS

DISCOUNT
```

---

`BONUS` se suma y `DISCOUNT` se resta. `MANUAL_ADJUSTMENT` no agrega un
término implícito separado a Producción Total; su tratamiento debe definirse
antes de incluirlo.

`amount` representa el monto total del ajuste. `units` es opcional y puede
usarse sólo con fines informativos.

---

# Producción Total

Fila:

```text
PRODUCCION TOTAL
```

La fórmula observada en Excel corresponde a:

```text
TOTAL A PAGAR

+

SEMANA CORRIDA

+

VACACIONES

+

BONOS

-

DESCUENTOS
```

---

Resultado:

```text
PRODUCCION TOTAL
```

La Producción Total se calcula únicamente para el `cost_center` y `role_type`
de la liquidación visualizada. No consolidar automáticamente múltiples centros
de costo.

---

# Campos Editables

Sólo usuarios ADMIN.

---

Editable:

```text
Celdas diarias de producción
```

---

Ejemplo:

```text
Evento

05-06

0 → 1
```

---

No editable:

```text
UNIDADES

VALOR UNITARIO

TOTAL

VARIABLE DIARIO

DIA TRABAJADO

SEMANA CORRIDA

TOTAL A PAGAR

VACACIONES

BONOS

PRODUCCION TOTAL
```

---

# Guardado

Al presionar:

```text
Guardar
```

El backend debe:

1. Actualizar payroll_records.
2. Registrar auditoría.
3. Recalcular liquidación completa.
4. Devolver liquidación recalculada.

---

# Auditoría

Registrar en:

```text
payroll_audit_log
```

Campos:

```text
usuario
fecha
concepto
fecha_produccion
valor_anterior
valor_nuevo
```

---

# Exportación

Formatos:

```text
Excel

CSV
```

La exportación debe reflejar exactamente la liquidación mostrada en pantalla.

---

# Restricción Importante

No modificar el frontend aprobado.

La API debe alimentar el layout existente.

No crear nuevas pantallas.

No modificar navegación.

No modificar estructura visual.

Toda la lógica de negocio debe implementarse en backend.
