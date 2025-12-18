-- Script para actualizar aprendices con grupos SENA correctos
-- Fecha: 2025-12-08
-- Descripción: Asigna grupos de formación SENA a aprendices existentes

-- ============================================
-- ACTUALIZAR APRENDIZ DE PRUEBA
-- ============================================

-- María Fernanda López Martínez (documento: 1000000002)
-- Colegio: Institución Educativa Técnico Industrial (id: 1)
-- Programa: Técnico en Sistemas (id: 1)
-- Grupo: 2824345 (Técnico en Sistemas - Mañana)

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

-- ============================================
-- VERIFICACIÓN
-- ============================================

-- Ver el aprendiz actualizado
SELECT
    u.nombres,
    u.apellidos,
    u.documento,
    c.nombre AS colegio,
    p.nombre AS programa,
    g.nombre AS grupo_sena,
    g.jornada,
    a.perfil_completo
FROM aprendices a
INNER JOIN usuarios u ON a.usuario_id = u.id
LEFT JOIN colegios c ON a.colegio_id = c.id
LEFT JOIN programas p ON a.programa_id = p.id
LEFT JOIN grupos g ON a.grupo_id = g.id
WHERE u.documento = '1000000002';
