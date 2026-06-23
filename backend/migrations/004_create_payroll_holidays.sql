CREATE TABLE payroll_holidays (
    id INT AUTO_INCREMENT PRIMARY KEY,
    holiday_date DATE NOT NULL,
    holiday_name VARCHAR(200) NOT NULL,
    holiday_scope VARCHAR(16) NOT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    is_default BOOLEAN NOT NULL DEFAULT FALSE,
    created_by INT NULL,
    updated_by INT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NULL,
    INDEX ix_payroll_holidays_holiday_date (holiday_date),
    INDEX ix_payroll_holidays_holiday_scope (holiday_scope),
    INDEX ix_payroll_holidays_active (active),
    CONSTRAINT fk_payroll_holidays_created_by FOREIGN KEY (created_by) REFERENCES payroll_users(id),
    CONSTRAINT fk_payroll_holidays_updated_by FOREIGN KEY (updated_by) REFERENCES payroll_users(id)
);
