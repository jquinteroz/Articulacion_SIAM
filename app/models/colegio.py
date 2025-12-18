from . import db
from datetime import datetime

class Colegio(db.Model):
    __tablename__ = 'colegios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False, index=True)
    tipo_colegio = db.Column(db.Enum('PUBLICO', 'PRIVADO', 'MIXTO'), nullable=False, default='PUBLICO')
    direccion = db.Column(db.String(255))
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(150))
    rector_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='SET NULL'))
    docente_enlace_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='SET NULL'))
    activo = db.Column(db.Boolean, default=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    rector = db.relationship('Usuario', foreign_keys=[rector_id], back_populates='colegios_rector')
    docente_enlace = db.relationship('Usuario', foreign_keys=[docente_enlace_id], back_populates='colegios_docente')
    grupos = db.relationship('Grupo', back_populates='colegio', cascade='all, delete-orphan')
    aprendices = db.relationship('Aprendiz', back_populates='colegio')

    def __repr__(self):
        return f'<Colegio {self.nombre}>'
