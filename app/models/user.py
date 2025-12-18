from . import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    documento = db.Column(db.String(20), unique=True, nullable=False, index=True)
    tipo_documento = db.Column(db.Enum('CC', 'TI', 'CE', 'PEP', 'PPT'), nullable=False, default='CC')
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=True)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    telefono = db.Column(db.String(20))
    password_hash = db.Column(db.String(255), nullable=False)
    password_cipher = db.Column(db.Text)
    rol = db.Column(db.Enum('APRENDIZ', 'DOCENTE', 'ADMINISTRADOR', 'RECTOR'), nullable=False, default='APRENDIZ', index=True)
    activo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    aprendiz = db.relationship('Aprendiz', back_populates='usuario', uselist=False, cascade='all, delete-orphan')
    colegios_rector = db.relationship('Colegio', foreign_keys='Colegio.rector_id', back_populates='rector')
    colegios_docente = db.relationship('Colegio', foreign_keys='Colegio.docente_enlace_id', back_populates='docente_enlace')

    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"

    @property
    def edad(self):
        """Calcula la edad del usuario basado en su fecha de nacimiento"""
        if not self.fecha_nacimiento:
            return None
        from datetime import date
        hoy = date.today()
        edad = hoy.year - self.fecha_nacimiento.year
        # Ajustar si aún no ha cumplido años este año
        if (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day):
            edad -= 1
        return edad

    @property
    def es_mayor_de_edad(self):
        """Retorna True si el usuario tiene 18 años o más"""
        edad = self.edad
        return edad >= 18 if edad is not None else False

    @property
    def tiene_documento_desactualizado(self):
        """Retorna True si tiene TI pero ya es mayor de edad"""
        return self.tipo_documento == 'TI' and self.es_mayor_de_edad

    @property
    def requiere_acudiente(self):
        """Retorna True si requiere acudiente (menor de 18 años)"""
        return not self.es_mayor_de_edad

    def set_password(self, password):
        """Genera el hash de la contraseña"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica la contraseña"""
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.rol == 'ADMINISTRADOR'

    def is_docente(self):
        return self.rol == 'DOCENTE'

    def is_aprendiz(self):
        return self.rol == 'APRENDIZ'

    def is_rector(self):
        return self.rol == 'RECTOR'

    def __repr__(self):
        return f'<Usuario {self.documento} - {self.nombre_completo}>'
