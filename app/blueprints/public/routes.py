from flask import render_template, redirect, url_for, flash, request, make_response
from flask_login import login_user, logout_user, current_user
from app.models import db, Usuario, Novedad, Programa, MensajeContacto
from app.services.auth_service import AuthService
from . import public_bp

@public_bp.route('/')
def index():
    """Landing page"""
    from app.models import Aprendiz, Colegio

    novedades = Novedad.query.filter_by(activo=True).order_by(Novedad.fecha_publicacion.desc()).limit(6).all()
    programas = Programa.query.filter_by(activo=True).limit(6).all()
    destacadas = Novedad.query.filter_by(activo=True, destacado=True).order_by(Novedad.fecha_publicacion.desc()).limit(3).all()

    # Calcular estadísticas desde la base de datos
    total_programas = Programa.query.filter_by(activo=True).count()
    total_estudiantes = Aprendiz.query.count()
    total_colegios = Colegio.query.filter_by(activo=True).count()

    estadisticas = {
        'programas': total_programas,
        'estudiantes': total_estudiantes,
        'colegios': total_colegios
    }

    return render_template('public/index.html',
                         novedades=novedades,
                         programas=programas,
                         destacadas=destacadas,
                         estadisticas=estadisticas)

@public_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de inicio de sesión"""
    if current_user.is_authenticated:
        return redirect(url_for('public.dashboard_redirect'))

    if request.method == 'POST':
        documento = request.form.get('documento')
        password = request.form.get('password')
        remember = request.form.get('remember', False)

        if not documento or not password:
            flash('Debe ingresar documento y contraseña', 'danger')
            return render_template('public/login.html')

        usuario = Usuario.query.filter_by(documento=documento).first()

        if not usuario or not usuario.check_password(password):
            flash('Documento o contraseña incorrectos', 'danger')
            return render_template('public/login.html')

        if not usuario.activo:
            flash('Su cuenta está inactiva. Contacte al administrador', 'warning')
            return render_template('public/login.html')

        login_user(usuario, remember=remember)
        flash(f'Bienvenido, {usuario.nombre_completo}', 'success')

        return redirect(url_for('public.dashboard_redirect'))

    return render_template('public/login.html')

@public_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    """Página de registro de aprendices"""
    if current_user.is_authenticated:
        return redirect(url_for('public.dashboard_redirect'))

    # Obtener colegios activos
    from app.models import Colegio
    from datetime import date
    colegios = Colegio.query.filter_by(activo=True).all()
    today = date.today().isoformat()

    if request.method == 'POST':
        documento = request.form.get('documento')
        tipo_documento = request.form.get('tipo_documento', 'CC')
        nombres = request.form.get('nombres')
        apellidos = request.form.get('apellidos')
        fecha_nacimiento = request.form.get('fecha_nacimiento')
        email = request.form.get('email')
        telefono = request.form.get('telefono')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        colegio_id = request.form.get('colegio_id')

        # Crear diccionario con datos del formulario
        form_data = {
            'documento': documento,
            'tipo_documento': tipo_documento,
            'nombres': nombres,
            'apellidos': apellidos,
            'fecha_nacimiento': fecha_nacimiento,
            'email': email,
            'telefono': telefono,
            'colegio_id': colegio_id
        }

        # Validaciones
        if not all([documento, nombres, apellidos, fecha_nacimiento, email, password, password_confirm, colegio_id]):
            flash('Todos los campos son obligatorios', 'danger')
            return render_template('public/registro.html', colegios=colegios, form_data=form_data, today=today)

        if password != password_confirm:
            flash('Las contraseñas no coinciden', 'danger')
            return render_template('public/registro.html', colegios=colegios, form_data=form_data, today=today)

        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres', 'danger')
            return render_template('public/registro.html', colegios=colegios, form_data=form_data, today=today)

        # Registrar aprendiz (grupo_id y programa_id se asignan después en el perfil)
        success, message, usuario = AuthService.register_aprendiz(
            documento, tipo_documento, nombres, apellidos, email, telefono, password,
            colegio_id, None, None, fecha_nacimiento
        )

        if success:
            flash('Registro exitoso. Complete su perfil con el grupo y programa asignados', 'success')
            return redirect(url_for('public.login'))
        else:
            # Determinar qué campo tiene el error
            error_field = None
            if 'documento' in message.lower() or 'ya existe' in message.lower():
                error_field = 'documento'
            elif 'email' in message.lower() or 'correo' in message.lower():
                error_field = 'email'

            flash(message, 'danger')
            return render_template('public/registro.html', colegios=colegios, form_data=form_data, error_field=error_field, today=today)

    return render_template('public/registro.html', colegios=colegios, form_data=None, error_field=None, today=today)

@public_bp.route('/logout')
def logout():
    """Cerrar sesión"""
    from flask import session
    logout_user()
    session.clear()  # Limpiar toda la sesión
    flash('Sesión cerrada exitosamente', 'info')

    # Crear respuesta con headers de no-caché
    response = make_response(redirect(url_for('public.index')))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'

    return response

@public_bp.route('/dashboard-redirect')
def dashboard_redirect():
    """Redirige al dashboard según el rol del usuario"""
    if not current_user.is_authenticated:
        return redirect(url_for('public.login'))

    if current_user.is_admin():
        return redirect(url_for('admin.dashboard'))
    elif current_user.is_docente():
        return redirect(url_for('docente.dashboard'))
    elif current_user.is_aprendiz():
        return redirect(url_for('aprendiz.dashboard'))
    else:
        flash('Rol de usuario no reconocido', 'warning')
        logout_user()
        return redirect(url_for('public.login'))

@public_bp.route('/contacto', methods=['GET', 'POST'])
def contacto():
    """Página de contacto"""
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        telefono = request.form.get('telefono')
        asunto = request.form.get('asunto')
        mensaje = request.form.get('mensaje')

        if not all([nombre, email, asunto, mensaje]):
            flash('Todos los campos son obligatorios', 'danger')
            return render_template('public/contacto.html')

        try:
            mensaje_contacto = MensajeContacto(
                nombre=nombre,
                email=email,
                telefono=telefono,
                asunto=asunto,
                mensaje=mensaje
            )
            db.session.add(mensaje_contacto)
            db.session.commit()

            flash('Mensaje enviado exitosamente. Nos contactaremos pronto', 'success')
            return redirect(url_for('public.contacto'))

        except Exception as e:
            db.session.rollback()
            flash('Error al enviar el mensaje. Intente nuevamente', 'danger')

    return render_template('public/contacto.html')

@public_bp.route('/programas')
def programas():
    """Página de programas"""
    programas = Programa.query.filter_by(activo=True).all()
    return render_template('public/programas.html', programas=programas)

@public_bp.route('/programa/<int:programa_id>')
def programa_detalle(programa_id):
    """Detalle de un programa"""
    programa = Programa.query.get_or_404(programa_id)
    return render_template('public/programa_detalle.html', programa=programa)
