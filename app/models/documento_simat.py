from . import db
from datetime import datetime

class DocumentoSIMAT(db.Model):
    """
    Modelo para almacenar documentos SIMAT (Sistema de Matrícula Estudiantil)
    subidos por docentes enlace y aprobados por administradores
    """
    __tablename__ = 'documentos_simat'

    id = db.Column(db.Integer, primary_key=True)

    # Tipo de documento SIMAT (por colegio o por grupo)
    tipo = db.Column(db.Enum('COLEGIO', 'GRUPO'), nullable=False, default='COLEGIO')

    # Relaciones
    colegio_id = db.Column(db.Integer, db.ForeignKey('colegios.id', ondelete='CASCADE'), nullable=False, index=True)
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupos.id', ondelete='SET NULL'), nullable=True, index=True)

    # Usuario que subió el documento (docente enlace)
    subido_por = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='SET NULL'), nullable=True)

    # Ruta del archivo
    ruta_archivo = db.Column(db.String(500), nullable=False)
    nombre_archivo_original = db.Column(db.String(255), nullable=False)

    # Estado del documento
    estado = db.Column(
        db.Enum('PENDIENTE', 'APROBADO', 'RECHAZADO'),
        default='PENDIENTE',
        nullable=False
    )

    # Observaciones del administrador
    observaciones = db.Column(db.Text, nullable=True)

    # Usuario que revisó (admin)
    revisado_por = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='SET NULL'), nullable=True)
    fecha_revision = db.Column(db.DateTime, nullable=True)

    # Metadatos
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    colegio = db.relationship('Colegio', foreign_keys=[colegio_id], backref='documentos_simat')
    grupo = db.relationship('Grupo', foreign_keys=[grupo_id], backref='documentos_simat')
    usuario_subio = db.relationship('Usuario', foreign_keys=[subido_por], backref='simat_subidos')
    usuario_reviso = db.relationship('Usuario', foreign_keys=[revisado_por], backref='simat_revisados')

    def __repr__(self):
        return f'<DocumentoSIMAT {self.id} - {self.tipo} - {self.estado}>'
