-- Script para insertar grupos de formación SENA de prueba
-- Fecha: 2025-12-08
-- Descripción: Grupos con números SENA para diferentes programas y colegios

-- IMPORTANTE: Los grupos tienen un número único de SENA (Ej: 2824345)
-- Cada grupo pertenece a UN programa de formación y UN colegio
-- Los aprendices solo ven grupos de SU colegio y del programa que seleccionen

-- Primero eliminamos los grupos de ejemplo antiguos (10-A, 10-B, etc.) y cualquier grupo con letras
-- NOTA: Esto también desvincula aprendices de esos grupos (grupo_id se pone en NULL)
DELETE FROM grupos WHERE nombre REGEXP '[A-Za-z]';

-- ============================================
-- GRUPOS PARA: Institución Educativa Técnico Industrial (colegio_id = 1)
-- ============================================

-- Programa: Técnico en Sistemas (programa_id = 1)
INSERT INTO grupos (nombre, colegio_id, programa_id, jornada, año_lectivo, activo) VALUES
('2824345', 1, 1, 'MAÑANA', 2025, TRUE),
('2824346', 1, 1, 'TARDE', 2025, TRUE);

-- Programa: Técnico en Mecánica (programa_id = 5)
INSERT INTO grupos (nombre, colegio_id, programa_id, jornada, año_lectivo, activo) VALUES
('2824350', 1, 5, 'MAÑANA', 2025, TRUE),
('2824351', 1, 5, 'TARDE', 2025, TRUE);

-- ============================================
-- GRUPOS PARA: Colegio Integrado Comercial (colegio_id = 2)
-- ============================================

-- Programa: Técnico en Contabilidad (programa_id = 2)
INSERT INTO grupos (nombre, colegio_id, programa_id, jornada, año_lectivo, activo) VALUES
('2824360', 2, 2, 'MAÑANA', 2025, TRUE),
('2824361', 2, 2, 'TARDE', 2025, TRUE);

-- Programa: Técnico en Administración (programa_id = 3)
INSERT INTO grupos (nombre, colegio_id, programa_id, jornada, año_lectivo, activo) VALUES
('2824365', 2, 3, 'MAÑANA', 2025, TRUE),
('2824366', 2, 3, 'TARDE', 2025, TRUE);

-- Programa: Técnico en Logística (programa_id = 4)
INSERT INTO grupos (nombre, colegio_id, programa_id, jornada, año_lectivo, activo) VALUES
('2824370', 2, 4, 'UNICA', 2025, TRUE);

-- ============================================
-- GRUPOS PARA: Instituto Técnico Empresarial (colegio_id = 3)
-- ============================================

-- Programa: Técnico en Sistemas (programa_id = 1)
INSERT INTO grupos (nombre, colegio_id, programa_id, jornada, año_lectivo, activo) VALUES
('2824380', 3, 1, 'MAÑANA', 2025, TRUE);

-- Programa: Técnico en Administración (programa_id = 3)
INSERT INTO grupos (nombre, colegio_id, programa_id, jornada, año_lectivo, activo) VALUES
('2824385', 3, 3, 'TARDE', 2025, TRUE);

-- Programa: Técnico en Logística (programa_id = 4)
INSERT INTO grupos (nombre, colegio_id, programa_id, jornada, año_lectivo, activo) VALUES
('2824390', 3, 4, 'NOCHE', 2025, TRUE);

-- ============================================
-- VERIFICACIÓN
-- ============================================

-- Ver todos los grupos insertados
SELECT
    g.nombre AS 'Número Grupo',
    c.nombre AS 'Colegio',
    p.nombre AS 'Programa',
    g.jornada AS 'Jornada',
    g.año_lectivo AS 'Año'
FROM grupos g
INNER JOIN colegios c ON g.colegio_id = c.id
INNER JOIN programas p ON g.programa_id = p.id
WHERE g.activo = TRUE
ORDER BY c.nombre, p.nombre, g.nombre;

-- Ver resumen por colegio
SELECT
    c.nombre AS 'Colegio',
    COUNT(*) AS 'Total Grupos'
FROM grupos g
INNER JOIN colegios c ON g.colegio_id = c.id
WHERE g.activo = TRUE
GROUP BY c.nombre;
