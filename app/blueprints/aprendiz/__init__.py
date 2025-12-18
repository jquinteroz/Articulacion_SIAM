from flask import Blueprint

aprendiz_bp = Blueprint('aprendiz', __name__, url_prefix='/aprendiz')

from . import routes
