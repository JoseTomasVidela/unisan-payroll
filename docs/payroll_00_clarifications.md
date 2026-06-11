# Payroll Module - Clarificaciones Oficiales

Versión: 1.0

Este documento tiene prioridad sobre cualquier definición previa cuando exista conflicto.

---

# Corrección de Carpetas Frontend

La carpeta oficial aprobada es:

```text
frontend/approved_ui
```

Si existe una carpeta:

```text
frontend/aproved_ui
```

debe renombrarse a:

```text
frontend/approved_ui
```

---

# Documento 06

La referencia correcta es:

```text
docs/payroll_06_queries_and_views.md
```

No existe:

```text
docs/payroll_06_api_plan.md
```

Toda referencia debe actualizarse.

---

# Frontend Congelado

La carpeta:

```text
frontend/approved_ui
```

contiene la versión aprobada por el cliente.

No modificar:

- Layout
- Navegación
- Sidebar
- Dashboard
- Tabla de Liquidación
- Login
- Modal de Confirmación
- Estilos

El backend debe adaptarse al frontend.

---

# Despacho / Retiro

Actualmente la liquidación considera:

```text
Despacho / Retiro
```

como un único concepto.

Utilizar únicamente:

```text
dispatch_flag
```

No utilizar:

```text
retrieval_flag
```

La columna queda reservada para una futura evolución del sistema.

---

# Fosa

La liquidación debe utilizar únicamente:

```text
fosa_qty
```

No utilizar:

```text
septic_tank_flag
```

---

# Succión Riles

El campo:

```text
riles_suction_flag
```

NO representa un valor booleano.

Debe interpretarse como:

```text
cantidad decimal
```

Ejemplo:

```text
1.5 m³

2.0 m³

3.25 m³
```

---

# Total a Pagar

Cada pantalla calcula solamente su contexto actual.

Ejemplos:

---

D&R Choferes

```text
cost_center = DR

role_type = DRIVER
```

---

Servicios Auxiliares

```text
cost_center = SERVICES

role_type = ASSISTANT
```

---

No mezclar:

```text
DR

SERVICES
```

en una misma liquidación.

---

# Producción Total

La Producción Total se calcula únicamente sobre la liquidación actualmente visualizada.

No consolidar automáticamente múltiples centros de costo.

---

# Edición de Celdas

Una celda diaria puede estar compuesta por múltiples registros de:

```text
payroll_records
```

Por lo tanto:

NO actualizar:

```text
primer registro encontrado
```

---

Implementación requerida:

Al editar una celda:

1. Obtener registros asociados.
2. Mostrar detalle.
3. Editar registro específico.
4. Guardar cambios.
5. Recalcular liquidación.

---

# Duplicados de Importación

NO utilizar:

```text
import_id
```

para detectar duplicados.

---

Criterio mínimo:

```text
cycle_id

source_employee_name

role_type

cost_center

work_date

source_type
```

---

# Semana Corrida

La implementación debe reproducir exactamente el comportamiento observado en el Excel original.

---

No utilizar:

```text
fórmulas genéricas
```

sin validación.

---

La lógica debe implementarse como componente aislado.

Ejemplo:

```text
WeekCorridaCalculator
```

para facilitar validación y pruebas.

---

# Tarifas Históricas

Las tarifas actualmente se consideran fijas.

Sin embargo:

```text
payroll_concept_rates
```

debe diseñarse para soportar histórico en futuras versiones.

Posibles campos futuros:

```text
effective_from

effective_to

cycle_id
```

No implementar aún.

Sólo considerar en arquitectura.

---

# Identificación de Trabajadores

Inicialmente:

```text
employee_name

role_type
```

serán utilizados para identificación.

---

Se asume que no existen duplicados.

---

En futuras versiones podrá agregarse:

```text
employee_code

rut

external_id
```

---

# Ajustes Manuales

Tabla:

```text
payroll_manual_adjustments
```

---

Campo:

```text
amount
```

representa:

```text
monto total del ajuste
```

---

Campo:

```text
units
```

es opcional.

Puede utilizarse con fines informativos.

---

# Descuentos

Los descuentos deben registrarse mediante:

```text
adjustment_type = DISCOUNT
```

---

Durante cálculo:

```text
Producción Total

=

Total a Pagar

+

Semana Corrida

+

Bonos

+

Vacaciones

-

Descuentos
```

---

# Calendario

Las columnas del calendario NO deben asumir 31 días.

La cantidad de días debe calcularse dinámicamente usando:

```text
payroll_cycles.start_date

payroll_cycles.end_date
```

---

El frontend debe adaptarse automáticamente.

---

# Conceptos

La lista de conceptos debe generarse desde:

```text
payroll_concepts
```

No hardcodear conceptos en frontend.

No hardcodear conceptos en backend.

---

# Orden de Conceptos

Agregar campo:

```text
display
```

Agregar columna:

display_order

en payroll_concepts.

El backend debe ordenar siempre por:

display_order ASC

No hardcodear orden de conceptos.
