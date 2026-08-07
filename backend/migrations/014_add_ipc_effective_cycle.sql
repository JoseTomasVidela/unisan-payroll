ALTER TABLE payroll_ipc_adjustments
    ADD COLUMN IF NOT EXISTS effective_from_cycle_id BIGINT NULL AFTER percentage;

UPDATE payroll_ipc_adjustments
SET effective_from_cycle_id = (
    SELECT id FROM payroll_cycles ORDER BY start_date ASC, id ASC LIMIT 1
)
WHERE effective_from_cycle_id IS NULL;

ALTER TABLE payroll_ipc_adjustments
    MODIFY effective_from_cycle_id BIGINT NOT NULL;

ALTER TABLE payroll_ipc_adjustments
    ADD INDEX ix_payroll_ipc_adjustments_cycle (effective_from_cycle_id),
    ADD CONSTRAINT fk_payroll_ipc_adjustments_cycle
        FOREIGN KEY (effective_from_cycle_id) REFERENCES payroll_cycles (id);

SELECT id, percentage, effective_from_cycle_id, status, created_at, applied_at
FROM payroll_ipc_adjustments
ORDER BY id DESC;
