CREATE TABLE IF NOT EXISTS payroll_ipc_adjustments (
    id BIGINT NOT NULL AUTO_INCREMENT,
    percentage DECIMAL(8,4) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'DRAFT',
    snapshot_before LONGTEXT NULL,
    snapshot_after LONGTEXT NULL,
    created_by BIGINT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NULL,
    applied_at DATETIME NULL,
    PRIMARY KEY (id),
    KEY ix_payroll_ipc_adjustments_status (status),
    CONSTRAINT fk_payroll_ipc_adjustments_created_by
        FOREIGN KEY (created_by) REFERENCES payroll_users (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SELECT id, percentage, status, created_at, applied_at
FROM payroll_ipc_adjustments
ORDER BY id DESC;
