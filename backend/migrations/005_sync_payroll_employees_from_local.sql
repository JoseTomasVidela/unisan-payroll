-- Sincroniza SOLO trabajadores desde la base local hacia Azure/MySQL.
-- No toca payroll_cycles, payroll_imports, payroll_records ni datos de liquidaciones.
SET NAMES utf8mb4;
USE unisan_db;

SET @has_column := (
    SELECT COUNT(*)
    FROM information_schema.columns
    WHERE table_schema = DATABASE()
      AND table_name = 'payroll_employees'
      AND column_name = 'contract_type'
);
SET @ddl := IF(@has_column = 0, 'ALTER TABLE payroll_employees ADD COLUMN contract_type VARCHAR(16) NULL', 'SELECT 1');
PREPARE stmt FROM @ddl;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @has_column := (
    SELECT COUNT(*)
    FROM information_schema.columns
    WHERE table_schema = DATABASE()
      AND table_name = 'payroll_employees'
      AND column_name = 'rut'
);
SET @ddl := IF(@has_column = 0, 'ALTER TABLE payroll_employees ADD COLUMN rut VARCHAR(32) NULL', 'SELECT 1');
PREPARE stmt FROM @ddl;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @has_column := (
    SELECT COUNT(*)
    FROM information_schema.columns
    WHERE table_schema = DATABASE()
      AND table_name = 'payroll_employees'
      AND column_name = 'email'
);
SET @ddl := IF(@has_column = 0, 'ALTER TABLE payroll_employees ADD COLUMN email VARCHAR(255) NULL', 'SELECT 1');
PREPARE stmt FROM @ddl;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @has_column := (
    SELECT COUNT(*)
    FROM information_schema.columns
    WHERE table_schema = DATABASE()
      AND table_name = 'payroll_employees'
      AND column_name = 'cargo'
);
SET @ddl := IF(@has_column = 0, 'ALTER TABLE payroll_employees ADD COLUMN cargo VARCHAR(180) NULL', 'SELECT 1');
PREPARE stmt FROM @ddl;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @has_column := (
    SELECT COUNT(*)
    FROM information_schema.columns
    WHERE table_schema = DATABASE()
      AND table_name = 'payroll_employees'
      AND column_name = 'first_name'
);
SET @ddl := IF(@has_column = 0, 'ALTER TABLE payroll_employees ADD COLUMN first_name VARCHAR(80) NULL', 'SELECT 1');
PREPARE stmt FROM @ddl;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @has_column := (
    SELECT COUNT(*)
    FROM information_schema.columns
    WHERE table_schema = DATABASE()
      AND table_name = 'payroll_employees'
      AND column_name = 'middle_name'
);
SET @ddl := IF(@has_column = 0, 'ALTER TABLE payroll_employees ADD COLUMN middle_name VARCHAR(80) NULL', 'SELECT 1');
PREPARE stmt FROM @ddl;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @has_column := (
    SELECT COUNT(*)
    FROM information_schema.columns
    WHERE table_schema = DATABASE()
      AND table_name = 'payroll_employees'
      AND column_name = 'paternal_surname'
);
SET @ddl := IF(@has_column = 0, 'ALTER TABLE payroll_employees ADD COLUMN paternal_surname VARCHAR(80) NULL', 'SELECT 1');
PREPARE stmt FROM @ddl;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @has_column := (
    SELECT COUNT(*)
    FROM information_schema.columns
    WHERE table_schema = DATABASE()
      AND table_name = 'payroll_employees'
      AND column_name = 'maternal_surname'
);
SET @ddl := IF(@has_column = 0, 'ALTER TABLE payroll_employees ADD COLUMN maternal_surname VARCHAR(80) NULL', 'SELECT 1');
PREPARE stmt FROM @ddl;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

DROP TEMPORARY TABLE IF EXISTS payroll_employee_sync_stage;
CREATE TEMPORARY TABLE payroll_employee_sync_stage (
    employee_name VARCHAR(180) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
    role_type VARCHAR(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
    contract_type VARCHAR(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
    rut VARCHAR(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
    email VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
    cargo VARCHAR(180) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
    first_name VARCHAR(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
    middle_name VARCHAR(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
    paternal_surname VARCHAR(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
    maternal_surname VARCHAR(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
    PRIMARY KEY (employee_name, role_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO payroll_employee_sync_stage (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
) VALUES
    ('Abel Tapia', 'DRIVER', 'NEW', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    ('Abraham Lucas', 'UNASSIGNED', NULL, '23499257-0', 'abraham.lucas.07@gmail.com', 'Chofer de Servicio y Despacho', 'Abraham', NULL, 'Lucas', 'Lizete'),
    ('Alan Bravo', 'UNASSIGNED', NULL, '16428519-7', 'alan.bravo.h@gmail.com', 'Chofer RS', 'Alan', 'Omar', 'Bravo', 'Herrera'),
    ('Albert Riveros', 'DRIVER', 'OLD', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    ('Alejandro Escoar', 'ASSISTANT', 'OLD', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    ('Alejandro Escobar', 'ASSISTANT', 'OLD', '19546813-3', 'ae5952575@gmail.com', 'auxiliar servicio', 'Alejandro', 'Fabian', 'Escobar', 'Rojas'),
    ('Alejandro Osorio', 'ASSISTANT', 'OLD', '17072087-3', 'raocjpc@gmail.com', 'auxiliar servicio', 'Alejandro', 'Enrique', 'Osorio', 'Gatica'),
    ('Alexa Figueroa', 'UNASSIGNED', NULL, '25912978-8', 'chela2015fg@gmail.com', 'Asistente de Serv y Despac', 'Alexa', 'Coromoto', 'Figueroa', 'Gonzalez'),
    ('Alexander Marchant', 'ASSISTANT', 'OLD', '19165687-3', 'aleyflorencia07@gmail.com', 'auxiliar servicio', 'Alexander', 'Esteban', 'Marchant', 'Roldan'),
    ('Alexander Marchant', 'DRIVER', 'OLD', '19165687-3', 'aleyflorencia07@gmail.com', 'auxiliar servicio', 'Alexander', 'Esteban', 'Marchant', 'Roldan'),
    ('Alexis Carvajal', 'UNASSIGNED', NULL, '17655668-4', 'alexis.carvajalg@gmail.com', 'Chofer Servicio', 'Alexis', 'Michael', 'Carvajal', 'Gajardo'),
    ('Alfredo Cona', 'ASSISTANT', 'NEW', '17623103-3', 'alfredocona28@gmail.com', 'Chofer Servicio', 'Alfredo', 'Alejandro', 'Cona', 'Soto'),
    ('Alfredo Cona', 'DRIVER', 'NEW', '17623103-3', 'alfredocona28@gmail.com', 'Chofer Servicio', 'Alfredo', 'Alejandro', 'Cona', 'Soto'),
    ('Andres Moya', 'ASSISTANT', NULL, '15424797-1', 'granizooo234@gmail.com', 'Auxiliar Despacho', 'Andres', 'Cristian', 'Moya', 'Gonzalez'),
    ('Andres Moya', 'DRIVER', NULL, '15424797-1', 'granizooo234@gmail.com', 'Auxiliar Despacho', 'Andres', 'Cristian', 'Moya', 'Gonzalez'),
    ('Angelo Rivera', 'UNASSIGNED', NULL, '17069748-0', 'angeloty125@gmail.com', 'Chofer RS', 'Angelo', 'Ariel', 'Rivera', 'Rojas'),
    ('Antonio Palma', 'ASSISTANT', NULL, '10605996-9', '008antoniopalma@gmail.com', 'auxiliar servicio', 'Antonio', 'Enrique', 'Palma', 'Gomez'),
    ('Antonio Riquelme', 'ASSISTANT', NULL, '16802037-6', 'mauricio.riquelme08@gmail.com', 'Chofer RS', 'Antonio', 'Ernesto', 'Riquelme', 'Astorga'),
    ('Antonio Riquelme', 'DRIVER', NULL, '16802037-6', 'mauricio.riquelme08@gmail.com', 'Chofer RS', 'Antonio', 'Ernesto', 'Riquelme', 'Astorga'),
    ('Boris Lopez', 'DRIVER', 'OLD', '12112657-5', 'claudia.itu78@gmail.com', 'Chofer Servicio', 'Boris', 'Hernan', 'Lopez', 'Alvarado'),
    ('Boris López', 'ASSISTANT', 'OLD', '12112657-5', 'claudia.itu78@gmail.com', 'Chofer Servicio', 'Boris', 'Hernan', 'Lopez', 'Alvarado'),
    ('Boris López', 'DRIVER', 'OLD', '12112657-5', 'claudia.itu78@gmail.com', 'Chofer Servicio', 'Boris', 'Hernan', 'Lopez', 'Alvarado'),
    ('Byron Lopez', 'DRIVER', 'NEW', '18838547-8', 'jopsanandres@gmail.com', 'Chofer Servicio', 'Byron', 'Andres', 'Lopez', 'Muñoz'),
    ('Byron López', 'DRIVER', 'NEW', '18838547-8', 'jopsanandres@gmail.com', 'Chofer Servicio', 'Byron', 'Andres', 'Lopez', 'Muñoz'),
    ('Carlos Correa', 'ASSISTANT', 'NEW', '20142692-8', 'alexander9carlos@gmail.com', 'auxiliar servicio', 'Carlos', 'Alexander', 'Correa', 'Chacana'),
    ('Carlos Jimenez', 'UNASSIGNED', NULL, '17092663-3', 'car.jimenezgonzalez8@gmail.com', 'Chofer Servicio', 'Carlos', 'Roberto', 'Jimenez', 'Gonzalez'),
    ('Carlos Maulen', 'ASSISTANT', NULL, '18947060-6', 'carlosmaulen94@gmail.com', 'Chofer y Auxiliar', 'Carlos', 'Hernan', 'Maulen', 'Cepeda'),
    ('Carlos Maulen', 'DRIVER', NULL, '18947060-6', 'carlosmaulen94@gmail.com', 'Chofer y Auxiliar', 'Carlos', 'Hernan', 'Maulen', 'Cepeda'),
    ('Cesar Moreno', 'DRIVER', 'OLD', '15334781-6', 'cesarmorenor69@gmail.com', 'Chofer Servicio', 'Cesar', 'Antonio', 'Moreno', 'Riveros'),
    ('Christian Araya', 'UNASSIGNED', NULL, '21023272-9', 'christianarayarivas45692@gmail.com', 'auxiliar servicio', 'Christian', 'Alejandro', 'Araya', 'Rivas'),
    ('Claudio Arenas', 'UNASSIGNED', NULL, '15460715-3', 'claudioarenas.a@gmail.com', 'Asistente de Serv y Despac', 'Claudio', 'Antonio', 'Arenas', 'Arenas'),
    ('Claudio Cardenas', 'UNASSIGNED', NULL, '16850588-4', 'cardenasclaudio051@gmail.com', 'Auxiliar de Patio', 'Claudio', 'Edgardo', 'Cardenas', 'Cardenas'),
    ('Claudio Garrdo', 'DRIVER', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    ('Claudio Garrido', 'ASSISTANT', NULL, '12876513-1', 'clauditocares7.0@gmail.com', 'Chofer y Auxiliar', 'Claudio', 'Luis', 'Garrido', 'Cares'),
    ('Claudio Garrido', 'DRIVER', NULL, '12876513-1', 'clauditocares7.0@gmail.com', 'Chofer y Auxiliar', 'Claudio', 'Luis', 'Garrido', 'Cares'),
    ('Cristian Araya', 'ASSISTANT', 'OLD', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    ('Cristian Araya', 'DRIVER', 'OLD', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    ('Cristian Diaz', 'UNASSIGNED', NULL, '12649756-3', 'cristian.diazmedina17@gmail.com', 'Chofer de Unibox', 'Cristian', NULL, 'Diaz', 'Medina'),
    ('Cristian Gonzalez', 'ASSISTANT', 'OLD', '15424797-1', 'granizooo234@gmail.com', 'Auxiliar Despacho', 'Cristian', 'Fabian', 'Gonzalez', 'Rodriguez'),
    ('Cristian Gonzalez', 'DRIVER', 'OLD', '15424797-1', 'granizooo234@gmail.com', 'Auxiliar Despacho', 'Cristian', 'Fabian', 'Gonzalez', 'Rodriguez'),
    ('Cristian Lobos', 'UNASSIGNED', NULL, '17337566-2', 'loboscristian.16@gmail.com', 'Chofer de Unibox', 'Cristian', 'Andres', 'Lobos', 'Valdes'),
    ('Cristian Valdivia', 'ASSISTANT', NULL, '13499219-0', 'kristianvaldivia1978@gmail.com', 'Chofer Servicio', 'Cristian', 'Andres', 'Valdivia', 'Zamorano'),
    ('Cristian Valdivia', 'DRIVER', NULL, '13499219-0', 'kristianvaldivia1978@gmail.com', 'Chofer Servicio', 'Cristian', 'Andres', 'Valdivia', 'Zamorano'),
    ('Cristobal Ramos', 'UNASSIGNED', NULL, '21239566-8', 'bobalabraham@gmail.com', 'Auxiliar Servicio Despacho', 'Cristobal', 'Abraham', 'Ramos', 'Gallardo'),
    ('Cristofer Troncoso', 'UNASSIGNED', NULL, '18946469-K', 'cristofertroncoso56@gmail.com', 'Chofer Servicio', 'Cristofer', 'Angel', 'Troncoso', 'Catalan'),
    ('Cristopher Muñoz', 'UNASSIGNED', NULL, '17109462-3', 'cris.munoz1524@gmail.com', 'Chofer de Unibox', 'Cristopher', NULL, 'Muñoz', 'Arevalo'),
    ('Daiel Diaz', 'DRIVER', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    ('Daniel Diaz', 'ASSISTANT', 'NEW', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    ('Daniel Diaz', 'DRIVER', 'NEW', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    ('Daniel Escobar', 'ASSISTANT', 'NEW', '18461720-K', 'daniel.escobark03@gmail.com', 'Auxiliar Servicio Despacho', 'Daniel', 'Ignacio', 'Escobar', 'Krausmann'),
    ('Daniel Peña', 'ASSISTANT', NULL, '13061923-1', 'danielp2706@yahoo.com', 'Chofer Despacho', 'Daniel', NULL, 'Peña', 'Bravo'),
    ('Daniel Peña', 'DRIVER', NULL, '13061923-1', 'danielp2706@yahoo.com', 'Chofer Despacho', 'Daniel', NULL, 'Peña', 'Bravo'),
    ('Deivis Santana', 'ASSISTANT', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    ('Edgar Benavides', 'ASSISTANT', 'NEW', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    ('Edgar Benavides', 'DRIVER', 'NEW', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    ('Edgard Benavides', 'UNASSIGNED', NULL, '18332258-3', 'edgardalex2304@gmail.com', 'Chofer y Auxiliar', 'Edgard', 'Alex', 'Benavides', 'Opazo'),
    ('Edson Ferreira', 'UNASSIGNED', NULL, '25590805-7', 'edsonferr476@gmail.com', 'Auxiliar Servicio Despacho', 'Edson', NULL, 'Ferreira', 'Sandoval'),
    ('Eduardo Monroy', 'UNASSIGNED', NULL, '13180820-8', 'edomonrroy.0806@hotmail.com', 'Chofer de Servicio y Despacho', 'Eduardo', 'Antonio', 'Monroy', 'Velasquez'),
    ('Eduardo Soto', 'ASSISTANT', NULL, '13282140-2', 'esotog1977@gmail.com', 'Chofer y Auxiliar', 'Juan', 'Eduardo', 'Soto', 'Guajardo'),
    ('Eduardo Soto', 'DRIVER', NULL, '13282140-2', 'esotog1977@gmail.com', 'Chofer y Auxiliar', 'Juan', 'Eduardo', 'Soto', 'Guajardo'),
    ('Elias Llancaqueo', 'ASSISTANT', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    ('Elias Llancaqueo', 'DRIVER', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    ('Emanuel Diaz', 'UNASSIGNED', NULL, '17071056-8', 'emanxel.diaz0815@gmail.com', 'Chofer RS', 'Emanuel', 'Alejandro', 'Diaz', 'Saavedra'),
    ('Enzo Chorolque', 'UNASSIGNED', NULL, '25400155-4', 'enzoe.chorolque@gmail.com', 'Chofer Servicio', 'Enzo', 'Esteban', 'Chorolque', 'Cuestas'),
    ('Eugenio Muñoz', 'UNASSIGNED', NULL, '13180945-K', 'eugenio.mc@hotmail.com', 'Auxiliar Servicio Despacho', 'Eugenio', 'Del', 'Muñoz', 'Campos'),
    ('Felipe Jimenez', 'UNASSIGNED', NULL, '20525558-3', 'f.jimenezd33@gmail.com', 'Auxiliar Servicio Despacho', 'Felipe', 'Ignacio', 'Jimenez', 'Diaz'),
    ('Fernando Diaz', 'ASSISTANT', 'NEW', '9462722-2', 'fernandodiazsepulveda62@gmail.com', 'Chofer y Auxiliar', 'Fernando', 'Aquiles', 'Diaz', 'Sepulveda'),
    ('Fernando Diaz', 'DRIVER', 'NEW', '9462722-2', 'fernandodiazsepulveda62@gmail.com', 'Chofer y Auxiliar', 'Fernando', 'Aquiles', 'Diaz', 'Sepulveda'),
    ('Fernando Ortiz', 'UNASSIGNED', NULL, '9205268-0', 'aridosespress@gmail.com', 'Chofer Servicio', 'Fernando', 'Arturo', 'Ortiz', 'Castillo'),
    ('Francisco Cuevas', 'DRIVER', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    ('Francisco Vega', 'UNASSIGNED', NULL, '16868232-8', 'vegaherrerafrancisco@gmail.com', 'Chofer Servicio', 'Francisco', 'Javier', 'Vega', 'Herrera'),
    ('Frank Alvarez', 'UNASSIGNED', NULL, '27063200-9', 'leones5353fa@gmail.com', 'Auxiliar de Aseo', 'Frank', 'Alexis', 'Alvarez', 'Melendez'),
    ('Freddy Ramos', 'UNASSIGNED', NULL, '12964068-5', 'alexisfre339@gmail.com', 'Chofer y Auxiliar', 'Freddy', 'Alexis', 'Ramos', 'Labrin'),
    ('Gerald Aguayo', 'ASSISTANT', 'NEW', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    ('Gerald Paredes', 'ASSISTANT', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    ('Gerard Aguayo', 'UNASSIGNED', NULL, '20334945-9', 'geraldaguayo03@gmail.com', 'Auxiliar Servicio Despacho', 'Gerard', 'Diego', 'Aguayo', 'Perez'),
    ('Gerardo Cartes', 'DRIVER', NULL, '16143616-K', 'g.cartes.avila@gmail.com', 'Chofer Despacho', 'Gerardo', NULL, 'Cartes', 'Avila'),
    ('Gilmar Ospino', 'ASSISTANT', 'NEW', '27891710-K', 'gilmarospino0619@gmail.com', 'auxiliar servicio', 'Gilmar', 'Andres', 'Ospino', 'Perea'),
    ('Gilmar Ospino', 'DRIVER', 'NEW', '27891710-K', 'gilmarospino0619@gmail.com', 'auxiliar servicio', 'Gilmar', 'Andres', 'Ospino', 'Perea'),
    ('Gino Tineo', 'UNASSIGNED', NULL, '23701491-K', 'gtineo.20zamudio@gmail.com', 'Chofer RS', 'Gino', 'Cesar', 'Tineo', 'Zamudio'),
    ('Gonzalo Gonzalez', 'ASSISTANT', 'OLD', '26450684-0', 'chalito1077@gmail.com', 'auxiliar servicio', 'Gonzalo', NULL, 'Gonzalez', 'Meneses'),
    ('Hjorge Vizcarra', 'ASSISTANT', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    ('Hugo Troncoso', 'ASSISTANT', NULL, '15416728-5', 'hugotroncoso139@yahoo.es', 'auxiliar servicio', 'Hugo', 'Antonio', 'Troncoso', 'Catalan'),
    ('Ignacio Villaroel', 'UNASSIGNED', NULL, '21893971-6', 'i.villarroel2305@gmail.com', 'Auxiliar Servicio Despacho', 'Ignacio', 'Alfredo', 'Villaroel', 'Orellana'),
    ('Jaime Condori', 'UNASSIGNED', NULL, '23671952-9', 'jaicon91ab@hotmail.com', 'Chofer de Servicio y Despacho', 'Jaime', NULL, 'Condori', 'Vargas'),
    ('Javier Prado', 'UNASSIGNED', NULL, '11506439-8', 'japraco@hotmail.com', 'auxiliar servicio', 'Javier', 'Antonio', 'Prado', 'Cornejo'),
    ('Jeremias Cerda', 'ASSISTANT', NULL, '18344143-4', 'jeremiascerda1993@gmail.com', 'auxiliar servicio', 'Jeremias', 'Esteban', 'Cerda', 'Vega'),
    ('Jeremias Cerda', 'DRIVER', NULL, '18344143-4', 'jeremiascerda1993@gmail.com', 'auxiliar servicio', 'Jeremias', 'Esteban', 'Cerda', 'Vega'),
    ('Jesus Barrera', 'ASSISTANT', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    ('Johan Torres', 'UNASSIGNED', NULL, '26835778-5', 'johantorres22.1985@gmail.com', 'Chofer Servicio', 'Johan', 'Ferley', 'Torres', 'Ramirez'),
    ('Jonathan Gajardo', 'UNASSIGNED', NULL, '16260494-5', 'jonathanegajardo@gmail.com', 'Chofer Servicio', 'Jonathan', 'Eduardo', 'Gajardo', 'Plaza'),
    ('Jonathan Reyes', 'UNASSIGNED', NULL, '15619238-4', 'jonathan.reyes26@gmail.com', 'Chofer RS', 'Jonathan', 'Luis', 'Reyes', 'Valdebenito'),
    ('Jordan Gaete', 'ASSISTANT', 'NEW', '18562616-4', 'jordan.gaete.donaire@gmail.com', 'auxiliar servicio', 'Jordan', NULL, 'Gaete', 'Donaire'),
    ('Jorge Viscarra', 'ASSISTANT', NULL, '16456021-K', 'jorviscarrasco1987@gmail.com', 'auxiliar servicio', 'Jorge', 'Luis', 'Viscarra', 'Carrasco'),
    ('Jorge Vizcarra', 'ASSISTANT', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    ('Jose Arredondo', 'DRIVER', NULL, '11890417-6', 'josearredondogonzalez227@gmail.com', 'Chofer y Auxiliar', 'Jose', 'Manuel', 'Arredondo', 'Gonzalez'),
    ('Jose Oca', 'ASSISTANT', 'OLD', '26017411-8', 'joseangelocag@gmail.com', 'auxiliar servicio', 'Jose', 'Angel', 'Oca', 'Gonzalez'),
    ('Josue Barra', 'UNASSIGNED', NULL, '24361952-1', 'joshuabarraking@gmail.com', 'Auxiliar Servicio Despacho', 'Josue', 'Evaristo', 'Barra', 'Poma'),
    ('José Arredondo', 'DRIVER', NULL, '11890417-6', 'josearredondogonzalez227@gmail.com', 'Chofer y Auxiliar', 'Jose', 'Manuel', 'Arredondo', 'Gonzalez'),
    ('José Soto Catalan', 'DRIVER', NULL, '10590216-6', 'josepatriciosoto23@gmail.com', 'Chofer Servicio', 'Jose', 'Patricio', 'Soto', 'Catalan'),
    ('Juan Aravena', 'ASSISTANT', 'OLD', '11971597-0', 'juanaravenaorellana28@gmail.com', 'auxiliar servicio', 'Juan', 'Manuel', 'Aravena', 'Orellana'),
    ('Juan Cuadra', 'ASSISTANT', 'OLD', '10431118-0', 'kalipzo37@gmail.com', 'auxiliar servicio', 'Juan', 'Carlos', 'Cuadra', 'Mugoreni'),
    ('Juan Santibañez', 'ASSISTANT', 'OLD', '12175354-5', 'santibanezj344@gmail.com', 'Chofer Servicio', 'Juan', 'Ramon', 'Santibañez', 'Santibañez'),
    ('Juan Santibañez', 'DRIVER', 'OLD', '12175354-5', 'santibanezj344@gmail.com', 'Chofer Servicio', 'Juan', 'Ramon', 'Santibañez', 'Santibañez'),
    ('Julio Sanhueza', 'DRIVER', NULL, '15107582-7', 'julio.sanhueza1983@gmail.com', 'Chofer y Auxiliar', 'Julio', 'Cesar', 'Sanhueza', 'Tobar'),
    ('Luis Acevedo', 'ASSISTANT', 'NEW', '10851926-6', 'acelugosan@gmail.com', 'Auxiliar Despacho', 'Luis', 'Alberto', 'Acevedo', 'Gonzalez'),
    ('Luis Acevedo', 'DRIVER', 'NEW', '10851926-6', 'acelugosan@gmail.com', 'Auxiliar Despacho', 'Luis', 'Alberto', 'Acevedo', 'Gonzalez'),
    ('Luis Alvarez', 'DRIVER', NULL, '16698073-9', 'luisalvarez2310@gmail.com', 'Chofer Despacho', 'Orlando', 'Luis', 'Alvarez', 'Avendaño'),
    ('Luis Cubillos', 'ASSISTANT', 'NEW', '8473758-5', 'patricio.cubillos.sanchez@gmail.com', 'Chofer Servicio', 'Luis', 'Patricio', 'Cubillos', 'Sanchez'),
    ('Luis Dugo', 'DRIVER', 'OLD', '13548053-3', 'joeldugo@gmail.com', 'Chofer Servicio', 'Luis', 'Joel', 'Dugo', 'Hernandez'),
    ('Luis Maraboli', 'UNASSIGNED', NULL, '19255717-8', 'maraboligluis@gmail.com', 'Auxiliar Servicio Despacho', 'Luis', 'Enrique', 'Maraboli', 'Contreras'),
    ('Manuel Caceres', 'UNASSIGNED', NULL, '17936722-K', 'manuelcaceresrojas1606@gmail.com', 'Chofer Servicio', 'Manuel', 'Jesus', 'Caceres', 'Rojas'),
    ('Manuel Lopez', 'UNASSIGNED', NULL, '13663701-0', 'nolo1978@icloud.com', 'Chofer Fosero', 'Manuel', 'Alejandro', 'Lopez', 'Errazuriz'),
    ('Manuel Tapia', 'UNASSIGNED', NULL, '17392585-9', 'tapiaxino77@gmail.com', 'Chofer y Auxiliar', 'Manuel', 'Moises', 'Tapia', 'Prado'),
    ('Marcelo Caceres', 'UNASSIGNED', NULL, '18406957-1', 'marcelo.caceresb@gmail.com', 'Chofer de Unibox', 'Marcelo', 'Alejandro', 'Caceres', 'Bascuñan'),
    ('Marcelo Caro', 'UNASSIGNED', NULL, '21134377-K', 'nao.caro09@gmail.com', 'Auxiliar Servicio Despacho', 'Marcelo', 'Alexi', 'Caro', 'Guerrero'),
    ('Mario Astorga', 'ASSISTANT', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    ('Mario Astorga', 'DRIVER', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    ('Mario Nuevo', 'ASSISTANT', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    ('Martin Reyes', 'UNASSIGNED', NULL, '16879567-K', 'mige14.rking@gmail.com', 'Chofer y Auxiliar', 'Martin', 'Jose', 'Reyes', 'San'),
    ('Maximiliano Arancibia', 'DRIVER', 'OLD', '13897180-5', 'max.arancibia.r@gmail.com', 'Chofer Servicio', 'Maximiliano', NULL, 'Arancibia', 'Ramirez'),
    ('Michael Suarez', 'ASSISTANT', NULL, '17782393-7', 'anthonyvera009@gmail.com', 'Auxiliar Despacho', 'Michael', 'Anthony', 'Suarez', 'Vera'),
    ('Michael Troncoso', 'ASSISTANT', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    ('Miguel Zamorano', 'DRIVER', NULL, '15107608-4', 'migelzamorano.2023@gmail.com', 'Chofer y Auxiliar', 'Miguel', 'Angel', 'Zamorano', 'Aravena'),
    ('Milagro Urdaneta', 'UNASSIGNED', NULL, '26804143-5', 'milagrourd@yahoo.com', 'ASISTENTE RRHH', 'Milagro', 'Del', 'Urdaneta', 'Coronel'),
    ('Milton Castillo', 'UNASSIGNED', NULL, '15785123-3', 'miltonalejandro2105@hotmail.com', 'Chofer y Auxiliar', 'Milton', 'Alejandro', 'Castillo', 'Tapia'),
    ('Nelson Paredes', 'ASSISTANT', 'NEW', '20499043-3', 'nelsonpv2000@gmail.com', 'Auxiliar Servicio Despacho', 'Nelson', 'Exequiel', 'Paredes', 'Valdebenito'),
    ('Nicole Salamanca', 'UNASSIGNED', NULL, '17196134-3', 'nsalamanca057@gmail.com', 'Asistente y Gestion Comercial', 'Nicole', 'Paulina', 'Salamanca', 'Ortega'),
    ('Oscar Rabanal', 'UNASSIGNED', NULL, '13369413-7', 'agustinrblokman@gmail.com', 'Chofer RS', 'Oscar', 'Alfonso', 'Rabanal', 'Araneda'),
    ('Osman Perez', 'ASSISTANT', 'NEW', '27231597-3', 'osmanutrix@gmail.com', 'auxiliar servicio', 'Osman', 'Jose', 'Perez', 'Utriz'),
    ('PDF Worker', 'DRIVER', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    ('Pablo Gonzalez', 'UNASSIGNED', NULL, '17150530-5', 'pablogonzalezccti@gmail.com', 'Chofer RS', 'Pablo', 'Eduardo', 'Gonzalez', 'Tapia'),
    ('Pato Ramirez', 'ASSISTANT', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    ('Patricio Cubillos', 'DRIVER', 'OLD', '8473758-5', 'patricio.cubillos.sanchez@gmail.com', 'Chofer Servicio', 'Luis', 'Patricio', 'Cubillos', 'Sanchez'),
    ('Patricio Ramirez', 'ASSISTANT', NULL, '14506321-3', 'patricioramirezcornejo269@gmail.com', 'auxiliar servicio', 'Bernardino', 'Patricio', 'Ramirez', 'Cornejo'),
    ('Paulo Frez', 'UNASSIGNED', NULL, '14379050-9', 'paulofrezn@gmail.com', 'Chofer y Auxiliar', 'Paulo', 'Fernando', 'Frez', 'Nuñez'),
    ('Pedro Arcos', 'ASSISTANT', 'NEW', '7365216-2', 'pedroarcos1721@gmail.com', 'Chofer y Auxiliar', 'Pedro', 'Moises', 'Arcos', 'Miralles'),
    ('Pedro Arcos', 'DRIVER', 'NEW', '7365216-2', 'pedroarcos1721@gmail.com', 'Chofer y Auxiliar', 'Pedro', 'Moises', 'Arcos', 'Miralles'),
    ('Rafael Garcia', 'UNASSIGNED', NULL, '26233919-K', 'rafaelgarcia779911@gmail.com', 'Chofer y Auxiliar', 'Rafael', 'Segundo', 'Garcia', 'Reyes'),
    ('Rafael Rodriguez', 'UNASSIGNED', NULL, '10834879-8', 'rafelrodriguezcalderon1966@gmail.com', 'Chofer y Auxiliar', 'Rafael', NULL, 'Rodriguez', 'Calderon'),
    ('Ramon Gallardo', 'DRIVER', NULL, '12948312-1', 'ramon.gallardo.estay@gmail.com', 'Chofer Servicio', 'Ramon', NULL, 'Gallardo', 'Estay'),
    ('Ramon Pereira', 'UNASSIGNED', NULL, '14347831-9', 'reimoncortes31@gmail.com', 'Chofer y Auxiliar', 'Ramon', 'Luis', 'Pereira', 'Cortes'),
    ('Raul Parra', 'DRIVER', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    ('Raul Toledo', 'ASSISTANT', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    ('Richard Ortiz', 'UNASSIGNED', NULL, '10889753-8', 'richard_ortiz_@hotmail.com', 'Chofer RS', 'Richard', 'Eugenio', 'Ortiz', 'Villablanca'),
    ('Roberto Briones', 'ASSISTANT', 'NEW', '16844647-0', 'brionesroberto441@gmail.com', 'Chofer Servicio', 'Roberto', 'Antonio', 'Briones', 'Belmar'),
    ('Roberto Briones', 'DRIVER', 'NEW', '16844647-0', 'brionesroberto441@gmail.com', 'Chofer Servicio', 'Roberto', 'Antonio', 'Briones', 'Belmar'),
    ('Roberto Ramirez', 'DRIVER', 'OLD', '14151649-3', 'ramitarobert21@gmail.com', 'Chofer Servicio', 'Roberto', 'Fernando', 'Ramirez', 'Gomez'),
    ('Rodrigo Arcos', 'ASSISTANT', NULL, '18424055-6', 'rodrigo.arcos.barrera24@gmail.com', 'Auxiliar Servicio Despacho', 'Rodrigo', 'Moises', 'Arcos', 'Barrera'),
    ('Rodrigo Arenas', 'ASSISTANT', NULL, '14191662-9', 'arenasrodrigoarenas65@gmail.com', 'auxiliar servicio', 'Rodrigo', 'Alejandro', 'Arenas', 'Arenas'),
    ('Rodrigo Bascuñan', 'ASSISTANT', 'NEW', '9705032-5', 'rodrigobascunan1@gmail.com', 'Chofer y Auxiliar', 'Rodrigo', 'Alonso', 'Bascuñan', 'Avio'),
    ('Rodrigo Bascuñan', 'DRIVER', 'NEW', '9705032-5', 'rodrigobascunan1@gmail.com', 'Chofer y Auxiliar', 'Rodrigo', 'Alonso', 'Bascuñan', 'Avio'),
    ('Rodrigo Urrutia', 'UNASSIGNED', NULL, '12945675-2', 'rodrigo.urrutian@gmail.com', 'auxiliar servicio', 'Rodrigo', 'Alejandro', 'Urrutia', 'Nuñez'),
    ('Rody Osorio', 'DRIVER', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    ('Ronald Nuñez', 'UNASSIGNED', NULL, '14518395-2', 'ronaldnunez081@gmail.com', 'Chofer RS', 'Ronald', 'Francisco', 'Nuñez', 'Araya'),
    ('Sebastian Farias', 'UNASSIGNED', NULL, '17850134-8', 'farias.seba91@gamil.com', 'Auxiliar de Patio', 'Sebastian', 'Daniel', 'Farias', 'Garcia'),
    ('Sergio Toledo', 'ASSISTANT', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    ('Sin Operador', 'DRIVER', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
    ('Victor Araneda', 'ASSISTANT', 'OLD', '14128269-7', 'vitocko1981@gmail.com', 'auxiliar servicio', 'Victor', 'German', 'Araneda', 'Figueroa'),
    ('Victor Reyes', 'ASSISTANT', NULL, '8869419-8', 'victor.reyesvivanco@gmail.com', 'Chofer Servicio', 'Victor', 'Manuel', 'Reyes', 'Vivanco'),
    ('Victor Reyes', 'DRIVER', NULL, '8869419-8', 'victor.reyesvivanco@gmail.com', 'Chofer Servicio', 'Victor', 'Manuel', 'Reyes', 'Vivanco'),
    ('Wilmer Villa', 'ASSISTANT', NULL, '27968336-6', 'dannyvilla1982@gmail.com', 'auxiliar servicio', 'Wilmer', 'Danny', 'Villa', 'Belleza'),
    ('Wilson Saavedra', 'UNASSIGNED', NULL, '24460411-0', 'saavedrawilson145@gmail.com', 'Chofer de Servicio y Despacho', 'Wilson', NULL, 'Saavedra', 'Roa'),
    ('Yennyfer Gatica', 'UNASSIGNED', NULL, '16537331-6', 'yennytta@gmail.com', 'Asistente Servicio', 'Yennyfer', 'Andre', 'Gatica', 'Leiva'),
    ('Yosman Perez', 'ASSISTANT', NULL, '27141631-8', 'yosmanismail1701@gmail.com', 'auxiliar servicio', 'Yosman', 'Jose', 'Perez', 'Diaz');

UPDATE payroll_employees AS target
JOIN payroll_employee_sync_stage AS src
  ON src.employee_name COLLATE utf8mb4_0900_ai_ci = target.employee_name COLLATE utf8mb4_0900_ai_ci
 AND src.role_type COLLATE utf8mb4_0900_ai_ci = target.role_type COLLATE utf8mb4_0900_ai_ci
SET
    target.contract_type = COALESCE(src.contract_type, target.contract_type),
    target.rut = COALESCE(src.rut, target.rut),
    target.email = COALESCE(src.email, target.email),
    target.cargo = COALESCE(src.cargo, target.cargo),
    target.first_name = COALESCE(src.first_name, target.first_name),
    target.middle_name = COALESCE(src.middle_name, target.middle_name),
    target.paternal_surname = COALESCE(src.paternal_surname, target.paternal_surname),
    target.maternal_surname = COALESCE(src.maternal_surname, target.maternal_surname);

INSERT INTO payroll_employees (
    employee_name, role_type, contract_type, rut, email, cargo,
    first_name, middle_name, paternal_surname, maternal_surname
)
SELECT
    src.employee_name, src.role_type, src.contract_type, src.rut, src.email, src.cargo,
    src.first_name, src.middle_name, src.paternal_surname, src.maternal_surname
FROM payroll_employee_sync_stage AS src
LEFT JOIN payroll_employees AS target
  ON target.employee_name COLLATE utf8mb4_0900_ai_ci = src.employee_name COLLATE utf8mb4_0900_ai_ci
 AND target.role_type COLLATE utf8mb4_0900_ai_ci = src.role_type COLLATE utf8mb4_0900_ai_ci
WHERE target.id IS NULL;

SELECT COUNT(*) AS synced_workers FROM payroll_employee_sync_stage;
SELECT COUNT(*) AS total_workers_after_sync FROM payroll_employees;
