# Integración Frontend - Backend

Versión: 1.0

---

# Objetivo

Conectar el frontend aprobado con la base de datos.

El frontend ya fue validado por el cliente.

No modificar:

- Layout
- Sidebar
- Navegación
- Tabla de liquidación
- Filtros
- Login

Sólo conectar datos reales.

---

# Menú Principal

El menú debe mantener exactamente estas opciones:

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

Pantalla inicial.

---

## Importar D&R

Botón:

```text
Importar D&R
```

Acción:

```text
Carga archivo Excel D&R
```

Proceso:

```text
Crear importación

Insertar payroll_records

Actualizar historial
```

---

## Importar Servicios

Botón:

```text
Importar Servicios
```

Acción:

```text
Carga archivo Excel Servicios
```

Proceso:

```text
Crear importación

Insertar payroll_records

Actualizar historial
```

---

## Historial de Importaciones

Fuente:

```sql
payroll_imports
```

Columnas:

```text
Fecha

Archivo

Tipo

Cantidad Registros

Usuario
```

Orden:

```text
Más reciente primero
```

---

# Pantallas de Liquidación

Existen cuatro pantallas:

```text
D&R Choferes

D&R Auxiliares

Servicios Choferes

Servicios Auxiliares
```

---

# Filtros

Todos los filtros son obligatorios.

---

## Ciclo

Fuente:

```sql
payroll_cycles
```

Mostrar:

```text
Ciclo Junio 2026

Ciclo Julio 2026

etc
```

---

## Trabajador

Fuente:

```sql
payroll_employees
```

Filtrado por:

```text
cost_center

role_type
```

según pantalla actual.

---

# Construcción de Liquidación

Fuente principal:

```sql
payroll_records
```

---

La tabla debe renderizarse dinámicamente.

No utilizar filas hardcodeadas.

La lista y definición de conceptos proviene de `payroll_concepts`.

---

El backend debe devolver:

```json
{
  "employee": {},
  "cycle": {},
  "dates": [],
  "rows": []
}
```

---

# Dates

Representan:

```text
22
23
24
...
21
```

del ciclo seleccionado.

---

# Rows

Cada fila representa un concepto.

Ejemplo:

```text
Despacho / Retiro

Evento

Viajes Cliente

Fosa

Punto de Agua
```

---

Estructura:

```json
{
  "concept_code": "",
  "concept_name": "",
  "units": 0,
  "rate": 0,
  "total": 0,
  "daily_values": []
}
```

---

# Filas Especiales

El backend debe agregar:

```text
TOTAL A PAGAR

VARIABLE DIARIO

DIA TRABAJADO

SEMANA CORRIDA

VACACIONES

BONO FUERA PRODUCCION

PRODUCCION TOTAL
```

---

Estas filas NO provienen directamente de payroll_records.

Son filas calculadas.

---

# Edición

Visible sólo para ADMIN.

---

Modo lectura:

```text
Tabla bloqueada
```

---

Botón:

```text
Editar
```

---

Al presionar:

```text
Editar
```

Las celdas diarias se vuelven editables.

Una celda puede representar múltiples registros de `payroll_records`. Antes de
editarla, el frontend debe solicitar y mostrar el detalle, permitir seleccionar
un registro específico y enviar su `record_id`.

---

No permitir editar:

```text
Totales

Tarifas

Semana Corrida

Producción Total
```

---

# Guardar

Botón:

```text
Guardar
```

---

Al presionar:

Mostrar modal:

```text
¿Está seguro de guardar estos cambios?
```

---

Si confirma:

```text
Actualizar DB

Registrar auditoría

Recalcular liquidación

Refrescar pantalla
```

---

# Usuarios

Pantalla exclusiva ADMIN.

---

Fuente:

```sql
payroll_users
```

---

Columnas:

```text
Usuario

Nombre

Perfil

Estado
```

---

Perfiles:

```text
ADMIN

USER
```

---

Permisos ADMIN

```text
Importar

Editar

Usuarios

Exportar
```

---

Permisos USER

```text
Consultar

Exportar
```

---

# Búsqueda

Pantalla:

```text
Búsqueda
```

---

Filtros:

```text
Ciclo Desde

Ciclo Hasta

Centro de Costo

Cargo

Trabajador
```

---

Centro de costo:

```text
DR

SERVICES
```

---

Cargo:

```text
DRIVER

ASSISTANT
```

---

# Resultado

El resultado debe visualizarse usando exactamente el mismo layout de liquidación.

No crear tablas distintas.

No crear vistas distintas.

---

# Exportación Excel

Disponible en:

```text
Liquidaciones

Búsqueda
```

---

Formato:

Debe replicar visualmente la liquidación mostrada.

---

# Exportación CSV

Disponible en:

```text
Liquidaciones

Búsqueda
```

---

Debe exportar:

- trabajador
- ciclo
- conceptos
- unidades
- tarifas
- totales

---

# Login

Pantalla inicial.

---

Fuente:

```sql
payroll_users
```

---

Validar:

```text
username

password_hash
```

---

Si usuario:

```text
is_active = 0
```

denegar acceso.

---

# Restricción Crítica

No modificar:

- Sidebar
- Dashboard
- Layout Excel
- Colores
- Navegación
- Modal de Guardado

El frontend ya está aprobado.

El backend debe adaptarse al frontend existente.
