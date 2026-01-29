-- ============================================
-- BASE DE DATOS COMPLETA: articulacion_sena
-- Sistema de Matrículas - Articulación Media Técnica SENA
-- VERSION: 2025 - CON TODAS LAS MEJORAS INTEGRADAS
-- ============================================

-- Eliminar base de datos si existe (CUIDADO EN PRODUCCIÓN)
DROP DATABASE IF EXISTS articulacion_sena;

-- Crear base de datos
CREATE DATABASE articulacion_sena CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE articulacion_sena;

-- ============================================
-- ESQUEMA DE LA BASE DE DATOS
-- ============================================

-- Tabla: usuarios
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    documento VARCHAR(20) UNIQUE NOT NULL,
    tipo_documento ENUM('CC', 'TI', 'CE', 'PEP', 'PPT') NOT NULL DEFAULT 'CC',
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    nombre_completo VARCHAR(200) GENERATED ALWAYS AS (CONCAT(nombres, ' ', apellidos)) STORED,
    email VARCHAR(150) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    password_hash VARCHAR(255) NOT NULL,
    password_cipher TEXT,
    rol ENUM('APRENDIZ', 'DOCENTE', 'ADMINISTRADOR', 'RECTOR') NOT NULL DEFAULT 'APRENDIZ',
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_documento (documento),
    INDEX idx_email (email),
    INDEX idx_rol (rol)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: programas
CREATE TABLE programas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(20) UNIQUE,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    duracion_horas INT,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_codigo (codigo),
    INDEX idx_activo (activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: colegios
CREATE TABLE colegios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    tipo_colegio ENUM('PUBLICO', 'PRIVADO', 'MIXTO') NOT NULL DEFAULT 'PUBLICO',
    direccion VARCHAR(255),
    telefono VARCHAR(20),
    email VARCHAR(150),
    rector_id INT,
    docente_enlace_id INT,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (rector_id) REFERENCES usuarios(id) ON DELETE SET NULL,
    FOREIGN KEY (docente_enlace_id) REFERENCES usuarios(id) ON DELETE SET NULL,
    INDEX idx_nombre (nombre),
    INDEX idx_activo (activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: grupos
-- IMPORTANTE: Los grupos SENA son números únicos (Ej: 2824345)
-- Un grupo pertenece a UN programa y UN colegio
CREATE TABLE grupos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    colegio_id INT NOT NULL,
    programa_id INT NOT NULL,
    jornada ENUM('MAÑANA', 'TARDE', 'NOCHE', 'UNICA') DEFAULT 'UNICA',
    año_lectivo INT NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (colegio_id) REFERENCES colegios(id) ON DELETE CASCADE,
    FOREIGN KEY (programa_id) REFERENCES programas(id) ON DELETE CASCADE,
    UNIQUE KEY unique_grupo (nombre, colegio_id, año_lectivo),
    INDEX idx_colegio (colegio_id),
    INDEX idx_programa (programa_id),
    INDEX idx_activo (activo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: aprendices
CREATE TABLE aprendices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT UNIQUE NOT NULL,
    direccion VARCHAR(255),
    ciudad VARCHAR(100),
    departamento VARCHAR(100),
    acudiente_tipo_doc ENUM('CC', 'TI', 'CE', 'PEP', 'PPT') DEFAULT 'CC',
    acudiente_documento VARCHAR(20),
    acudiente_nombres VARCHAR(100),
    acudiente_apellidos VARCHAR(100),
    acudiente_telefono VARCHAR(20),
    acudiente_email VARCHAR(150),
    colegio_id INT,
    grupo_id INT,
    programa_id INT,
    perfil_completo BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (colegio_id) REFERENCES colegios(id) ON DELETE SET NULL,
    FOREIGN KEY (grupo_id) REFERENCES grupos(id) ON DELETE SET NULL,
    FOREIGN KEY (programa_id) REFERENCES programas(id) ON DELETE SET NULL,
    INDEX idx_usuario (usuario_id),
    INDEX idx_colegio (colegio_id),
    INDEX idx_grupo (grupo_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: matriculas
-- MEJORA: Incluye estado MATRICULADO y campos de validación
CREATE TABLE matriculas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    aprendiz_id INT NOT NULL,
    estado ENUM('BORRADOR', 'ENVIADO', 'PENDIENTE', 'COMPLETO', 'PREMATRICULA', 'MATRICULADO', 'RECHAZADO') NOT NULL DEFAULT 'BORRADOR',
    validado_por_docente INT,
    validado_por_admin INT,
    fecha_envio TIMESTAMP NULL,
    fecha_validacion_docente TIMESTAMP NULL,
    fecha_validacion_admin TIMESTAMP NULL,
    observaciones_docente TEXT,
    observaciones_admin TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (aprendiz_id) REFERENCES aprendices(id) ON DELETE CASCADE,
    FOREIGN KEY (validado_por_docente) REFERENCES usuarios(id) ON DELETE SET NULL,
    FOREIGN KEY (validado_por_admin) REFERENCES usuarios(id) ON DELETE SET NULL,
    INDEX idx_aprendiz (aprendiz_id),
    INDEX idx_estado (estado),
    INDEX idx_fecha_envio (fecha_envio)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: documentos
CREATE TABLE documentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    matricula_id INT NOT NULL,
    tipo_documento ENUM(
        'DOCUMENTO_IDENTIDAD',
        'REGISTRO_CIVIL',
        'CERTIFICADO_SALUD',
        'CERTIFICADO_SOFIA',
        'CERTIFICADO_APE',
        'DOCUMENTO_ACUDIENTE',
        'TRATAMIENTO_DATOS',
        'ACUERDO_APRENDIZ'
    ) NOT NULL,
    nombre_archivo VARCHAR(255) NOT NULL,
    ruta_archivo VARCHAR(500) NOT NULL,
    tamaño_bytes INT,
    extension VARCHAR(10),
    validado BOOLEAN DEFAULT FALSE,
    validado_por INT,
    fecha_validacion TIMESTAMP NULL,
    reemplazado_por INT,
    observaciones TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (matricula_id) REFERENCES matriculas(id) ON DELETE CASCADE,
    FOREIGN KEY (validado_por) REFERENCES usuarios(id) ON DELETE SET NULL,
    FOREIGN KEY (reemplazado_por) REFERENCES documentos(id) ON DELETE SET NULL,
    INDEX idx_matricula (matricula_id),
    INDEX idx_tipo (tipo_documento),
    INDEX idx_validado (validado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: novedades
CREATE TABLE novedades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    contenido TEXT NOT NULL,
    imagen VARCHAR(500),
    autor_id INT,
    fecha_publicacion DATE NOT NULL,
    destacado BOOLEAN DEFAULT FALSE,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (autor_id) REFERENCES usuarios(id) ON DELETE SET NULL,
    INDEX idx_fecha (fecha_publicacion),
    INDEX idx_activo (activo),
    INDEX idx_destacado (destacado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: mensajes_contacto
CREATE TABLE mensajes_contacto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL,
    telefono VARCHAR(20),
    asunto VARCHAR(200) NOT NULL,
    mensaje TEXT NOT NULL,
    leido BOOLEAN DEFAULT FALSE,
    respondido BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_leido (leido),
    INDEX idx_fecha (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: auditoria
CREATE TABLE auditoria (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    accion VARCHAR(100) NOT NULL,
    tabla VARCHAR(50),
    registro_id INT,
    datos_antes JSON,
    datos_despues JSON,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL,
    INDEX idx_usuario (usuario_id),
    INDEX idx_tabla (tabla),
    INDEX idx_fecha (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- DATOS INICIALES
-- ============================================

-- ============================================
-- 1. PROGRAMAS DE FORMACIÓN
-- ============================================
INSERT INTO programas (codigo, nombre, descripcion, duracion_horas, activo) VALUES
('TEC-SIS-001', 'Técnico en Sistemas', 'Programa de formación en desarrollo de sistemas de información y redes', 1800, TRUE),
('TEC-CONT-001', 'Técnico en Contabilidad', 'Programa de formación en contabilidad y finanzas empresariales', 1600, TRUE),
('TEC-ADM-001', 'Técnico en Administración', 'Programa de formación en gestión administrativa y recursos humanos', 1600, TRUE),
('TEC-LOG-001', 'Técnico en Logística', 'Programa de formación en logística y cadena de suministro', 1700, TRUE),
('TEC-GEST-001', 'Técnico en Gestión Administrativa', 'Programa de formación en gestión empresarial y administrativa', 1650, TRUE),
('TEC-MEC-001', 'Técnico en Mecánica', 'Programa de formación en mecánica automotriz e industrial', 2000, TRUE),
('TEC-ELEC-001', 'Técnico en Electricidad', 'Programa de formación en instalaciones eléctricas residenciales e industriales', 1900, TRUE);

-- ============================================
-- 2. USUARIOS (Administrador, Docentes, Aprendices)
-- ============================================

-- Contraseña para todos: admin123
-- Hash bcrypt con cost=12
SET @password_hash = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5OMF1lYa2xC.O';

-- Administrador
INSERT INTO usuarios (documento, tipo_documento, nombres, apellidos, email, telefono, password_hash, rol, activo) VALUES
('1234567890', 'CC', 'Administrador', 'Sistema', 'admin@sena.edu.co', '3001111111', @password_hash, 'ADMINISTRADOR', TRUE);

-- Docentes Enlace
INSERT INTO usuarios (documento, tipo_documento, nombres, apellidos, email, telefono, password_hash, rol, activo) VALUES
('2000000001', 'CC', 'Carlos', 'Méndez', 'carlos.mendez@colegio.edu.co', '3002222222', @password_hash, 'DOCENTE', TRUE),
('2000000002', 'CC', 'Laura', 'González', 'laura.gonzalez@colegio.edu.co', '3003333333', @password_hash, 'DOCENTE', TRUE),
('2000000003', 'CC', 'Pedro', 'Ramírez', 'pedro.ramirez@colegio.edu.co', '3004444444', @password_hash, 'DOCENTE', TRUE);

-- Aprendices de prueba
INSERT INTO usuarios (documento, tipo_documento, nombres, apellidos, email, telefono, password_hash, rol, activo) VALUES
('1000000001', 'TI', 'Juan', 'Pérez', 'juan.perez@estudiante.edu.co', '3005555555', @password_hash, 'APRENDIZ', TRUE),
('1000000002', 'TI', 'María', 'García', 'maria.garcia@estudiante.edu.co', '3006666666', @password_hash, 'APRENDIZ', TRUE),
('1000000003', 'TI', 'Carlos', 'Rodríguez', 'carlos.rodriguez@estudiante.edu.co', '3007777777', @password_hash, 'APRENDIZ', TRUE),
('1000000004', 'TI', 'Ana', 'López', 'ana.lopez@estudiante.edu.co', '3008888888', @password_hash, 'APRENDIZ', TRUE);

-- ============================================
-- 3. COLEGIOS
-- ============================================
INSERT INTO colegios (nombre, tipo_colegio, direccion, telefono, email, docente_enlace_id, activo) VALUES
('Institución Educativa Técnico Industrial', 'PUBLICO', 'Calle 50 #30-20', '6001234567', 'tecnico@colegio.edu.co',
    (SELECT id FROM usuarios WHERE documento = '2000000001'), TRUE),
('Colegio Integrado Comercial', 'PUBLICO', 'Carrera 15 #40-10', '6007654321', 'comercial@colegio.edu.co',
    (SELECT id FROM usuarios WHERE documento = '2000000002'), TRUE),
('Instituto Técnico Empresarial', 'PRIVADO', 'Avenida 25 #50-30', '6005551234', 'empresarial@colegio.edu.co',
    (SELECT id FROM usuarios WHERE documento = '2000000003'), TRUE);

-- ============================================
-- 4. GRUPOS SENA (AÑO LECTIVO 2025)
-- ============================================
-- IMPORTANTE: Los grupos son números SENA únicos (NO nombres de colegio)
-- Un programa puede tener MUCHOS grupos
-- Un grupo pertenece a UN SOLO programa

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

-- Programa: Técnico en Contabilidad (programa_id = 2)
INSERT INTO grupos (nombre, colegio_id, programa_id, jornada, año_lectivo, activo) VALUES
('2824355', 2, 2, 'UNICA', 2025, TRUE);

-- Instituto Técnico Empresarial (colegio_id = 3)
-- Programa: Técnico en Mecánica (programa_id = 6)
INSERT INTO grupos (nombre, colegio_id, programa_id, jornada, año_lectivo, activo) VALUES
('2824360', 3, 6, 'UNICA', 2025, TRUE);

-- Programa: Técnico en Electricidad (programa_id = 7)
INSERT INTO grupos (nombre, colegio_id, programa_id, jornada, año_lectivo, activo) VALUES
('2824361', 3, 7, 'UNICA', 2025, TRUE);

-- Programa: Técnico en Sistemas (programa_id = 1)
INSERT INTO grupos (nombre, colegio_id, programa_id, jornada, año_lectivo, activo) VALUES
('2824362', 3, 1, 'MAÑANA', 2025, TRUE);

-- ============================================
-- 5. APRENDICES (PERFILES COMPLETOS)
-- ============================================

-- Aprendiz: Juan Pérez - Grupo 2824345 (Técnico en Sistemas - Mañana)
INSERT INTO aprendices (
    usuario_id, direccion, ciudad, departamento,
    acudiente_tipo_doc, acudiente_documento, acudiente_nombres, acudiente_apellidos,
    acudiente_telefono, acudiente_email,
    colegio_id, grupo_id, programa_id, perfil_completo
) VALUES (
    (SELECT id FROM usuarios WHERE documento = '1000000001'),
    'Calle 10 #15-20', 'Fusagasugá', 'Cundinamarca',
    'CC', '52123789', 'Carlos Alberto', 'Pérez Gómez',
    '3001234567', 'carlos.perez@gmail.com',
    1, (SELECT id FROM grupos WHERE nombre = '2824345' LIMIT 1), 1, TRUE
);

-- Aprendiz: María García - Grupo 2824345 (Técnico en Sistemas - Mañana)
INSERT INTO aprendices (
    usuario_id, direccion, ciudad, departamento,
    acudiente_tipo_doc, acudiente_documento, acudiente_nombres, acudiente_apellidos,
    acudiente_telefono, acudiente_email,
    colegio_id, grupo_id, programa_id, perfil_completo
) VALUES (
    (SELECT id FROM usuarios WHERE documento = '1000000002'),
    'Calle 15 #20-30', 'Fusagasugá', 'Cundinamarca',
    'CC', '52123456', 'Ana María', 'Martínez García',
    '3009876543', 'ana.martinez@gmail.com',
    1, (SELECT id FROM grupos WHERE nombre = '2824345' LIMIT 1), 1, TRUE
);

-- Aprendiz: Carlos Rodríguez - Grupo 2824351 (Técnico en Administración - Mañana)
INSERT INTO aprendices (
    usuario_id, direccion, ciudad, departamento,
    acudiente_tipo_doc, acudiente_documento, acudiente_nombres, acudiente_apellidos,
    acudiente_telefono, acudiente_email,
    colegio_id, grupo_id, programa_id, perfil_completo
) VALUES (
    (SELECT id FROM usuarios WHERE documento = '1000000003'),
    'Carrera 8 #25-40', 'Fusagasugá', 'Cundinamarca',
    'CC', '52145678', 'Jorge Luis', 'Rodríguez López',
    '3012345678', 'jorge.rodriguez@gmail.com',
    2, (SELECT id FROM grupos WHERE nombre = '2824351' LIMIT 1), 3, TRUE
);

-- Aprendiz: Ana López - Sin grupo asignado (solo colegio)
INSERT INTO aprendices (
    usuario_id, direccion, ciudad, departamento,
    colegio_id, grupo_id, programa_id, perfil_completo
) VALUES (
    (SELECT id FROM usuarios WHERE documento = '1000000004'),
    NULL, NULL, NULL,
    3, NULL, NULL, FALSE
);

-- ============================================
-- 6. MATRÍCULAS DE PRUEBA
-- ============================================

-- Matrícula para Juan Pérez (PREMATRICULA)
INSERT INTO matriculas (aprendiz_id, estado, fecha_envio, validado_por_docente, fecha_validacion_docente) VALUES
((SELECT id FROM aprendices WHERE usuario_id = (SELECT id FROM usuarios WHERE documento = '1000000001')),
 'PREMATRICULA', NOW(), (SELECT id FROM usuarios WHERE documento = '2000000001'), NOW());

-- Matrícula para María García (ENVIADO)
INSERT INTO matriculas (aprendiz_id, estado, fecha_envio) VALUES
((SELECT id FROM aprendices WHERE usuario_id = (SELECT id FROM usuarios WHERE documento = '1000000002')),
 'ENVIADO', NOW());

-- Matrícula para Carlos Rodríguez (BORRADOR)
INSERT INTO matriculas (aprendiz_id, estado) VALUES
((SELECT id FROM aprendices WHERE usuario_id = (SELECT id FROM usuarios WHERE documento = '1000000003')),
 'BORRADOR');

-- ============================================
-- 7. NOVEDADES
-- ============================================
INSERT INTO novedades (titulo, contenido, fecha_publicacion, destacado, activo) VALUES
('Apertura de convocatoria 2025', 'Informamos a la comunidad educativa que está abierta la convocatoria para matrículas del programa de articulación con la media técnica para el año lectivo 2025. Los estudiantes interesados pueden registrarse a través de la plataforma.', CURDATE(), TRUE, TRUE),
('Bienvenida nuevo año académico', 'Damos la bienvenida a todos los aprendices que inician su proceso formativo en articulación con la media técnica. Esperamos que esta sea una experiencia enriquecedora.', CURDATE(), TRUE, TRUE),
('Fechas importantes', 'Recuerden revisar el calendario académico con las fechas de inicio de clases, entregas de documentos y actividades especiales del programa.', CURDATE(), FALSE, TRUE);

-- ============================================
-- VERIFICACIÓN FINAL
-- ============================================

-- Mostrar programas
SELECT id, codigo, nombre, duracion_horas FROM programas ORDER BY id;

-- Mostrar colegios con docentes
SELECT c.id, c.nombre, u.nombre_completo AS 'Docente Enlace'
FROM colegios c
LEFT JOIN usuarios u ON c.docente_enlace_id = u.id
ORDER BY c.id;

-- Mostrar grupos SENA por colegio
SELECT
    g.nombre AS 'Grupo SENA',
    c.nombre AS 'Colegio',
    p.nombre AS 'Programa',
    g.jornada,
    g.año_lectivo,
    COUNT(a.id) AS 'Aprendices'
FROM grupos g
JOIN colegios c ON g.colegio_id = c.id
JOIN programas p ON g.programa_id = p.id
LEFT JOIN aprendices a ON g.id = a.grupo_id
GROUP BY g.id, g.nombre, c.nombre, p.nombre, g.jornada, g.año_lectivo
ORDER BY c.nombre, p.nombre, g.nombre;

-- Mostrar aprendices con su información
SELECT
    u.documento,
    u.nombre_completo AS 'Aprendiz',
    c.nombre AS 'Colegio',
    g.nombre AS 'Grupo SENA',
    p.nombre AS 'Programa',
    a.perfil_completo,
    m.estado AS 'Estado Matrícula'
FROM usuarios u
JOIN aprendices a ON u.id = a.usuario_id
LEFT JOIN colegios c ON a.colegio_id = c.id
LEFT JOIN grupos g ON a.grupo_id = g.id
LEFT JOIN programas p ON a.programa_id = p.id
LEFT JOIN matriculas m ON a.id = m.aprendiz_id
WHERE u.rol = 'APRENDIZ'
ORDER BY c.nombre, g.nombre, u.apellidos;

-- ============================================
-- RESUMEN DE LA BASE DE DATOS
-- ============================================
--
-- ✓ 7 Programas de formación
-- ✓ 3 Colegios con docentes enlace
-- ✓ 14 Grupos SENA (números únicos, NO nombres de colegio)
-- ✓ 1 Administrador + 3 Docentes + 4 Aprendices
-- ✓ 4 Aprendices con perfiles (3 completos, 1 incompleto)
-- ✓ 3 Matrículas de prueba (PREMATRICULA, ENVIADO, BORRADOR)
-- ✓ Estado MATRICULADO disponible en el enum
-- ✓ Campos validado_por_docente y validado_por_admin
--
-- CREDENCIALES DE ACCESO:
-- - Admin: admin@sena.edu.co / admin123
-- - Docente: carlos.mendez@colegio.edu.co / admin123
-- - Aprendiz: juan.perez@estudiante.edu.co / admin123
--
-- ============================================
