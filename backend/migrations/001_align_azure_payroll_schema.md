# Migración 001 - Alineación Azure Payroll

Estado: POSTERGADA hasta el cierre del proyecto. No ejecutar durante Etapa 3A.

Incluye también el plan pendiente de versionado de `payroll_concept_rates`:
`effective_from_cycle_id`, `effective_to_cycle_id`, `created_by` y `updated_at`.
Las columnas quedan inicialmente nullable para permitir el backfill controlado de
tarifas legadas. La aplicación nunca sobrescribe una tarifa histórica.

## Objetivo

Alinear manualmente el esquema payroll existente en Azure MySQL con el contrato
actual del backend, sin utilizar `Base.metadata.create_all` y sin eliminar datos.

Script para revisión y ejecución manual:

```text
backend/migrations/001_align_azure_payroll_schema.sql
```

## Alcance

- Valida que el esquema activo sea `unisan_db`.
- Crea `payroll_permissions` y `payroll_role_permissions` si no existen.
- Agrega y normaliza las columnas requeridas por `payroll_roles` y
  `payroll_users`.
- Migra `payroll_imports.imported_by` desde nombre de usuario a
  `payroll_users.id`.
- Agrega `payroll_concepts.db_field` y `payroll_concepts.display_order`.
- Amplía los conceptos y ajustes numéricos a `DECIMAL(14,4)`.
- Conserva `retrieval_flag` y `septic_tank_flag` como columnas reservadas.
- Normaliza campos fuente requeridos por la importación.
- Siembra permisos y sus asociaciones con `ADMIN` y `USER`.
- Entrega consultas de verificación al finalizar.

## Cambio de imported_by

El backend guarda y consulta:

```text
payroll_imports.imported_by -> payroll_users.id
```

Azure originalmente define `imported_by` como `VARCHAR(100)`. La migración:

1. Verifica que cada valor existente coincida con `payroll_users.username`.
2. Aborta si encuentra un valor sin correspondencia.
3. Conserva el texto original en `imported_by_legacy`.
4. Convierte `imported_by` a `BIGINT NOT NULL`.
5. Agrega una FK hacia `payroll_users.id`.

Al momento del análisis, `payroll_imports` y `payroll_users` estaban vacías, por
lo que no existían valores que convertir.

## Seguridad

- No contiene `DROP TABLE`, `DROP COLUMN`, `DELETE` ni `TRUNCATE`.
- No crea restricciones `UNIQUE` sobre `payroll_records`.
- No modifica tablas sin prefijo `payroll_`.
- No inventa valores para registros fuente incompletos; aborta si los encuentra.
- MySQL realiza commits implícitos para DDL. Crear respaldo antes de ejecutar.

## Ejecución manual

1. Revisar el script completo.
2. Crear un respaldo del esquema.
3. Conectarse a Azure MySQL con un usuario autorizado para DDL.
4. Confirmar que el esquema activo sea `unisan_db`.
5. Ejecutar el script completo en DBeaver.
6. Revisar las consultas de verificación entregadas al final.

La aplicación no ejecuta esta migración automáticamente.

Antes de ejecutar la migración final, cada concepto existente debe tener
`db_field` informado con la columna de `payroll_records` que debe agregar. La
migración aborta si encuentra conceptos sin ese mapping.

## Base local

Este SQL apunta exclusivamente a Azure MySQL y no modifica SQLite local. La
alineación local deberá realizarse posteriormente mediante una migración
específica para SQLite o recreando una base local descartable bajo aprobación
explícita. Un mismo archivo SQL no puede aplicar de forma segura ambos dialectos.
