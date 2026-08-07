-- Configuracion global de Unisan Payroll.
-- Ejecutar en unisan_db si la cuenta de la aplicacion no tiene permiso CREATE.

CREATE TABLE IF NOT EXISTS payroll_settings (
    id INT NOT NULL AUTO_INCREMENT,
    setting_key VARCHAR(100) NOT NULL,
    setting_value VARCHAR(255) NOT NULL,
    updated_by INT NULL,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE INDEX ix_payroll_settings_setting_key (setting_key),
    INDEX ix_payroll_settings_updated_by (updated_by)
);

INSERT INTO payroll_settings (setting_key, setting_value, updated_by, updated_at)
SELECT 'operations_edit_locked', 'false', NULL, CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1
    FROM payroll_settings
    WHERE setting_key = 'operations_edit_locked'
);

SELECT setting_key, setting_value, updated_by, updated_at
FROM payroll_settings
WHERE setting_key = 'operations_edit_locked';
