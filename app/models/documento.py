from . import db
from datetime import datetime

class Documento(db.Model):
    __tablename__ = 'documentos'

    id = db.Column(db.Integer, primary_key=True)
    matricula_id = db.Column(db.Integer, db.ForeignKey('matriculas.id', ondelete='CASCADE'), nullable=False, index=True)
    tipo_documento = db.Column(
        db.Enum(
            'DOCUMENTO_IDENTIDAD',
            'REGISTRO_CIVIL',
            'CERTIFICADO_SALUD',
            'CERTIFICADO_SOFIA',
            'CERTIFICADO_APE',
            'DOCUMENTO_ACUDIENTE',
            'TRATAMIENTO_DATOS',
            'ACUERDO_APRENDIZ'
        ),
        nullable=False,
        index=True
    )
    nombre_archivo = db.Column(db.String(255), nullable=False)
    ruta_archivo = db.Column(db.String(500), nullable=False)
    tamaño_bytes = db.Column(db.Integer)
    extension = db.Column(db.String(10))
    validado = db.Column(db.Boolean, default=None, index=True)
    validado_por = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='SET NULL'))
    fecha_validacion = db.Column(db.DateTime)
    reemplazado_por = db.Column(db.Integer, db.ForeignKey('documentos.id', ondelete='SET NULL'))
    observaciones = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones
    matricula = db.relationship('Matricula', back_populates='documentos')
    validador = db.relationship('Usuario', foreign_keys=[validado_por])
    reemplazo = db.relationship('Documento', remote_side=[id], uselist=False)

    TIPOS_LABELS = {
        'DOCUMENTO_IDENTIDAD': 'Documento de Identidad',
        'REGISTRO_CIVIL': 'Registro Civil',
        'CERTIFICADO_SALUD': 'Certificado de Afiliación a Salud',
        'CERTIFICADO_SOFIA': 'Certificado SOFIA Plus',
        'CERTIFICADO_APE': 'Certificado APE',
        'DOCUMENTO_ACUDIENTE': 'Documento del Acudiente',
        'TRATAMIENTO_DATOS': 'Tratamiento de Datos',
        'ACUERDO_APRENDIZ': 'Acuerdo del Aprendiz'
    }

    @property
    def tipo_label(self):
        return self.TIPOS_LABELS.get(self.tipo_documento, self.tipo_documento)

    @property
    def fecha_subida(self):
        """Alias para created_at para compatibilidad con templates"""
        return self.created_at

    @property
    def estado(self):
        """Retorna el estado del documento basado en validacion"""
        if self.reemplazado_por:
            return 'REEMPLAZADO'
        elif self.validado == True:
            return 'APROBADO'
        elif self.validado == False:
            return 'RECHAZADO'
        else:
            # validado es None - documento subido pero no revisado
            return 'PENDIENTE'

    def __repr__(self):
        return f'<Documento {self.tipo_documento} - {self.nombre_archivo}>'
