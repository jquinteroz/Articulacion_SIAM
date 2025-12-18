-- ============================================
-- BASE DE DATOS COMPLETA: articulacion_sena
-- Sistema de Matrículas - Articulación Media Técnica SENA
-- ARCHIVO COMPLETO CON DATOS INICIALES
-- ============================================

-- Eliminar base de datos si existe (CUIDADO EN PRODUCCIÓN)
-- DROP DATABASE IF EXISTS articulacion_sena;

-- Crear base de datos
CREATE DATABASE IF NOT EXISTS articulacion_sena CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE articulacion_sena;

-- ============================================
-- ESQUEMA DE LA BASE DE DATOS
-- ============================================

-- Tabla: usuarios
CREATE TABLE IF NOT EXISTS usuarios (
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
CREATE TABLE IF NOT EXISTS programas (
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
CREATE TABLE IF NOT EXISTS colegios (
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
CREATE TABLE IF NOT EXISTS grupos (
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
CREATE TABLE IF NOT EXISTS aprendices (
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
CREATE TABLE IF NOT EXISTS matriculas (
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
CREATE TABLE IF NOT EXISTS documentos (
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
CREATE TABLE IF NOT EXISTS novedades (
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
CREATE TABLE IF NOT EXISTS mensajes_contacto (
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
CREATE TABLE IF NOT EXISTS auditoria (
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

-- Programas de formación
INSERT INTO programas (codigo, nombre, descripcion, duracion_horas, activo) VALUES
('TEC-SIS-001', 'Técnico en Sistemas', 'Programa de formación en desarrollo de sistemas de información y redes', 1800, TRUE),
('TEC-CONT-001', 'Técnico en Contabilidad', 'Programa de formación en contabilidad y finanzas empresariales', 1600, TRUE),
('TEC-ADM-001', 'Técnico en Administración', 'Programa de formación en gestión administrativa y recursos humanos', 1600, TRUE),
('TEC-LOG-001', 'Técnico en Logística', 'Programa de formación en logística y cadena de suministro', 1700, TRUE),
('TEC-MEC-001', 'Técnico en Mecánica', 'Programa de formación en mecánica automotriz e industrial', 2000, TRUE);

-- Colegios de ejemplo
INSERT INTO colegios (nombre, tipo_colegio, direccion, telefono, email, activo) VALUES
('Institución Educativa Técnico Industrial', 'PUBLICO', 'Calle 50 #30-20', '6001234567', 'tecnico@colegio.edu.co', TRUE),
('Colegio Integrado Comercial', 'PUBLICO', 'Carrera 15 #40-10', '6007654321', 'comercial@colegio.edu.co', TRUE),
('Instituto Técnico Empresarial', 'PRIVADO', 'Avenida 25 #50-30', '6005551234', 'empresarial@colegio.edu.co', TRUE);

-- ============================================
-- GRUPOS DE FORMACIÓN SENA (año lectivo 2025)
-- ============================================
-- IMPORTANTE: Los grupos tienen números únicos de SENA (Ej: 2824345)
-- Cada grupo pertenece a UN programa de formación y UN colegio
-- Los aprendices solo ven grupos de SU colegio y del programa que seleccionen

-- Institución Educativa Técnico Industrial (colegio_id = 1)
-- Programa: Técnico en Sistemas (programa_id = 1)
INSERT INTO grupos (nombre, colegio_id, programa_id, jornada, año_lectivo, activo) VALUES
('2824345', 1, 1, 'MAÑANA', 2025, TRUE),
('2824346', 1, 1, 'TARDE', 2025, TRUE);

-- Programa: Técnico en Mecánica (programa_id = 5)
INSERT INTO grupos (nombre, colegio_id, programa_id, jornada, año_lectivo, activo) VALUES
('2824350', 1, 5, 'MAÑANA', 2025, TRUE),
('2824351', 1, 5, 'TARDE', 2025, TRUE);

-- Colegio Integrado Comercial (colegio_id = 2)
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

-- Instituto Técnico Empresarial (colegio_id = 3)
-- Programa: Técnico en Sistemas (programa_id = 1)
INSERT INTO grupos (nombre, colegio_id, programa_id, jornada, año_lectivo, activo) VALUES
('2824380', 3, 1, 'MAÑANA', 2025, TRUE);

-- Programa: Técnico en Administración (programa_id = 3)
INSERT INTO grupos (nombre, colegio_id, programa_id, jornada, año_lectivo, activo) VALUES
('2824385', 3, 3, 'TARDE', 2025, TRUE);

-- Programa: Técnico en Logística (programa_id = 4)
INSERT INTO grupos (nombre, colegio_id, programa_id, jornada, año_lectivo, activo) VALUES
('2824390', 3, 4, 'NOCHE', 2025, TRUE);

-- Novedades
INSERT INTO novedades (titulo, contenido, fecha_publicacion, destacado, activo) VALUES
('Apertura de convocatoria 2025', 'Informamos a la comunidad educativa que está abierta la convocatoria para matrículas del programa de articulación con la media técnica para el año lectivo 2025. Los estudiantes interesados pueden registrarse a través de la plataforma.', CURDATE(), TRUE, TRUE),
('Bienvenida nuevo año académico', 'Damos la bienvenida a todos los aprendices que inician su proceso formativo en articulación con la media técnica. Esperamos que esta sea una experiencia enriquecedora.', CURDATE(), TRUE, TRUE),
('Fechas importantes', 'Recuerden revisar el calendario académico con las fechas de inicio de clases, entregas de documentos y actividades especiales del programa.', CURDATE(), FALSE, TRUE);

-- ============================================
-- USUARIOS DE PRUEBA CON CONTRASEÑAS HASHEADAS
-- ============================================

-- IMPORTANTE: Antes de ejecutar esto, asegúrate de agregar esta clave al archivo .env:
-- ENCRYPTION_KEY=cXNkL8qstj6vaRFTfJRqihhA1RBX-gi6PqJBdBWutJs=

-- Usuario Administrador
-- Documento: 1000000000 | Contraseña: Admin123!
INSERT INTO usuarios (documento, tipo_documento, nombres, apellidos, email, telefono, password_hash, password_cipher, rol, activo) VALUES
('1000000000', 'CC', 'Administrador', 'Sistema', 'admin@sena.edu.co', '3001234567',
'scrypt:32768:8:1$QTKW8oVWx6M9vdeg$ed669ef23d6b789f77f8ccd97eef6a74242596acfd1f1940377ab243ab9f9da75340eeec58a503984c1247ceb067adc463f102fe52f54168276be6efe35607fb',
'gAAAAABpM2fiO4BldgeggpkkbOxKd5YF-iM0ptNGA0BKFHfxtPH4jOXT4gOG5r5x4xUOS2J5IbE9mhSB1f-4_Wde0eikCupxFg==',
'ADMINISTRADOR', TRUE);

-- Usuario Docente Enlace
-- Documento: 1000000001 | Contraseña: Docente123!
INSERT INTO usuarios (documento, tipo_documento, nombres, apellidos, email, telefono, password_hash, password_cipher, rol, activo) VALUES
('1000000001', 'CC', 'Juan Carlos', 'Pérez Gómez', 'docente@colegio.edu.co', '3001234568',
'scrypt:32768:8:1$If8u46gJ0tWK8AH1$3f9e665ffcccd6082f81b7220661ea6353b01b86d61335bca90725b7fe26eea9364e3600b22c0a0f0d655347a8cd98b74231d51dbed5fc6028ad4c4caf8296ff',
'gAAAAABpM2fienpV7vCHl_0h5UQdGdAshGgK3KBN63dhe0lFzcUqyOrCucSXnAFm2OBxTWaQ_cACpNqlEBHAVwCL7Q7z1ZY8Bg==',
'DOCENTE', TRUE);

-- Usuario Aprendiz
-- Documento: 1000000002 | Contraseña: Aprendiz123!
INSERT INTO usuarios (documento, tipo_documento, nombres, apellidos, email, telefono, password_hash, password_cipher, rol, activo) VALUES
('1000000002', 'TI', 'María Fernanda', 'López Martínez', 'aprendiz@estudiante.com', '3001234569',
'scrypt:32768:8:1$0OpxUNiSiWpy6weS$f7775b32df2fe1bb41b4b1ee132f5c2173a0388684b3d9e8d212e51e3c1135e3e7b1057cb43e6ec68e8b485fb639295e2f7240d8acce5bc0a0d71ea3953fe31a',
'gAAAAABpM2fj1tsPiCaJM1WxchhjyXmIhDz6ZOl7QN98cgxycpz3_LYwgYPzCC3bUNptzVrSXpRXBGlGOJ3bS-AfGt6Q0-eSsA==',
'APRENDIZ', TRUE);

-- Crear perfil de aprendiz para el usuario aprendiz con datos completos
INSERT INTO aprendices (
    usuario_id,
    direccion,
    ciudad,
    departamento,
    acudiente_tipo_doc,
    acudiente_documento,
    acudiente_nombres,
    acudiente_apellidos,
    acudiente_telefono,
    acudiente_email,
    colegio_id,
    grupo_id,
    programa_id,
    perfil_completo
) VALUES (
    (SELECT id FROM usuarios WHERE documento = '1000000002'),
    'Calle 15 #20-30',
    'Fusagasugá',
    'Cundinamarca',
    'CC',
    '52123456',
    'Ana María',
    'Martínez García',
    '3009876543',
    'ana.martinez@gmail.com',
    1, -- Institución Educativa Técnico Industrial
    1, -- Grupo 2824345 (Técnico en Sistemas - Mañana)
    1, -- Técnico en Sistemas
    TRUE
);

-- Vincular docente enlace al primer colegio
UPDATE colegios SET docente_enlace_id = (SELECT id FROM usuarios WHERE documento = '1000000001') WHERE id = 1;

-- ============================================
-- VERIFICACIÓN DE DATOS INSERTADOS
-- ============================================

SELECT '✓ Base de datos creada' AS Estado;
SELECT 'Programas creados:' AS Info, COUNT(*) AS Total FROM programas;
SELECT 'Colegios creados:' AS Info, COUNT(*) AS Total FROM colegios;
SELECT 'Grupos creados:' AS Info, COUNT(*) AS Total FROM grupos;
SELECT 'Novedades creadas:' AS Info, COUNT(*) AS Total FROM novedades;
SELECT 'Usuarios creados:' AS Info, COUNT(*) AS Total FROM usuarios;
SELECT 'Aprendices creados:' AS Info, COUNT(*) AS Total FROM aprendices;

-- ============================================
-- INFORMACIÓN IMPORTANTE
-- ============================================

SELECT '
==================================================================================
INSTALACIÓN COMPLETADA
==================================================================================

CREDENCIALES DE ACCESO:

Administrador:
  Usuario: 1000000000
  Contraseña: Admin123!

Docente Enlace:
  Usuario: 1000000001
  Contraseña: Docente123!

Aprendiz:
  Usuario: 1000000002
  Contraseña: Aprendiz123!

==================================================================================
CONFIGURACIÓN DEL ARCHIVO .env
==================================================================================

Asegúrate de agregar esta línea a tu archivo .env:

ENCRYPTION_KEY=cXNkL8qstj6vaRFTfJRqihhA1RBX-gi6PqJBdBWutJs=

IMPORTANTE: Esta clave es necesaria para que el administrador pueda ver las
contraseñas encriptadas de los usuarios.

==================================================================================
PASOS SIGUIENTES:
==================================================================================

1. Verifica que el archivo .env tenga la ENCRYPTION_KEY
2. Ejecuta la aplicación: python run.py
3. Accede a http://localhost:5000
4. Inicia sesión con las credenciales de prueba

==================================================================================
SEGURIDAD EN PRODUCCIÓN:
==================================================================================

⚠ ANTES DE PASAR A PRODUCCIÓN:
  - Cambia TODAS las contraseñas de prueba
  - Genera una nueva ENCRYPTION_KEY única
  - Actualiza los hashes en la base de datos
  - Elimina o deshabilita usuarios de prueba que no necesites
  - Configura SECRET_KEY único y seguro en .env

==================================================================================
' AS 'INFORMACIÓN IMPORTANTE';
