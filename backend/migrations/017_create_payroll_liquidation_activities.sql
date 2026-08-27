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
    CONSTRAINT fk_payroll_liquidation_activities_cycle FOREIGN KEY (cycle_id) REFERENCES payroll_cycles (id),
    CONSTRAINT fk_payroll_liquidation_activities_employee FOREIGN KEY (employee_id) REFERENCES payroll_employees (id),
    CONSTRAINT fk_payroll_liquidation_activities_concept FOREIGN KEY (concept_id) REFERENCES payroll_concepts (id),
    CONSTRAINT fk_payroll_liquidation_activities_user FOREIGN KEY (created_by) REFERENCES payroll_users (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
