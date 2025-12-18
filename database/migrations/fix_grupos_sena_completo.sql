-- =====================================================
-- MIGRACIÓN: CORRECCIÓN DE GRUPOS SENA
-- Fecha: 2025-12-08
-- Descripción: Reemplaza nombres de grupos de colegio (10-A, 11-B, etc.)
--              con números de grupos SENA (2824345, 2824346, etc.)
-- =====================================================

-- IMPORTANTE: Los grupos SENA son números únicos generados por el SENA
-- NO son nombres de cursos de colegio (10-A, 11-B, etc.)
-- Un programa de formación puede tener MUCHOS grupos
-- Un grupo pertenece a UN SOLO programa de formación

-- =====================================================
-- PASO 1: ELIMINAR GRUPOS CON NOMBRES DE COLEGIO
-- =====================================================

-- Primero, eliminar aprendices asociados a grupos con letras
-- (esto es temporal, los re-crearemos con datos correctos)
DELETE FROM aprendices WHERE grupo_id IN (
    SELECT id FROM grupos WHERE nombre REGEXP '[A-Za-z]'
);

-- Eliminar grupos con letras en el nombre
DELETE FROM grupos WHERE nombre REGEXP '[A-Za-z]';

-- =====================================================
-- PASO 2: INSERTAR GRUPOS SENA CORRECTOS
-- =====================================================

-- Institución Educativa Técnico Industrial (colegio_id = 1)
-- Programa: Técnico en Sistemas (programa_id = 1)
INSERT INTO grupos (nombre, colegio_id, programa_id, jornada, año_lectivo, activo) VALUES
('2824345', 1, 1, 'MAÑANA', 2025, TRUE),
('2824346', 1, 1, 'TARDE', 2025, TRUE);

-- Programa: Técnico en Contabilidad (programa_id = 2)
INSERT INTO grupos (nombre, colegio_id, programa_id, jornada, año_lectivo, activo) VALUES
('2824347', 1, 2, 'MAÑANA', 2025, TRUE),
('2824348', 1, 2, 'TARDE', 2025, TRUE);

-- Programa: Técnico en Gestión Administrativa (programa_id = 5)
INSERT INTO grupos (nombre, colegio_id, programa_id, jornada, año_lectivo, activo) VALUES
('2824350', 1, 5, 'MAÑANA', 2025, TRUE);

-- Colegio Integrado Comercial (colegio_id = 2)
-- Programa: Técnico en Administración (programa_id = 3)
INSERT INTO grupos (nombre, colegio_id, programa_id, jornada, año_lectivo, activo) VALUES
('2824351', 2, 3, 'MAÑANA', 2025, TRUE),
('2824352', 2, 3, 'TARDE', 2025, TRUE);

-- Programa: Técnico en Logística (programa_id = 4)
INSERT INTO grupos (nombre, colegio_id, programa_id, jornada, año_lectivo, activo) VALUES
('2824353', 2, 4, 'MAÑANA', 2025, TRUE),
('2824354', 2, 4, 'TARDE', 2025, TRUE);

-- Instituto Técnico Empresarial (colegio_id = 3)
-- Programa: Técnico en Mecánica (programa_id = 6)
INSERT INTO grupos (nombre, colegio_id, programa_id, jornada, año_lectivo, activo) VALUES
('2824360', 3, 6, 'ÚNICA', 2025, TRUE);

-- Programa: Técnico en Electricidad (programa_id = 7)
INSERT INTO grupos (nombre, colegio_id, programa_id, jornada, año_lectivo, activo) VALUES
('2824361', 3, 7, 'ÚNICA', 2025, TRUE);

-- =====================================================
-- PASO 3: ACTUALIZAR APRENDICES CON GRUPOS SENA
-- =====================================================

-- Actualizar aprendiz Juan Pérez (documento 1000000001)
-- Asignar al grupo 2824345 (Técnico en Sistemas - Mañana)
UPDATE aprendices
SET
    grupo_id = (SELECT id FROM grupos WHERE nombre = '2824345' AND colegio_id = 1 LIMIT 1),
    programa_id = 1,
    colegio_id = 1,
    direccion = 'Calle 10 #15-20',
    ciudad = 'Fusagasugá',
    departamento = 'Cundinamarca',
    acudiente_tipo_doc = 'CC',
    acudiente_documento = '52123789',
    acudiente_nombres = 'Carlos Alberto',
    acudiente_apellidos = 'Pérez Gómez',
    acudiente_telefono = '3001234567',
    acudiente_email = 'carlos.perez@gmail.com',
    perfil_completo = TRUE
WHERE usuario_id = (SELECT id FROM usuarios WHERE documento = '1000000001');

-- Actualizar aprendiz María García (documento 1000000002)
-- Asignar al grupo 2824345 (Técnico en Sistemas - Mañana)
UPDATE aprendices
SET
    grupo_id = (SELECT id FROM grupos WHERE nombre = '2824345' AND colegio_id = 1 LIMIT 1),
    programa_id = 1,
    colegio_id = 1,
    direccion = 'Calle 15 #20-30',
    ciudad = 'Fusagasugá',
    departamento = 'Cundinamarca',
    acudiente_tipo_doc = 'CC',
    acudiente_documento = '52123456',
    acudiente_nombres = 'Ana María',
    acudiente_apellidos = 'Martínez García',
    acudiente_telefono = '3009876543',
    acudiente_email = 'ana.martinez@gmail.com',
    perfil_completo = TRUE
WHERE usuario_id = (SELECT id FROM usuarios WHERE documento = '1000000002');

-- Actualizar aprendiz Carlos Rodríguez (documento 1000000003)
-- Asignar al grupo 2824351 (Técnico en Administración - Mañana)
UPDATE aprendices
SET
    grupo_id = (SELECT id FROM grupos WHERE nombre = '2824351' AND colegio_id = 2 LIMIT 1),
    programa_id = 3,
    colegio_id = 2,
    direccion = 'Carrera 8 #25-40',
    ciudad = 'Fusagasugá',
    departamento = 'Cundinamarca',
    acudiente_tipo_doc = 'CC',
    acudiente_documento = '52145678',
    acudiente_nombres = 'Jorge Luis',
    acudiente_apellidos = 'Rodríguez López',
    acudiente_telefono = '3012345678',
    acudiente_email = 'jorge.rodriguez@gmail.com',
    perfil_completo = TRUE
WHERE usuario_id = (SELECT id FROM usuarios WHERE documento = '1000000003');

-- =====================================================
-- VERIFICACIÓN
-- =====================================================

-- Verificar grupos creados
SELECT
    g.id,
    g.nombre AS 'Grupo SENA',
    c.nombre AS 'Colegio',
    p.nombre AS 'Programa',
    g.jornada,
    g.año_lectivo,
    COUNT(a.id) AS 'Aprendices'
FROM grupos g
LEFT JOIN colegios c ON g.colegio_id = c.id
LEFT JOIN programas p ON g.programa_id = p.id
LEFT JOIN aprendices a ON g.id = a.grupo_id
GROUP BY g.id, g.nombre, c.nombre, p.nombre, g.jornada, g.año_lectivo
ORDER BY c.nombre, p.nombre, g.nombre;

-- Verificar que no existan grupos con letras
SELECT COUNT(*) AS 'Grupos con Letras (debe ser 0)'
FROM grupos
WHERE nombre REGEXP '[A-Za-z]';

-- =====================================================
-- NOTAS IMPORTANTES
-- =====================================================
-- 1. Los grupos SENA son números únicos (ej: 2824345)
-- 2. Cada grupo pertenece a UN programa de formación
-- 3. Un programa puede tener MÚLTIPLES grupos
-- 4. Los grupos se asignan en el PERFIL del aprendiz, no en el registro
-- 5. El formulario de registro solo pide el COLEGIO
-- =====================================================
