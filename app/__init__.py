"""
Sistema de Articulación SENA
Versión: 1.0.0
Fecha: 2025-12-18

Desarrollado por: Johann Quintero (jsquinteroz)
GitHub: @jsquinteroz

Copyright (c) 2025 - Todos los derechos reservados
"""

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from config import config
import os

# Inicializar extensiones
from app.models import db

login_manager = LoginManager()
migrate = Migrate()

def create_app(config_name='default'):
    """Factory para crear la aplicación Flask"""

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Asegurar que existan las carpetas necesarias
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['REPORTS_FOLDER'], exist_ok=True)

    # Inicializar extensiones con la app
    db.init_app(app)
    migrate.init_app(app, db)

    # Configurar Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'public.login'
    login_manager.login_message = 'Por favor, inicie sesión para acceder a esta página.'
    login_manager.login_message_category = 'warning'

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import Usuario
        return Usuario.query.get(int(user_id))

    # Registrar blueprints
    from app.blueprints.public import public_bp
    from app.blueprints.aprendiz import aprendiz_bp
    from app.blueprints.docente import docente_bp
    from app.blueprints.admin import admin_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(aprendiz_bp)
    app.register_blueprint(docente_bp)
    app.register_blueprint(admin_bp)

    # Context processors para templates
    @app.context_processor
    def inject_helpers():
        from app.utils.helpers import format_datetime, format_file_size, get_estado_badge_class
        from datetime import datetime
        return dict(
            format_datetime=format_datetime,
            format_file_size=format_file_size,
            get_estado_badge_class=get_estado_badge_class,
            current_year=lambda: datetime.now().year
        )

    # Manejadores de errores
    @app.errorhandler(404)
    def not_found(error):
        from flask import render_template
        return render_template('errors/404.html'), 404

    @app.errorhandler(403)
    def forbidden(error):
        from flask import render_template
        return render_template('errors/403.html'), 403

    @app.errorhandler(500)
    def internal_error(error):
        from flask import render_template
        db.session.rollback()
        return render_template('errors/500.html'), 500

    # Manejador específico para errores de base de datos
    from sqlalchemy.exc import OperationalError, DatabaseError

    @app.errorhandler(OperationalError)
    def handle_db_connection_error(error):
        from flask import render_template, request
        db.session.rollback()

        # Si es una petición AJAX, devolver JSON
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return {
                'error': 'Error de conexión a la base de datos',
                'message': '¿Olvidaste encender el servidor MySQL/XAMPP?'
            }, 503

        # Para peticiones normales, mostrar página de error
        return render_template('errors/database_error.html',
                             error_type='conexión',
                             suggestion='Verifica que MySQL/XAMPP esté ejecutándose'), 503

    @app.errorhandler(DatabaseError)
    def handle_db_error(error):
        from flask import render_template, request
        db.session.rollback()

        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return {
                'error': 'Error de base de datos',
                'message': str(error)
            }, 500

        return render_template('errors/database_error.html',
                             error_type='base de datos',
                             suggestion='Verifica la integridad de la base de datos'), 500

    return app
