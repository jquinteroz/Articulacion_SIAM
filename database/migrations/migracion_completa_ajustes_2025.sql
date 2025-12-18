-- =====================================================
-- MIGRACIÓN COMPLETA: AJUSTES DEL SISTEMA 2025
-- Fecha: 2025-12-08
-- Descripción: Script completo con todos los ajustes realizados
--              en las sesiones de desarrollo
-- =====================================================

-- =====================================================
-- AJUSTE 1: AGREGAR ESTADO 'MATRICULADO' AL ENUM
-- =====================================================

-- Modificar la columna estado para incluir MATRICULADO
ALTER TABLE matriculas
MODIFY COLUMN estado ENUM('BORRADOR', 'ENVIADO', 'PENDIENTE', 'COMPLETO', 'PREMATRICULA', 'MATRICULADO')
DEFAULT 'BORRADOR';

-- Agregar campos de validación por admin
ALTER TABLE matriculas
ADD COLUMN IF NOT EXISTS fecha_validacion_admin DATETIME NULL AFTER fecha_validacion_docente,
ADD COLUMN IF NOT EXISTS validado_por_admin INT NULL AFTER fecha_validacion_admin,
ADD FOREIGN KEY IF NOT EXISTS fk_matriculas_admin (validado_por_admin) REFERENCES usuarios(id) ON DELETE SET NULL;

-- =====================================================
-- AJUSTE 2: AGREGAR TRACKING DE VALIDACIÓN POR DOCENTE
-- =====================================================

-- Agregar campo validado_por_docente si no existe
ALTER TABLE matriculas
ADD COLUMN IF NOT EXISTS validado_por_docente INT NULL AFTER fecha_validacion_docente,
ADD FOREIGN KEY IF NOT EXISTS fk_matriculas_docente (validado_por_docente) REFERENCES usuarios(id) ON DELETE SET NULL;

-- =====================================================
-- AJUSTE 3: ELIMINAR GRUPOS CON NOMBRES DE COLEGIO
-- =====================================================

-- IMPORTANTE: Los grupos SENA son números únicos (ej: 2824345)
-- NO son nombres de cursos de colegio (10-A, 11-B, etc.)

-- Eliminar relaciones antes de borrar grupos
DELETE FROM aprendices WHERE grupo_id IN (
    SELECT id FROM grupos WHERE nombre REGEXP '[A-Za-z]'
);

-- Eliminar grupos con letras en el nombre
DELETE FROM grupos WHERE nombre REGEXP '[A-Za-z]';

-- =====================================================
-- AJUSTE 4: INSERTAR GRUPOS SENA CORRECTOS
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
-- AJUSTE 5: ACTUALIZAR PERFILES DE APRENDICES
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
-- VERIFICACIÓN FINAL
-- =====================================================

-- 1. Verificar grupos SENA creados
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

-- 2. Verificar que no existan grupos con letras
SELECT COUNT(*) AS 'Grupos con Letras (debe ser 0)'
FROM grupos
WHERE nombre REGEXP '[A-Za-z]';

-- 3. Verificar estados de matrícula disponibles
SELECT COLUMN_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'articulacion'
  AND TABLE_NAME = 'matriculas'
  AND COLUMN_NAME = 'estado';

-- 4. Verificar aprendices con perfil completo
SELECT
    u.documento,
    u.nombres,
    u.apellidos,
    c.nombre AS 'Colegio',
    g.nombre AS 'Grupo SENA',
    p.nombre AS 'Programa',
    a.perfil_completo
FROM aprendices a
JOIN usuarios u ON a.usuario_id = u.id
LEFT JOIN colegios c ON a.colegio_id = c.id
LEFT JOIN grupos g ON a.grupo_id = g.id
LEFT JOIN programas p ON a.programa_id = p.id
ORDER BY c.nombre, g.nombre, u.apellidos;

-- =====================================================
-- RESUMEN DE CAMBIOS APLICADOS
-- =====================================================
--
-- 1. ✓ Agregado estado MATRICULADO al enum de matriculas
-- 2. ✓ Agregados campos fecha_validacion_admin y validado_por_admin
-- 3. ✓ Agregado campo validado_por_docente
-- 4. ✓ Eliminados grupos con nombres de colegio (10-A, 11-B, etc.)
-- 5. ✓ Creados grupos SENA con números únicos (2824345, 2824346, etc.)
-- 6. ✓ Actualizados perfiles de aprendices con datos completos
-- 7. ✓ Asociados aprendices a grupos SENA correctos
--
-- RELACIONES IMPORTANTES:
-- - Un programa de formación puede tener MUCHOS grupos
-- - Un grupo pertenece a UN SOLO programa de formación
-- - El registro de aprendiz solo requiere COLEGIO
-- - Grupo y programa se asignan en el PERFIL del aprendiz
--
-- =====================================================
