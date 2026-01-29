-- Migración para agregar el estado MATRICULADO al enum de matriculas
-- Fecha: 2025-12-08

-- Modificar la columna estado para incluir MATRICULADO
ALTER TABLE matriculas
MODIFY COLUMN estado ENUM('BORRADOR', 'ENVIADO', 'PENDIENTE', 'COMPLETO', 'PREMATRICULA', 'MATRICULADO', 'RECHAZADO')
NOT NULL DEFAULT 'BORRADOR';

-- Verificar que la migración funcionó
SELECT COLUMN_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = DATABASE()
  AND TABLE_NAME = 'matriculas'
  AND COLUMN_NAME = 'estado';
