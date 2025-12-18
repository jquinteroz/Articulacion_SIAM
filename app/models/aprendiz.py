from . import db
from datetime import datetime

class Aprendiz(db.Model):
    __tablename__ = 'aprendices'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='CASCADE'), unique=True, nullable=False, index=True)
    ciudad = db.Column(db.String(100))
    departamento = db.Column(db.String(100))

    # Datos del acudiente
    acudiente_tipo_doc = db.Column(db.Enum('CC', 'TI', 'CE', 'PEP', 'PPT'), default='CC')
    acudiente_documento = db.Column(db.String(20))
    acudiente_lugar_expedicion = db.Column(db.String(100))
    acudiente_nombres = db.Column(db.String(100))
    acudiente_apellidos = db.Column(db.String(100))
    acudiente_direccion = db.Column(db.String(255))
    acudiente_telefono = db.Column(db.String(20))
    acudiente_email = db.Column(db.String(150))

    # Datos académicos
    colegio_id = db.Column(db.Integer, db.ForeignKey('colegios.id', ondelete='SET NULL'), index=True)
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupos.id', ondelete='SET NULL'), index=True)
    programa_id = db.Column(db.Integer, db.ForeignKey('programas.id', ondelete='SET NULL'))

    perfil_completo = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    usuario = db.relationship('Usuario', back_populates='aprendiz')
    colegio = db.relationship('Colegio', back_populates='aprendices')
    grupo = db.relationship('Grupo', back_populates='aprendices')
    programa = db.relationship('Programa', back_populates='aprendices')
    matriculas = db.relationship('Matricula', back_populates='aprendiz', cascade='all, delete-orphan')

    @property
    def acudiente_nombre_completo(self):
        if self.acudiente_nombres and self.acudiente_apellidos:
            return f"{self.acudiente_nombres} {self.acudiente_apellidos}"
        return None

    def __repr__(self):
        return f'<Aprendiz {self.usuario.nombre_completo if self.usuario else "Sin usuario"}>'
