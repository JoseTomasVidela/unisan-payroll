-- Homologa Bono Vacaciones y Vacaciones al codigo Softland H040.
-- Es idempotente y puede ejecutarse mas de una vez.

START TRANSACTION;

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

COMMIT;

SELECT mapping_type, mapping_key, source_label, softland_code, active
FROM payroll_softland_concept_mappings
WHERE mapping_type = 'ADJUSTMENT'
  AND mapping_key IN ('VACATION_BONUS', 'VACATION')
ORDER BY mapping_key;
