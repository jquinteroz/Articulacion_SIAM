from . import db
from datetime import datetime

class Grupo(db.Model):
    __tablename__ = 'grupos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    colegio_id = db.Column(db.Integer, db.ForeignKey('colegios.id', ondelete='CASCADE'), nullable=False, index=True)
    programa_id = db.Column(db.Integer, db.ForeignKey('programas.id', ondelete='CASCADE'), nullable=False, index=True)
    jornada = db.Column(db.Enum('MAÑANA', 'TARDE', 'NOCHE', 'UNICA'), default='UNICA')
    año_lectivo = db.Column(db.Integer, nullable=False)
    activo = db.Column(db.Boolean, default=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    colegio = db.relationship('Colegio', back_populates='grupos')
    programa = db.relationship('Programa', back_populates='grupos')
    aprendices = db.relationship('Aprendiz', back_populates='grupo')

    __table_args__ = (
        db.UniqueConstraint('nombre', 'colegio_id', 'año_lectivo', name='unique_grupo'),
    )

    @property
    def nombre_completo(self):
        return f"{self.nombre} - {self.colegio.nombre} ({self.año_lectivo})"

    def __repr__(self):
        return f'<Grupo {self.nombre} - {self.programa.nombre if self.programa else "Sin programa"}>'
