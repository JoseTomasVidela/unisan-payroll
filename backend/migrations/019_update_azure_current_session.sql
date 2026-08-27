-- Actualizacion consolidada de Azure MySQL.
-- Ejecutar conectado a la base unisan_db.
-- El script es idempotente y conserva todos los datos existentes.

CREATE TABLE IF NOT EXISTS payroll_cost_centers (
    id BIGINT NOT NULL AUTO_INCREMENT,
    code VARCHAR(32) NOT NULL,
    name VARCHAR(100) NOT NULL,
    active TINYINT(1) NOT NULL DEFAULT 1,
    created_by BIGINT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_payroll_cost_centers_code (code),
    UNIQUE KEY uq_payroll_cost_centers_name (name),
    KEY ix_payroll_cost_centers_active (active),
    CONSTRAINT fk_payroll_cost_centers_created_by
        FOREIGN KEY (created_by) REFERENCES payroll_users (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS payroll_adjustment_types (
    id BIGINT NOT NULL AUTO_INCREMENT,
    code VARCHAR(64) NOT NULL,
    name VARCHAR(100) NOT NULL,
    worked_day_value TINYINT NOT NULL,
    active TINYINT(1) NOT NULL DEFAULT 1,
    created_by BIGINT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_payroll_adjustment_types_code (code),
    UNIQUE KEY uq_payroll_adjustment_types_name (name),
    KEY ix_payroll_adjustment_types_active (active),
    CONSTRAINT fk_payroll_adjustment_types_created_by
        FOREIGN KEY (created_by) REFERENCES payroll_users (id),
    CONSTRAINT ck_payroll_adjustment_types_worked_day_value
        CHECK (worked_day_value IN (0, 1))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS payroll_liquidation_activities (
    id BIGINT NOT NULL AUTO_INCREMENT,
    cycle_id BIGINT NOT NULL,
    employee_id BIGINT NOT NULL,
    concept_id BIGINT NOT NULL,
    created_by BIGINT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_payroll_liquidation_activity (cycle_id, employee_id, concept_id),
    KEY ix_payroll_liquidation_activities_cycle (cycle_id),
    KEY ix_payroll_liquidation_activities_employee (employee_id),
    KEY ix_payroll_liquidation_activities_concept (concept_id),
    CONSTRAINT fk_payroll_liquidation_activities_cycle
        FOREIGN KEY (cycle_id) REFERENCES payroll_cycles (id),
    CONSTRAINT fk_payroll_liquidation_activities_employee
        FOREIGN KEY (employee_id) REFERENCES payroll_employees (id),
    CONSTRAINT fk_payroll_liquidation_activities_concept
        FOREIGN KEY (concept_id) REFERENCES payroll_concepts (id),
    CONSTRAINT fk_payroll_liquidation_activities_user
        FOREIGN KEY (created_by) REFERENCES payroll_users (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO payroll_cost_centers (code, name, active)
VALUES
    ('DR', 'D&R', 1),
    ('SERVICES', 'Servicios', 1)
ON DUPLICATE KEY UPDATE
    name = VALUES(name),
    active = 1;

INSERT INTO payroll_adjustment_types (code, name, worked_day_value, active)
VALUES
    ('PERMISO', 'Permiso', 1, 1),
    ('CUMPLEANOS', 'Cumpleaños', 0, 1)
ON DUPLICATE KEY UPDATE
    name = VALUES(name),
    worked_day_value = VALUES(worked_day_value),
    active = 1;

UPDATE payroll_softland_concept_mappings
SET
    softland_code = 'H040',
    source_label = 'Bono Vacaciones',
    active = 1,
    updated_at = CURRENT_TIMESTAMP
WHERE mapping_type = 'ADJUSTMENT'
  AND mapping_key = 'VACATION_BONUS';

UPDATE payroll_softland_concept_mappings
SET
    softland_code = 'H040',
    source_label = 'VACACIONES',
    active = 1,
    updated_at = CURRENT_TIMESTAMP
WHERE mapping_type = 'ADJUSTMENT'
  AND mapping_key = 'VACATION';

-- Verificacion final. Debe devolver tres filas con table_exists = 1.
SELECT 'payroll_cost_centers' AS table_name,
       COUNT(*) AS table_exists
FROM information_schema.tables
WHERE table_schema = DATABASE()
  AND table_name = 'payroll_cost_centers'
UNION ALL
SELECT 'payroll_adjustment_types', COUNT(*)
FROM information_schema.tables
WHERE table_schema = DATABASE()
  AND table_name = 'payroll_adjustment_types'
UNION ALL
SELECT 'payroll_liquidation_activities', COUNT(*)
FROM information_schema.tables
WHERE table_schema = DATABASE()
  AND table_name = 'payroll_liquidation_activities';

-- Ambos conceptos deben quedar asociados a H040.
SELECT mapping_key, source_label, softland_code, active
FROM payroll_softland_concept_mappings
WHERE mapping_type = 'ADJUSTMENT'
  AND mapping_key IN ('VACATION_BONUS', 'VACATION')
ORDER BY mapping_key;
