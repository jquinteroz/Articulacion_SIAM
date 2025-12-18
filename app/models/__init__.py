from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import Usuario
from .aprendiz import Aprendiz
from .colegio import Colegio
from .programa import Programa
from .grupo import Grupo
from .matricula import Matricula
from .documento import Documento
from .documento_simat import DocumentoSIMAT
from .novedad import Novedad
from .mensaje_contacto import MensajeContacto
from .auditoria import Auditoria
