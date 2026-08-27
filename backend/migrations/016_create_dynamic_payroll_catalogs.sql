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

INSERT INTO payroll_cost_centers (code, name)
VALUES ('DR', 'D&R'), ('SERVICES', 'Servicios')
ON DUPLICATE KEY UPDATE name = VALUES(name), active = 1;

INSERT INTO payroll_adjustment_types (code, name, worked_day_value)
VALUES
    ('PERMISO', 'Permiso', 1),
    ('CUMPLEANOS', 'Cumpleaños', 0)
ON DUPLICATE KEY UPDATE
    name = VALUES(name),
    worked_day_value = VALUES(worked_day_value),
    active = 1;

SELECT code, name, active FROM payroll_cost_centers ORDER BY name;
SELECT code, name, worked_day_value, active FROM payroll_adjustment_types ORDER BY name;
