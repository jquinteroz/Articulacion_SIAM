-- Migración: Agregar tabla documentos_simat para registro SIMAT
-- Fecha: 2025-12-11
-- Descripción: Tabla para almacenar documentos SIMAT subidos por docentes y aprobados por admin

CREATE TABLE IF NOT EXISTS documentos_simat (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo ENUM('COLEGIO', 'GRUPO') NOT NULL DEFAULT 'COLEGIO' COMMENT 'Si el SIMAT es por colegio o por grupo específico',
    colegio_id INT NOT NULL COMMENT 'Colegio al que pertenece el documento',
    grupo_id INT NULL COMMENT 'Grupo específico (null si es para todo el colegio)',
    subido_por INT NULL COMMENT 'ID del docente que subió el documento',
    ruta_archivo VARCHAR(500) NOT NULL COMMENT 'Ruta donde se almacena el archivo',
    nombre_archivo_original VARCHAR(255) NOT NULL COMMENT 'Nombre original del archivo subido',
    estado ENUM('PENDIENTE', 'APROBADO', 'RECHAZADO') NOT NULL DEFAULT 'PENDIENTE' COMMENT 'Estado de revisión',
    observaciones TEXT NULL COMMENT 'Comentarios del administrador',
    revisado_por INT NULL COMMENT 'ID del admin que revisó',
    fecha_revision DATETIME NULL COMMENT 'Fecha de aprobación/rechazo',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- Claves foráneas
    CONSTRAINT fk_simat_colegio FOREIGN KEY (colegio_id) REFERENCES colegios(id) ON DELETE CASCADE,
    CONSTRAINT fk_simat_grupo FOREIGN KEY (grupo_id) REFERENCES grupos(id) ON DELETE SET NULL,
    CONSTRAINT fk_simat_subido_por FOREIGN KEY (subido_por) REFERENCES usuarios(id) ON DELETE SET NULL,
    CONSTRAINT fk_simat_revisado_por FOREIGN KEY (revisado_por) REFERENCES usuarios(id) ON DELETE SET NULL,

    -- Índices
    INDEX idx_simat_colegio (colegio_id),
    INDEX idx_simat_grupo (grupo_id),
    INDEX idx_simat_estado (estado),
    INDEX idx_simat_created (created_at DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
