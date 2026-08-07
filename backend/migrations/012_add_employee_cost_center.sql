-- Agrega Centro de Costo al maestro de trabajadores.
-- Ejecutar en unisan_db antes de desplegar el backend.

ALTER TABLE payroll_employees
    ADD COLUMN IF NOT EXISTS cost_center VARCHAR(32) NULL AFTER role_type;

-- Homologa trabajadores históricos desde sus registros de producción.
UPDATE payroll_employees AS employee
LEFT JOIN (
    SELECT employee_id, MIN(cost_center) AS cost_center
    FROM payroll_records
    WHERE cost_center IN ('DR', 'SERVICES')
    GROUP BY employee_id
) AS history ON history.employee_id = employee.id
SET employee.cost_center = history.cost_center
WHERE employee.cost_center IS NULL
  AND history.cost_center IS NOT NULL;

SELECT id, employee_name, cost_center
FROM payroll_employees
ORDER BY employee_name;
