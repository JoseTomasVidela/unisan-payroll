-- Homologacion de tablas de Unisan Payroll para Azure MySQL.
-- Seleccionar unisan_db como base activa y ejecutar desde CREATE TABLE hasta el final.

CREATE TABLE IF NOT EXISTS payroll_holidays (
    id INT NOT NULL AUTO_INCREMENT,
    holiday_date DATE NOT NULL,
    holiday_name VARCHAR(200) NOT NULL,
    holiday_scope VARCHAR(16) NOT NULL,
    active TINYINT(1) NOT NULL DEFAULT 1,
    is_default TINYINT(1) NOT NULL DEFAULT 0,
    created_by INT NULL,
    updated_by INT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NULL,
    PRIMARY KEY (id),
    INDEX ix_payroll_holidays_holiday_date (holiday_date),
    INDEX ix_payroll_holidays_holiday_scope (holiday_scope),
    INDEX ix_payroll_holidays_active (active),
    INDEX ix_payroll_holidays_created_by (created_by),
    INDEX ix_payroll_holidays_updated_by (updated_by)
);

SHOW TABLES LIKE 'payroll_holidays';

SHOW COLUMNS FROM payroll_holidays;
