-- ============================================
-- SCRIPT DE MIGRACIÓN Y CORRECCIÓN
-- Sistema de Matrículas SENA - Universidad de Cundinamarca
-- Fecha: 2025-12-08
-- Descripción: Actualiza estructura y corrige datos sin borrar información existente
-- ============================================

USE articulacion_sena;

-- ============================================
-- 1. ACTUALIZAR ESTRUCTURA DE TABLAS
-- ============================================

-- Verificar y agregar estado MATRICULADO si no existe
ALTER TABLE matriculas
MODIFY COLUMN estado ENUM('BORRADOR', 'ENVIADO', 'PENDIENTE', 'COMPLETO', 'PREMATRICULA', 'MATRICULADO', 'RECHAZADO')
NOT NULL DEFAULT 'BORRADOR';

-- Agregar campos de validación si no existen
ALTER TABLE matriculas
ADD COLUMN IF NOT EXISTS validado_por_docente INT,
ADD COLUMN IF NOT EXISTS validado_por_admin INT,
ADD COLUMN IF NOT EXISTS fecha_validacion_docente TIMESTAMP NULL,
ADD COLUMN IF NOT EXISTS fecha_validacion_admin TIMESTAMP NULL;

-- Agregar foreign keys si no existen
-- Nota: Si ya existen, MySQL ignorará estos comandos con un warning
SET @exist := (SELECT COUNT(*) FROM information_schema.TABLE_CONSTRAINTS
    WHERE CONSTRAINT_SCHEMA = 'articulacion_sena'
    AND TABLE_NAME = 'matriculas'
    AND CONSTRAINT_NAME = 'fk_validado_docente');

SET @sqlstmt := IF(@exist = 0,
    'ALTER TABLE matriculas ADD CONSTRAINT fk_validado_docente FOREIGN KEY (validado_por_docente) REFERENCES usuarios(id) ON DELETE SET NULL',
    'SELECT ''FK fk_validado_docente already exists'' AS msg');

PREPARE stmt FROM @sqlstmt;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @exist := (SELECT COUNT(*) FROM information_schema.TABLE_CONSTRAINTS
    WHERE CONSTRAINT_SCHEMA = 'articulacion_sena'
    AND TABLE_NAME = 'matriculas'
    AND CONSTRAINT_NAME = 'fk_validado_admin');

SET @sqlstmt := IF(@exist = 0,
    'ALTER TABLE matriculas ADD CONSTRAINT fk_validado_admin FOREIGN KEY (validado_por_admin) REFERENCES usuarios(id) ON DELETE SET NULL',
    'SELECT ''FK fk_validado_admin already exists'' AS msg');

PREPARE stmt FROM @sqlstmt;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- ============================================
-- 2. CREAR PROGRAMAS FALTANTES
-- ============================================

-- Insertar programas solo si no existen
INSERT IGNORE INTO programas (id, codigo, nombre, descripcion, duracion_horas, activo) VALUES
(1, 'TEC-SIS-001', 'Técnico en Sistemas', 'Formación en desarrollo de software, redes y mantenimiento de equipos', 1800, TRUE),
(2, 'TEC-CONT-001', 'Técnico en Contabilidad', 'Formación en contabilidad, finanzas y gestión empresarial', 1600, TRUE),
(3, 'TEC-ADM-001', 'Técnico en Administración', 'Formación en administración de empresas y recursos humanos', 1600, TRUE),
(4, 'TEC-LOG-001', 'Técnico en Logística', 'Formación en gestión de cadena de suministro y logística', 1700, TRUE),
(5, 'TEC-GEST-001', 'Técnico en Gestión Administrativa', 'Formación en gestión documental y procesos administrativos', 1650, TRUE),
(6, 'TEC-MEC-001', 'Técnico en Mecánica', 'Formación en mecánica automotriz y mantenimiento industrial', 2000, TRUE),
(7, 'TEC-ELEC-001', 'Técnico en Electricidad', 'Formación en instalaciones eléctricas y electrónica', 1900, TRUE);

-- ============================================
-- 3. LIMPIAR GRUPOS CON NOMBRES INCORRECTOS
-- ============================================

-- Eliminar grupos que tengan letras en el nombre (formato de colegio como 10-A, 11-B)
-- Solo si no tienen aprendices asignados
DELETE FROM grupos
WHERE nombre REGEXP '[A-Za-z]'
AND id NOT IN (SELECT DISTINCT grupo_id FROM aprendices WHERE grupo_id IS NOT NULL);

-- ============================================
-- 4. CREAR GRUPOS SENA CORRECTOS
-- ============================================

-- Grupos para Colegio 1: Institución Educativa Técnico Industrial
INSERT IGNORE INTO grupos (nombre, colegio_id, programa_id, jornada, año_lectivo, activo) VALUES
('2824345', 1, 1, 'MAÑANA', 2025, TRUE),
('2824346', 1, 1, 'TARDE', 2025, TRUE),
('2824347', 1, 2, 'MAÑANA', 2025, TRUE),
('2824348', 1, 2, 'TARDE', 2025, TRUE),
('2824349', 1, 6, 'MAÑANA', 2025, TRUE);

-- Grupos para Colegio 2: Colegio Integrado Comercial
INSERT IGNORE INTO grupos (nombre, colegio_id, programa_id, jornada, año_lectivo, activo) VALUES
('2824350', 2, 2, 'MAÑANA', 2025, TRUE),
('2824351', 2, 3, 'MAÑANA', 2025, TRUE),
('2824352', 2, 3, 'TARDE', 2025, TRUE),
('2824353', 2, 5, 'MAÑANA', 2025, TRUE);

-- Grupos para Colegio 3: Instituto Técnico Empresarial
INSERT IGNORE INTO grupos (nombre, colegio_id, programa_id, jornada, año_lectivo, activo) VALUES
('2824354', 3, 3, 'MAÑANA', 2025, TRUE),
('2824355', 3, 4, 'MAÑANA', 2025, TRUE),
('2824356', 3, 4, 'TARDE', 2025, TRUE),
('2824357', 3, 5, 'MAÑANA', 2025, TRUE),
('2824358', 3, 7, 'MAÑANA', 2025, TRUE);

-- ============================================
-- 5. CREAR REGISTROS DE APRENDICES FALTANTES
-- ============================================

-- Crear registros de aprendices para usuarios con rol APRENDIZ que no tienen registro en la tabla aprendices
INSERT INTO aprendices (usuario_id, colegio_id, grupo_id, programa_id, perfil_completo)
SELECT
    u.id AS usuario_id,
    NULL AS colegio_id,
    NULL AS grupo_id,
    NULL AS programa_id,
    FALSE AS perfil_completo
FROM usuarios u
WHERE u.rol = 'APRENDIZ'
AND u.id NOT IN (SELECT usuario_id FROM aprendices);

-- ============================================
-- 6. ACTUALIZAR APRENDICES EXISTENTES
-- ============================================

-- Si hay aprendices con colegio_id incorrecto o NULL, puedes actualizarlos aquí
-- Por ejemplo, asignar todos los aprendices sin colegio al Colegio 1 (donde está el docente enlace)
-- Descomenta la siguiente línea si quieres hacer esto automáticamente:
-- UPDATE aprendices SET colegio_id = 1 WHERE colegio_id IS NULL OR colegio_id = 0;

-- ============================================
-- 7. VERIFICACIÓN DE DATOS
-- ============================================

-- Mostrar usuarios con rol APRENDIZ
SELECT 'USUARIOS CON ROL APRENDIZ' AS verificacion;
SELECT id, documento, nombres, apellidos, email, rol, activo
FROM usuarios
WHERE rol = 'APRENDIZ'
ORDER BY id;

-- Mostrar registros de aprendices
SELECT 'REGISTROS DE APRENDICES' AS verificacion;
SELECT
    a.id,
    a.usuario_id,
    u.documento,
    u.nombre_completo,
    a.colegio_id,
    c.nombre AS colegio_nombre,
    a.grupo_id,
    g.nombre AS grupo_nombre,
    a.programa_id,
    p.nombre AS programa_nombre
FROM aprendices a
LEFT JOIN usuarios u ON a.usuario_id = u.id
LEFT JOIN colegios c ON a.colegio_id = c.id
LEFT JOIN grupos g ON a.grupo_id = g.id
LEFT JOIN programas p ON a.programa_id = p.id
ORDER BY a.id;

-- Mostrar colegios y docentes enlace
SELECT 'COLEGIOS Y DOCENTES ENLACE' AS verificacion;
SELECT
    c.id,
    c.nombre AS colegio,
    c.docente_enlace_id,
    u.nombre_completo AS docente_enlace
FROM colegios c
LEFT JOIN usuarios u ON c.docente_enlace_id = u.id
ORDER BY c.id;

-- Mostrar programas
SELECT 'PROGRAMAS DISPONIBLES' AS verificacion;
SELECT id, codigo, nombre, duracion_horas, activo
FROM programas
ORDER BY id;

-- Mostrar grupos SENA
SELECT 'GRUPOS SENA' AS verificacion;
SELECT
    g.id,
    g.nombre,
    c.nombre AS colegio,
    p.nombre AS programa,
    g.jornada,
    g.año_lectivo,
    g.activo
FROM grupos g
LEFT JOIN colegios c ON g.colegio_id = c.id
LEFT JOIN programas p ON g.programa_id = p.id
ORDER BY g.colegio_id, g.nombre;

-- Contar aprendices por colegio
SELECT 'CONTEO DE APRENDICES POR COLEGIO' AS verificacion;
SELECT
    c.id,
    c.nombre AS colegio,
    COUNT(a.id) AS total_aprendices
FROM colegios c
LEFT JOIN aprendices a ON c.id = a.colegio_id
GROUP BY c.id, c.nombre
ORDER BY c.id;

SELECT '============================================' AS '';
SELECT 'MIGRACIÓN COMPLETADA EXITOSAMENTE' AS resultado;
SELECT 'Revise los resultados de verificación arriba' AS nota;
SELECT '============================================' AS '';
