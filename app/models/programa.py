from . import db
from datetime import datetime

class Programa(db.Model):
    __tablename__ = 'programas'

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    duracion_horas = db.Column(db.Integer)
    activo = db.Column(db.Boolean, default=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    grupos = db.relationship('Grupo', back_populates='programa', cascade='all, delete-orphan')
    aprendices = db.relationship('Aprendiz', back_populates='programa')

    def __repr__(self):
        return f'<Programa {self.codigo} - {self.nombre}>'
