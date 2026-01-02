-- =====================================================
-- SCRIPT BASE DE DATOS - SISTEMA DE ARTICULACIÓN SENA
-- Versión: 1.0 - Producción con datos de prueba
-- Fecha: Diciembre 2025
-- =====================================================

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `articulacion_sena`
--

-- =====================================================
-- ESTRUCTURA DE TABLAS
-- =====================================================

-- Tabla: alembic_version
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Tabla: usuarios
CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `documento` varchar(20) NOT NULL,
  `tipo_documento` enum('CC','TI','CE','PEP','PPT') NOT NULL DEFAULT 'CC',
  `nombres` varchar(100) NOT NULL,
  `apellidos` varchar(100) NOT NULL,
  `fecha_nacimiento` date DEFAULT NULL,
  `nombre_completo` varchar(200) GENERATED ALWAYS AS (concat(`nombres`,' ',`apellidos`)) STORED,
  `email` varchar(150) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `password_hash` varchar(255) NOT NULL,
  `password_cipher` text DEFAULT NULL,
  `rol` enum('APRENDIZ','DOCENTE','ADMINISTRADOR','RECTOR') NOT NULL DEFAULT 'APRENDIZ',
  `activo` tinyint(1) DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `documento` (`documento`),
  UNIQUE KEY `email` (`email`),
  KEY `idx_documento` (`documento`),
  KEY `idx_email` (`email`),
  KEY `idx_rol` (`rol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: programas
CREATE TABLE `programas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `codigo` varchar(20) DEFAULT NULL,
  `nombre` varchar(200) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `duracion_horas` int(11) DEFAULT NULL,
  `activo` tinyint(1) DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `codigo` (`codigo`),
  KEY `idx_codigo` (`codigo`),
  KEY `idx_activo` (`activo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: colegios
CREATE TABLE `colegios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(200) NOT NULL,
  `tipo_colegio` enum('PUBLICO','PRIVADO','MIXTO') NOT NULL DEFAULT 'PUBLICO',
  `direccion` varchar(255) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `email` varchar(150) DEFAULT NULL,
  `rector_id` int(11) DEFAULT NULL,
  `docente_enlace_id` int(11) DEFAULT NULL,
  `activo` tinyint(1) DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `rector_id` (`rector_id`),
  KEY `docente_enlace_id` (`docente_enlace_id`),
  KEY `idx_nombre` (`nombre`),
  KEY `idx_activo` (`activo`),
  CONSTRAINT `colegios_ibfk_1` FOREIGN KEY (`rector_id`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL,
  CONSTRAINT `colegios_ibfk_2` FOREIGN KEY (`docente_enlace_id`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: grupos
CREATE TABLE `grupos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `colegio_id` int(11) NOT NULL,
  `programa_id` int(11) NOT NULL,
  `jornada` enum('MAÑANA','TARDE','NOCHE','UNICA') DEFAULT 'UNICA',
  `año_lectivo` int(11) NOT NULL,
  `activo` tinyint(1) DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_grupo` (`nombre`,`colegio_id`,`año_lectivo`),
  KEY `idx_colegio` (`colegio_id`),
  KEY `idx_programa` (`programa_id`),
  KEY `idx_activo` (`activo`),
  CONSTRAINT `grupos_ibfk_1` FOREIGN KEY (`colegio_id`) REFERENCES `colegios` (`id`) ON DELETE CASCADE,
  CONSTRAINT `grupos_ibfk_2` FOREIGN KEY (`programa_id`) REFERENCES `programas` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: aprendices
CREATE TABLE `aprendices` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usuario_id` int(11) NOT NULL,
  `ciudad` varchar(100) DEFAULT NULL,
  `departamento` varchar(100) DEFAULT NULL,
  `acudiente_tipo_doc` enum('CC','TI','CE','PEP','PPT') DEFAULT 'CC',
  `acudiente_documento` varchar(20) DEFAULT NULL,
  `acudiente_lugar_expedicion` varchar(100) DEFAULT NULL,
  `acudiente_nombres` varchar(100) DEFAULT NULL,
  `acudiente_apellidos` varchar(100) DEFAULT NULL,
  `acudiente_direccion` varchar(255) DEFAULT NULL,
  `acudiente_telefono` varchar(20) DEFAULT NULL,
  `acudiente_email` varchar(150) DEFAULT NULL,
  `colegio_id` int(11) DEFAULT NULL,
  `grupo_id` int(11) DEFAULT NULL,
  `programa_id` int(11) DEFAULT NULL,
  `perfil_completo` tinyint(1) DEFAULT 0,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuario_id` (`usuario_id`),
  KEY `programa_id` (`programa_id`),
  KEY `idx_usuario` (`usuario_id`),
  KEY `idx_colegio` (`colegio_id`),
  KEY `idx_grupo` (`grupo_id`),
  CONSTRAINT `aprendices_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  CONSTRAINT `aprendices_ibfk_2` FOREIGN KEY (`colegio_id`) REFERENCES `colegios` (`id`) ON DELETE SET NULL,
  CONSTRAINT `aprendices_ibfk_3` FOREIGN KEY (`grupo_id`) REFERENCES `grupos` (`id`) ON DELETE SET NULL,
  CONSTRAINT `aprendices_ibfk_4` FOREIGN KEY (`programa_id`) REFERENCES `programas` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: matriculas
CREATE TABLE `matriculas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `aprendiz_id` int(11) NOT NULL,
  `estado` enum('BORRADOR','ENVIADO','PENDIENTE','COMPLETO','PREMATRICULA','MATRICULADO') DEFAULT 'BORRADOR',
  `validado_por_docente` int(11) DEFAULT NULL,
  `validado_por_admin` int(11) DEFAULT NULL,
  `fecha_envio` timestamp NULL DEFAULT NULL,
  `fecha_validacion_docente` timestamp NULL DEFAULT NULL,
  `fecha_validacion_admin` timestamp NULL DEFAULT NULL,
  `observaciones_docente` text DEFAULT NULL,
  `observaciones_admin` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `idx_aprendiz` (`aprendiz_id`),
  KEY `idx_estado` (`estado`),
  KEY `idx_fecha_envio` (`fecha_envio`),
  KEY `fk_matriculas_admin` (`validado_por_admin`),
  KEY `fk_matriculas_docente` (`validado_por_docente`),
  CONSTRAINT `fk_matriculas_admin` FOREIGN KEY (`validado_por_admin`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_matriculas_docente` FOREIGN KEY (`validado_por_docente`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL,
  CONSTRAINT `matriculas_ibfk_1` FOREIGN KEY (`aprendiz_id`) REFERENCES `aprendices` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: documentos
CREATE TABLE `documentos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `matricula_id` int(11) NOT NULL,
  `tipo_documento` enum('DOCUMENTO_IDENTIDAD','REGISTRO_CIVIL','CERTIFICADO_SALUD','CERTIFICADO_SOFIA','CERTIFICADO_APE','DOCUMENTO_ACUDIENTE','TRATAMIENTO_DATOS','ACUERDO_APRENDIZ') NOT NULL,
  `nombre_archivo` varchar(255) NOT NULL,
  `ruta_archivo` varchar(500) NOT NULL,
  `tamaño_bytes` int(11) DEFAULT NULL,
  `extension` varchar(10) DEFAULT NULL,
  `validado` tinyint(1) DEFAULT 0,
  `validado_por` int(11) DEFAULT NULL,
  `fecha_validacion` timestamp NULL DEFAULT NULL,
  `reemplazado_por` int(11) DEFAULT NULL,
  `observaciones` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `validado_por` (`validado_por`),
  KEY `reemplazado_por` (`reemplazado_por`),
  KEY `idx_matricula` (`matricula_id`),
  KEY `idx_tipo` (`tipo_documento`),
  KEY `idx_validado` (`validado`),
  CONSTRAINT `documentos_ibfk_1` FOREIGN KEY (`matricula_id`) REFERENCES `matriculas` (`id`) ON DELETE CASCADE,
  CONSTRAINT `documentos_ibfk_2` FOREIGN KEY (`validado_por`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL,
  CONSTRAINT `documentos_ibfk_3` FOREIGN KEY (`reemplazado_por`) REFERENCES `documentos` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: documentos_simat
CREATE TABLE `documentos_simat` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tipo` enum('COLEGIO','GRUPO') NOT NULL DEFAULT 'COLEGIO',
  `colegio_id` int(11) NOT NULL,
  `grupo_id` int(11) DEFAULT NULL,
  `subido_por` int(11) DEFAULT NULL,
  `ruta_archivo` varchar(500) NOT NULL,
  `nombre_archivo_original` varchar(255) NOT NULL,
  `estado` enum('PENDIENTE','APROBADO','RECHAZADO') NOT NULL DEFAULT 'PENDIENTE',
  `observaciones` text DEFAULT NULL,
  `revisado_por` int(11) DEFAULT NULL,
  `fecha_revision` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `fk_simat_subido_por` (`subido_por`),
  KEY `fk_simat_revisado_por` (`revisado_por`),
  KEY `idx_simat_colegio` (`colegio_id`),
  KEY `idx_simat_grupo` (`grupo_id`),
  KEY `idx_simat_estado` (`estado`),
  KEY `idx_simat_created` (`created_at`),
  CONSTRAINT `fk_simat_colegio` FOREIGN KEY (`colegio_id`) REFERENCES `colegios` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_simat_grupo` FOREIGN KEY (`grupo_id`) REFERENCES `grupos` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_simat_revisado_por` FOREIGN KEY (`revisado_por`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_simat_subido_por` FOREIGN KEY (`subido_por`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: novedades
CREATE TABLE `novedades` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `titulo` varchar(200) NOT NULL,
  `contenido` text NOT NULL,
  `imagen` varchar(500) DEFAULT NULL,
  `autor_id` int(11) DEFAULT NULL,
  `fecha_publicacion` date NOT NULL,
  `destacado` tinyint(1) DEFAULT 0,
  `activo` tinyint(1) DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `autor_id` (`autor_id`),
  KEY `idx_fecha` (`fecha_publicacion`),
  KEY `idx_activo` (`activo`),
  KEY `idx_destacado` (`destacado`),
  CONSTRAINT `novedades_ibfk_1` FOREIGN KEY (`autor_id`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: mensajes_contacto
CREATE TABLE `mensajes_contacto` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(150) NOT NULL,
  `email` varchar(150) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `asunto` varchar(200) NOT NULL,
  `mensaje` text NOT NULL,
  `leido` tinyint(1) DEFAULT 0,
  `respondido` tinyint(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `idx_leido` (`leido`),
  KEY `idx_fecha` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla: auditoria
CREATE TABLE `auditoria` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usuario_id` int(11) DEFAULT NULL,
  `accion` varchar(100) NOT NULL,
  `tabla` varchar(50) DEFAULT NULL,
  `registro_id` int(11) DEFAULT NULL,
  `datos_antes` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`datos_antes`)),
  `datos_despues` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`datos_despues`)),
  `ip_address` varchar(45) DEFAULT NULL,
  `user_agent` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `idx_usuario` (`usuario_id`),
  KEY `idx_tabla` (`tabla`),
  KEY `idx_fecha` (`created_at`),
  CONSTRAINT `auditoria_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- DATOS DE PRUEBA
-- =====================================================

-- USUARIOS DE PRUEBA
-- Contraseña para todos: Admin123!
INSERT INTO `usuarios` (`id`, `documento`, `tipo_documento`, `nombres`, `apellidos`, `fecha_nacimiento`, `email`, `telefono`, `password_hash`, `rol`, `activo`) VALUES
(1, '1000000001', 'CC', 'Admin', 'Sistema', '1990-01-01', 'admin@sena.edu.co', '3001234567', 'scrypt:32768:8:1$PCZgbrgMznk3MY5k$c5341878864a97caeb6740e7b17f17dd999bf3bacff89f262079cd117204fda74b39e86fd4cdcb616e981df0183895c8f952b5556caf4d8c4e93366dc0aa5f69', 'ADMINISTRADOR', 1),
(2, '1000000002', 'CC', 'Carlos', 'Rodríguez', '1975-05-15', 'rector@colegio1.edu.co', '3109876543', 'scrypt:32768:8:1$PCZgbrgMznk3MY5k$c5341878864a97caeb6740e7b17f17dd999bf3bacff89f262079cd117204fda74b39e86fd4cdcb616e981df0183895c8f952b5556caf4d8c4e93366dc0aa5f69', 'RECTOR', 1),
(3, '1000000003', 'CC', 'María', 'González', '1985-08-20', 'docente1@colegio1.edu.co', '3201234567', 'scrypt:32768:8:1$PCZgbrgMznk3MY5k$c5341878864a97caeb6740e7b17f17dd999bf3bacff89f262079cd117204fda74b39e86fd4cdcb616e981df0183895c8f952b5556caf4d8c4e93366dc0aa5f69', 'DOCENTE', 1),
(4, '1000000004', 'TI', 'Juan', 'Pérez', '2007-03-10', 'juan.perez@estudiante.edu.co', '3158765432', 'scrypt:32768:8:1$PCZgbrgMznk3MY5k$c5341878864a97caeb6740e7b17f17dd999bf3bacff89f262079cd117204fda74b39e86fd4cdcb616e981df0183895c8f952b5556caf4d8c4e93366dc0aa5f69', 'APRENDIZ', 1),
(5, '1000000005', 'TI', 'Ana', 'Martínez', '2007-07-25', 'ana.martinez@estudiante.edu.co', '3167654321', 'scrypt:32768:8:1$PCZgbrgMznk3MY5k$c5341878864a97caeb6740e7b17f17dd999bf3bacff89f262079cd117204fda74b39e86fd4cdcb616e981df0183895c8f952b5556caf4d8c4e93366dc0aa5f69', 'APRENDIZ', 1);

-- PROGRAMAS
INSERT INTO `programas` (`id`, `codigo`, `nombre`, `descripcion`, `duracion_horas`, `activo`) VALUES
(1, 'TEC-SIS-001', 'Técnico en Sistemas', 'Programa de formación técnica en desarrollo de software y administración de sistemas informáticos.', 1980, 1),
(2, 'TEC-ADM-001', 'Técnico en Administración', 'Formación en gestión administrativa y procesos organizacionales.', 1760, 1),
(3, 'TEC-CON-001', 'Técnico en Contabilidad', 'Programa de formación en contabilidad y finanzas empresariales.', 1760, 1),
(4, 'TEC-MEC-001', 'Técnico en Mecánica Industrial', 'Formación en mantenimiento y operación de maquinaria industrial.', 2200, 1),
(5, 'TEC-ELE-001', 'Técnico en Electricidad', 'Programa de instalaciones eléctricas residenciales e industriales.', 2000, 1),
(6, 'TEC-LOG-001', 'Técnico en Logística', 'Formación en gestión de cadena de suministro y operaciones logísticas.', 1980, 1);

-- COLEGIOS
INSERT INTO `colegios` (`id`, `nombre`, `tipo_colegio`, `direccion`, `telefono`, `email`, `rector_id`, `docente_enlace_id`, `activo`) VALUES
(1, 'Institución Educativa Distrital San José', 'PUBLICO', 'Calle 45 # 12-34', '6012345678', 'contacto@colegiosanjose.edu.co', 2, 3, 1),
(2, 'Colegio Departamental La Esperanza', 'PUBLICO', 'Carrera 20 # 30-15', '6013456789', 'info@laesperanza.edu.co', NULL, NULL, 1),
(3, 'Instituto Técnico Industrial', 'PUBLICO', 'Avenida 68 # 25-80', '6014567890', 'contacto@itindustrial.edu.co', NULL, NULL, 1);

-- GRUPOS
INSERT INTO `grupos` (`id`, `nombre`, `colegio_id`, `programa_id`, `jornada`, `año_lectivo`, `activo`) VALUES
(1, '11-A', 1, 1, 'MAÑANA', 2025, 1),
(2, '11-B', 1, 2, 'MAÑANA', 2025, 1),
(3, '11-C', 1, 3, 'TARDE', 2025, 1),
(4, '11-A', 2, 4, 'MAÑANA', 2025, 1),
(5, '11-B', 2, 5, 'TARDE', 2025, 1);

-- APRENDICES
INSERT INTO `aprendices` (`id`, `usuario_id`, `ciudad`, `departamento`, `colegio_id`, `grupo_id`, `programa_id`, `perfil_completo`, `acudiente_tipo_doc`, `acudiente_documento`, `acudiente_nombres`, `acudiente_apellidos`, `acudiente_telefono`, `acudiente_email`) VALUES
(1, 4, 'Bogotá', 'Cundinamarca', 1, 1, 1, 1, 'CC', '80000001', 'Roberto', 'Pérez', '3001112222', 'roberto.perez@email.com'),
(2, 5, 'Bogotá', 'Cundinamarca', 1, 2, 2, 1, 'CC', '80000002', 'Patricia', 'Martínez', '3002223333', 'patricia.martinez@email.com');

-- NOVEDADES
INSERT INTO `novedades` (`id`, `titulo`, `contenido`, `autor_id`, `fecha_publicacion`, `destacado`, `activo`) VALUES
(1, 'Bienvenidos al proceso de articulación 2025', 'Nos complace darles la bienvenida al programa de articulación con la media técnica del SENA. Este año contamos con 6 programas técnicos disponibles para que nuestros estudiantes puedan formarse en competencias laborales de alta calidad.', 1, '2025-01-15', 1, 1),
(2, 'Fechas importantes primer semestre', 'Recuerden las fechas clave del primer semestre: Inicio de clases: Febrero 3, Entrega de documentos: Hasta febrero 10, Primera evaluación: Marzo 15-20.', 1, '2025-01-20', 1, 1),
(3, 'Inscripciones abiertas', 'Las inscripciones para el programa de articulación están abiertas. Los estudiantes interesados pueden registrarse en la plataforma y completar su información.', 1, '2025-01-10', 0, 1);

-- =====================================================
-- RESETEAR AUTO_INCREMENT
-- =====================================================

ALTER TABLE `usuarios` AUTO_INCREMENT = 6;
ALTER TABLE `programas` AUTO_INCREMENT = 7;
ALTER TABLE `colegios` AUTO_INCREMENT = 4;
ALTER TABLE `grupos` AUTO_INCREMENT = 6;
ALTER TABLE `aprendices` AUTO_INCREMENT = 3;
ALTER TABLE `matriculas` AUTO_INCREMENT = 1;
ALTER TABLE `documentos` AUTO_INCREMENT = 1;
ALTER TABLE `documentos_simat` AUTO_INCREMENT = 1;
ALTER TABLE `novedades` AUTO_INCREMENT = 4;
ALTER TABLE `mensajes_contacto` AUTO_INCREMENT = 1;
ALTER TABLE `auditoria` AUTO_INCREMENT = 1;

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

-- =====================================================
-- INFORMACIÓN DE USUARIOS DE PRUEBA
-- =====================================================
-- TODOS LOS USUARIOS TIENEN LA CONTRASEÑA: Admin123!
--
-- ADMINISTRADOR:
--   Email: admin@sena.edu.co
--   Documento: 1000000001
--
-- RECTOR:
--   Email: rector@colegio1.edu.co
--   Documento: 1000000002
--
-- DOCENTE:
--   Email: docente1@colegio1.edu.co
--   Documento: 1000000003
--
-- APRENDICES:
--   Email: juan.perez@estudiante.edu.co
--   Documento: 1000000004
--
--   Email: ana.martinez@estudiante.edu.co
--   Documento: 1000000005
-- =====================================================
