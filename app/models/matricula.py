from . import db
from datetime import datetime

class Matricula(db.Model):
    __tablename__ = 'matriculas'

    id = db.Column(db.Integer, primary_key=True)
    aprendiz_id = db.Column(db.Integer, db.ForeignKey('aprendices.id', ondelete='CASCADE'), nullable=False, index=True)
    estado = db.Column(
        db.Enum('BORRADOR', 'ENVIADO', 'PENDIENTE', 'COMPLETO', 'PREMATRICULA', 'MATRICULADO', 'RECHAZADO'),
        nullable=False,
        default='BORRADOR',
        index=True
    )
    validado_por_docente = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='SET NULL'))
    validado_por_admin = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='SET NULL'))
    fecha_envio = db.Column(db.DateTime, index=True)
    fecha_validacion_docente = db.Column(db.DateTime)
    fecha_validacion_admin = db.Column(db.DateTime)
    observaciones_docente = db.Column(db.Text)
    observaciones_admin = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    aprendiz = db.relationship('Aprendiz', back_populates='matriculas')
    docente_validador = db.relationship('Usuario', foreign_keys=[validado_por_docente])
    admin_validador = db.relationship('Usuario', foreign_keys=[validado_por_admin])
    documentos = db.relationship('Documento', back_populates='matricula', cascade='all, delete-orphan')

    def puede_editar(self):
        """Verifica si la matrícula puede ser editada"""
        return self.estado in ['BORRADOR', 'PENDIENTE']

    def tiene_todos_documentos(self):
        """Verifica si tiene todos los documentos obligatorios"""
        # CC con 18+ años = mayor de edad (no necesita documentos de acudiente)
        # TI, CE, PPT, PEP = menor de edad (necesita documentos de acudiente)
        usuario = self.aprendiz.usuario
        es_mayor = usuario.tipo_documento == 'CC' and usuario.es_mayor_de_edad

        if es_mayor:
            # Mayores de edad (CC con 18+): 5 documentos (sin acudiente, registro civil, ni tratamiento datos)
            tipos_requeridos = [
                'DOCUMENTO_IDENTIDAD',
                'CERTIFICADO_SALUD',
                'CERTIFICADO_SOFIA',
                'CERTIFICADO_APE',
                'ACUERDO_APRENDIZ'
            ]
        else:
            # Menores de edad (TI, CE, PPT, PEP o CC menor de 18): todos los 8 documentos
            tipos_requeridos = [
                'DOCUMENTO_IDENTIDAD',
                'REGISTRO_CIVIL',
                'CERTIFICADO_SALUD',
                'CERTIFICADO_SOFIA',
                'CERTIFICADO_APE',
                'DOCUMENTO_ACUDIENTE',
                'TRATAMIENTO_DATOS',
                'ACUERDO_APRENDIZ'
            ]

        tipos_cargados = [doc.tipo_documento for doc in self.documentos if not doc.reemplazado_por]
        return all(tipo in tipos_cargados for tipo in tipos_requeridos)

    def __repr__(self):
        return f'<Matricula {self.id} - {self.estado}>'
