-- UNISAN Payroll baseline schema for Azure MySQL
-- Target schema: unisan_db
-- Purpose:
--   Create the payroll module from zero using only payroll_ tables.
-- Notes:
--   - Does not create users or passwords.
--   - Does not insert business data.
--   - Does not use SQLAlchemy create_all in production.
--   - Safe to review and execute manually in DBeaver after selecting unisan_db.

USE unisan_db;

CREATE TABLE IF NOT EXISTS payroll_permissions (
    id BIGINT NOT NULL AUTO_INCREMENT,
    permission_code VARCHAR(64) NOT NULL,
    description VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uk_payroll_permissions_code (permission_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS payroll_roles (
    id BIGINT NOT NULL AUTO_INCREMENT,
    role_name VARCHAR(32) NOT NULL,
    description VARCHAR(255) NOT NULL,
    active TINYINT(1) NOT NULL DEFAULT 1,
    PRIMARY KEY (id),
    UNIQUE KEY uk_payroll_roles_name (role_name),
    KEY ix_payroll_roles_role_name (role_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS payroll_role_permissions (
    role_id BIGINT NOT NULL,
    permission_id BIGINT NOT NULL,
    PRIMARY KEY (role_id, permission_id),
    CONSTRAINT fk_payroll_role_permissions_role
        FOREIGN KEY (role_id) REFERENCES payroll_roles (id) ON DELETE CASCADE,
    CONSTRAINT fk_payroll_role_permissions_permission
        FOREIGN KEY (permission_id) REFERENCES payroll_permissions (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS payroll_users (
    id BIGINT NOT NULL AUTO_INCREMENT,
    username VARCHAR(80) NOT NULL,
    full_name VARCHAR(160) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role_id BIGINT NOT NULL,
    active TINYINT(1) NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login_at DATETIME NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uk_payroll_users_username (username),
    KEY ix_payroll_users_username (username),
    KEY ix_payroll_users_active (active),
    CONSTRAINT fk_payroll_users_role
        FOREIGN KEY (role_id) REFERENCES payroll_roles (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS payroll_cycles (
    id BIGINT NOT NULL AUTO_INCREMENT,
    cycle_name VARCHAR(120) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    PRIMARY KEY (id),
    KEY ix_payroll_cycles_start_date (start_date),
    KEY ix_payroll_cycles_end_date (end_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS payroll_employees (
    id BIGINT NOT NULL AUTO_INCREMENT,
    employee_name VARCHAR(180) NOT NULL,
    role_type VARCHAR(32) NOT NULL,
    contract_type VARCHAR(16) NULL,
    PRIMARY KEY (id),
    KEY ix_payroll_employees_employee_name (employee_name),
    KEY ix_payroll_employees_role_type (role_type),
    KEY ix_payroll_employees_contract_type (contract_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS payroll_imports (
    id BIGINT NOT NULL AUTO_INCREMENT,
    cycle_id BIGINT NOT NULL,
    source_type VARCHAR(32) NOT NULL,
    cost_center VARCHAR(32) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    imported_by BIGINT NOT NULL,
    rows_imported INT NOT NULL DEFAULT 0,
    imported_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY ix_payroll_imports_cycle_id (cycle_id),
    KEY ix_payroll_imports_source_type (source_type),
    KEY ix_payroll_imports_cost_center (cost_center),
    KEY ix_payroll_imports_imported_by (imported_by),
    CONSTRAINT fk_payroll_imports_cycle
        FOREIGN KEY (cycle_id) REFERENCES payroll_cycles (id),
    CONSTRAINT fk_payroll_imports_user
        FOREIGN KEY (imported_by) REFERENCES payroll_users (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS payroll_records (
    id BIGINT NOT NULL AUTO_INCREMENT,
    cycle_id BIGINT NOT NULL,
    import_id BIGINT NOT NULL,
    employee_id BIGINT NOT NULL,
    source_type VARCHAR(32) NOT NULL,
    cost_center VARCHAR(32) NOT NULL,
    role_type VARCHAR(32) NOT NULL,
    source_employee_name VARCHAR(180) NOT NULL,
    source_employee_code VARCHAR(100) NULL,
    source_row_number INT NOT NULL,
    source_row_hash VARCHAR(64) NOT NULL,
    source_person_slot VARCHAR(32) NOT NULL,
    work_date DATE NOT NULL,
    duration_minutes INT NULL,
    status VARCHAR(120) NULL,
    dispatch_flag DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
    entry_before_1930_qty DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
    entry_before_0730_qty DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
    exit_after_1930_qty DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
    fair_week_1_flag DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
    fair_week_2_flag DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
    outside_radius_flag DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
    outside_radius_v_region_qty DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
    saturday_week_1_qty DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
    sunday_week_1_qty DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
    saturday_week_2_qty DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
    sunday_week_2_qty DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
    client_trips_qty DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
    saturday_after_1600_qty DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
    sunday_after_1600_qty DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
    cleaning_flag DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
    drying_flag DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
    weekend_cleaning_qty DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
    weekend_drying_qty DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
    event_flag DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
    water_point_flag DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
    kit_delivery_flag DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
    lavatory_load_flag DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
    large_trash_bin_qty DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
    small_trash_bin_qty DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
    fosa_qty DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
    riles_suction_flag DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
    PRIMARY KEY (id),
    KEY ix_payroll_records_cycle_id (cycle_id),
    KEY ix_payroll_records_import_id (import_id),
    KEY ix_payroll_records_employee_id (employee_id),
    KEY ix_payroll_records_source_type (source_type),
    KEY ix_payroll_records_cost_center (cost_center),
    KEY ix_payroll_records_role_type (role_type),
    KEY ix_payroll_records_source_employee_name (source_employee_name),
    KEY ix_payroll_records_source_row_hash (source_row_hash),
    KEY ix_payroll_records_source_person_slot (source_person_slot),
    KEY ix_payroll_records_work_date (work_date),
    CONSTRAINT fk_payroll_records_cycle
        FOREIGN KEY (cycle_id) REFERENCES payroll_cycles (id),
    CONSTRAINT fk_payroll_records_import
        FOREIGN KEY (import_id) REFERENCES payroll_imports (id),
    CONSTRAINT fk_payroll_records_employee
        FOREIGN KEY (employee_id) REFERENCES payroll_employees (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS payroll_concepts (
    id BIGINT NOT NULL AUTO_INCREMENT,
    concept_code VARCHAR(50) NOT NULL,
    concept_name VARCHAR(200) NOT NULL,
    db_field VARCHAR(64) NOT NULL,
    source_type VARCHAR(32) NOT NULL,
    cost_center VARCHAR(32) NOT NULL,
    role_type VARCHAR(32) NOT NULL,
    display_order INT NOT NULL DEFAULT 0,
    active TINYINT(1) NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY ix_payroll_concepts_cost_center (cost_center),
    KEY ix_payroll_concepts_role_type (role_type),
    KEY ix_payroll_concepts_display_order (display_order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS payroll_concept_rates (
    id BIGINT NOT NULL AUTO_INCREMENT,
    concept_id BIGINT NOT NULL,
    amount DECIMAL(14,4) NOT NULL,
    contract_type VARCHAR(16) NULL,
    effective_from_cycle_id BIGINT NULL,
    effective_to_cycle_id BIGINT NULL,
    created_by BIGINT NULL,
    active TINYINT(1) NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NULL,
    PRIMARY KEY (id),
    KEY ix_payroll_concept_rates_concept_id (concept_id),
    KEY ix_payroll_concept_rates_contract_type (contract_type),
    KEY ix_payroll_concept_rates_from_cycle (effective_from_cycle_id),
    KEY ix_payroll_concept_rates_to_cycle (effective_to_cycle_id),
    CONSTRAINT fk_payroll_concept_rates_concept
        FOREIGN KEY (concept_id) REFERENCES payroll_concepts (id),
    CONSTRAINT fk_payroll_concept_rates_from_cycle
        FOREIGN KEY (effective_from_cycle_id) REFERENCES payroll_cycles (id),
    CONSTRAINT fk_payroll_concept_rates_to_cycle
        FOREIGN KEY (effective_to_cycle_id) REFERENCES payroll_cycles (id),
    CONSTRAINT fk_payroll_concept_rates_created_by
        FOREIGN KEY (created_by) REFERENCES payroll_users (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS payroll_manual_adjustments (
    id BIGINT NOT NULL AUTO_INCREMENT,
    cycle_id BIGINT NOT NULL,
    employee_id BIGINT NOT NULL,
    cost_center VARCHAR(32) NOT NULL,
    role_type VARCHAR(32) NOT NULL,
    adjustment_type VARCHAR(40) NOT NULL,
    adjustment_name VARCHAR(200) NOT NULL,
    adjustment_date DATE NULL,
    units DECIMAL(14,4) NULL,
    amount DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
    notes TEXT NULL,
    active TINYINT(1) NOT NULL DEFAULT 1,
    created_by BIGINT NULL,
    updated_by BIGINT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NULL,
    deleted_at DATETIME NULL,
    PRIMARY KEY (id),
    KEY ix_payroll_manual_adjustments_cycle_id (cycle_id),
    KEY ix_payroll_manual_adjustments_employee_id (employee_id),
    KEY ix_payroll_manual_adjustments_cost_center (cost_center),
    KEY ix_payroll_manual_adjustments_role_type (role_type),
    KEY ix_payroll_manual_adjustments_adjustment_type (adjustment_type),
    KEY ix_payroll_manual_adjustments_active (active),
    CONSTRAINT fk_payroll_manual_adjustments_cycle
        FOREIGN KEY (cycle_id) REFERENCES payroll_cycles (id),
    CONSTRAINT fk_payroll_manual_adjustments_employee
        FOREIGN KEY (employee_id) REFERENCES payroll_employees (id),
    CONSTRAINT fk_payroll_manual_adjustments_created_by
        FOREIGN KEY (created_by) REFERENCES payroll_users (id),
    CONSTRAINT fk_payroll_manual_adjustments_updated_by
        FOREIGN KEY (updated_by) REFERENCES payroll_users (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS payroll_cell_overrides (
    id BIGINT NOT NULL AUTO_INCREMENT,
    cycle_id BIGINT NOT NULL,
    employee_id BIGINT NOT NULL,
    concept_id BIGINT NOT NULL,
    cost_center VARCHAR(32) NOT NULL,
    role_type VARCHAR(32) NOT NULL,
    work_date DATE NOT NULL,
    override_value DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
    created_by BIGINT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NULL,
    PRIMARY KEY (id),
    KEY ix_payroll_cell_overrides_cycle_id (cycle_id),
    KEY ix_payroll_cell_overrides_employee_id (employee_id),
    KEY ix_payroll_cell_overrides_concept_id (concept_id),
    KEY ix_payroll_cell_overrides_cost_center (cost_center),
    KEY ix_payroll_cell_overrides_role_type (role_type),
    KEY ix_payroll_cell_overrides_work_date (work_date),
    CONSTRAINT fk_payroll_cell_overrides_cycle
        FOREIGN KEY (cycle_id) REFERENCES payroll_cycles (id),
    CONSTRAINT fk_payroll_cell_overrides_employee
        FOREIGN KEY (employee_id) REFERENCES payroll_employees (id),
    CONSTRAINT fk_payroll_cell_overrides_concept
        FOREIGN KEY (concept_id) REFERENCES payroll_concepts (id),
    CONSTRAINT fk_payroll_cell_overrides_created_by
        FOREIGN KEY (created_by) REFERENCES payroll_users (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS payroll_audit_log (
    id BIGINT NOT NULL AUTO_INCREMENT,
    user_id BIGINT NULL,
    action_type VARCHAR(50) NOT NULL,
    table_name VARCHAR(100) NOT NULL,
    record_id INT NOT NULL,
    field_name VARCHAR(100) NULL,
    old_value TEXT NULL,
    new_value TEXT NULL,
    action_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY ix_payroll_audit_log_user_id (user_id),
    KEY ix_payroll_audit_log_table_name (table_name),
    KEY ix_payroll_audit_log_record_id (record_id),
    CONSTRAINT fk_payroll_audit_log_user
        FOREIGN KEY (user_id) REFERENCES payroll_users (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS payroll_export_logs (
    id BIGINT NOT NULL AUTO_INCREMENT,
    user_id BIGINT NULL,
    export_scope VARCHAR(32) NOT NULL,
    file_format VARCHAR(16) NOT NULL,
    cycle_id BIGINT NOT NULL,
    employee_id BIGINT NOT NULL,
    cost_center VARCHAR(32) NULL,
    role_type VARCHAR(32) NULL,
    file_name VARCHAR(255) NOT NULL,
    exported_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY ix_payroll_export_logs_user_id (user_id),
    KEY ix_payroll_export_logs_cycle_id (cycle_id),
    KEY ix_payroll_export_logs_employee_id (employee_id),
    KEY ix_payroll_export_logs_cost_center (cost_center),
    KEY ix_payroll_export_logs_role_type (role_type),
    CONSTRAINT fk_payroll_export_logs_user
        FOREIGN KEY (user_id) REFERENCES payroll_users (id),
    CONSTRAINT fk_payroll_export_logs_cycle
        FOREIGN KEY (cycle_id) REFERENCES payroll_cycles (id),
    CONSTRAINT fk_payroll_export_logs_employee
        FOREIGN KEY (employee_id) REFERENCES payroll_employees (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO payroll_permissions (permission_code, description) VALUES
    ('payroll.read', 'Consultar liquidaciones'),
    ('payroll.export', 'Exportar liquidaciones'),
    ('payroll.import', 'Importar archivos operacionales'),
    ('payroll.edit', 'Editar produccion diaria'),
    ('users.manage', 'Administrar usuarios')
ON DUPLICATE KEY UPDATE description = VALUES(description);

INSERT INTO payroll_roles (role_name, description, active) VALUES
    ('ADMIN', 'Perfil ADMIN', 1),
    ('USER', 'Perfil USER', 1)
ON DUPLICATE KEY UPDATE description = VALUES(description), active = VALUES(active);

INSERT IGNORE INTO payroll_role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM payroll_roles r
JOIN payroll_permissions p
  ON r.role_name = 'ADMIN'
 AND p.permission_code IN (
     'payroll.read',
     'payroll.export',
     'payroll.import',
     'payroll.edit',
     'users.manage'
 );

INSERT IGNORE INTO payroll_role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM payroll_roles r
JOIN payroll_permissions p
  ON r.role_name = 'USER'
 AND p.permission_code IN ('payroll.read', 'payroll.export');
