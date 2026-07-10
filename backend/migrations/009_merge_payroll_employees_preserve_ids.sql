-- Merge de payroll_employees preservando IDs existentes.
-- No elimina filas. No toca payroll_cycles, payroll_records, payroll_imports ni tablas hijas.
SET NAMES utf8mb4;
USE unisan_db;

START TRANSACTION;

UPDATE payroll_employees
SET
    contract_type = COALESCE('NEW', contract_type),
    rut = COALESCE(NULL, rut),
    email = COALESCE(NULL, email),
    cargo = COALESCE(NULL, cargo),
    first_name = COALESCE(NULL, first_name),
    middle_name = COALESCE(NULL, middle_name),
    paternal_surname = COALESCE(NULL, paternal_surname),
    maternal_surname = COALESCE(NULL, maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Abel Tapia' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Abel Tapia', 'DRIVER', 'NEW', NULL, NULL, NULL,
    NULL, NULL, NULL, NULL
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Abel Tapia' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('23499257-0', rut),
    email = COALESCE('abraham.lucas.07@gmail.com', email),
    cargo = COALESCE('Chofer de Servicio y Despacho', cargo),
    first_name = COALESCE('Abraham', first_name),
    middle_name = COALESCE(NULL, middle_name),
    paternal_surname = COALESCE('Lucas', paternal_surname),
    maternal_surname = COALESCE('Lizete', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Abraham Lucas' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Abraham Lucas', 'UNASSIGNED', NULL, '23499257-0', 'abraham.lucas.07@gmail.com', 'Chofer de Servicio y Despacho',
    'Abraham', NULL, 'Lucas', 'Lizete'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Abraham Lucas' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('16428519-7', rut),
    email = COALESCE('alan.bravo.h@gmail.com', email),
    cargo = COALESCE('Chofer RS', cargo),
    first_name = COALESCE('Alan', first_name),
    middle_name = COALESCE('Omar', middle_name),
    paternal_surname = COALESCE('Bravo', paternal_surname),
    maternal_surname = COALESCE('Herrera', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Alan Bravo' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Alan Bravo', 'UNASSIGNED', NULL, '16428519-7', 'alan.bravo.h@gmail.com', 'Chofer RS',
    'Alan', 'Omar', 'Bravo', 'Herrera'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Alan Bravo' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('OLD', contract_type),
    rut = COALESCE(NULL, rut),
    email = COALESCE(NULL, email),
    cargo = COALESCE(NULL, cargo),
    first_name = COALESCE(NULL, first_name),
    middle_name = COALESCE(NULL, middle_name),
    paternal_surname = COALESCE(NULL, paternal_surname),
    maternal_surname = COALESCE(NULL, maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Albert Riveros' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Albert Riveros', 'DRIVER', 'OLD', NULL, NULL, NULL,
    NULL, NULL, NULL, NULL
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Albert Riveros' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('OLD', contract_type),
    rut = COALESCE(NULL, rut),
    email = COALESCE(NULL, email),
    cargo = COALESCE(NULL, cargo),
    first_name = COALESCE(NULL, first_name),
    middle_name = COALESCE(NULL, middle_name),
    paternal_surname = COALESCE(NULL, paternal_surname),
    maternal_surname = COALESCE(NULL, maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Alejandro Escoar' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Alejandro Escoar', 'ASSISTANT', 'OLD', NULL, NULL, NULL,
    NULL, NULL, NULL, NULL
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Alejandro Escoar' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('OLD', contract_type),
    rut = COALESCE('19546813-3', rut),
    email = COALESCE('ae5952575@gmail.com', email),
    cargo = COALESCE('auxiliar servicio', cargo),
    first_name = COALESCE('Alejandro', first_name),
    middle_name = COALESCE('Fabian', middle_name),
    paternal_surname = COALESCE('Escobar', paternal_surname),
    maternal_surname = COALESCE('Rojas', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Alejandro Escobar' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Alejandro Escobar', 'ASSISTANT', 'OLD', '19546813-3', 'ae5952575@gmail.com', 'auxiliar servicio',
    'Alejandro', 'Fabian', 'Escobar', 'Rojas'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Alejandro Escobar' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('OLD', contract_type),
    rut = COALESCE('17072087-3', rut),
    email = COALESCE('raocjpc@gmail.com', email),
    cargo = COALESCE('auxiliar servicio', cargo),
    first_name = COALESCE('Alejandro', first_name),
    middle_name = COALESCE('Enrique', middle_name),
    paternal_surname = COALESCE('Osorio', paternal_surname),
    maternal_surname = COALESCE('Gatica', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Alejandro Osorio' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Alejandro Osorio', 'ASSISTANT', 'OLD', '17072087-3', 'raocjpc@gmail.com', 'auxiliar servicio',
    'Alejandro', 'Enrique', 'Osorio', 'Gatica'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Alejandro Osorio' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('25912978-8', rut),
    email = COALESCE('chela2015fg@gmail.com', email),
    cargo = COALESCE('Asistente de Serv y Despac', cargo),
    first_name = COALESCE('Alexa', first_name),
    middle_name = COALESCE('Coromoto', middle_name),
    paternal_surname = COALESCE('Figueroa', paternal_surname),
    maternal_surname = COALESCE('Gonzalez', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Alexa Figueroa' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Alexa Figueroa', 'UNASSIGNED', NULL, '25912978-8', 'chela2015fg@gmail.com', 'Asistente de Serv y Despac',
    'Alexa', 'Coromoto', 'Figueroa', 'Gonzalez'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Alexa Figueroa' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('OLD', contract_type),
    rut = COALESCE('19165687-3', rut),
    email = COALESCE('aleyflorencia07@gmail.com', email),
    cargo = COALESCE('auxiliar servicio', cargo),
    first_name = COALESCE('Alexander', first_name),
    middle_name = COALESCE('Esteban', middle_name),
    paternal_surname = COALESCE('Marchant', paternal_surname),
    maternal_surname = COALESCE('Roldan', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Alexander Marchant' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Alexander Marchant', 'ASSISTANT', 'OLD', '19165687-3', 'aleyflorencia07@gmail.com', 'auxiliar servicio',
    'Alexander', 'Esteban', 'Marchant', 'Roldan'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Alexander Marchant' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('OLD', contract_type),
    rut = COALESCE('19165687-3', rut),
    email = COALESCE('aleyflorencia07@gmail.com', email),
    cargo = COALESCE('auxiliar servicio', cargo),
    first_name = COALESCE('Alexander', first_name),
    middle_name = COALESCE('Esteban', middle_name),
    paternal_surname = COALESCE('Marchant', paternal_surname),
    maternal_surname = COALESCE('Roldan', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Alexander Marchant' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Alexander Marchant', 'DRIVER', 'OLD', '19165687-3', 'aleyflorencia07@gmail.com', 'auxiliar servicio',
    'Alexander', 'Esteban', 'Marchant', 'Roldan'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Alexander Marchant' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('17655668-4', rut),
    email = COALESCE('alexis.carvajalg@gmail.com', email),
    cargo = COALESCE('Chofer Servicio', cargo),
    first_name = COALESCE('Alexis', first_name),
    middle_name = COALESCE('Michael', middle_name),
    paternal_surname = COALESCE('Carvajal', paternal_surname),
    maternal_surname = COALESCE('Gajardo', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Alexis Carvajal' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Alexis Carvajal', 'UNASSIGNED', NULL, '17655668-4', 'alexis.carvajalg@gmail.com', 'Chofer Servicio',
    'Alexis', 'Michael', 'Carvajal', 'Gajardo'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Alexis Carvajal' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('NEW', contract_type),
    rut = COALESCE('17623103-3', rut),
    email = COALESCE('alfredocona28@gmail.com', email),
    cargo = COALESCE('Chofer Servicio', cargo),
    first_name = COALESCE('Alfredo', first_name),
    middle_name = COALESCE('Alejandro', middle_name),
    paternal_surname = COALESCE('Cona', paternal_surname),
    maternal_surname = COALESCE('Soto', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Alfredo Cona' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Alfredo Cona', 'ASSISTANT', 'NEW', '17623103-3', 'alfredocona28@gmail.com', 'Chofer Servicio',
    'Alfredo', 'Alejandro', 'Cona', 'Soto'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Alfredo Cona' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('NEW', contract_type),
    rut = COALESCE('17623103-3', rut),
    email = COALESCE('alfredocona28@gmail.com', email),
    cargo = COALESCE('Chofer Servicio', cargo),
    first_name = COALESCE('Alfredo', first_name),
    middle_name = COALESCE('Alejandro', middle_name),
    paternal_surname = COALESCE('Cona', paternal_surname),
    maternal_surname = COALESCE('Soto', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Alfredo Cona' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Alfredo Cona', 'DRIVER', 'NEW', '17623103-3', 'alfredocona28@gmail.com', 'Chofer Servicio',
    'Alfredo', 'Alejandro', 'Cona', 'Soto'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Alfredo Cona' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('15424797-1', rut),
    email = COALESCE('granizooo234@gmail.com', email),
    cargo = COALESCE('Auxiliar Despacho', cargo),
    first_name = COALESCE('Andres', first_name),
    middle_name = COALESCE('Cristian', middle_name),
    paternal_surname = COALESCE('Moya', paternal_surname),
    maternal_surname = COALESCE('Gonzalez', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Andres Moya' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Andres Moya', 'ASSISTANT', NULL, '15424797-1', 'granizooo234@gmail.com', 'Auxiliar Despacho',
    'Andres', 'Cristian', 'Moya', 'Gonzalez'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Andres Moya' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('15424797-1', rut),
    email = COALESCE('granizooo234@gmail.com', email),
    cargo = COALESCE('Auxiliar Despacho', cargo),
    first_name = COALESCE('Andres', first_name),
    middle_name = COALESCE('Cristian', middle_name),
    paternal_surname = COALESCE('Moya', paternal_surname),
    maternal_surname = COALESCE('Gonzalez', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Andres Moya' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Andres Moya', 'DRIVER', NULL, '15424797-1', 'granizooo234@gmail.com', 'Auxiliar Despacho',
    'Andres', 'Cristian', 'Moya', 'Gonzalez'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Andres Moya' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('17069748-0', rut),
    email = COALESCE('angeloty125@gmail.com', email),
    cargo = COALESCE('Chofer RS', cargo),
    first_name = COALESCE('Angelo', first_name),
    middle_name = COALESCE('Ariel', middle_name),
    paternal_surname = COALESCE('Rivera', paternal_surname),
    maternal_surname = COALESCE('Rojas', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Angelo Rivera' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Angelo Rivera', 'UNASSIGNED', NULL, '17069748-0', 'angeloty125@gmail.com', 'Chofer RS',
    'Angelo', 'Ariel', 'Rivera', 'Rojas'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Angelo Rivera' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('10605996-9', rut),
    email = COALESCE('008antoniopalma@gmail.com', email),
    cargo = COALESCE('auxiliar servicio', cargo),
    first_name = COALESCE('Antonio', first_name),
    middle_name = COALESCE('Enrique', middle_name),
    paternal_surname = COALESCE('Palma', paternal_surname),
    maternal_surname = COALESCE('Gomez', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Antonio Palma' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Antonio Palma', 'ASSISTANT', NULL, '10605996-9', '008antoniopalma@gmail.com', 'auxiliar servicio',
    'Antonio', 'Enrique', 'Palma', 'Gomez'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Antonio Palma' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('16802037-6', rut),
    email = COALESCE('mauricio.riquelme08@gmail.com', email),
    cargo = COALESCE('Chofer RS', cargo),
    first_name = COALESCE('Antonio', first_name),
    middle_name = COALESCE('Ernesto', middle_name),
    paternal_surname = COALESCE('Riquelme', paternal_surname),
    maternal_surname = COALESCE('Astorga', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Antonio Riquelme' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Antonio Riquelme', 'ASSISTANT', NULL, '16802037-6', 'mauricio.riquelme08@gmail.com', 'Chofer RS',
    'Antonio', 'Ernesto', 'Riquelme', 'Astorga'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Antonio Riquelme' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('16802037-6', rut),
    email = COALESCE('mauricio.riquelme08@gmail.com', email),
    cargo = COALESCE('Chofer RS', cargo),
    first_name = COALESCE('Antonio', first_name),
    middle_name = COALESCE('Ernesto', middle_name),
    paternal_surname = COALESCE('Riquelme', paternal_surname),
    maternal_surname = COALESCE('Astorga', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Antonio Riquelme' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Antonio Riquelme', 'DRIVER', NULL, '16802037-6', 'mauricio.riquelme08@gmail.com', 'Chofer RS',
    'Antonio', 'Ernesto', 'Riquelme', 'Astorga'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Antonio Riquelme' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('OLD', contract_type),
    rut = COALESCE('12112657-5', rut),
    email = COALESCE('claudia.itu78@gmail.com', email),
    cargo = COALESCE('Chofer Servicio', cargo),
    first_name = COALESCE('Boris', first_name),
    middle_name = COALESCE('Hernan', middle_name),
    paternal_surname = COALESCE('Lopez', paternal_surname),
    maternal_surname = COALESCE('Alvarado', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Boris Lopez' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Boris Lopez', 'DRIVER', 'OLD', '12112657-5', 'claudia.itu78@gmail.com', 'Chofer Servicio',
    'Boris', 'Hernan', 'Lopez', 'Alvarado'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Boris Lopez' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('OLD', contract_type),
    rut = COALESCE('12112657-5', rut),
    email = COALESCE('claudia.itu78@gmail.com', email),
    cargo = COALESCE('Chofer Servicio', cargo),
    first_name = COALESCE('Boris', first_name),
    middle_name = COALESCE('Hernan', middle_name),
    paternal_surname = COALESCE('Lopez', paternal_surname),
    maternal_surname = COALESCE('Alvarado', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Boris López' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Boris López', 'ASSISTANT', 'OLD', '12112657-5', 'claudia.itu78@gmail.com', 'Chofer Servicio',
    'Boris', 'Hernan', 'Lopez', 'Alvarado'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Boris López' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('OLD', contract_type),
    rut = COALESCE('12112657-5', rut),
    email = COALESCE('claudia.itu78@gmail.com', email),
    cargo = COALESCE('Chofer Servicio', cargo),
    first_name = COALESCE('Boris', first_name),
    middle_name = COALESCE('Hernan', middle_name),
    paternal_surname = COALESCE('Lopez', paternal_surname),
    maternal_surname = COALESCE('Alvarado', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Boris López' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Boris López', 'DRIVER', 'OLD', '12112657-5', 'claudia.itu78@gmail.com', 'Chofer Servicio',
    'Boris', 'Hernan', 'Lopez', 'Alvarado'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Boris López' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('NEW', contract_type),
    rut = COALESCE('18838547-8', rut),
    email = COALESCE('jopsanandres@gmail.com', email),
    cargo = COALESCE('Chofer Servicio', cargo),
    first_name = COALESCE('Byron', first_name),
    middle_name = COALESCE('Andres', middle_name),
    paternal_surname = COALESCE('Lopez', paternal_surname),
    maternal_surname = COALESCE('Muñoz', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Byron Lopez' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Byron Lopez', 'DRIVER', 'NEW', '18838547-8', 'jopsanandres@gmail.com', 'Chofer Servicio',
    'Byron', 'Andres', 'Lopez', 'Muñoz'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Byron Lopez' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('NEW', contract_type),
    rut = COALESCE('18838547-8', rut),
    email = COALESCE('jopsanandres@gmail.com', email),
    cargo = COALESCE('Chofer Servicio', cargo),
    first_name = COALESCE('Byron', first_name),
    middle_name = COALESCE('Andres', middle_name),
    paternal_surname = COALESCE('Lopez', paternal_surname),
    maternal_surname = COALESCE('Muñoz', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Byron López' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Byron López', 'DRIVER', 'NEW', '18838547-8', 'jopsanandres@gmail.com', 'Chofer Servicio',
    'Byron', 'Andres', 'Lopez', 'Muñoz'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Byron López' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('NEW', contract_type),
    rut = COALESCE('20142692-8', rut),
    email = COALESCE('alexander9carlos@gmail.com', email),
    cargo = COALESCE('auxiliar servicio', cargo),
    first_name = COALESCE('Carlos', first_name),
    middle_name = COALESCE('Alexander', middle_name),
    paternal_surname = COALESCE('Correa', paternal_surname),
    maternal_surname = COALESCE('Chacana', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Carlos Correa' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Carlos Correa', 'ASSISTANT', 'NEW', '20142692-8', 'alexander9carlos@gmail.com', 'auxiliar servicio',
    'Carlos', 'Alexander', 'Correa', 'Chacana'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Carlos Correa' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('17092663-3', rut),
    email = COALESCE('car.jimenezgonzalez8@gmail.com', email),
    cargo = COALESCE('Chofer Servicio', cargo),
    first_name = COALESCE('Carlos', first_name),
    middle_name = COALESCE('Roberto', middle_name),
    paternal_surname = COALESCE('Jimenez', paternal_surname),
    maternal_surname = COALESCE('Gonzalez', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Carlos Jimenez' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Carlos Jimenez', 'UNASSIGNED', NULL, '17092663-3', 'car.jimenezgonzalez8@gmail.com', 'Chofer Servicio',
    'Carlos', 'Roberto', 'Jimenez', 'Gonzalez'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Carlos Jimenez' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('18947060-6', rut),
    email = COALESCE('carlosmaulen94@gmail.com', email),
    cargo = COALESCE('Chofer y Auxiliar', cargo),
    first_name = COALESCE('Carlos', first_name),
    middle_name = COALESCE('Hernan', middle_name),
    paternal_surname = COALESCE('Maulen', paternal_surname),
    maternal_surname = COALESCE('Cepeda', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Carlos Maulen' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Carlos Maulen', 'ASSISTANT', NULL, '18947060-6', 'carlosmaulen94@gmail.com', 'Chofer y Auxiliar',
    'Carlos', 'Hernan', 'Maulen', 'Cepeda'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Carlos Maulen' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('18947060-6', rut),
    email = COALESCE('carlosmaulen94@gmail.com', email),
    cargo = COALESCE('Chofer y Auxiliar', cargo),
    first_name = COALESCE('Carlos', first_name),
    middle_name = COALESCE('Hernan', middle_name),
    paternal_surname = COALESCE('Maulen', paternal_surname),
    maternal_surname = COALESCE('Cepeda', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Carlos Maulen' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Carlos Maulen', 'DRIVER', NULL, '18947060-6', 'carlosmaulen94@gmail.com', 'Chofer y Auxiliar',
    'Carlos', 'Hernan', 'Maulen', 'Cepeda'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Carlos Maulen' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('OLD', contract_type),
    rut = COALESCE('15334781-6', rut),
    email = COALESCE('cesarmorenor69@gmail.com', email),
    cargo = COALESCE('Chofer Servicio', cargo),
    first_name = COALESCE('Cesar', first_name),
    middle_name = COALESCE('Antonio', middle_name),
    paternal_surname = COALESCE('Moreno', paternal_surname),
    maternal_surname = COALESCE('Riveros', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Cesar Moreno' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Cesar Moreno', 'DRIVER', 'OLD', '15334781-6', 'cesarmorenor69@gmail.com', 'Chofer Servicio',
    'Cesar', 'Antonio', 'Moreno', 'Riveros'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Cesar Moreno' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('21023272-9', rut),
    email = COALESCE('christianarayarivas45692@gmail.com', email),
    cargo = COALESCE('auxiliar servicio', cargo),
    first_name = COALESCE('Christian', first_name),
    middle_name = COALESCE('Alejandro', middle_name),
    paternal_surname = COALESCE('Araya', paternal_surname),
    maternal_surname = COALESCE('Rivas', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Christian Araya' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Christian Araya', 'UNASSIGNED', NULL, '21023272-9', 'christianarayarivas45692@gmail.com', 'auxiliar servicio',
    'Christian', 'Alejandro', 'Araya', 'Rivas'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Christian Araya' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('15460715-3', rut),
    email = COALESCE('claudioarenas.a@gmail.com', email),
    cargo = COALESCE('Asistente de Serv y Despac', cargo),
    first_name = COALESCE('Claudio', first_name),
    middle_name = COALESCE('Antonio', middle_name),
    paternal_surname = COALESCE('Arenas', paternal_surname),
    maternal_surname = COALESCE('Arenas', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Claudio Arenas' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Claudio Arenas', 'UNASSIGNED', NULL, '15460715-3', 'claudioarenas.a@gmail.com', 'Asistente de Serv y Despac',
    'Claudio', 'Antonio', 'Arenas', 'Arenas'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Claudio Arenas' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('16850588-4', rut),
    email = COALESCE('cardenasclaudio051@gmail.com', email),
    cargo = COALESCE('Auxiliar de Patio', cargo),
    first_name = COALESCE('Claudio', first_name),
    middle_name = COALESCE('Edgardo', middle_name),
    paternal_surname = COALESCE('Cardenas', paternal_surname),
    maternal_surname = COALESCE('Cardenas', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Claudio Cardenas' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Claudio Cardenas', 'UNASSIGNED', NULL, '16850588-4', 'cardenasclaudio051@gmail.com', 'Auxiliar de Patio',
    'Claudio', 'Edgardo', 'Cardenas', 'Cardenas'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Claudio Cardenas' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE(NULL, rut),
    email = COALESCE(NULL, email),
    cargo = COALESCE(NULL, cargo),
    first_name = COALESCE(NULL, first_name),
    middle_name = COALESCE(NULL, middle_name),
    paternal_surname = COALESCE(NULL, paternal_surname),
    maternal_surname = COALESCE(NULL, maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Claudio Garrdo' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Claudio Garrdo', 'DRIVER', NULL, NULL, NULL, NULL,
    NULL, NULL, NULL, NULL
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Claudio Garrdo' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('12876513-1', rut),
    email = COALESCE('clauditocares7.0@gmail.com', email),
    cargo = COALESCE('Chofer y Auxiliar', cargo),
    first_name = COALESCE('Claudio', first_name),
    middle_name = COALESCE('Luis', middle_name),
    paternal_surname = COALESCE('Garrido', paternal_surname),
    maternal_surname = COALESCE('Cares', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Claudio Garrido' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Claudio Garrido', 'ASSISTANT', NULL, '12876513-1', 'clauditocares7.0@gmail.com', 'Chofer y Auxiliar',
    'Claudio', 'Luis', 'Garrido', 'Cares'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Claudio Garrido' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('12876513-1', rut),
    email = COALESCE('clauditocares7.0@gmail.com', email),
    cargo = COALESCE('Chofer y Auxiliar', cargo),
    first_name = COALESCE('Claudio', first_name),
    middle_name = COALESCE('Luis', middle_name),
    paternal_surname = COALESCE('Garrido', paternal_surname),
    maternal_surname = COALESCE('Cares', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Claudio Garrido' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Claudio Garrido', 'DRIVER', NULL, '12876513-1', 'clauditocares7.0@gmail.com', 'Chofer y Auxiliar',
    'Claudio', 'Luis', 'Garrido', 'Cares'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Claudio Garrido' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('OLD', contract_type),
    rut = COALESCE(NULL, rut),
    email = COALESCE(NULL, email),
    cargo = COALESCE(NULL, cargo),
    first_name = COALESCE(NULL, first_name),
    middle_name = COALESCE(NULL, middle_name),
    paternal_surname = COALESCE(NULL, paternal_surname),
    maternal_surname = COALESCE(NULL, maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Cristian Araya' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Cristian Araya', 'ASSISTANT', 'OLD', NULL, NULL, NULL,
    NULL, NULL, NULL, NULL
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Cristian Araya' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('OLD', contract_type),
    rut = COALESCE(NULL, rut),
    email = COALESCE(NULL, email),
    cargo = COALESCE(NULL, cargo),
    first_name = COALESCE(NULL, first_name),
    middle_name = COALESCE(NULL, middle_name),
    paternal_surname = COALESCE(NULL, paternal_surname),
    maternal_surname = COALESCE(NULL, maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Cristian Araya' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Cristian Araya', 'DRIVER', 'OLD', NULL, NULL, NULL,
    NULL, NULL, NULL, NULL
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Cristian Araya' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('12649756-3', rut),
    email = COALESCE('cristian.diazmedina17@gmail.com', email),
    cargo = COALESCE('Chofer de Unibox', cargo),
    first_name = COALESCE('Cristian', first_name),
    middle_name = COALESCE(NULL, middle_name),
    paternal_surname = COALESCE('Diaz', paternal_surname),
    maternal_surname = COALESCE('Medina', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Cristian Diaz' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Cristian Diaz', 'UNASSIGNED', NULL, '12649756-3', 'cristian.diazmedina17@gmail.com', 'Chofer de Unibox',
    'Cristian', NULL, 'Diaz', 'Medina'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Cristian Diaz' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('OLD', contract_type),
    rut = COALESCE('15424797-1', rut),
    email = COALESCE('granizooo234@gmail.com', email),
    cargo = COALESCE('Auxiliar Despacho', cargo),
    first_name = COALESCE('Cristian', first_name),
    middle_name = COALESCE('Fabian', middle_name),
    paternal_surname = COALESCE('Gonzalez', paternal_surname),
    maternal_surname = COALESCE('Rodriguez', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Cristian Gonzalez' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Cristian Gonzalez', 'ASSISTANT', 'OLD', '15424797-1', 'granizooo234@gmail.com', 'Auxiliar Despacho',
    'Cristian', 'Fabian', 'Gonzalez', 'Rodriguez'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Cristian Gonzalez' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('OLD', contract_type),
    rut = COALESCE('15424797-1', rut),
    email = COALESCE('granizooo234@gmail.com', email),
    cargo = COALESCE('Auxiliar Despacho', cargo),
    first_name = COALESCE('Cristian', first_name),
    middle_name = COALESCE('Fabian', middle_name),
    paternal_surname = COALESCE('Gonzalez', paternal_surname),
    maternal_surname = COALESCE('Rodriguez', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Cristian Gonzalez' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Cristian Gonzalez', 'DRIVER', 'OLD', '15424797-1', 'granizooo234@gmail.com', 'Auxiliar Despacho',
    'Cristian', 'Fabian', 'Gonzalez', 'Rodriguez'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Cristian Gonzalez' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('17337566-2', rut),
    email = COALESCE('loboscristian.16@gmail.com', email),
    cargo = COALESCE('Chofer de Unibox', cargo),
    first_name = COALESCE('Cristian', first_name),
    middle_name = COALESCE('Andres', middle_name),
    paternal_surname = COALESCE('Lobos', paternal_surname),
    maternal_surname = COALESCE('Valdes', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Cristian Lobos' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Cristian Lobos', 'UNASSIGNED', NULL, '17337566-2', 'loboscristian.16@gmail.com', 'Chofer de Unibox',
    'Cristian', 'Andres', 'Lobos', 'Valdes'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Cristian Lobos' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('13499219-0', rut),
    email = COALESCE('kristianvaldivia1978@gmail.com', email),
    cargo = COALESCE('Chofer Servicio', cargo),
    first_name = COALESCE('Cristian', first_name),
    middle_name = COALESCE('Andres', middle_name),
    paternal_surname = COALESCE('Valdivia', paternal_surname),
    maternal_surname = COALESCE('Zamorano', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Cristian Valdivia' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Cristian Valdivia', 'ASSISTANT', NULL, '13499219-0', 'kristianvaldivia1978@gmail.com', 'Chofer Servicio',
    'Cristian', 'Andres', 'Valdivia', 'Zamorano'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Cristian Valdivia' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('13499219-0', rut),
    email = COALESCE('kristianvaldivia1978@gmail.com', email),
    cargo = COALESCE('Chofer Servicio', cargo),
    first_name = COALESCE('Cristian', first_name),
    middle_name = COALESCE('Andres', middle_name),
    paternal_surname = COALESCE('Valdivia', paternal_surname),
    maternal_surname = COALESCE('Zamorano', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Cristian Valdivia' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Cristian Valdivia', 'DRIVER', NULL, '13499219-0', 'kristianvaldivia1978@gmail.com', 'Chofer Servicio',
    'Cristian', 'Andres', 'Valdivia', 'Zamorano'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Cristian Valdivia' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('21239566-8', rut),
    email = COALESCE('bobalabraham@gmail.com', email),
    cargo = COALESCE('Auxiliar Servicio Despacho', cargo),
    first_name = COALESCE('Cristobal', first_name),
    middle_name = COALESCE('Abraham', middle_name),
    paternal_surname = COALESCE('Ramos', paternal_surname),
    maternal_surname = COALESCE('Gallardo', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Cristobal Ramos' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Cristobal Ramos', 'UNASSIGNED', NULL, '21239566-8', 'bobalabraham@gmail.com', 'Auxiliar Servicio Despacho',
    'Cristobal', 'Abraham', 'Ramos', 'Gallardo'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Cristobal Ramos' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('18946469-K', rut),
    email = COALESCE('cristofertroncoso56@gmail.com', email),
    cargo = COALESCE('Chofer Servicio', cargo),
    first_name = COALESCE('Cristofer', first_name),
    middle_name = COALESCE('Angel', middle_name),
    paternal_surname = COALESCE('Troncoso', paternal_surname),
    maternal_surname = COALESCE('Catalan', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Cristofer Troncoso' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Cristofer Troncoso', 'UNASSIGNED', NULL, '18946469-K', 'cristofertroncoso56@gmail.com', 'Chofer Servicio',
    'Cristofer', 'Angel', 'Troncoso', 'Catalan'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Cristofer Troncoso' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('17109462-3', rut),
    email = COALESCE('cris.munoz1524@gmail.com', email),
    cargo = COALESCE('Chofer de Unibox', cargo),
    first_name = COALESCE('Cristopher', first_name),
    middle_name = COALESCE(NULL, middle_name),
    paternal_surname = COALESCE('Muñoz', paternal_surname),
    maternal_surname = COALESCE('Arevalo', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Cristopher Muñoz' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Cristopher Muñoz', 'UNASSIGNED', NULL, '17109462-3', 'cris.munoz1524@gmail.com', 'Chofer de Unibox',
    'Cristopher', NULL, 'Muñoz', 'Arevalo'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Cristopher Muñoz' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE(NULL, rut),
    email = COALESCE(NULL, email),
    cargo = COALESCE(NULL, cargo),
    first_name = COALESCE(NULL, first_name),
    middle_name = COALESCE(NULL, middle_name),
    paternal_surname = COALESCE(NULL, paternal_surname),
    maternal_surname = COALESCE(NULL, maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Daiel Diaz' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Daiel Diaz', 'DRIVER', NULL, NULL, NULL, NULL,
    NULL, NULL, NULL, NULL
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Daiel Diaz' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('NEW', contract_type),
    rut = COALESCE(NULL, rut),
    email = COALESCE(NULL, email),
    cargo = COALESCE(NULL, cargo),
    first_name = COALESCE(NULL, first_name),
    middle_name = COALESCE(NULL, middle_name),
    paternal_surname = COALESCE(NULL, paternal_surname),
    maternal_surname = COALESCE(NULL, maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Daniel Diaz' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Daniel Diaz', 'ASSISTANT', 'NEW', NULL, NULL, NULL,
    NULL, NULL, NULL, NULL
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Daniel Diaz' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('NEW', contract_type),
    rut = COALESCE(NULL, rut),
    email = COALESCE(NULL, email),
    cargo = COALESCE(NULL, cargo),
    first_name = COALESCE(NULL, first_name),
    middle_name = COALESCE(NULL, middle_name),
    paternal_surname = COALESCE(NULL, paternal_surname),
    maternal_surname = COALESCE(NULL, maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Daniel Diaz' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Daniel Diaz', 'DRIVER', 'NEW', NULL, NULL, NULL,
    NULL, NULL, NULL, NULL
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Daniel Diaz' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('NEW', contract_type),
    rut = COALESCE('18461720-K', rut),
    email = COALESCE('daniel.escobark03@gmail.com', email),
    cargo = COALESCE('Auxiliar Servicio Despacho', cargo),
    first_name = COALESCE('Daniel', first_name),
    middle_name = COALESCE('Ignacio', middle_name),
    paternal_surname = COALESCE('Escobar', paternal_surname),
    maternal_surname = COALESCE('Krausmann', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Daniel Escobar' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Daniel Escobar', 'ASSISTANT', 'NEW', '18461720-K', 'daniel.escobark03@gmail.com', 'Auxiliar Servicio Despacho',
    'Daniel', 'Ignacio', 'Escobar', 'Krausmann'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Daniel Escobar' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('13061923-1', rut),
    email = COALESCE('danielp2706@yahoo.com', email),
    cargo = COALESCE('Chofer Despacho', cargo),
    first_name = COALESCE('Daniel', first_name),
    middle_name = COALESCE(NULL, middle_name),
    paternal_surname = COALESCE('Peña', paternal_surname),
    maternal_surname = COALESCE('Bravo', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Daniel Peña' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Daniel Peña', 'ASSISTANT', NULL, '13061923-1', 'danielp2706@yahoo.com', 'Chofer Despacho',
    'Daniel', NULL, 'Peña', 'Bravo'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Daniel Peña' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('13061923-1', rut),
    email = COALESCE('danielp2706@yahoo.com', email),
    cargo = COALESCE('Chofer Despacho', cargo),
    first_name = COALESCE('Daniel', first_name),
    middle_name = COALESCE(NULL, middle_name),
    paternal_surname = COALESCE('Peña', paternal_surname),
    maternal_surname = COALESCE('Bravo', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Daniel Peña' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Daniel Peña', 'DRIVER', NULL, '13061923-1', 'danielp2706@yahoo.com', 'Chofer Despacho',
    'Daniel', NULL, 'Peña', 'Bravo'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Daniel Peña' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE(NULL, rut),
    email = COALESCE(NULL, email),
    cargo = COALESCE(NULL, cargo),
    first_name = COALESCE(NULL, first_name),
    middle_name = COALESCE(NULL, middle_name),
    paternal_surname = COALESCE(NULL, paternal_surname),
    maternal_surname = COALESCE(NULL, maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Deivis Santana' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Deivis Santana', 'ASSISTANT', NULL, NULL, NULL, NULL,
    NULL, NULL, NULL, NULL
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Deivis Santana' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('NEW', contract_type),
    rut = COALESCE(NULL, rut),
    email = COALESCE(NULL, email),
    cargo = COALESCE(NULL, cargo),
    first_name = COALESCE(NULL, first_name),
    middle_name = COALESCE(NULL, middle_name),
    paternal_surname = COALESCE(NULL, paternal_surname),
    maternal_surname = COALESCE(NULL, maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Edgar Benavides' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Edgar Benavides', 'ASSISTANT', 'NEW', NULL, NULL, NULL,
    NULL, NULL, NULL, NULL
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Edgar Benavides' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('NEW', contract_type),
    rut = COALESCE(NULL, rut),
    email = COALESCE(NULL, email),
    cargo = COALESCE(NULL, cargo),
    first_name = COALESCE(NULL, first_name),
    middle_name = COALESCE(NULL, middle_name),
    paternal_surname = COALESCE(NULL, paternal_surname),
    maternal_surname = COALESCE(NULL, maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Edgar Benavides' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Edgar Benavides', 'DRIVER', 'NEW', NULL, NULL, NULL,
    NULL, NULL, NULL, NULL
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Edgar Benavides' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('18332258-3', rut),
    email = COALESCE('edgardalex2304@gmail.com', email),
    cargo = COALESCE('Chofer y Auxiliar', cargo),
    first_name = COALESCE('Edgard', first_name),
    middle_name = COALESCE('Alex', middle_name),
    paternal_surname = COALESCE('Benavides', paternal_surname),
    maternal_surname = COALESCE('Opazo', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Edgard Benavides' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Edgard Benavides', 'UNASSIGNED', NULL, '18332258-3', 'edgardalex2304@gmail.com', 'Chofer y Auxiliar',
    'Edgard', 'Alex', 'Benavides', 'Opazo'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Edgard Benavides' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('25590805-7', rut),
    email = COALESCE('edsonferr476@gmail.com', email),
    cargo = COALESCE('Auxiliar Servicio Despacho', cargo),
    first_name = COALESCE('Edson', first_name),
    middle_name = COALESCE(NULL, middle_name),
    paternal_surname = COALESCE('Ferreira', paternal_surname),
    maternal_surname = COALESCE('Sandoval', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Edson Ferreira' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Edson Ferreira', 'UNASSIGNED', NULL, '25590805-7', 'edsonferr476@gmail.com', 'Auxiliar Servicio Despacho',
    'Edson', NULL, 'Ferreira', 'Sandoval'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Edson Ferreira' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('13180820-8', rut),
    email = COALESCE('edomonrroy.0806@hotmail.com', email),
    cargo = COALESCE('Chofer de Servicio y Despacho', cargo),
    first_name = COALESCE('Eduardo', first_name),
    middle_name = COALESCE('Antonio', middle_name),
    paternal_surname = COALESCE('Monroy', paternal_surname),
    maternal_surname = COALESCE('Velasquez', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Eduardo Monroy' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Eduardo Monroy', 'UNASSIGNED', NULL, '13180820-8', 'edomonrroy.0806@hotmail.com', 'Chofer de Servicio y Despacho',
    'Eduardo', 'Antonio', 'Monroy', 'Velasquez'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Eduardo Monroy' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('13282140-2', rut),
    email = COALESCE('esotog1977@gmail.com', email),
    cargo = COALESCE('Chofer y Auxiliar', cargo),
    first_name = COALESCE('Juan', first_name),
    middle_name = COALESCE('Eduardo', middle_name),
    paternal_surname = COALESCE('Soto', paternal_surname),
    maternal_surname = COALESCE('Guajardo', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Eduardo Soto' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Eduardo Soto', 'ASSISTANT', NULL, '13282140-2', 'esotog1977@gmail.com', 'Chofer y Auxiliar',
    'Juan', 'Eduardo', 'Soto', 'Guajardo'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Eduardo Soto' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('13282140-2', rut),
    email = COALESCE('esotog1977@gmail.com', email),
    cargo = COALESCE('Chofer y Auxiliar', cargo),
    first_name = COALESCE('Juan', first_name),
    middle_name = COALESCE('Eduardo', middle_name),
    paternal_surname = COALESCE('Soto', paternal_surname),
    maternal_surname = COALESCE('Guajardo', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Eduardo Soto' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Eduardo Soto', 'DRIVER', NULL, '13282140-2', 'esotog1977@gmail.com', 'Chofer y Auxiliar',
    'Juan', 'Eduardo', 'Soto', 'Guajardo'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Eduardo Soto' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE(NULL, rut),
    email = COALESCE(NULL, email),
    cargo = COALESCE(NULL, cargo),
    first_name = COALESCE(NULL, first_name),
    middle_name = COALESCE(NULL, middle_name),
    paternal_surname = COALESCE(NULL, paternal_surname),
    maternal_surname = COALESCE(NULL, maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Elias Llancaqueo' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Elias Llancaqueo', 'ASSISTANT', NULL, NULL, NULL, NULL,
    NULL, NULL, NULL, NULL
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Elias Llancaqueo' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE(NULL, rut),
    email = COALESCE(NULL, email),
    cargo = COALESCE(NULL, cargo),
    first_name = COALESCE(NULL, first_name),
    middle_name = COALESCE(NULL, middle_name),
    paternal_surname = COALESCE(NULL, paternal_surname),
    maternal_surname = COALESCE(NULL, maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Elias Llancaqueo' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Elias Llancaqueo', 'DRIVER', NULL, NULL, NULL, NULL,
    NULL, NULL, NULL, NULL
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Elias Llancaqueo' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('17071056-8', rut),
    email = COALESCE('emanxel.diaz0815@gmail.com', email),
    cargo = COALESCE('Chofer RS', cargo),
    first_name = COALESCE('Emanuel', first_name),
    middle_name = COALESCE('Alejandro', middle_name),
    paternal_surname = COALESCE('Diaz', paternal_surname),
    maternal_surname = COALESCE('Saavedra', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Emanuel Diaz' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Emanuel Diaz', 'UNASSIGNED', NULL, '17071056-8', 'emanxel.diaz0815@gmail.com', 'Chofer RS',
    'Emanuel', 'Alejandro', 'Diaz', 'Saavedra'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Emanuel Diaz' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('25400155-4', rut),
    email = COALESCE('enzoe.chorolque@gmail.com', email),
    cargo = COALESCE('Chofer Servicio', cargo),
    first_name = COALESCE('Enzo', first_name),
    middle_name = COALESCE('Esteban', middle_name),
    paternal_surname = COALESCE('Chorolque', paternal_surname),
    maternal_surname = COALESCE('Cuestas', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Enzo Chorolque' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Enzo Chorolque', 'UNASSIGNED', NULL, '25400155-4', 'enzoe.chorolque@gmail.com', 'Chofer Servicio',
    'Enzo', 'Esteban', 'Chorolque', 'Cuestas'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Enzo Chorolque' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('13180945-K', rut),
    email = COALESCE('eugenio.mc@hotmail.com', email),
    cargo = COALESCE('Auxiliar Servicio Despacho', cargo),
    first_name = COALESCE('Eugenio', first_name),
    middle_name = COALESCE('Del', middle_name),
    paternal_surname = COALESCE('Muñoz', paternal_surname),
    maternal_surname = COALESCE('Campos', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Eugenio Muñoz' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Eugenio Muñoz', 'UNASSIGNED', NULL, '13180945-K', 'eugenio.mc@hotmail.com', 'Auxiliar Servicio Despacho',
    'Eugenio', 'Del', 'Muñoz', 'Campos'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Eugenio Muñoz' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('20525558-3', rut),
    email = COALESCE('f.jimenezd33@gmail.com', email),
    cargo = COALESCE('Auxiliar Servicio Despacho', cargo),
    first_name = COALESCE('Felipe', first_name),
    middle_name = COALESCE('Ignacio', middle_name),
    paternal_surname = COALESCE('Jimenez', paternal_surname),
    maternal_surname = COALESCE('Diaz', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Felipe Jimenez' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Felipe Jimenez', 'UNASSIGNED', NULL, '20525558-3', 'f.jimenezd33@gmail.com', 'Auxiliar Servicio Despacho',
    'Felipe', 'Ignacio', 'Jimenez', 'Diaz'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Felipe Jimenez' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('NEW', contract_type),
    rut = COALESCE('9462722-2', rut),
    email = COALESCE('fernandodiazsepulveda62@gmail.com', email),
    cargo = COALESCE('Chofer y Auxiliar', cargo),
    first_name = COALESCE('Fernando', first_name),
    middle_name = COALESCE('Aquiles', middle_name),
    paternal_surname = COALESCE('Diaz', paternal_surname),
    maternal_surname = COALESCE('Sepulveda', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Fernando Diaz' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Fernando Diaz', 'ASSISTANT', 'NEW', '9462722-2', 'fernandodiazsepulveda62@gmail.com', 'Chofer y Auxiliar',
    'Fernando', 'Aquiles', 'Diaz', 'Sepulveda'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Fernando Diaz' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('NEW', contract_type),
    rut = COALESCE('9462722-2', rut),
    email = COALESCE('fernandodiazsepulveda62@gmail.com', email),
    cargo = COALESCE('Chofer y Auxiliar', cargo),
    first_name = COALESCE('Fernando', first_name),
    middle_name = COALESCE('Aquiles', middle_name),
    paternal_surname = COALESCE('Diaz', paternal_surname),
    maternal_surname = COALESCE('Sepulveda', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Fernando Diaz' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Fernando Diaz', 'DRIVER', 'NEW', '9462722-2', 'fernandodiazsepulveda62@gmail.com', 'Chofer y Auxiliar',
    'Fernando', 'Aquiles', 'Diaz', 'Sepulveda'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Fernando Diaz' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('9205268-0', rut),
    email = COALESCE('aridosespress@gmail.com', email),
    cargo = COALESCE('Chofer Servicio', cargo),
    first_name = COALESCE('Fernando', first_name),
    middle_name = COALESCE('Arturo', middle_name),
    paternal_surname = COALESCE('Ortiz', paternal_surname),
    maternal_surname = COALESCE('Castillo', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Fernando Ortiz' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Fernando Ortiz', 'UNASSIGNED', NULL, '9205268-0', 'aridosespress@gmail.com', 'Chofer Servicio',
    'Fernando', 'Arturo', 'Ortiz', 'Castillo'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Fernando Ortiz' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE(NULL, rut),
    email = COALESCE(NULL, email),
    cargo = COALESCE(NULL, cargo),
    first_name = COALESCE(NULL, first_name),
    middle_name = COALESCE(NULL, middle_name),
    paternal_surname = COALESCE(NULL, paternal_surname),
    maternal_surname = COALESCE(NULL, maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Francisco Cuevas' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Francisco Cuevas', 'DRIVER', NULL, NULL, NULL, NULL,
    NULL, NULL, NULL, NULL
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Francisco Cuevas' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('16868232-8', rut),
    email = COALESCE('vegaherrerafrancisco@gmail.com', email),
    cargo = COALESCE('Chofer Servicio', cargo),
    first_name = COALESCE('Francisco', first_name),
    middle_name = COALESCE('Javier', middle_name),
    paternal_surname = COALESCE('Vega', paternal_surname),
    maternal_surname = COALESCE('Herrera', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Francisco Vega' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Francisco Vega', 'UNASSIGNED', NULL, '16868232-8', 'vegaherrerafrancisco@gmail.com', 'Chofer Servicio',
    'Francisco', 'Javier', 'Vega', 'Herrera'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Francisco Vega' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('27063200-9', rut),
    email = COALESCE('leones5353fa@gmail.com', email),
    cargo = COALESCE('Auxiliar de Aseo', cargo),
    first_name = COALESCE('Frank', first_name),
    middle_name = COALESCE('Alexis', middle_name),
    paternal_surname = COALESCE('Alvarez', paternal_surname),
    maternal_surname = COALESCE('Melendez', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Frank Alvarez' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Frank Alvarez', 'UNASSIGNED', NULL, '27063200-9', 'leones5353fa@gmail.com', 'Auxiliar de Aseo',
    'Frank', 'Alexis', 'Alvarez', 'Melendez'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Frank Alvarez' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('12964068-5', rut),
    email = COALESCE('alexisfre339@gmail.com', email),
    cargo = COALESCE('Chofer y Auxiliar', cargo),
    first_name = COALESCE('Freddy', first_name),
    middle_name = COALESCE('Alexis', middle_name),
    paternal_surname = COALESCE('Ramos', paternal_surname),
    maternal_surname = COALESCE('Labrin', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Freddy Ramos' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Freddy Ramos', 'UNASSIGNED', NULL, '12964068-5', 'alexisfre339@gmail.com', 'Chofer y Auxiliar',
    'Freddy', 'Alexis', 'Ramos', 'Labrin'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Freddy Ramos' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('NEW', contract_type),
    rut = COALESCE(NULL, rut),
    email = COALESCE(NULL, email),
    cargo = COALESCE(NULL, cargo),
    first_name = COALESCE(NULL, first_name),
    middle_name = COALESCE(NULL, middle_name),
    paternal_surname = COALESCE(NULL, paternal_surname),
    maternal_surname = COALESCE(NULL, maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Gerald Aguayo' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Gerald Aguayo', 'ASSISTANT', 'NEW', NULL, NULL, NULL,
    NULL, NULL, NULL, NULL
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Gerald Aguayo' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE(NULL, rut),
    email = COALESCE(NULL, email),
    cargo = COALESCE(NULL, cargo),
    first_name = COALESCE(NULL, first_name),
    middle_name = COALESCE(NULL, middle_name),
    paternal_surname = COALESCE(NULL, paternal_surname),
    maternal_surname = COALESCE(NULL, maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Gerald Paredes' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Gerald Paredes', 'ASSISTANT', NULL, NULL, NULL, NULL,
    NULL, NULL, NULL, NULL
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Gerald Paredes' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('20334945-9', rut),
    email = COALESCE('geraldaguayo03@gmail.com', email),
    cargo = COALESCE('Auxiliar Servicio Despacho', cargo),
    first_name = COALESCE('Gerard', first_name),
    middle_name = COALESCE('Diego', middle_name),
    paternal_surname = COALESCE('Aguayo', paternal_surname),
    maternal_surname = COALESCE('Perez', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Gerard Aguayo' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Gerard Aguayo', 'UNASSIGNED', NULL, '20334945-9', 'geraldaguayo03@gmail.com', 'Auxiliar Servicio Despacho',
    'Gerard', 'Diego', 'Aguayo', 'Perez'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Gerard Aguayo' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('16143616-K', rut),
    email = COALESCE('g.cartes.avila@gmail.com', email),
    cargo = COALESCE('Chofer Despacho', cargo),
    first_name = COALESCE('Gerardo', first_name),
    middle_name = COALESCE(NULL, middle_name),
    paternal_surname = COALESCE('Cartes', paternal_surname),
    maternal_surname = COALESCE('Avila', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Gerardo Cartes' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Gerardo Cartes', 'DRIVER', NULL, '16143616-K', 'g.cartes.avila@gmail.com', 'Chofer Despacho',
    'Gerardo', NULL, 'Cartes', 'Avila'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Gerardo Cartes' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('NEW', contract_type),
    rut = COALESCE('27891710-K', rut),
    email = COALESCE('gilmarospino0619@gmail.com', email),
    cargo = COALESCE('auxiliar servicio', cargo),
    first_name = COALESCE('Gilmar', first_name),
    middle_name = COALESCE('Andres', middle_name),
    paternal_surname = COALESCE('Ospino', paternal_surname),
    maternal_surname = COALESCE('Perea', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Gilmar Ospino' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Gilmar Ospino', 'ASSISTANT', 'NEW', '27891710-K', 'gilmarospino0619@gmail.com', 'auxiliar servicio',
    'Gilmar', 'Andres', 'Ospino', 'Perea'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Gilmar Ospino' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('NEW', contract_type),
    rut = COALESCE('27891710-K', rut),
    email = COALESCE('gilmarospino0619@gmail.com', email),
    cargo = COALESCE('auxiliar servicio', cargo),
    first_name = COALESCE('Gilmar', first_name),
    middle_name = COALESCE('Andres', middle_name),
    paternal_surname = COALESCE('Ospino', paternal_surname),
    maternal_surname = COALESCE('Perea', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Gilmar Ospino' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Gilmar Ospino', 'DRIVER', 'NEW', '27891710-K', 'gilmarospino0619@gmail.com', 'auxiliar servicio',
    'Gilmar', 'Andres', 'Ospino', 'Perea'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Gilmar Ospino' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('23701491-K', rut),
    email = COALESCE('gtineo.20zamudio@gmail.com', email),
    cargo = COALESCE('Chofer RS', cargo),
    first_name = COALESCE('Gino', first_name),
    middle_name = COALESCE('Cesar', middle_name),
    paternal_surname = COALESCE('Tineo', paternal_surname),
    maternal_surname = COALESCE('Zamudio', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Gino Tineo' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Gino Tineo', 'UNASSIGNED', NULL, '23701491-K', 'gtineo.20zamudio@gmail.com', 'Chofer RS',
    'Gino', 'Cesar', 'Tineo', 'Zamudio'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Gino Tineo' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('OLD', contract_type),
    rut = COALESCE('26450684-0', rut),
    email = COALESCE('chalito1077@gmail.com', email),
    cargo = COALESCE('auxiliar servicio', cargo),
    first_name = COALESCE('Gonzalo', first_name),
    middle_name = COALESCE(NULL, middle_name),
    paternal_surname = COALESCE('Gonzalez', paternal_surname),
    maternal_surname = COALESCE('Meneses', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Gonzalo Gonzalez' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Gonzalo Gonzalez', 'ASSISTANT', 'OLD', '26450684-0', 'chalito1077@gmail.com', 'auxiliar servicio',
    'Gonzalo', NULL, 'Gonzalez', 'Meneses'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Gonzalo Gonzalez' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE(NULL, rut),
    email = COALESCE(NULL, email),
    cargo = COALESCE(NULL, cargo),
    first_name = COALESCE(NULL, first_name),
    middle_name = COALESCE(NULL, middle_name),
    paternal_surname = COALESCE(NULL, paternal_surname),
    maternal_surname = COALESCE(NULL, maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Hjorge Vizcarra' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Hjorge Vizcarra', 'ASSISTANT', NULL, NULL, NULL, NULL,
    NULL, NULL, NULL, NULL
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Hjorge Vizcarra' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('15416728-5', rut),
    email = COALESCE('hugotroncoso139@yahoo.es', email),
    cargo = COALESCE('auxiliar servicio', cargo),
    first_name = COALESCE('Hugo', first_name),
    middle_name = COALESCE('Antonio', middle_name),
    paternal_surname = COALESCE('Troncoso', paternal_surname),
    maternal_surname = COALESCE('Catalan', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Hugo Troncoso' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Hugo Troncoso', 'ASSISTANT', NULL, '15416728-5', 'hugotroncoso139@yahoo.es', 'auxiliar servicio',
    'Hugo', 'Antonio', 'Troncoso', 'Catalan'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Hugo Troncoso' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('21893971-6', rut),
    email = COALESCE('i.villarroel2305@gmail.com', email),
    cargo = COALESCE('Auxiliar Servicio Despacho', cargo),
    first_name = COALESCE('Ignacio', first_name),
    middle_name = COALESCE('Alfredo', middle_name),
    paternal_surname = COALESCE('Villaroel', paternal_surname),
    maternal_surname = COALESCE('Orellana', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Ignacio Villaroel' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Ignacio Villaroel', 'UNASSIGNED', NULL, '21893971-6', 'i.villarroel2305@gmail.com', 'Auxiliar Servicio Despacho',
    'Ignacio', 'Alfredo', 'Villaroel', 'Orellana'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Ignacio Villaroel' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('23671952-9', rut),
    email = COALESCE('jaicon91ab@hotmail.com', email),
    cargo = COALESCE('Chofer de Servicio y Despacho', cargo),
    first_name = COALESCE('Jaime', first_name),
    middle_name = COALESCE(NULL, middle_name),
    paternal_surname = COALESCE('Condori', paternal_surname),
    maternal_surname = COALESCE('Vargas', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Jaime Condori' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Jaime Condori', 'UNASSIGNED', NULL, '23671952-9', 'jaicon91ab@hotmail.com', 'Chofer de Servicio y Despacho',
    'Jaime', NULL, 'Condori', 'Vargas'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Jaime Condori' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('11506439-8', rut),
    email = COALESCE('japraco@hotmail.com', email),
    cargo = COALESCE('auxiliar servicio', cargo),
    first_name = COALESCE('Javier', first_name),
    middle_name = COALESCE('Antonio', middle_name),
    paternal_surname = COALESCE('Prado', paternal_surname),
    maternal_surname = COALESCE('Cornejo', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Javier Prado' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Javier Prado', 'UNASSIGNED', NULL, '11506439-8', 'japraco@hotmail.com', 'auxiliar servicio',
    'Javier', 'Antonio', 'Prado', 'Cornejo'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Javier Prado' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('18344143-4', rut),
    email = COALESCE('jeremiascerda1993@gmail.com', email),
    cargo = COALESCE('auxiliar servicio', cargo),
    first_name = COALESCE('Jeremias', first_name),
    middle_name = COALESCE('Esteban', middle_name),
    paternal_surname = COALESCE('Cerda', paternal_surname),
    maternal_surname = COALESCE('Vega', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Jeremias Cerda' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Jeremias Cerda', 'ASSISTANT', NULL, '18344143-4', 'jeremiascerda1993@gmail.com', 'auxiliar servicio',
    'Jeremias', 'Esteban', 'Cerda', 'Vega'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Jeremias Cerda' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('18344143-4', rut),
    email = COALESCE('jeremiascerda1993@gmail.com', email),
    cargo = COALESCE('auxiliar servicio', cargo),
    first_name = COALESCE('Jeremias', first_name),
    middle_name = COALESCE('Esteban', middle_name),
    paternal_surname = COALESCE('Cerda', paternal_surname),
    maternal_surname = COALESCE('Vega', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Jeremias Cerda' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Jeremias Cerda', 'DRIVER', NULL, '18344143-4', 'jeremiascerda1993@gmail.com', 'auxiliar servicio',
    'Jeremias', 'Esteban', 'Cerda', 'Vega'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Jeremias Cerda' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE(NULL, rut),
    email = COALESCE(NULL, email),
    cargo = COALESCE(NULL, cargo),
    first_name = COALESCE(NULL, first_name),
    middle_name = COALESCE(NULL, middle_name),
    paternal_surname = COALESCE(NULL, paternal_surname),
    maternal_surname = COALESCE(NULL, maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Jesus Barrera' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Jesus Barrera', 'ASSISTANT', NULL, NULL, NULL, NULL,
    NULL, NULL, NULL, NULL
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Jesus Barrera' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('26835778-5', rut),
    email = COALESCE('johantorres22.1985@gmail.com', email),
    cargo = COALESCE('Chofer Servicio', cargo),
    first_name = COALESCE('Johan', first_name),
    middle_name = COALESCE('Ferley', middle_name),
    paternal_surname = COALESCE('Torres', paternal_surname),
    maternal_surname = COALESCE('Ramirez', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Johan Torres' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Johan Torres', 'UNASSIGNED', NULL, '26835778-5', 'johantorres22.1985@gmail.com', 'Chofer Servicio',
    'Johan', 'Ferley', 'Torres', 'Ramirez'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Johan Torres' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('16260494-5', rut),
    email = COALESCE('jonathanegajardo@gmail.com', email),
    cargo = COALESCE('Chofer Servicio', cargo),
    first_name = COALESCE('Jonathan', first_name),
    middle_name = COALESCE('Eduardo', middle_name),
    paternal_surname = COALESCE('Gajardo', paternal_surname),
    maternal_surname = COALESCE('Plaza', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Jonathan Gajardo' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Jonathan Gajardo', 'UNASSIGNED', NULL, '16260494-5', 'jonathanegajardo@gmail.com', 'Chofer Servicio',
    'Jonathan', 'Eduardo', 'Gajardo', 'Plaza'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Jonathan Gajardo' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('15619238-4', rut),
    email = COALESCE('jonathan.reyes26@gmail.com', email),
    cargo = COALESCE('Chofer RS', cargo),
    first_name = COALESCE('Jonathan', first_name),
    middle_name = COALESCE('Luis', middle_name),
    paternal_surname = COALESCE('Reyes', paternal_surname),
    maternal_surname = COALESCE('Valdebenito', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Jonathan Reyes' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Jonathan Reyes', 'UNASSIGNED', NULL, '15619238-4', 'jonathan.reyes26@gmail.com', 'Chofer RS',
    'Jonathan', 'Luis', 'Reyes', 'Valdebenito'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Jonathan Reyes' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('NEW', contract_type),
    rut = COALESCE('18562616-4', rut),
    email = COALESCE('jordan.gaete.donaire@gmail.com', email),
    cargo = COALESCE('auxiliar servicio', cargo),
    first_name = COALESCE('Jordan', first_name),
    middle_name = COALESCE(NULL, middle_name),
    paternal_surname = COALESCE('Gaete', paternal_surname),
    maternal_surname = COALESCE('Donaire', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Jordan Gaete' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Jordan Gaete', 'ASSISTANT', 'NEW', '18562616-4', 'jordan.gaete.donaire@gmail.com', 'auxiliar servicio',
    'Jordan', NULL, 'Gaete', 'Donaire'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Jordan Gaete' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('16456021-K', rut),
    email = COALESCE('jorviscarrasco1987@gmail.com', email),
    cargo = COALESCE('auxiliar servicio', cargo),
    first_name = COALESCE('Jorge', first_name),
    middle_name = COALESCE('Luis', middle_name),
    paternal_surname = COALESCE('Viscarra', paternal_surname),
    maternal_surname = COALESCE('Carrasco', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Jorge Viscarra' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Jorge Viscarra', 'ASSISTANT', NULL, '16456021-K', 'jorviscarrasco1987@gmail.com', 'auxiliar servicio',
    'Jorge', 'Luis', 'Viscarra', 'Carrasco'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Jorge Viscarra' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE(NULL, rut),
    email = COALESCE(NULL, email),
    cargo = COALESCE(NULL, cargo),
    first_name = COALESCE(NULL, first_name),
    middle_name = COALESCE(NULL, middle_name),
    paternal_surname = COALESCE(NULL, paternal_surname),
    maternal_surname = COALESCE(NULL, maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Jorge Vizcarra' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Jorge Vizcarra', 'ASSISTANT', NULL, NULL, NULL, NULL,
    NULL, NULL, NULL, NULL
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Jorge Vizcarra' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('11890417-6', rut),
    email = COALESCE('josearredondogonzalez227@gmail.com', email),
    cargo = COALESCE('Chofer y Auxiliar', cargo),
    first_name = COALESCE('Jose', first_name),
    middle_name = COALESCE('Manuel', middle_name),
    paternal_surname = COALESCE('Arredondo', paternal_surname),
    maternal_surname = COALESCE('Gonzalez', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Jose Arredondo' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Jose Arredondo', 'DRIVER', NULL, '11890417-6', 'josearredondogonzalez227@gmail.com', 'Chofer y Auxiliar',
    'Jose', 'Manuel', 'Arredondo', 'Gonzalez'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Jose Arredondo' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('OLD', contract_type),
    rut = COALESCE('26017411-8', rut),
    email = COALESCE('joseangelocag@gmail.com', email),
    cargo = COALESCE('auxiliar servicio', cargo),
    first_name = COALESCE('Jose', first_name),
    middle_name = COALESCE('Angel', middle_name),
    paternal_surname = COALESCE('Oca', paternal_surname),
    maternal_surname = COALESCE('Gonzalez', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Jose Oca' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Jose Oca', 'ASSISTANT', 'OLD', '26017411-8', 'joseangelocag@gmail.com', 'auxiliar servicio',
    'Jose', 'Angel', 'Oca', 'Gonzalez'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Jose Oca' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('24361952-1', rut),
    email = COALESCE('joshuabarraking@gmail.com', email),
    cargo = COALESCE('Auxiliar Servicio Despacho', cargo),
    first_name = COALESCE('Josue', first_name),
    middle_name = COALESCE('Evaristo', middle_name),
    paternal_surname = COALESCE('Barra', paternal_surname),
    maternal_surname = COALESCE('Poma', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Josue Barra' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Josue Barra', 'UNASSIGNED', NULL, '24361952-1', 'joshuabarraking@gmail.com', 'Auxiliar Servicio Despacho',
    'Josue', 'Evaristo', 'Barra', 'Poma'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Josue Barra' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('11890417-6', rut),
    email = COALESCE('josearredondogonzalez227@gmail.com', email),
    cargo = COALESCE('Chofer y Auxiliar', cargo),
    first_name = COALESCE('Jose', first_name),
    middle_name = COALESCE('Manuel', middle_name),
    paternal_surname = COALESCE('Arredondo', paternal_surname),
    maternal_surname = COALESCE('Gonzalez', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'José Arredondo' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'José Arredondo', 'DRIVER', NULL, '11890417-6', 'josearredondogonzalez227@gmail.com', 'Chofer y Auxiliar',
    'Jose', 'Manuel', 'Arredondo', 'Gonzalez'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'José Arredondo' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('10590216-6', rut),
    email = COALESCE('josepatriciosoto23@gmail.com', email),
    cargo = COALESCE('Chofer Servicio', cargo),
    first_name = COALESCE('Jose', first_name),
    middle_name = COALESCE('Patricio', middle_name),
    paternal_surname = COALESCE('Soto', paternal_surname),
    maternal_surname = COALESCE('Catalan', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'José Soto Catalan' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'José Soto Catalan', 'DRIVER', NULL, '10590216-6', 'josepatriciosoto23@gmail.com', 'Chofer Servicio',
    'Jose', 'Patricio', 'Soto', 'Catalan'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'José Soto Catalan' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('OLD', contract_type),
    rut = COALESCE('11971597-0', rut),
    email = COALESCE('juanaravenaorellana28@gmail.com', email),
    cargo = COALESCE('auxiliar servicio', cargo),
    first_name = COALESCE('Juan', first_name),
    middle_name = COALESCE('Manuel', middle_name),
    paternal_surname = COALESCE('Aravena', paternal_surname),
    maternal_surname = COALESCE('Orellana', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Juan Aravena' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Juan Aravena', 'ASSISTANT', 'OLD', '11971597-0', 'juanaravenaorellana28@gmail.com', 'auxiliar servicio',
    'Juan', 'Manuel', 'Aravena', 'Orellana'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Juan Aravena' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('OLD', contract_type),
    rut = COALESCE('10431118-0', rut),
    email = COALESCE('kalipzo37@gmail.com', email),
    cargo = COALESCE('auxiliar servicio', cargo),
    first_name = COALESCE('Juan', first_name),
    middle_name = COALESCE('Carlos', middle_name),
    paternal_surname = COALESCE('Cuadra', paternal_surname),
    maternal_surname = COALESCE('Mugoreni', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Juan Cuadra' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Juan Cuadra', 'ASSISTANT', 'OLD', '10431118-0', 'kalipzo37@gmail.com', 'auxiliar servicio',
    'Juan', 'Carlos', 'Cuadra', 'Mugoreni'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Juan Cuadra' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('OLD', contract_type),
    rut = COALESCE('12175354-5', rut),
    email = COALESCE('santibanezj344@gmail.com', email),
    cargo = COALESCE('Chofer Servicio', cargo),
    first_name = COALESCE('Juan', first_name),
    middle_name = COALESCE('Ramon', middle_name),
    paternal_surname = COALESCE('Santibañez', paternal_surname),
    maternal_surname = COALESCE('Santibañez', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Juan Santibañez' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Juan Santibañez', 'ASSISTANT', 'OLD', '12175354-5', 'santibanezj344@gmail.com', 'Chofer Servicio',
    'Juan', 'Ramon', 'Santibañez', 'Santibañez'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Juan Santibañez' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('OLD', contract_type),
    rut = COALESCE('12175354-5', rut),
    email = COALESCE('santibanezj344@gmail.com', email),
    cargo = COALESCE('Chofer Servicio', cargo),
    first_name = COALESCE('Juan', first_name),
    middle_name = COALESCE('Ramon', middle_name),
    paternal_surname = COALESCE('Santibañez', paternal_surname),
    maternal_surname = COALESCE('Santibañez', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Juan Santibañez' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Juan Santibañez', 'DRIVER', 'OLD', '12175354-5', 'santibanezj344@gmail.com', 'Chofer Servicio',
    'Juan', 'Ramon', 'Santibañez', 'Santibañez'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Juan Santibañez' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('15107582-7', rut),
    email = COALESCE('julio.sanhueza1983@gmail.com', email),
    cargo = COALESCE('Chofer y Auxiliar', cargo),
    first_name = COALESCE('Julio', first_name),
    middle_name = COALESCE('Cesar', middle_name),
    paternal_surname = COALESCE('Sanhueza', paternal_surname),
    maternal_surname = COALESCE('Tobar', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Julio Sanhueza' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Julio Sanhueza', 'DRIVER', NULL, '15107582-7', 'julio.sanhueza1983@gmail.com', 'Chofer y Auxiliar',
    'Julio', 'Cesar', 'Sanhueza', 'Tobar'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Julio Sanhueza' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('NEW', contract_type),
    rut = COALESCE('10851926-6', rut),
    email = COALESCE('acelugosan@gmail.com', email),
    cargo = COALESCE('Auxiliar Despacho', cargo),
    first_name = COALESCE('Luis', first_name),
    middle_name = COALESCE('Alberto', middle_name),
    paternal_surname = COALESCE('Acevedo', paternal_surname),
    maternal_surname = COALESCE('Gonzalez', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Luis Acevedo' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Luis Acevedo', 'ASSISTANT', 'NEW', '10851926-6', 'acelugosan@gmail.com', 'Auxiliar Despacho',
    'Luis', 'Alberto', 'Acevedo', 'Gonzalez'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Luis Acevedo' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('NEW', contract_type),
    rut = COALESCE('10851926-6', rut),
    email = COALESCE('acelugosan@gmail.com', email),
    cargo = COALESCE('Auxiliar Despacho', cargo),
    first_name = COALESCE('Luis', first_name),
    middle_name = COALESCE('Alberto', middle_name),
    paternal_surname = COALESCE('Acevedo', paternal_surname),
    maternal_surname = COALESCE('Gonzalez', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Luis Acevedo' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Luis Acevedo', 'DRIVER', 'NEW', '10851926-6', 'acelugosan@gmail.com', 'Auxiliar Despacho',
    'Luis', 'Alberto', 'Acevedo', 'Gonzalez'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Luis Acevedo' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('16698073-9', rut),
    email = COALESCE('luisalvarez2310@gmail.com', email),
    cargo = COALESCE('Chofer Despacho', cargo),
    first_name = COALESCE('Orlando', first_name),
    middle_name = COALESCE('Luis', middle_name),
    paternal_surname = COALESCE('Alvarez', paternal_surname),
    maternal_surname = COALESCE('Avendaño', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Luis Alvarez' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Luis Alvarez', 'DRIVER', NULL, '16698073-9', 'luisalvarez2310@gmail.com', 'Chofer Despacho',
    'Orlando', 'Luis', 'Alvarez', 'Avendaño'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Luis Alvarez' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('NEW', contract_type),
    rut = COALESCE('8473758-5', rut),
    email = COALESCE('patricio.cubillos.sanchez@gmail.com', email),
    cargo = COALESCE('Chofer Servicio', cargo),
    first_name = COALESCE('Luis', first_name),
    middle_name = COALESCE('Patricio', middle_name),
    paternal_surname = COALESCE('Cubillos', paternal_surname),
    maternal_surname = COALESCE('Sanchez', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Luis Cubillos' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Luis Cubillos', 'ASSISTANT', 'NEW', '8473758-5', 'patricio.cubillos.sanchez@gmail.com', 'Chofer Servicio',
    'Luis', 'Patricio', 'Cubillos', 'Sanchez'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Luis Cubillos' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('OLD', contract_type),
    rut = COALESCE('13548053-3', rut),
    email = COALESCE('joeldugo@gmail.com', email),
    cargo = COALESCE('Chofer Servicio', cargo),
    first_name = COALESCE('Luis', first_name),
    middle_name = COALESCE('Joel', middle_name),
    paternal_surname = COALESCE('Dugo', paternal_surname),
    maternal_surname = COALESCE('Hernandez', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Luis Dugo' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Luis Dugo', 'DRIVER', 'OLD', '13548053-3', 'joeldugo@gmail.com', 'Chofer Servicio',
    'Luis', 'Joel', 'Dugo', 'Hernandez'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Luis Dugo' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('19255717-8', rut),
    email = COALESCE('maraboligluis@gmail.com', email),
    cargo = COALESCE('Auxiliar Servicio Despacho', cargo),
    first_name = COALESCE('Luis', first_name),
    middle_name = COALESCE('Enrique', middle_name),
    paternal_surname = COALESCE('Maraboli', paternal_surname),
    maternal_surname = COALESCE('Contreras', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Luis Maraboli' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Luis Maraboli', 'UNASSIGNED', NULL, '19255717-8', 'maraboligluis@gmail.com', 'Auxiliar Servicio Despacho',
    'Luis', 'Enrique', 'Maraboli', 'Contreras'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Luis Maraboli' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('17936722-K', rut),
    email = COALESCE('manuelcaceresrojas1606@gmail.com', email),
    cargo = COALESCE('Chofer Servicio', cargo),
    first_name = COALESCE('Manuel', first_name),
    middle_name = COALESCE('Jesus', middle_name),
    paternal_surname = COALESCE('Caceres', paternal_surname),
    maternal_surname = COALESCE('Rojas', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Manuel Caceres' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Manuel Caceres', 'UNASSIGNED', NULL, '17936722-K', 'manuelcaceresrojas1606@gmail.com', 'Chofer Servicio',
    'Manuel', 'Jesus', 'Caceres', 'Rojas'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Manuel Caceres' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('13663701-0', rut),
    email = COALESCE('nolo1978@icloud.com', email),
    cargo = COALESCE('Chofer Fosero', cargo),
    first_name = COALESCE('Manuel', first_name),
    middle_name = COALESCE('Alejandro', middle_name),
    paternal_surname = COALESCE('Lopez', paternal_surname),
    maternal_surname = COALESCE('Errazuriz', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Manuel Lopez' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Manuel Lopez', 'UNASSIGNED', NULL, '13663701-0', 'nolo1978@icloud.com', 'Chofer Fosero',
    'Manuel', 'Alejandro', 'Lopez', 'Errazuriz'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Manuel Lopez' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('17392585-9', rut),
    email = COALESCE('tapiaxino77@gmail.com', email),
    cargo = COALESCE('Chofer y Auxiliar', cargo),
    first_name = COALESCE('Manuel', first_name),
    middle_name = COALESCE('Moises', middle_name),
    paternal_surname = COALESCE('Tapia', paternal_surname),
    maternal_surname = COALESCE('Prado', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Manuel Tapia' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Manuel Tapia', 'UNASSIGNED', NULL, '17392585-9', 'tapiaxino77@gmail.com', 'Chofer y Auxiliar',
    'Manuel', 'Moises', 'Tapia', 'Prado'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Manuel Tapia' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('18406957-1', rut),
    email = COALESCE('marcelo.caceresb@gmail.com', email),
    cargo = COALESCE('Chofer de Unibox', cargo),
    first_name = COALESCE('Marcelo', first_name),
    middle_name = COALESCE('Alejandro', middle_name),
    paternal_surname = COALESCE('Caceres', paternal_surname),
    maternal_surname = COALESCE('Bascuñan', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Marcelo Caceres' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Marcelo Caceres', 'UNASSIGNED', NULL, '18406957-1', 'marcelo.caceresb@gmail.com', 'Chofer de Unibox',
    'Marcelo', 'Alejandro', 'Caceres', 'Bascuñan'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Marcelo Caceres' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('21134377-K', rut),
    email = COALESCE('nao.caro09@gmail.com', email),
    cargo = COALESCE('Auxiliar Servicio Despacho', cargo),
    first_name = COALESCE('Marcelo', first_name),
    middle_name = COALESCE('Alexi', middle_name),
    paternal_surname = COALESCE('Caro', paternal_surname),
    maternal_surname = COALESCE('Guerrero', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Marcelo Caro' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Marcelo Caro', 'UNASSIGNED', NULL, '21134377-K', 'nao.caro09@gmail.com', 'Auxiliar Servicio Despacho',
    'Marcelo', 'Alexi', 'Caro', 'Guerrero'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Marcelo Caro' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE(NULL, rut),
    email = COALESCE(NULL, email),
    cargo = COALESCE(NULL, cargo),
    first_name = COALESCE(NULL, first_name),
    middle_name = COALESCE(NULL, middle_name),
    paternal_surname = COALESCE(NULL, paternal_surname),
    maternal_surname = COALESCE(NULL, maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Mario Astorga' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Mario Astorga', 'ASSISTANT', NULL, NULL, NULL, NULL,
    NULL, NULL, NULL, NULL
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Mario Astorga' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE(NULL, rut),
    email = COALESCE(NULL, email),
    cargo = COALESCE(NULL, cargo),
    first_name = COALESCE(NULL, first_name),
    middle_name = COALESCE(NULL, middle_name),
    paternal_surname = COALESCE(NULL, paternal_surname),
    maternal_surname = COALESCE(NULL, maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Mario Astorga' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Mario Astorga', 'DRIVER', NULL, NULL, NULL, NULL,
    NULL, NULL, NULL, NULL
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Mario Astorga' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE(NULL, rut),
    email = COALESCE(NULL, email),
    cargo = COALESCE(NULL, cargo),
    first_name = COALESCE(NULL, first_name),
    middle_name = COALESCE(NULL, middle_name),
    paternal_surname = COALESCE(NULL, paternal_surname),
    maternal_surname = COALESCE(NULL, maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Mario Nuevo' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Mario Nuevo', 'ASSISTANT', NULL, NULL, NULL, NULL,
    NULL, NULL, NULL, NULL
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Mario Nuevo' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('16879567-K', rut),
    email = COALESCE('mige14.rking@gmail.com', email),
    cargo = COALESCE('Chofer y Auxiliar', cargo),
    first_name = COALESCE('Martin', first_name),
    middle_name = COALESCE('Jose', middle_name),
    paternal_surname = COALESCE('Reyes', paternal_surname),
    maternal_surname = COALESCE('San', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Martin Reyes' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Martin Reyes', 'UNASSIGNED', NULL, '16879567-K', 'mige14.rking@gmail.com', 'Chofer y Auxiliar',
    'Martin', 'Jose', 'Reyes', 'San'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Martin Reyes' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('OLD', contract_type),
    rut = COALESCE('13897180-5', rut),
    email = COALESCE('max.arancibia.r@gmail.com', email),
    cargo = COALESCE('Chofer Servicio', cargo),
    first_name = COALESCE('Maximiliano', first_name),
    middle_name = COALESCE(NULL, middle_name),
    paternal_surname = COALESCE('Arancibia', paternal_surname),
    maternal_surname = COALESCE('Ramirez', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Maximiliano Arancibia' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Maximiliano Arancibia', 'DRIVER', 'OLD', '13897180-5', 'max.arancibia.r@gmail.com', 'Chofer Servicio',
    'Maximiliano', NULL, 'Arancibia', 'Ramirez'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Maximiliano Arancibia' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('17782393-7', rut),
    email = COALESCE('anthonyvera009@gmail.com', email),
    cargo = COALESCE('Auxiliar Despacho', cargo),
    first_name = COALESCE('Michael', first_name),
    middle_name = COALESCE('Anthony', middle_name),
    paternal_surname = COALESCE('Suarez', paternal_surname),
    maternal_surname = COALESCE('Vera', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Michael Suarez' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Michael Suarez', 'ASSISTANT', NULL, '17782393-7', 'anthonyvera009@gmail.com', 'Auxiliar Despacho',
    'Michael', 'Anthony', 'Suarez', 'Vera'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Michael Suarez' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE(NULL, rut),
    email = COALESCE(NULL, email),
    cargo = COALESCE(NULL, cargo),
    first_name = COALESCE(NULL, first_name),
    middle_name = COALESCE(NULL, middle_name),
    paternal_surname = COALESCE(NULL, paternal_surname),
    maternal_surname = COALESCE(NULL, maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Michael Troncoso' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Michael Troncoso', 'ASSISTANT', NULL, NULL, NULL, NULL,
    NULL, NULL, NULL, NULL
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Michael Troncoso' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('15107608-4', rut),
    email = COALESCE('migelzamorano.2023@gmail.com', email),
    cargo = COALESCE('Chofer y Auxiliar', cargo),
    first_name = COALESCE('Miguel', first_name),
    middle_name = COALESCE('Angel', middle_name),
    paternal_surname = COALESCE('Zamorano', paternal_surname),
    maternal_surname = COALESCE('Aravena', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Miguel Zamorano' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Miguel Zamorano', 'DRIVER', NULL, '15107608-4', 'migelzamorano.2023@gmail.com', 'Chofer y Auxiliar',
    'Miguel', 'Angel', 'Zamorano', 'Aravena'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Miguel Zamorano' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('26804143-5', rut),
    email = COALESCE('milagrourd@yahoo.com', email),
    cargo = COALESCE('ASISTENTE RRHH', cargo),
    first_name = COALESCE('Milagro', first_name),
    middle_name = COALESCE('Del', middle_name),
    paternal_surname = COALESCE('Urdaneta', paternal_surname),
    maternal_surname = COALESCE('Coronel', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Milagro Urdaneta' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Milagro Urdaneta', 'UNASSIGNED', NULL, '26804143-5', 'milagrourd@yahoo.com', 'ASISTENTE RRHH',
    'Milagro', 'Del', 'Urdaneta', 'Coronel'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Milagro Urdaneta' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('15785123-3', rut),
    email = COALESCE('miltonalejandro2105@hotmail.com', email),
    cargo = COALESCE('Chofer y Auxiliar', cargo),
    first_name = COALESCE('Milton', first_name),
    middle_name = COALESCE('Alejandro', middle_name),
    paternal_surname = COALESCE('Castillo', paternal_surname),
    maternal_surname = COALESCE('Tapia', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Milton Castillo' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Milton Castillo', 'UNASSIGNED', NULL, '15785123-3', 'miltonalejandro2105@hotmail.com', 'Chofer y Auxiliar',
    'Milton', 'Alejandro', 'Castillo', 'Tapia'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Milton Castillo' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('NEW', contract_type),
    rut = COALESCE('20499043-3', rut),
    email = COALESCE('nelsonpv2000@gmail.com', email),
    cargo = COALESCE('Auxiliar Servicio Despacho', cargo),
    first_name = COALESCE('Nelson', first_name),
    middle_name = COALESCE('Exequiel', middle_name),
    paternal_surname = COALESCE('Paredes', paternal_surname),
    maternal_surname = COALESCE('Valdebenito', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Nelson Paredes' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Nelson Paredes', 'ASSISTANT', 'NEW', '20499043-3', 'nelsonpv2000@gmail.com', 'Auxiliar Servicio Despacho',
    'Nelson', 'Exequiel', 'Paredes', 'Valdebenito'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Nelson Paredes' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('17196134-3', rut),
    email = COALESCE('nsalamanca057@gmail.com', email),
    cargo = COALESCE('Asistente y Gestion Comercial', cargo),
    first_name = COALESCE('Nicole', first_name),
    middle_name = COALESCE('Paulina', middle_name),
    paternal_surname = COALESCE('Salamanca', paternal_surname),
    maternal_surname = COALESCE('Ortega', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Nicole Salamanca' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Nicole Salamanca', 'UNASSIGNED', NULL, '17196134-3', 'nsalamanca057@gmail.com', 'Asistente y Gestion Comercial',
    'Nicole', 'Paulina', 'Salamanca', 'Ortega'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Nicole Salamanca' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('13369413-7', rut),
    email = COALESCE('agustinrblokman@gmail.com', email),
    cargo = COALESCE('Chofer RS', cargo),
    first_name = COALESCE('Oscar', first_name),
    middle_name = COALESCE('Alfonso', middle_name),
    paternal_surname = COALESCE('Rabanal', paternal_surname),
    maternal_surname = COALESCE('Araneda', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Oscar Rabanal' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Oscar Rabanal', 'UNASSIGNED', NULL, '13369413-7', 'agustinrblokman@gmail.com', 'Chofer RS',
    'Oscar', 'Alfonso', 'Rabanal', 'Araneda'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Oscar Rabanal' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('NEW', contract_type),
    rut = COALESCE('27231597-3', rut),
    email = COALESCE('osmanutrix@gmail.com', email),
    cargo = COALESCE('auxiliar servicio', cargo),
    first_name = COALESCE('Osman', first_name),
    middle_name = COALESCE('Jose', middle_name),
    paternal_surname = COALESCE('Perez', paternal_surname),
    maternal_surname = COALESCE('Utriz', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Osman Perez' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Osman Perez', 'ASSISTANT', 'NEW', '27231597-3', 'osmanutrix@gmail.com', 'auxiliar servicio',
    'Osman', 'Jose', 'Perez', 'Utriz'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Osman Perez' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE(NULL, rut),
    email = COALESCE(NULL, email),
    cargo = COALESCE(NULL, cargo),
    first_name = COALESCE(NULL, first_name),
    middle_name = COALESCE(NULL, middle_name),
    paternal_surname = COALESCE(NULL, paternal_surname),
    maternal_surname = COALESCE(NULL, maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'PDF Worker' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'PDF Worker', 'DRIVER', NULL, NULL, NULL, NULL,
    NULL, NULL, NULL, NULL
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'PDF Worker' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('17150530-5', rut),
    email = COALESCE('pablogonzalezccti@gmail.com', email),
    cargo = COALESCE('Chofer RS', cargo),
    first_name = COALESCE('Pablo', first_name),
    middle_name = COALESCE('Eduardo', middle_name),
    paternal_surname = COALESCE('Gonzalez', paternal_surname),
    maternal_surname = COALESCE('Tapia', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Pablo Gonzalez' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Pablo Gonzalez', 'UNASSIGNED', NULL, '17150530-5', 'pablogonzalezccti@gmail.com', 'Chofer RS',
    'Pablo', 'Eduardo', 'Gonzalez', 'Tapia'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Pablo Gonzalez' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE(NULL, rut),
    email = COALESCE(NULL, email),
    cargo = COALESCE(NULL, cargo),
    first_name = COALESCE(NULL, first_name),
    middle_name = COALESCE(NULL, middle_name),
    paternal_surname = COALESCE(NULL, paternal_surname),
    maternal_surname = COALESCE(NULL, maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Pato Ramirez' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Pato Ramirez', 'ASSISTANT', NULL, NULL, NULL, NULL,
    NULL, NULL, NULL, NULL
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Pato Ramirez' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('OLD', contract_type),
    rut = COALESCE('8473758-5', rut),
    email = COALESCE('patricio.cubillos.sanchez@gmail.com', email),
    cargo = COALESCE('Chofer Servicio', cargo),
    first_name = COALESCE('Luis', first_name),
    middle_name = COALESCE('Patricio', middle_name),
    paternal_surname = COALESCE('Cubillos', paternal_surname),
    maternal_surname = COALESCE('Sanchez', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Patricio Cubillos' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Patricio Cubillos', 'DRIVER', 'OLD', '8473758-5', 'patricio.cubillos.sanchez@gmail.com', 'Chofer Servicio',
    'Luis', 'Patricio', 'Cubillos', 'Sanchez'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Patricio Cubillos' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('14506321-3', rut),
    email = COALESCE('patricioramirezcornejo269@gmail.com', email),
    cargo = COALESCE('auxiliar servicio', cargo),
    first_name = COALESCE('Bernardino', first_name),
    middle_name = COALESCE('Patricio', middle_name),
    paternal_surname = COALESCE('Ramirez', paternal_surname),
    maternal_surname = COALESCE('Cornejo', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Patricio Ramirez' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Patricio Ramirez', 'ASSISTANT', NULL, '14506321-3', 'patricioramirezcornejo269@gmail.com', 'auxiliar servicio',
    'Bernardino', 'Patricio', 'Ramirez', 'Cornejo'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Patricio Ramirez' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('14379050-9', rut),
    email = COALESCE('paulofrezn@gmail.com', email),
    cargo = COALESCE('Chofer y Auxiliar', cargo),
    first_name = COALESCE('Paulo', first_name),
    middle_name = COALESCE('Fernando', middle_name),
    paternal_surname = COALESCE('Frez', paternal_surname),
    maternal_surname = COALESCE('Nuñez', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Paulo Frez' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Paulo Frez', 'UNASSIGNED', NULL, '14379050-9', 'paulofrezn@gmail.com', 'Chofer y Auxiliar',
    'Paulo', 'Fernando', 'Frez', 'Nuñez'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Paulo Frez' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('NEW', contract_type),
    rut = COALESCE('7365216-2', rut),
    email = COALESCE('pedroarcos1721@gmail.com', email),
    cargo = COALESCE('Chofer y Auxiliar', cargo),
    first_name = COALESCE('Pedro', first_name),
    middle_name = COALESCE('Moises', middle_name),
    paternal_surname = COALESCE('Arcos', paternal_surname),
    maternal_surname = COALESCE('Miralles', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Pedro Arcos' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Pedro Arcos', 'ASSISTANT', 'NEW', '7365216-2', 'pedroarcos1721@gmail.com', 'Chofer y Auxiliar',
    'Pedro', 'Moises', 'Arcos', 'Miralles'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Pedro Arcos' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('NEW', contract_type),
    rut = COALESCE('7365216-2', rut),
    email = COALESCE('pedroarcos1721@gmail.com', email),
    cargo = COALESCE('Chofer y Auxiliar', cargo),
    first_name = COALESCE('Pedro', first_name),
    middle_name = COALESCE('Moises', middle_name),
    paternal_surname = COALESCE('Arcos', paternal_surname),
    maternal_surname = COALESCE('Miralles', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Pedro Arcos' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Pedro Arcos', 'DRIVER', 'NEW', '7365216-2', 'pedroarcos1721@gmail.com', 'Chofer y Auxiliar',
    'Pedro', 'Moises', 'Arcos', 'Miralles'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Pedro Arcos' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('26233919-K', rut),
    email = COALESCE('rafaelgarcia779911@gmail.com', email),
    cargo = COALESCE('Chofer y Auxiliar', cargo),
    first_name = COALESCE('Rafael', first_name),
    middle_name = COALESCE('Segundo', middle_name),
    paternal_surname = COALESCE('Garcia', paternal_surname),
    maternal_surname = COALESCE('Reyes', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Rafael Garcia' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Rafael Garcia', 'UNASSIGNED', NULL, '26233919-K', 'rafaelgarcia779911@gmail.com', 'Chofer y Auxiliar',
    'Rafael', 'Segundo', 'Garcia', 'Reyes'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Rafael Garcia' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('10834879-8', rut),
    email = COALESCE('rafelrodriguezcalderon1966@gmail.com', email),
    cargo = COALESCE('Chofer y Auxiliar', cargo),
    first_name = COALESCE('Rafael', first_name),
    middle_name = COALESCE(NULL, middle_name),
    paternal_surname = COALESCE('Rodriguez', paternal_surname),
    maternal_surname = COALESCE('Calderon', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Rafael Rodriguez' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Rafael Rodriguez', 'UNASSIGNED', NULL, '10834879-8', 'rafelrodriguezcalderon1966@gmail.com', 'Chofer y Auxiliar',
    'Rafael', NULL, 'Rodriguez', 'Calderon'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Rafael Rodriguez' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('12948312-1', rut),
    email = COALESCE('ramon.gallardo.estay@gmail.com', email),
    cargo = COALESCE('Chofer Servicio', cargo),
    first_name = COALESCE('Ramon', first_name),
    middle_name = COALESCE(NULL, middle_name),
    paternal_surname = COALESCE('Gallardo', paternal_surname),
    maternal_surname = COALESCE('Estay', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Ramon Gallardo' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Ramon Gallardo', 'DRIVER', NULL, '12948312-1', 'ramon.gallardo.estay@gmail.com', 'Chofer Servicio',
    'Ramon', NULL, 'Gallardo', 'Estay'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Ramon Gallardo' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('14347831-9', rut),
    email = COALESCE('reimoncortes31@gmail.com', email),
    cargo = COALESCE('Chofer y Auxiliar', cargo),
    first_name = COALESCE('Ramon', first_name),
    middle_name = COALESCE('Luis', middle_name),
    paternal_surname = COALESCE('Pereira', paternal_surname),
    maternal_surname = COALESCE('Cortes', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Ramon Pereira' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Ramon Pereira', 'UNASSIGNED', NULL, '14347831-9', 'reimoncortes31@gmail.com', 'Chofer y Auxiliar',
    'Ramon', 'Luis', 'Pereira', 'Cortes'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Ramon Pereira' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE(NULL, rut),
    email = COALESCE(NULL, email),
    cargo = COALESCE(NULL, cargo),
    first_name = COALESCE(NULL, first_name),
    middle_name = COALESCE(NULL, middle_name),
    paternal_surname = COALESCE(NULL, paternal_surname),
    maternal_surname = COALESCE(NULL, maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Raul Parra' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Raul Parra', 'DRIVER', NULL, NULL, NULL, NULL,
    NULL, NULL, NULL, NULL
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Raul Parra' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE(NULL, rut),
    email = COALESCE(NULL, email),
    cargo = COALESCE(NULL, cargo),
    first_name = COALESCE(NULL, first_name),
    middle_name = COALESCE(NULL, middle_name),
    paternal_surname = COALESCE(NULL, paternal_surname),
    maternal_surname = COALESCE(NULL, maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Raul Toledo' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Raul Toledo', 'ASSISTANT', NULL, NULL, NULL, NULL,
    NULL, NULL, NULL, NULL
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Raul Toledo' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('10889753-8', rut),
    email = COALESCE('richard_ortiz_@hotmail.com', email),
    cargo = COALESCE('Chofer RS', cargo),
    first_name = COALESCE('Richard', first_name),
    middle_name = COALESCE('Eugenio', middle_name),
    paternal_surname = COALESCE('Ortiz', paternal_surname),
    maternal_surname = COALESCE('Villablanca', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Richard Ortiz' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Richard Ortiz', 'UNASSIGNED', NULL, '10889753-8', 'richard_ortiz_@hotmail.com', 'Chofer RS',
    'Richard', 'Eugenio', 'Ortiz', 'Villablanca'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Richard Ortiz' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('NEW', contract_type),
    rut = COALESCE('16844647-0', rut),
    email = COALESCE('brionesroberto441@gmail.com', email),
    cargo = COALESCE('Chofer Servicio', cargo),
    first_name = COALESCE('Roberto', first_name),
    middle_name = COALESCE('Antonio', middle_name),
    paternal_surname = COALESCE('Briones', paternal_surname),
    maternal_surname = COALESCE('Belmar', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Roberto Briones' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Roberto Briones', 'ASSISTANT', 'NEW', '16844647-0', 'brionesroberto441@gmail.com', 'Chofer Servicio',
    'Roberto', 'Antonio', 'Briones', 'Belmar'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Roberto Briones' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('NEW', contract_type),
    rut = COALESCE('16844647-0', rut),
    email = COALESCE('brionesroberto441@gmail.com', email),
    cargo = COALESCE('Chofer Servicio', cargo),
    first_name = COALESCE('Roberto', first_name),
    middle_name = COALESCE('Antonio', middle_name),
    paternal_surname = COALESCE('Briones', paternal_surname),
    maternal_surname = COALESCE('Belmar', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Roberto Briones' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Roberto Briones', 'DRIVER', 'NEW', '16844647-0', 'brionesroberto441@gmail.com', 'Chofer Servicio',
    'Roberto', 'Antonio', 'Briones', 'Belmar'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Roberto Briones' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('OLD', contract_type),
    rut = COALESCE('14151649-3', rut),
    email = COALESCE('ramitarobert21@gmail.com', email),
    cargo = COALESCE('Chofer Servicio', cargo),
    first_name = COALESCE('Roberto', first_name),
    middle_name = COALESCE('Fernando', middle_name),
    paternal_surname = COALESCE('Ramirez', paternal_surname),
    maternal_surname = COALESCE('Gomez', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Roberto Ramirez' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Roberto Ramirez', 'DRIVER', 'OLD', '14151649-3', 'ramitarobert21@gmail.com', 'Chofer Servicio',
    'Roberto', 'Fernando', 'Ramirez', 'Gomez'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Roberto Ramirez' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('18424055-6', rut),
    email = COALESCE('rodrigo.arcos.barrera24@gmail.com', email),
    cargo = COALESCE('Auxiliar Servicio Despacho', cargo),
    first_name = COALESCE('Rodrigo', first_name),
    middle_name = COALESCE('Moises', middle_name),
    paternal_surname = COALESCE('Arcos', paternal_surname),
    maternal_surname = COALESCE('Barrera', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Rodrigo Arcos' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Rodrigo Arcos', 'ASSISTANT', NULL, '18424055-6', 'rodrigo.arcos.barrera24@gmail.com', 'Auxiliar Servicio Despacho',
    'Rodrigo', 'Moises', 'Arcos', 'Barrera'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Rodrigo Arcos' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('14191662-9', rut),
    email = COALESCE('arenasrodrigoarenas65@gmail.com', email),
    cargo = COALESCE('auxiliar servicio', cargo),
    first_name = COALESCE('Rodrigo', first_name),
    middle_name = COALESCE('Alejandro', middle_name),
    paternal_surname = COALESCE('Arenas', paternal_surname),
    maternal_surname = COALESCE('Arenas', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Rodrigo Arenas' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Rodrigo Arenas', 'ASSISTANT', NULL, '14191662-9', 'arenasrodrigoarenas65@gmail.com', 'auxiliar servicio',
    'Rodrigo', 'Alejandro', 'Arenas', 'Arenas'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Rodrigo Arenas' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('NEW', contract_type),
    rut = COALESCE('9705032-5', rut),
    email = COALESCE('rodrigobascunan1@gmail.com', email),
    cargo = COALESCE('Chofer y Auxiliar', cargo),
    first_name = COALESCE('Rodrigo', first_name),
    middle_name = COALESCE('Alonso', middle_name),
    paternal_surname = COALESCE('Bascuñan', paternal_surname),
    maternal_surname = COALESCE('Avio', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Rodrigo Bascuñan' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Rodrigo Bascuñan', 'ASSISTANT', 'NEW', '9705032-5', 'rodrigobascunan1@gmail.com', 'Chofer y Auxiliar',
    'Rodrigo', 'Alonso', 'Bascuñan', 'Avio'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Rodrigo Bascuñan' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('NEW', contract_type),
    rut = COALESCE('9705032-5', rut),
    email = COALESCE('rodrigobascunan1@gmail.com', email),
    cargo = COALESCE('Chofer y Auxiliar', cargo),
    first_name = COALESCE('Rodrigo', first_name),
    middle_name = COALESCE('Alonso', middle_name),
    paternal_surname = COALESCE('Bascuñan', paternal_surname),
    maternal_surname = COALESCE('Avio', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Rodrigo Bascuñan' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Rodrigo Bascuñan', 'DRIVER', 'NEW', '9705032-5', 'rodrigobascunan1@gmail.com', 'Chofer y Auxiliar',
    'Rodrigo', 'Alonso', 'Bascuñan', 'Avio'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Rodrigo Bascuñan' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('12945675-2', rut),
    email = COALESCE('rodrigo.urrutian@gmail.com', email),
    cargo = COALESCE('auxiliar servicio', cargo),
    first_name = COALESCE('Rodrigo', first_name),
    middle_name = COALESCE('Alejandro', middle_name),
    paternal_surname = COALESCE('Urrutia', paternal_surname),
    maternal_surname = COALESCE('Nuñez', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Rodrigo Urrutia' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Rodrigo Urrutia', 'UNASSIGNED', NULL, '12945675-2', 'rodrigo.urrutian@gmail.com', 'auxiliar servicio',
    'Rodrigo', 'Alejandro', 'Urrutia', 'Nuñez'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Rodrigo Urrutia' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE(NULL, rut),
    email = COALESCE(NULL, email),
    cargo = COALESCE(NULL, cargo),
    first_name = COALESCE(NULL, first_name),
    middle_name = COALESCE(NULL, middle_name),
    paternal_surname = COALESCE(NULL, paternal_surname),
    maternal_surname = COALESCE(NULL, maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Rody Osorio' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Rody Osorio', 'DRIVER', NULL, NULL, NULL, NULL,
    NULL, NULL, NULL, NULL
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Rody Osorio' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('14518395-2', rut),
    email = COALESCE('ronaldnunez081@gmail.com', email),
    cargo = COALESCE('Chofer RS', cargo),
    first_name = COALESCE('Ronald', first_name),
    middle_name = COALESCE('Francisco', middle_name),
    paternal_surname = COALESCE('Nuñez', paternal_surname),
    maternal_surname = COALESCE('Araya', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Ronald Nuñez' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Ronald Nuñez', 'UNASSIGNED', NULL, '14518395-2', 'ronaldnunez081@gmail.com', 'Chofer RS',
    'Ronald', 'Francisco', 'Nuñez', 'Araya'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Ronald Nuñez' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('17850134-8', rut),
    email = COALESCE('farias.seba91@gamil.com', email),
    cargo = COALESCE('Auxiliar de Patio', cargo),
    first_name = COALESCE('Sebastian', first_name),
    middle_name = COALESCE('Daniel', middle_name),
    paternal_surname = COALESCE('Farias', paternal_surname),
    maternal_surname = COALESCE('Garcia', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Sebastian Farias' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Sebastian Farias', 'UNASSIGNED', NULL, '17850134-8', 'farias.seba91@gamil.com', 'Auxiliar de Patio',
    'Sebastian', 'Daniel', 'Farias', 'Garcia'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Sebastian Farias' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE(NULL, rut),
    email = COALESCE(NULL, email),
    cargo = COALESCE(NULL, cargo),
    first_name = COALESCE(NULL, first_name),
    middle_name = COALESCE(NULL, middle_name),
    paternal_surname = COALESCE(NULL, paternal_surname),
    maternal_surname = COALESCE(NULL, maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Sergio Toledo' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Sergio Toledo', 'ASSISTANT', NULL, NULL, NULL, NULL,
    NULL, NULL, NULL, NULL
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Sergio Toledo' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE(NULL, rut),
    email = COALESCE(NULL, email),
    cargo = COALESCE(NULL, cargo),
    first_name = COALESCE(NULL, first_name),
    middle_name = COALESCE(NULL, middle_name),
    paternal_surname = COALESCE(NULL, paternal_surname),
    maternal_surname = COALESCE(NULL, maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Sin Operador' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Sin Operador', 'DRIVER', NULL, NULL, NULL, NULL,
    NULL, NULL, NULL, NULL
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Sin Operador' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE('OLD', contract_type),
    rut = COALESCE('14128269-7', rut),
    email = COALESCE('vitocko1981@gmail.com', email),
    cargo = COALESCE('auxiliar servicio', cargo),
    first_name = COALESCE('Victor', first_name),
    middle_name = COALESCE('German', middle_name),
    paternal_surname = COALESCE('Araneda', paternal_surname),
    maternal_surname = COALESCE('Figueroa', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Victor Araneda' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Victor Araneda', 'ASSISTANT', 'OLD', '14128269-7', 'vitocko1981@gmail.com', 'auxiliar servicio',
    'Victor', 'German', 'Araneda', 'Figueroa'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Victor Araneda' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('8869419-8', rut),
    email = COALESCE('victor.reyesvivanco@gmail.com', email),
    cargo = COALESCE('Chofer Servicio', cargo),
    first_name = COALESCE('Victor', first_name),
    middle_name = COALESCE('Manuel', middle_name),
    paternal_surname = COALESCE('Reyes', paternal_surname),
    maternal_surname = COALESCE('Vivanco', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Victor Reyes' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Victor Reyes', 'ASSISTANT', NULL, '8869419-8', 'victor.reyesvivanco@gmail.com', 'Chofer Servicio',
    'Victor', 'Manuel', 'Reyes', 'Vivanco'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Victor Reyes' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('8869419-8', rut),
    email = COALESCE('victor.reyesvivanco@gmail.com', email),
    cargo = COALESCE('Chofer Servicio', cargo),
    first_name = COALESCE('Victor', first_name),
    middle_name = COALESCE('Manuel', middle_name),
    paternal_surname = COALESCE('Reyes', paternal_surname),
    maternal_surname = COALESCE('Vivanco', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Victor Reyes' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Victor Reyes', 'DRIVER', NULL, '8869419-8', 'victor.reyesvivanco@gmail.com', 'Chofer Servicio',
    'Victor', 'Manuel', 'Reyes', 'Vivanco'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Victor Reyes' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'DRIVER' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('27968336-6', rut),
    email = COALESCE('dannyvilla1982@gmail.com', email),
    cargo = COALESCE('auxiliar servicio', cargo),
    first_name = COALESCE('Wilmer', first_name),
    middle_name = COALESCE('Danny', middle_name),
    paternal_surname = COALESCE('Villa', paternal_surname),
    maternal_surname = COALESCE('Belleza', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Wilmer Villa' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Wilmer Villa', 'ASSISTANT', NULL, '27968336-6', 'dannyvilla1982@gmail.com', 'auxiliar servicio',
    'Wilmer', 'Danny', 'Villa', 'Belleza'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Wilmer Villa' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('24460411-0', rut),
    email = COALESCE('saavedrawilson145@gmail.com', email),
    cargo = COALESCE('Chofer de Servicio y Despacho', cargo),
    first_name = COALESCE('Wilson', first_name),
    middle_name = COALESCE(NULL, middle_name),
    paternal_surname = COALESCE('Saavedra', paternal_surname),
    maternal_surname = COALESCE('Roa', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Wilson Saavedra' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Wilson Saavedra', 'UNASSIGNED', NULL, '24460411-0', 'saavedrawilson145@gmail.com', 'Chofer de Servicio y Despacho',
    'Wilson', NULL, 'Saavedra', 'Roa'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Wilson Saavedra' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('16537331-6', rut),
    email = COALESCE('yennytta@gmail.com', email),
    cargo = COALESCE('Asistente Servicio', cargo),
    first_name = COALESCE('Yennyfer', first_name),
    middle_name = COALESCE('Andre', middle_name),
    paternal_surname = COALESCE('Gatica', paternal_surname),
    maternal_surname = COALESCE('Leiva', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Yennyfer Gatica' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Yennyfer Gatica', 'UNASSIGNED', NULL, '16537331-6', 'yennytta@gmail.com', 'Asistente Servicio',
    'Yennyfer', 'Andre', 'Gatica', 'Leiva'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Yennyfer Gatica' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'UNASSIGNED' COLLATE utf8mb4_unicode_ci);

UPDATE payroll_employees
SET
    contract_type = COALESCE(NULL, contract_type),
    rut = COALESCE('27141631-8', rut),
    email = COALESCE('yosmanismail1701@gmail.com', email),
    cargo = COALESCE('auxiliar servicio', cargo),
    first_name = COALESCE('Yosman', first_name),
    middle_name = COALESCE('Jose', middle_name),
    paternal_surname = COALESCE('Perez', paternal_surname),
    maternal_surname = COALESCE('Diaz', maternal_surname)
WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Yosman Perez' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci;

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    'Yosman Perez', 'ASSISTANT', NULL, '27141631-8', 'yosmanismail1701@gmail.com', 'auxiliar servicio',
    'Yosman', 'Jose', 'Perez', 'Diaz'
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM payroll_employees WHERE employee_name COLLATE utf8mb4_unicode_ci = 'Yosman Perez' COLLATE utf8mb4_unicode_ci AND role_type COLLATE utf8mb4_unicode_ci = 'ASSISTANT' COLLATE utf8mb4_unicode_ci);

COMMIT;

SELECT COUNT(*) AS total_workers_after_merge FROM payroll_employees;
SELECT COUNT(*) AS workers_with_rut_after_merge FROM payroll_employees WHERE rut IS NOT NULL AND TRIM(rut) <> ''; 
SELECT COUNT(*) AS workers_with_email_after_merge FROM payroll_employees WHERE email IS NOT NULL AND TRIM(email) <> ''; 
