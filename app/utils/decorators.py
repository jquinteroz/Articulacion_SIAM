from functools import wraps
from flask import redirect, url_for, flash, abort
from flask_login import current_user

def role_required(*roles):
    """
    Decorador para requerir roles específicos
    Usage: @role_required('ADMINISTRADOR', 'DOCENTE')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Debe iniciar sesión para acceder a esta página.', 'warning')
                return redirect(url_for('public.login'))

            if current_user.rol not in roles:
                flash('No tiene permisos para acceder a esta página.', 'danger')
                abort(403)

            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    """Decorador para requerir rol de administrador"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Debe iniciar sesión para acceder a esta página.', 'warning')
            return redirect(url_for('public.login'))

        if not current_user.is_admin():
            flash('Solo los administradores pueden acceder a esta página.', 'danger')
            abort(403)

        return f(*args, **kwargs)
    return decorated_function

def docente_required(f):
    """Decorador para requerir rol de docente o administrador"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Debe iniciar sesión para acceder a esta página.', 'warning')
            return redirect(url_for('public.login'))

        if not (current_user.is_docente() or current_user.is_admin()):
            flash('Solo docentes y administradores pueden acceder a esta página.', 'danger')
            abort(403)

        return f(*args, **kwargs)
    return decorated_function

def aprendiz_required(f):
    """Decorador para requerir rol de aprendiz"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Debe iniciar sesión para acceder a esta página.', 'warning')
            return redirect(url_for('public.login'))

        if not current_user.is_aprendiz():
            flash('Solo los aprendices pueden acceder a esta página.', 'danger')
            abort(403)

        return f(*args, **kwargs)
    return decorated_function
