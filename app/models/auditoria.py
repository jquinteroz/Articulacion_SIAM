from . import db
from datetime import datetime

class Auditoria(db.Model):
    __tablename__ = 'auditoria'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='SET NULL'), index=True)
    accion = db.Column(db.String(100), nullable=False)
    tabla = db.Column(db.String(50), index=True)
    registro_id = db.Column(db.Integer)
    datos_antes = db.Column(db.JSON)
    datos_despues = db.Column(db.JSON)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    # Relaciones
    usuario = db.relationship('Usuario')

    def __repr__(self):
        return f'<Auditoria {self.accion} - {self.tabla}>'
