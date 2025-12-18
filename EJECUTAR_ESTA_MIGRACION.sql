-- =====================================================================
-- IMPORTANTE: EJECUTA ESTE SCRIPT EN TU GESTOR DE BASE DE DATOS MySQL
-- Base de datos: articulacion_cgmlti
-- =====================================================================

USE articulacion_cgmlti;

-- 1. Agregar nuevo campo acudiente_lugar_expedicion
ALTER TABLE aprendices
ADD COLUMN acudiente_lugar_expedicion VARCHAR(100)
AFTER acudiente_documento;

-- 2. Agregar nuevo campo acudiente_direccion
ALTER TABLE aprendices
ADD COLUMN acudiente_direccion VARCHAR(255)
AFTER acudiente_apellidos;

-- 3. Migrar datos existentes de direccion a acudiente_direccion
UPDATE aprendices
SET acudiente_direccion = direccion
WHERE direccion IS NOT NULL;

-- 4. Eliminar el campo direccion del aprendiz
ALTER TABLE aprendices
DROP COLUMN direccion;

-- 5. Verificar cambios
SELECT
    'aprendices' as tabla,
    COUNT(*) as total_registros,
    COUNT(acudiente_lugar_expedicion) as con_lugar_expedicion,
    COUNT(acudiente_direccion) as con_direccion
FROM aprendices;

-- =====================================================================
-- FIN DE LA MIGRACIÓN
-- =====================================================================
