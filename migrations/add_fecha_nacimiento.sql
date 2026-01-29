-- Migración: Agregar campo fecha_nacimiento a tabla usuarios
-- Fecha: 2025-12-09
-- Descripción: Agrega el campo fecha_nacimiento para validaciones de edad y tipo de documento

-- Agregar columna fecha_nacimiento
ALTER TABLE usuarios
ADD COLUMN fecha_nacimiento DATE NULL AFTER apellidos;

-- Agregar comentario a la columna
ALTER TABLE usuarios
MODIFY COLUMN fecha_nacimiento DATE NULL COMMENT 'Fecha de nacimiento del usuario (requerido para aprendices)';
