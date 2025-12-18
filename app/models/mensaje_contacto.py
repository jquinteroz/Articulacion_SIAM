from . import db
from datetime import datetime

class MensajeContacto(db.Model):
    __tablename__ = 'mensajes_contacto'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    telefono = db.Column(db.String(20))
    asunto = db.Column(db.String(200), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    leido = db.Column(db.Boolean, default=False, index=True)
    respondido = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f'<MensajeContacto {self.nombre} - {self.asunto}>'
