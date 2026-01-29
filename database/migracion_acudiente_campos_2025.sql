-- Migración: Mover campo dirección del aprendiz al acudiente y agregar lugar de expedición
-- Fecha: 2025-01-10
-- Descripción:
--   1. Agregar acudiente_lugar_expedicion
--   2. Agregar acudiente_direccion
--   3. Migrar datos de direccion a acudiente_direccion
--   4. Eliminar campo direccion de aprendiz

-- 1. Agregar nuevo campo acudiente_lugar_expedicion
ALTER TABLE aprendices ADD COLUMN acudiente_lugar_expedicion VARCHAR(100) AFTER acudiente_documento;

-- 2. Agregar nuevo campo acudiente_direccion
ALTER TABLE aprendices ADD COLUMN acudiente_direccion VARCHAR(255) AFTER acudiente_apellidos;

-- 3. Migrar datos existentes de direccion a acudiente_direccion
UPDATE aprendices SET acudiente_direccion = direccion WHERE direccion IS NOT NULL;

-- 4. Eliminar el campo direccion del aprendiz
ALTER TABLE aprendices DROP COLUMN direccion;

-- Verificar cambios
SELECT
    'aprendices' as tabla,
    COUNT(*) as total_registros,
    COUNT(acudiente_lugar_expedicion) as con_lugar_expedicion,
    COUNT(acudiente_direccion) as con_direccion
FROM aprendices;
