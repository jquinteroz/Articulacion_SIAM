from . import db
from datetime import datetime

class Novedad(db.Model):
    __tablename__ = 'novedades'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    imagen = db.Column(db.String(500))
    autor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='SET NULL'))
    fecha_publicacion = db.Column(db.Date, nullable=False, index=True)
    destacado = db.Column(db.Boolean, default=False, index=True)
    activo = db.Column(db.Boolean, default=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    autor = db.relationship('Usuario')

    def __repr__(self):
        return f'<Novedad {self.titulo}>'
