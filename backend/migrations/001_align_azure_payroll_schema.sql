-- UNISAN Payroll - Azure MySQL schema alignment
-- Target: MySQL 8 / schema unisan_db
-- Execution: manual review and execution in DBeaver
--
-- Guarantees:
-- - Does not use Base.metadata.create_all.
-- - Does not drop tables, columns, or data.
-- - Does not add UNIQUE constraints to payroll_records.
-- - Keeps retrieval_flag and septic_tank_flag as reserved DECIMAL(14,4) columns.
--
-- Important:
-- MySQL DDL performs implicit commits. Take a schema backup before execution.

USE unisan_db;

DELIMITER $$

DROP PROCEDURE IF EXISTS payroll_align_schema$$
CREATE PROCEDURE payroll_align_schema()
BEGIN
    DECLARE v_count BIGINT DEFAULT 0;
    DECLARE v_invalid BIGINT DEFAULT 0;

    IF DATABASE() <> 'unisan_db' THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Migration aborted: active schema must be unisan_db';
    END IF;

    -- Required base tables must already exist. This migration only creates the
    -- two authorization tables that are currently absent from Azure.
    SELECT COUNT(*) INTO v_count
    FROM information_schema.tables
    WHERE table_schema = DATABASE()
      AND table_name IN (
          'payroll_audit_log',
          'payroll_concept_rates',
          'payroll_concepts',
          'payroll_roles',
          'payroll_users',
          'payroll_cycles',
          'payroll_employees',
          'payroll_export_logs',
          'payroll_imports',
          'payroll_manual_adjustments',
          'payroll_records'
      );

    IF v_count <> 11 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Migration aborted: required payroll base tables are missing';
    END IF;

    -- Complete every data-dependent preflight before the first DDL statement.
    SELECT COUNT(*) INTO v_invalid
    FROM payroll_roles
    WHERE CHAR_LENGTH(role_name) > 32;
    IF v_invalid > 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Migration aborted: payroll_roles.role_name exceeds 32 characters';
    END IF;

    SELECT COUNT(*) INTO v_invalid
    FROM payroll_users
    WHERE CHAR_LENGTH(username) > 80;
    IF v_invalid > 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Migration aborted: payroll_users.username exceeds 80 characters';
    END IF;

    SELECT COUNT(*) INTO v_invalid
    FROM payroll_employees
    WHERE CHAR_LENGTH(employee_name) > 180;
    IF v_invalid > 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Migration aborted: payroll_employees.employee_name exceeds 180 characters';
    END IF;

    SELECT COUNT(*) INTO v_invalid
    FROM payroll_records
    WHERE CHAR_LENGTH(source_employee_name) > 180;
    IF v_invalid > 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Migration aborted: payroll_records.source_employee_name exceeds 180 characters';
    END IF;

    SELECT COUNT(*) INTO v_invalid
    FROM payroll_users
    WHERE password_hash IS NULL OR TRIM(password_hash) = '';
    IF v_invalid > 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Migration aborted: payroll_users contains empty password_hash values';
    END IF;

    SELECT COUNT(*) INTO v_invalid
    FROM payroll_records
    WHERE source_employee_name IS NULL
       OR source_row_number IS NULL
       OR source_row_hash IS NULL
       OR source_person_slot IS NULL;
    IF v_invalid > 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Migration aborted: payroll_records contains NULL source identity fields';
    END IF;

    SELECT COUNT(*) INTO v_count
    FROM information_schema.columns
    WHERE table_schema = DATABASE()
      AND table_name = 'payroll_imports'
      AND column_name = 'imported_by'
      AND data_type IN ('varchar', 'char', 'text', 'tinytext', 'mediumtext', 'longtext');
    IF v_count > 0 THEN
        SELECT COUNT(*) INTO v_invalid
        FROM payroll_imports i
        LEFT JOIN payroll_users u
          ON u.username = i.imported_by
        WHERE i.imported_by IS NULL
           OR TRIM(i.imported_by) = ''
           OR u.id IS NULL;
        IF v_invalid > 0 THEN
            SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Migration aborted: payroll_imports.imported_by has values not mapped to payroll_users.username';
        END IF;
    END IF;

    CREATE TABLE IF NOT EXISTS payroll_permissions (
        id BIGINT NOT NULL AUTO_INCREMENT,
        permission_code VARCHAR(64) NOT NULL,
        description VARCHAR(255) NOT NULL,
        PRIMARY KEY (id),
        UNIQUE KEY uk_payroll_permissions_code (permission_code)
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

    -- payroll_roles: columns required by backend Role model.
    SELECT COUNT(*) INTO v_count
    FROM information_schema.columns
    WHERE table_schema = DATABASE()
      AND table_name = 'payroll_roles'
      AND column_name = 'description';
    IF v_count = 0 THEN
        ALTER TABLE payroll_roles
            ADD COLUMN description VARCHAR(255) NULL AFTER role_name;
    END IF;

    SELECT COUNT(*) INTO v_count
    FROM information_schema.columns
    WHERE table_schema = DATABASE()
      AND table_name = 'payroll_roles'
      AND column_name = 'active';
    IF v_count = 0 THEN
        ALTER TABLE payroll_roles
            ADD COLUMN active TINYINT(1) NOT NULL DEFAULT 1 AFTER description;
    END IF;

    UPDATE payroll_roles
    SET description = CONCAT('Perfil ', role_name)
    WHERE description IS NULL OR TRIM(description) = '';

    ALTER TABLE payroll_roles
        MODIFY COLUMN role_name VARCHAR(32) NOT NULL,
        MODIFY COLUMN description VARCHAR(255) NOT NULL,
        MODIFY COLUMN active TINYINT(1) NOT NULL DEFAULT 1;

    -- payroll_users: columns and nullability required by backend User model.
    SELECT COUNT(*) INTO v_count
    FROM information_schema.columns
    WHERE table_schema = DATABASE()
      AND table_name = 'payroll_users'
      AND column_name = 'full_name';
    IF v_count = 0 THEN
        ALTER TABLE payroll_users
            ADD COLUMN full_name VARCHAR(160) NULL AFTER username;
    END IF;

    SELECT COUNT(*) INTO v_count
    FROM information_schema.columns
    WHERE table_schema = DATABASE()
      AND table_name = 'payroll_users'
      AND column_name = 'last_login_at';
    IF v_count = 0 THEN
        ALTER TABLE payroll_users
            ADD COLUMN last_login_at DATETIME NULL AFTER created_at;
    END IF;

    UPDATE payroll_users
    SET full_name = username
    WHERE full_name IS NULL OR TRIM(full_name) = '';

    ALTER TABLE payroll_users
        MODIFY COLUMN username VARCHAR(80) NOT NULL,
        MODIFY COLUMN full_name VARCHAR(160) NOT NULL,
        MODIFY COLUMN password_hash VARCHAR(255) NOT NULL,
        MODIFY COLUMN active TINYINT(1) NOT NULL DEFAULT 1,
        MODIFY COLUMN created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        MODIFY COLUMN last_login_at DATETIME NULL;

    -- payroll_imports.imported_by changes from username text to payroll_users.id.
    SELECT COUNT(*) INTO v_count
    FROM information_schema.columns
    WHERE table_schema = DATABASE()
      AND table_name = 'payroll_imports'
      AND column_name = 'imported_by'
      AND data_type IN ('varchar', 'char', 'text', 'tinytext', 'mediumtext', 'longtext');
    IF v_count > 0 THEN
        SELECT COUNT(*) INTO v_count
        FROM information_schema.columns
        WHERE table_schema = DATABASE()
          AND table_name = 'payroll_imports'
          AND column_name = 'imported_by_user_id';
        IF v_count = 0 THEN
            ALTER TABLE payroll_imports
                ADD COLUMN imported_by_user_id BIGINT NULL AFTER file_name;
        END IF;

        UPDATE payroll_imports i
        JOIN payroll_users u ON u.username = i.imported_by
        SET i.imported_by_user_id = u.id;

        ALTER TABLE payroll_imports
            MODIFY COLUMN imported_by VARCHAR(100) NULL;

        ALTER TABLE payroll_imports
            CHANGE COLUMN imported_by imported_by_legacy VARCHAR(100) NULL,
            CHANGE COLUMN imported_by_user_id imported_by BIGINT NOT NULL;
    END IF;

    SELECT COUNT(*) INTO v_count
    FROM information_schema.key_column_usage
    WHERE table_schema = DATABASE()
      AND table_name = 'payroll_imports'
      AND column_name = 'imported_by'
      AND referenced_table_name = 'payroll_users'
      AND referenced_column_name = 'id';
    IF v_count = 0 THEN
        ALTER TABLE payroll_imports
            ADD CONSTRAINT fk_payroll_imports_user
            FOREIGN KEY (imported_by) REFERENCES payroll_users (id);
    END IF;

    -- Keep the legacy username column when a text-to-FK conversion occurred.
    -- It is retained for audit/reconciliation and may be removed only in a later,
    -- separately approved migration.

    -- Concepts are ordered from the database, never hardcoded in frontend/backend.
    SELECT COUNT(*) INTO v_count
    FROM information_schema.columns
    WHERE table_schema = DATABASE()
      AND table_name = 'payroll_concepts'
      AND column_name = 'db_field';
    IF v_count = 0 THEN
        ALTER TABLE payroll_concepts
            ADD COLUMN db_field VARCHAR(64) NULL AFTER concept_name;
    END IF;

    SELECT COUNT(*) INTO v_invalid
    FROM payroll_concepts
    WHERE db_field IS NULL OR TRIM(db_field) = '';
    IF v_invalid > 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Migration aborted: payroll_concepts.db_field must be populated';
    END IF;

    ALTER TABLE payroll_concepts
        MODIFY COLUMN db_field VARCHAR(64) NOT NULL;

    SELECT COUNT(*) INTO v_count
    FROM information_schema.columns
    WHERE table_schema = DATABASE()
      AND table_name = 'payroll_concepts'
      AND column_name = 'display_order';
    IF v_count = 0 THEN
        ALTER TABLE payroll_concepts
            ADD COLUMN display_order INT NOT NULL DEFAULT 0 AFTER role_type;
    END IF;

    -- Historical concept-rate versioning. Nullable columns permit controlled
    -- backfill of legacy rates before making them mandatory in a later migration.
    SELECT COUNT(*) INTO v_count FROM information_schema.columns
    WHERE table_schema = DATABASE() AND table_name = 'payroll_concept_rates'
      AND column_name = 'effective_from_cycle_id';
    IF v_count = 0 THEN
        ALTER TABLE payroll_concept_rates
            ADD COLUMN effective_from_cycle_id BIGINT NULL AFTER amount;
    END IF;

    SELECT COUNT(*) INTO v_count FROM information_schema.columns
    WHERE table_schema = DATABASE() AND table_name = 'payroll_concept_rates'
      AND column_name = 'effective_to_cycle_id';
    IF v_count = 0 THEN
        ALTER TABLE payroll_concept_rates
            ADD COLUMN effective_to_cycle_id BIGINT NULL AFTER effective_from_cycle_id;
    END IF;

    SELECT COUNT(*) INTO v_count FROM information_schema.columns
    WHERE table_schema = DATABASE() AND table_name = 'payroll_concept_rates'
      AND column_name = 'created_by';
    IF v_count = 0 THEN
        ALTER TABLE payroll_concept_rates
            ADD COLUMN created_by BIGINT NULL AFTER effective_to_cycle_id;
    END IF;

    SELECT COUNT(*) INTO v_count FROM information_schema.columns
    WHERE table_schema = DATABASE() AND table_name = 'payroll_concept_rates'
      AND column_name = 'updated_at';
    IF v_count = 0 THEN
        ALTER TABLE payroll_concept_rates
            ADD COLUMN updated_at DATETIME NULL AFTER created_at;
    END IF;

    ALTER TABLE payroll_concept_rates
        MODIFY COLUMN amount DECIMAL(14,4) NOT NULL;

    SELECT COUNT(*) INTO v_count FROM information_schema.key_column_usage
    WHERE table_schema = DATABASE() AND table_name = 'payroll_concept_rates'
      AND column_name = 'effective_from_cycle_id'
      AND referenced_table_name = 'payroll_cycles';
    IF v_count = 0 THEN
        ALTER TABLE payroll_concept_rates
            ADD CONSTRAINT fk_payroll_rates_from_cycle
            FOREIGN KEY (effective_from_cycle_id) REFERENCES payroll_cycles (id);
    END IF;

    SELECT COUNT(*) INTO v_count FROM information_schema.key_column_usage
    WHERE table_schema = DATABASE() AND table_name = 'payroll_concept_rates'
      AND column_name = 'effective_to_cycle_id'
      AND referenced_table_name = 'payroll_cycles';
    IF v_count = 0 THEN
        ALTER TABLE payroll_concept_rates
            ADD CONSTRAINT fk_payroll_rates_to_cycle
            FOREIGN KEY (effective_to_cycle_id) REFERENCES payroll_cycles (id);
    END IF;

    SELECT COUNT(*) INTO v_count FROM information_schema.key_column_usage
    WHERE table_schema = DATABASE() AND table_name = 'payroll_concept_rates'
      AND column_name = 'created_by'
      AND referenced_table_name = 'payroll_users';
    IF v_count = 0 THEN
        ALTER TABLE payroll_concept_rates
            ADD CONSTRAINT fk_payroll_rates_created_by
            FOREIGN KEY (created_by) REFERENCES payroll_users (id);
    END IF;

    ALTER TABLE payroll_manual_adjustments
        MODIFY COLUMN units DECIMAL(14,4) NULL,
        MODIFY COLUMN amount DECIMAL(14,4) NOT NULL DEFAULT 0.0000;

    -- All production quantities use DECIMAL(14,4). Reserved columns remain
    -- present but are not used by import or calculation code.
    ALTER TABLE payroll_records
        MODIFY COLUMN dispatch_flag DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
        MODIFY COLUMN retrieval_flag DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
        MODIFY COLUMN cleaning_flag DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
        MODIFY COLUMN drying_flag DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
        MODIFY COLUMN event_flag DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
        MODIFY COLUMN fair_week_1_flag DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
        MODIFY COLUMN fair_week_2_flag DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
        MODIFY COLUMN outside_radius_flag DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
        MODIFY COLUMN water_point_flag DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
        MODIFY COLUMN septic_tank_flag DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
        MODIFY COLUMN kit_delivery_flag DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
        MODIFY COLUMN lavatory_load_flag DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
        MODIFY COLUMN riles_suction_flag DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
        MODIFY COLUMN entry_before_1930_qty DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
        MODIFY COLUMN entry_before_0730_qty DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
        MODIFY COLUMN exit_after_1930_qty DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
        MODIFY COLUMN outside_radius_v_region_qty DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
        MODIFY COLUMN saturday_week_1_qty DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
        MODIFY COLUMN sunday_week_1_qty DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
        MODIFY COLUMN saturday_week_2_qty DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
        MODIFY COLUMN sunday_week_2_qty DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
        MODIFY COLUMN client_trips_qty DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
        MODIFY COLUMN saturday_after_1600_qty DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
        MODIFY COLUMN sunday_after_1600_qty DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
        MODIFY COLUMN weekend_cleaning_qty DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
        MODIFY COLUMN weekend_drying_qty DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
        MODIFY COLUMN large_trash_bin_qty DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
        MODIFY COLUMN small_trash_bin_qty DECIMAL(14,4) NOT NULL DEFAULT 0.0000,
        MODIFY COLUMN fosa_qty DECIMAL(14,4) NOT NULL DEFAULT 0.0000;

    ALTER TABLE payroll_records
        MODIFY COLUMN source_employee_name VARCHAR(180) NOT NULL,
        MODIFY COLUMN source_row_number INT NOT NULL,
        MODIFY COLUMN source_row_hash VARCHAR(64) NOT NULL,
        MODIFY COLUMN source_person_slot VARCHAR(32) NOT NULL,
        MODIFY COLUMN source_type VARCHAR(32) NOT NULL,
        MODIFY COLUMN cost_center VARCHAR(32) NOT NULL,
        MODIFY COLUMN role_type VARCHAR(32) NOT NULL,
        MODIFY COLUMN status VARCHAR(120) NULL;

    ALTER TABLE payroll_imports
        MODIFY COLUMN source_type VARCHAR(32) NOT NULL,
        MODIFY COLUMN cost_center VARCHAR(32) NOT NULL;

    ALTER TABLE payroll_employees
        MODIFY COLUMN employee_name VARCHAR(180) NOT NULL,
        MODIFY COLUMN role_type VARCHAR(32) NOT NULL;

    ALTER TABLE payroll_cycles
        MODIFY COLUMN cycle_name VARCHAR(120) NOT NULL;

    -- Seed only authorization metadata required by the backend. These operations
    -- are idempotent and do not remove custom role-permission assignments.
    INSERT INTO payroll_permissions (permission_code, description) VALUES
        ('payroll.read', 'Consultar liquidaciones'),
        ('payroll.export', 'Exportar liquidaciones'),
        ('payroll.import', 'Importar archivos operacionales'),
        ('payroll.edit', 'Editar produccion diaria'),
        ('users.manage', 'Administrar usuarios')
    ON DUPLICATE KEY UPDATE description = VALUES(description);

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
END$$

DELIMITER ;

-- Explicit execution point. Review the full procedure before running this line.
CALL payroll_align_schema();

-- Keep the procedure available only for this migration execution.
DROP PROCEDURE payroll_align_schema;

-- Post-migration verification report.
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'unisan_db'
  AND table_name LIKE 'payroll\_%'
ORDER BY table_name;

SELECT table_name, column_name, column_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_schema = 'unisan_db'
  AND table_name IN (
      'payroll_roles',
      'payroll_users',
      'payroll_imports',
      'payroll_records',
      'payroll_concepts',
      'payroll_concept_rates',
      'payroll_manual_adjustments'
  )
ORDER BY table_name, ordinal_position;

SELECT permission_code, description
FROM payroll_permissions
ORDER BY permission_code;

SELECT r.role_name, p.permission_code
FROM payroll_role_permissions rp
JOIN payroll_roles r ON r.id = rp.role_id
JOIN payroll_permissions p ON p.id = rp.permission_id
ORDER BY r.role_name, p.permission_code;
