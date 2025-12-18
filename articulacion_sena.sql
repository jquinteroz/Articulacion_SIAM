-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 18-12-2025 a las 21:36:01
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

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

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `alembic_version`
--

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `aprendices`
--

CREATE TABLE `aprendices` (
  `id` int(11) NOT NULL,
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
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auditoria`
--

CREATE TABLE `auditoria` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `accion` varchar(100) NOT NULL,
  `tabla` varchar(50) DEFAULT NULL,
  `registro_id` int(11) DEFAULT NULL,
  `datos_antes` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`datos_antes`)),
  `datos_despues` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`datos_despues`)),
  `ip_address` varchar(45) DEFAULT NULL,
  `user_agent` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `colegios`
--

CREATE TABLE `colegios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(200) NOT NULL,
  `tipo_colegio` enum('PUBLICO','PRIVADO','MIXTO') NOT NULL DEFAULT 'PUBLICO',
  `direccion` varchar(255) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `email` varchar(150) DEFAULT NULL,
  `rector_id` int(11) DEFAULT NULL,
  `docente_enlace_id` int(11) DEFAULT NULL,
  `activo` tinyint(1) DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `documentos`
--

CREATE TABLE `documentos` (
  `id` int(11) NOT NULL,
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
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `documentos_simat`
--

CREATE TABLE `documentos_simat` (
  `id` int(11) NOT NULL,
  `tipo` enum('COLEGIO','GRUPO') NOT NULL DEFAULT 'COLEGIO' COMMENT 'Si el SIMAT es por colegio o por grupo espec├¡fico',
  `colegio_id` int(11) NOT NULL COMMENT 'Colegio al que pertenece el documento',
  `grupo_id` int(11) DEFAULT NULL COMMENT 'Grupo espec├¡fico (null si es para todo el colegio)',
  `subido_por` int(11) DEFAULT NULL COMMENT 'ID del docente que subi├│ el documento',
  `ruta_archivo` varchar(500) NOT NULL COMMENT 'Ruta donde se almacena el archivo',
  `nombre_archivo_original` varchar(255) NOT NULL COMMENT 'Nombre original del archivo subido',
  `estado` enum('PENDIENTE','APROBADO','RECHAZADO') NOT NULL DEFAULT 'PENDIENTE' COMMENT 'Estado de revisi├│n',
  `observaciones` text DEFAULT NULL COMMENT 'Comentarios del administrador',
  `revisado_por` int(11) DEFAULT NULL COMMENT 'ID del admin que revis├│',
  `fecha_revision` datetime DEFAULT NULL COMMENT 'Fecha de aprobaci├│n/rechazo',
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `grupos`
--

CREATE TABLE `grupos` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `colegio_id` int(11) NOT NULL,
  `programa_id` int(11) NOT NULL,
  `jornada` enum('MAÑANA','TARDE','NOCHE','UNICA') DEFAULT 'UNICA',
  `año_lectivo` int(11) NOT NULL,
  `activo` tinyint(1) DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `matriculas`
--

CREATE TABLE `matriculas` (
  `id` int(11) NOT NULL,
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
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `mensajes_contacto`
--

CREATE TABLE `mensajes_contacto` (
  `id` int(11) NOT NULL,
  `nombre` varchar(150) NOT NULL,
  `email` varchar(150) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `asunto` varchar(200) NOT NULL,
  `mensaje` text NOT NULL,
  `leido` tinyint(1) DEFAULT 0,
  `respondido` tinyint(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `mensajes_contacto`
--

INSERT INTO `mensajes_contacto` (`id`, `nombre`, `email`, `telefono`, `asunto`, `mensaje`, `leido`, `respondido`, `created_at`) VALUES
(1, 'Maria Rodriguez Test', 'maria.test@ejemplo.com', '3109876543', 'Pregunta sobre horarios - PRUEBA AUTOMATICA', 'Hola, me gustaria saber los horarios de los programas de articulacion. Esta es una prueba automatica del sistema de contacto.', 1, 0, '2025-12-16 19:26:16'),
(2, 'Carlos Martinez Prueba', 'carlos.test@ejemplo.com', '3201234567', 'Consulta sobre inscripciones - TEST', 'Buenos dias, quisiera saber como puedo inscribirme en los programas de articulacion. Esta es una prueba del formulario.', 1, 0, '2025-12-16 19:26:46'),
(3, 'Edwin Cañon', 'admin@tienda.com', '1234567', 'Inscripcion a los tecnologos', 'envio solicitud para validar la inscripción de los aprendices del colegio arborizadora al tecnologo', 1, 1, '2025-12-16 19:54:19');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `novedades`
--

CREATE TABLE `novedades` (
  `id` int(11) NOT NULL,
  `titulo` varchar(200) NOT NULL,
  `contenido` text NOT NULL,
  `imagen` varchar(500) DEFAULT NULL,
  `autor_id` int(11) DEFAULT NULL,
  `fecha_publicacion` date NOT NULL,
  `destacado` tinyint(1) DEFAULT 0,
  `activo` tinyint(1) DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `novedades`
--

INSERT INTO `novedades` (`id`, `titulo`, `contenido`, `imagen`, `autor_id`, `fecha_publicacion`, `destacado`, `activo`, `created_at`, `updated_at`) VALUES
(1, 'Apertura de convocatoria 2025', 'Informamos a la comunidad educativa que está abierta la convocatoria para matrículas del programa de articulación con la media técnica para el año lectivo 2025. Los estudiantes interesados pueden registrarse a través de la plataforma.', NULL, NULL, '2025-12-06', 1, 1, '2025-12-06 19:42:24', '2025-12-06 19:42:24'),
(2, 'Bienvenida nuevo año académico', 'Damos la bienvenida a todos los aprendices que inician su proceso formativo en articulación con la media técnica. Esperamos que esta sea una experiencia enriquecedora.', NULL, NULL, '2025-12-06', 1, 1, '2025-12-06 19:42:24', '2025-12-06 19:42:24'),
(3, 'Fechas importantes', 'Recuerden revisar el calendario académico con las fechas de inicio de clases, entregas de documentos y actividades especiales del programa.', NULL, NULL, '2025-12-06', 0, 1, '2025-12-06 19:42:24', '2025-12-06 19:42:24');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `programas`
--

CREATE TABLE `programas` (
  `id` int(11) NOT NULL,
  `codigo` varchar(20) DEFAULT NULL,
  `nombre` varchar(200) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `duracion_horas` int(11) DEFAULT NULL,
  `activo` tinyint(1) DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
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
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `documento`, `tipo_documento`, `nombres`, `apellidos`, `fecha_nacimiento`, `email`, `telefono`, `password_hash`, `password_cipher`, `rol`, `activo`, `created_at`, `updated_at`) VALUES
(19, '1000000000', 'CC', 'Administrador', 'Sistema', NULL, 'admin@articulacion.sena.edu.co', NULL, 'scrypt:32768:8:1$PCZgbrgMznk3MY5k$c5341878864a97caeb6740e7b17f17dd999bf3bacff89f262079cd117204fda74b39e86fd4cdcb616e981df0183895c8f952b5556caf4d8c4e93366dc0aa5f69', NULL, 'ADMINISTRADOR', 1, '2025-12-19 00:59:33', '2025-12-19 00:59:33');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `alembic_version`
--
ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);

--
-- Indices de la tabla `aprendices`
--
ALTER TABLE `aprendices`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `usuario_id` (`usuario_id`),
  ADD KEY `programa_id` (`programa_id`),
  ADD KEY `idx_usuario` (`usuario_id`),
  ADD KEY `idx_colegio` (`colegio_id`),
  ADD KEY `idx_grupo` (`grupo_id`);

--
-- Indices de la tabla `auditoria`
--
ALTER TABLE `auditoria`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_usuario` (`usuario_id`),
  ADD KEY `idx_tabla` (`tabla`),
  ADD KEY `idx_fecha` (`created_at`);

--
-- Indices de la tabla `colegios`
--
ALTER TABLE `colegios`
  ADD PRIMARY KEY (`id`),
  ADD KEY `rector_id` (`rector_id`),
  ADD KEY `docente_enlace_id` (`docente_enlace_id`),
  ADD KEY `idx_nombre` (`nombre`),
  ADD KEY `idx_activo` (`activo`);

--
-- Indices de la tabla `documentos`
--
ALTER TABLE `documentos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `validado_por` (`validado_por`),
  ADD KEY `reemplazado_por` (`reemplazado_por`),
  ADD KEY `idx_matricula` (`matricula_id`),
  ADD KEY `idx_tipo` (`tipo_documento`),
  ADD KEY `idx_validado` (`validado`);

--
-- Indices de la tabla `documentos_simat`
--
ALTER TABLE `documentos_simat`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_simat_subido_por` (`subido_por`),
  ADD KEY `fk_simat_revisado_por` (`revisado_por`),
  ADD KEY `idx_simat_colegio` (`colegio_id`),
  ADD KEY `idx_simat_grupo` (`grupo_id`),
  ADD KEY `idx_simat_estado` (`estado`),
  ADD KEY `idx_simat_created` (`created_at`);

--
-- Indices de la tabla `grupos`
--
ALTER TABLE `grupos`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_grupo` (`nombre`,`colegio_id`,`año_lectivo`),
  ADD KEY `idx_colegio` (`colegio_id`),
  ADD KEY `idx_programa` (`programa_id`),
  ADD KEY `idx_activo` (`activo`);

--
-- Indices de la tabla `matriculas`
--
ALTER TABLE `matriculas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_aprendiz` (`aprendiz_id`),
  ADD KEY `idx_estado` (`estado`),
  ADD KEY `idx_fecha_envio` (`fecha_envio`),
  ADD KEY `fk_matriculas_admin` (`validado_por_admin`),
  ADD KEY `fk_matriculas_docente` (`validado_por_docente`);

--
-- Indices de la tabla `mensajes_contacto`
--
ALTER TABLE `mensajes_contacto`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_leido` (`leido`),
  ADD KEY `idx_fecha` (`created_at`);

--
-- Indices de la tabla `novedades`
--
ALTER TABLE `novedades`
  ADD PRIMARY KEY (`id`),
  ADD KEY `autor_id` (`autor_id`),
  ADD KEY `idx_fecha` (`fecha_publicacion`),
  ADD KEY `idx_activo` (`activo`),
  ADD KEY `idx_destacado` (`destacado`);

--
-- Indices de la tabla `programas`
--
ALTER TABLE `programas`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `codigo` (`codigo`),
  ADD KEY `idx_codigo` (`codigo`),
  ADD KEY `idx_activo` (`activo`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `documento` (`documento`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `idx_documento` (`documento`),
  ADD KEY `idx_email` (`email`),
  ADD KEY `idx_rol` (`rol`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `aprendices`
--
ALTER TABLE `aprendices`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `auditoria`
--
ALTER TABLE `auditoria`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `colegios`
--
ALTER TABLE `colegios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `documentos`
--
ALTER TABLE `documentos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=63;

--
-- AUTO_INCREMENT de la tabla `documentos_simat`
--
ALTER TABLE `documentos_simat`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `grupos`
--
ALTER TABLE `grupos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT de la tabla `matriculas`
--
ALTER TABLE `matriculas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `mensajes_contacto`
--
ALTER TABLE `mensajes_contacto`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `novedades`
--
ALTER TABLE `novedades`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `programas`
--
ALTER TABLE `programas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `aprendices`
--
ALTER TABLE `aprendices`
  ADD CONSTRAINT `aprendices_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `aprendices_ibfk_2` FOREIGN KEY (`colegio_id`) REFERENCES `colegios` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `aprendices_ibfk_3` FOREIGN KEY (`grupo_id`) REFERENCES `grupos` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `aprendices_ibfk_4` FOREIGN KEY (`programa_id`) REFERENCES `programas` (`id`) ON DELETE SET NULL;

--
-- Filtros para la tabla `auditoria`
--
ALTER TABLE `auditoria`
  ADD CONSTRAINT `auditoria_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL;

--
-- Filtros para la tabla `colegios`
--
ALTER TABLE `colegios`
  ADD CONSTRAINT `colegios_ibfk_1` FOREIGN KEY (`rector_id`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `colegios_ibfk_2` FOREIGN KEY (`docente_enlace_id`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL;

--
-- Filtros para la tabla `documentos`
--
ALTER TABLE `documentos`
  ADD CONSTRAINT `documentos_ibfk_1` FOREIGN KEY (`matricula_id`) REFERENCES `matriculas` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `documentos_ibfk_2` FOREIGN KEY (`validado_por`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `documentos_ibfk_3` FOREIGN KEY (`reemplazado_por`) REFERENCES `documentos` (`id`) ON DELETE SET NULL;

--
-- Filtros para la tabla `documentos_simat`
--
ALTER TABLE `documentos_simat`
  ADD CONSTRAINT `fk_simat_colegio` FOREIGN KEY (`colegio_id`) REFERENCES `colegios` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_simat_grupo` FOREIGN KEY (`grupo_id`) REFERENCES `grupos` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `fk_simat_revisado_por` FOREIGN KEY (`revisado_por`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `fk_simat_subido_por` FOREIGN KEY (`subido_por`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL;

--
-- Filtros para la tabla `grupos`
--
ALTER TABLE `grupos`
  ADD CONSTRAINT `grupos_ibfk_1` FOREIGN KEY (`colegio_id`) REFERENCES `colegios` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `grupos_ibfk_2` FOREIGN KEY (`programa_id`) REFERENCES `programas` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `matriculas`
--
ALTER TABLE `matriculas`
  ADD CONSTRAINT `fk_matriculas_admin` FOREIGN KEY (`validado_por_admin`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `fk_matriculas_docente` FOREIGN KEY (`validado_por_docente`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `matriculas_ibfk_1` FOREIGN KEY (`aprendiz_id`) REFERENCES `aprendices` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `matriculas_ibfk_2` FOREIGN KEY (`validado_por_docente`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `matriculas_ibfk_3` FOREIGN KEY (`validado_por_admin`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL;

--
-- Filtros para la tabla `novedades`
--
ALTER TABLE `novedades`
  ADD CONSTRAINT `novedades_ibfk_1` FOREIGN KEY (`autor_id`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
