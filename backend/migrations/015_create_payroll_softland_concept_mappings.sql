-- Actualizacion final Azure MySQL para la integracion Payroll -> Softland.
-- Es idempotente: se puede ejecutar mas de una vez sin duplicar registros.
-- Antes de ejecutarlo, seleccionar unisan_db como base activa en DBeaver.

CREATE TABLE IF NOT EXISTS payroll_softland_codes (
    softland_code VARCHAR(16) NOT NULL,
    concept_name VARCHAR(200) NOT NULL,
    active TINYINT(1) NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NULL,
    PRIMARY KEY (softland_code)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS payroll_softland_concept_mappings (
    id BIGINT NOT NULL AUTO_INCREMENT,
    concept_id BIGINT NULL,
    mapping_type VARCHAR(20) NOT NULL,
    mapping_key VARCHAR(160) NOT NULL,
    source_label VARCHAR(200) NOT NULL,
    softland_code VARCHAR(16) NOT NULL,
    active TINYINT(1) NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uq_payroll_softland_mapping_key (mapping_type, mapping_key),
    UNIQUE KEY uq_payroll_softland_mapping_concept (concept_id),
    KEY ix_payroll_softland_mapping_type (mapping_type),
    KEY ix_payroll_softland_mapping_code (softland_code),
    CONSTRAINT fk_payroll_softland_mapping_concept
        FOREIGN KEY (concept_id)
        REFERENCES payroll_concepts (id),
    CONSTRAINT fk_payroll_softland_mapping_code
        FOREIGN KEY (softland_code)
        REFERENCES payroll_softland_codes (softland_code)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci;

START TRANSACTION;

INSERT INTO payroll_softland_codes (
    softland_code,
    concept_name,
    active,
    created_at,
    updated_at
)
VALUES
    ('H005', 'SEMANA CORRIDA', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('H008', 'BONO RENDIMIENTO', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('H022', 'UNIBOX', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('H040', 'VACACIONES', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON DUPLICATE KEY UPDATE
    concept_name = VALUES(concept_name),
    active = VALUES(active),
    updated_at = CURRENT_TIMESTAMP;

-- Homologar todos los conceptos operacionales registrados en payroll_concepts.
INSERT INTO payroll_softland_concept_mappings (
    concept_id,
    mapping_type,
    mapping_key,
    source_label,
    softland_code,
    active,
    created_at,
    updated_at
)
SELECT
    concept.id,
    'CONCEPT',
    CONCAT(
        concept.source_type,
        '|',
        concept.cost_center,
        '|',
        concept.role_type,
        '|',
        concept.concept_code
    ),
    CASE
        WHEN concept.source_type = 'DR'
             AND concept.role_type = 'ASSISTANT'
            THEN CONCAT('Aux ', concept.concept_name)
        WHEN concept.source_type = 'SERVICES'
             AND concept.role_type = 'DRIVER'
            THEN CONCAT('Servicio Chofer ', concept.concept_name)
        WHEN concept.source_type = 'SERVICES'
             AND concept.role_type = 'ASSISTANT'
            THEN CONCAT('Servicio Aux ', concept.concept_name)
        ELSE concept.concept_name
    END,
    CASE
        WHEN concept.concept_code IN (
            'EVENT',
            'WATER_POINT',
            'LARGE_TRASH_BIN',
            'SMALL_TRASH_BIN',
            'FOSA'
        ) THEN 'H022'
        ELSE 'H008'
    END,
    1,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
FROM payroll_concepts AS concept
ON DUPLICATE KEY UPDATE
    concept_id = VALUES(concept_id),
    mapping_type = VALUES(mapping_type),
    mapping_key = VALUES(mapping_key),
    source_label = VALUES(source_label),
    softland_code = VALUES(softland_code),
    active = VALUES(active),
    updated_at = CURRENT_TIMESTAMP;

-- Conceptos calculados y ajustes que no tienen concept_id.
-- BONUS se conserva para poder exportar registros historicos ya guardados.
INSERT INTO payroll_softland_concept_mappings (
    concept_id,
    mapping_type,
    mapping_key,
    source_label,
    softland_code,
    active,
    created_at,
    updated_at
)
VALUES
    (
        NULL,
        'CALCULATED',
        'WEEK_CORRIDA',
        'SEMANA CORRIDA',
        'H005',
        1,
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP
    ),
    (
        NULL,
        'ADJUSTMENT',
        'OUT_OF_PRODUCTION_BONUS',
        'Bono fuera de produccion',
        'H008',
        1,
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP
    ),
    (
        NULL,
        'ADJUSTMENT',
        'BONUS',
        'Bono historico',
        'H008',
        1,
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP
    ),
    (
        NULL,
        'ADJUSTMENT',
        'VACATION_BONUS',
        'Bono Vacaciones',
        'H008',
        1,
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP
    ),
    (
        NULL,
        'ADJUSTMENT',
        'PRODUCTION_BONUS',
        'Bono Produccion',
        'H008',
        1,
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP
    ),
    (
        NULL,
        'ADJUSTMENT',
        'EVENT_BONUS',
        'Bono Evento',
        'H022',
        1,
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP
    ),
    (
        NULL,
        'ADJUSTMENT',
        'VACATION',
        'VACACIONES',
        'H040',
        1,
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP
    )
ON DUPLICATE KEY UPDATE
    source_label = VALUES(source_label),
    softland_code = VALUES(softland_code),
    active = VALUES(active),
    updated_at = CURRENT_TIMESTAMP;

COMMIT;

-- Verificacion de las tablas creadas.
SHOW TABLES LIKE 'payroll_softland_codes';
SHOW TABLES LIKE 'payroll_softland_concept_mappings';

-- Verificacion del catalogo Softland.
SELECT
    softland_code,
    concept_name,
    active
FROM payroll_softland_codes
ORDER BY softland_code;

-- Verificacion de las homologaciones cargadas.
SELECT
    mapping_type,
    mapping_key,
    source_label,
    softland_code,
    active
FROM payroll_softland_concept_mappings
ORDER BY
    FIELD(softland_code, 'H005', 'H008', 'H022', 'H040'),
    mapping_type,
    mapping_key;

-- El resultado esperado de esta consulta es 0.
SELECT COUNT(*) AS active_concepts_without_softland_mapping
FROM payroll_concepts AS concept
LEFT JOIN payroll_softland_concept_mappings AS mapping
    ON mapping.concept_id = concept.id
   AND mapping.mapping_type = 'CONCEPT'
   AND mapping.active = 1
WHERE concept.active = 1
  AND mapping.id IS NULL;
