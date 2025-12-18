from flask import render_template, redirect, url_for, flash, request, send_file, jsonify
from flask_login import login_required, current_user
from app.models import db, Usuario, Aprendiz, Colegio, Grupo, Programa, Matricula, Documento, Novedad, MensajeContacto, DocumentoSIMAT
from app.services.auth_service import AuthService
from app.services.documento_service import DocumentoService
from app.services.matricula_service import MatriculaService
from app.services.reporte_service import ReporteService
from app.services.sofia_service import SofiaService
from app.utils.decorators import admin_required
from app.utils.crypto import CryptoService
from . import admin_bp
import os
import shutil
from datetime import datetime

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Dashboard del administrador"""
    # Estadísticas generales
    stats = {
        'total_usuarios': Usuario.query.count(),
        'total_aprendices': Aprendiz.query.count(),
        'total_colegios': Colegio.query.filter_by(activo=True).count(),
        'total_programas': Programa.query.filter_by(activo=True).count(),
        'matriculas_pendientes': Matricula.query.filter(
            Matricula.estado.in_(['ENVIADO', 'PENDIENTE'])
        ).count(),
        'simat_pendientes': DocumentoSIMAT.query.filter_by(estado='PENDIENTE').count(),
        'programas': []
    }

    # Distribución por programas
    programas = Programa.query.filter_by(activo=True).all()
    for programa in programas:
        aprendices_count = Aprendiz.query.filter_by(programa_id=programa.id).count()
        stats['programas'].append({
            'nombre': programa.nombre,
            'aprendices_count': aprendices_count
        })

    # Matrículas recientes (últimas 10)
    matriculas_recientes = Matricula.query.order_by(
        Matricula.created_at.desc()
    ).limit(10).all()

    # Mensajes de contacto pendientes (últimos 5)
    mensajes_pendientes = MensajeContacto.query.filter_by(
        leido=False
    ).order_by(MensajeContacto.created_at.desc()).limit(5).all()

    return render_template('admin/dashboard.html',
                         stats=stats,
                         matriculas_recientes=matriculas_recientes,
                         mensajes_pendientes=mensajes_pendientes)

# ============================================
# CRUD USUARIOS
# ============================================
@admin_bp.route('/usuarios')
@login_required
@admin_required
def usuarios():
    """Listado de usuarios"""
    rol_filtro = request.args.get('rol', 'todos')

    query = Usuario.query

    if rol_filtro != 'todos':
        query = query.filter_by(rol=rol_filtro)

    usuarios = query.order_by(Usuario.created_at.desc()).all()

    return render_template('admin/usuarios/list.html',
                         usuarios=usuarios,
                         rol_filtro=rol_filtro)

@admin_bp.route('/usuarios/crear', methods=['GET', 'POST'])
@login_required
@admin_required
def crear_usuario():
    """Crear nuevo usuario"""
    from datetime import date

    if request.method == 'POST':
        data = {
            'documento': request.form.get('documento'),
            'tipo_documento': request.form.get('tipo_documento'),
            'nombres': request.form.get('nombres'),
            'apellidos': request.form.get('apellidos'),
            'fecha_nacimiento': request.form.get('fecha_nacimiento'),
            'email': request.form.get('email'),
            'telefono': request.form.get('telefono'),
            'password': request.form.get('password'),
            'rol': request.form.get('rol')
        }

        success, message, usuario = AuthService.create_user(**data)

        if success:
            flash('Usuario creado exitosamente', 'success')
            return redirect(url_for('admin.usuarios'))
        else:
            flash(message, 'danger')

    # Obtener lista de colegios para el formulario
    colegios = Colegio.query.filter_by(activo=True).order_by(Colegio.nombre).all()
    today = date.today().isoformat()

    return render_template('admin/usuarios/form.html', usuario=None, colegios=colegios, action='crear', today=today)

@admin_bp.route('/usuarios/editar/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_usuario(user_id):
    """Editar usuario"""
    from datetime import date
    usuario = Usuario.query.get_or_404(user_id)

    if request.method == 'POST':
        data = {
            'nombres': request.form.get('nombres'),
            'apellidos': request.form.get('apellidos'),
            'email': request.form.get('email'),
            'telefono': request.form.get('telefono'),
            'tipo_documento': request.form.get('tipo_documento'),
            'fecha_nacimiento': request.form.get('fecha_nacimiento'),
            'rol': request.form.get('rol'),
            'activo': request.form.get('activo') == 'on'
        }

        # Si es aprendiz, incluir colegio_id, grupo_id y programa_id
        if usuario.rol == 'APRENDIZ':
            colegio_id = request.form.get('colegio_id')
            data['colegio_id'] = int(colegio_id) if colegio_id else None

            grupo_id = request.form.get('grupo_id')
            data['grupo_id'] = int(grupo_id) if grupo_id else None

            programa_id = request.form.get('programa_id')
            data['programa_id'] = int(programa_id) if programa_id else None

        # Si es docente, actualizar el colegio donde es docente_enlace
        if usuario.rol == 'DOCENTE':
            colegio_id = request.form.get('colegio_docente_id')
            # Primero, quitar al docente de cualquier colegio anterior
            Colegio.query.filter_by(docente_enlace_id=usuario.id).update({'docente_enlace_id': None})
            # Luego, asignarlo al nuevo colegio si se seleccionó uno
            if colegio_id:
                colegio = Colegio.query.get(int(colegio_id))
                if colegio:
                    colegio.docente_enlace_id = usuario.id

        # Si es rector, actualizar el colegio donde es rector
        if usuario.rol == 'RECTOR':
            colegio_id = request.form.get('colegio_rector_id')
            # Primero, quitar al rector de cualquier colegio anterior
            Colegio.query.filter_by(rector_id=usuario.id).update({'rector_id': None})
            # Luego, asignarlo al nuevo colegio si se seleccionó uno
            if colegio_id:
                colegio = Colegio.query.get(int(colegio_id))
                if colegio:
                    colegio.rector_id = usuario.id

        # Solo actualizar contraseña si se proporciona
        password = request.form.get('password')
        if password:
            data['password'] = password

        success, message = AuthService.update_user(user_id, **data)

        if success:
            flash('Usuario actualizado exitosamente', 'success')
            return redirect(url_for('admin.usuarios'))
        else:
            flash(message, 'danger')

    # Obtener listas para el formulario
    colegios = Colegio.query.filter_by(activo=True).order_by(Colegio.nombre).all()
    grupos = Grupo.query.order_by(Grupo.nombre).all()
    programas = Programa.query.filter_by(activo=True).order_by(Programa.nombre).all()
    today = date.today().isoformat()

    return render_template('admin/usuarios/form.html',
                         usuario=usuario,
                         colegios=colegios,
                         grupos=grupos,
                         programas=programas,
                         action='editar',
                         today=today)

@admin_bp.route('/usuarios/eliminar/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def eliminar_usuario(user_id):
    """Eliminar usuario"""
    if user_id == current_user.id:
        return jsonify({'success': False, 'message': 'No puede eliminarse a sí mismo'}), 400

    success, message = AuthService.delete_user(user_id)

    if success:
        flash('Usuario eliminado exitosamente', 'success')
    else:
        flash(message, 'danger')

    return redirect(url_for('admin.usuarios'))

@admin_bp.route('/usuarios/get-password/<int:user_id>')
@login_required
@admin_required
def get_password(user_id):
    """Obtener contraseña desencriptada (AJAX)"""
    password = AuthService.get_decrypted_password(user_id)

    if password:
        return jsonify({'success': True, 'password': password})
    else:
        return jsonify({'success': False, 'message': 'No se pudo obtener la contraseña'}), 400

# ============================================
# CRUD COLEGIOS
# ============================================
@admin_bp.route('/colegios')
@login_required
@admin_required
def colegios():
    """Listado de colegios"""
    colegios = Colegio.query.order_by(Colegio.nombre).all()
    return render_template('admin/colegios/list.html', colegios=colegios)

@admin_bp.route('/colegios/crear', methods=['GET', 'POST'])
@login_required
@admin_required
def crear_colegio():
    """Crear nuevo colegio"""
    if request.method == 'POST':
        try:
            colegio = Colegio(
                nombre=request.form.get('nombre'),
                tipo_colegio=request.form.get('tipo_colegio'),
                direccion=request.form.get('direccion'),
                telefono=request.form.get('telefono'),
                email=request.form.get('email'),
                rector_id=request.form.get('rector_id') or None,
                docente_enlace_id=request.form.get('docente_enlace_id') or None
            )

            db.session.add(colegio)
            db.session.commit()

            flash('Colegio creado exitosamente', 'success')
            return redirect(url_for('admin.colegios'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear colegio: {str(e)}', 'danger')

    # Obtener rectores y docentes disponibles
    rectores = Usuario.query.filter_by(rol='RECTOR', activo=True).all()
    docentes = Usuario.query.filter_by(rol='DOCENTE', activo=True).all()

    return render_template('admin/colegios/form.html',
                         colegio=None,
                         rectores=rectores,
                         docentes=docentes,
                         action='crear')

@admin_bp.route('/colegios/editar/<int:colegio_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_colegio(colegio_id):
    """Editar colegio"""
    colegio = Colegio.query.get_or_404(colegio_id)

    if request.method == 'POST':
        try:
            colegio.nombre = request.form.get('nombre')
            colegio.tipo_colegio = request.form.get('tipo_colegio')
            colegio.direccion = request.form.get('direccion')
            colegio.telefono = request.form.get('telefono')
            colegio.email = request.form.get('email')
            colegio.rector_id = request.form.get('rector_id') or None
            colegio.docente_enlace_id = request.form.get('docente_enlace_id') or None
            colegio.activo = request.form.get('activo') == 'on'

            db.session.commit()

            flash('Colegio actualizado exitosamente', 'success')
            return redirect(url_for('admin.colegios'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar colegio: {str(e)}', 'danger')

    rectores = Usuario.query.filter_by(rol='RECTOR', activo=True).all()
    docentes = Usuario.query.filter_by(rol='DOCENTE', activo=True).all()

    return render_template('admin/colegios/form.html',
                         colegio=colegio,
                         rectores=rectores,
                         docentes=docentes,
                         action='editar')

@admin_bp.route('/colegios/eliminar/<int:colegio_id>', methods=['POST'])
@login_required
@admin_required
def eliminar_colegio(colegio_id):
    """Eliminar colegio"""
    try:
        colegio = Colegio.query.get_or_404(colegio_id)
        db.session.delete(colegio)
        db.session.commit()

        flash('Colegio eliminado exitosamente', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar colegio: {str(e)}', 'danger')

    return redirect(url_for('admin.colegios'))

# ============================================
# CRUD PROGRAMAS
# ============================================
@admin_bp.route('/programas')
@login_required
@admin_required
def programas():
    """Listado de programas"""
    programas = Programa.query.order_by(Programa.nombre).all()
    return render_template('admin/programas/list.html', programas=programas)

@admin_bp.route('/programas/crear', methods=['GET', 'POST'])
@login_required
@admin_required
def crear_programa():
    """Crear nuevo programa"""
    if request.method == 'POST':
        try:
            programa = Programa(
                codigo=request.form.get('codigo'),
                nombre=request.form.get('nombre'),
                descripcion=request.form.get('descripcion'),
                duracion_horas=request.form.get('duracion_horas')
            )

            db.session.add(programa)
            db.session.commit()

            flash('Programa creado exitosamente', 'success')
            return redirect(url_for('admin.programas'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear programa: {str(e)}', 'danger')

    return render_template('admin/programas/form.html', programa=None, action='crear')

@admin_bp.route('/programas/editar/<int:programa_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_programa(programa_id):
    """Editar programa"""
    programa = Programa.query.get_or_404(programa_id)

    if request.method == 'POST':
        try:
            programa.codigo = request.form.get('codigo')
            programa.nombre = request.form.get('nombre')
            programa.descripcion = request.form.get('descripcion')
            programa.duracion_horas = request.form.get('duracion_horas')
            programa.activo = request.form.get('activo') == 'on'

            db.session.commit()

            flash('Programa actualizado exitosamente', 'success')
            return redirect(url_for('admin.programas'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar programa: {str(e)}', 'danger')

    return render_template('admin/programas/form.html', programa=programa, action='editar')

@admin_bp.route('/programas/eliminar/<int:programa_id>', methods=['POST'])
@login_required
@admin_required
def eliminar_programa(programa_id):
    """Eliminar programa"""
    try:
        programa = Programa.query.get_or_404(programa_id)
        db.session.delete(programa)
        db.session.commit()

        flash('Programa eliminado exitosamente', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar programa: {str(e)}', 'danger')

    return redirect(url_for('admin.programas'))

# ============================================
# CRUD GRUPOS
# ============================================
@admin_bp.route('/grupos')
@login_required
@admin_required
def grupos():
    """Listado de grupos"""
    grupos = Grupo.query.order_by(Grupo.colegio_id, Grupo.nombre).all()
    colegios = Colegio.query.filter_by(activo=True).all()
    return render_template('admin/grupos/list.html', grupos=grupos, colegios=colegios)

@admin_bp.route('/grupos/crear', methods=['GET', 'POST'])
@login_required
@admin_required
def crear_grupo():
    """Crear nuevo grupo"""
    if request.method == 'POST':
        try:
            grupo = Grupo(
                nombre=request.form.get('nombre'),
                colegio_id=request.form.get('colegio_id'),
                programa_id=request.form.get('programa_id'),
                jornada=request.form.get('jornada'),
                año_lectivo=request.form.get('año_lectivo')
            )

            db.session.add(grupo)
            db.session.commit()

            flash('Grupo creado exitosamente', 'success')
            return redirect(url_for('admin.grupos'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear grupo: {str(e)}', 'danger')

    colegios = Colegio.query.filter_by(activo=True).all()
    programas = Programa.query.filter_by(activo=True).all()

    return render_template('admin/grupos/form.html',
                         grupo=None,
                         colegios=colegios,
                         programas=programas,
                         action='crear')

@admin_bp.route('/grupos/editar/<int:grupo_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_grupo(grupo_id):
    """Editar grupo"""
    grupo = Grupo.query.get_or_404(grupo_id)

    if request.method == 'POST':
        try:
            grupo.nombre = request.form.get('nombre')
            grupo.colegio_id = request.form.get('colegio_id')
            grupo.programa_id = request.form.get('programa_id')
            grupo.jornada = request.form.get('jornada')
            grupo.año_lectivo = request.form.get('año_lectivo')
            grupo.activo = request.form.get('activo') == 'on'

            db.session.commit()

            flash('Grupo actualizado exitosamente', 'success')
            return redirect(url_for('admin.grupos'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar grupo: {str(e)}', 'danger')

    colegios = Colegio.query.filter_by(activo=True).all()
    programas = Programa.query.filter_by(activo=True).all()

    return render_template('admin/grupos/form.html',
                         grupo=grupo,
                         colegios=colegios,
                         programas=programas,
                         action='editar')

@admin_bp.route('/grupos/eliminar/<int:grupo_id>', methods=['POST'])
@login_required
@admin_required
def eliminar_grupo(grupo_id):
    """Eliminar grupo"""
    try:
        grupo = Grupo.query.get_or_404(grupo_id)
        db.session.delete(grupo)
        db.session.commit()

        flash('Grupo eliminado exitosamente', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar grupo: {str(e)}', 'danger')

    return redirect(url_for('admin.grupos'))

# ============================================
# GESTIÓN DE MATRÍCULAS
# ============================================
@admin_bp.route('/matriculas')
@login_required
@admin_required
def matriculas():
    """Listado de matrículas"""
    estado_filtro = request.args.get('estado', 'todos')
    colegio_filtro = request.args.get('colegio', 'todos')

    query = Matricula.query.join(Aprendiz)

    if estado_filtro != 'todos':
        query = query.filter(Matricula.estado == estado_filtro)

    if colegio_filtro != 'todos':
        query = query.filter(Aprendiz.colegio_id == int(colegio_filtro))

    matriculas = query.order_by(Matricula.created_at.desc()).all()
    colegios = Colegio.query.filter_by(activo=True).all()
    programas = Programa.query.filter_by(activo=True).all()
    grupos = Grupo.query.filter_by(activo=True).order_by(Grupo.nombre).all()

    # Calcular estadísticas
    stats = {
        'total': Matricula.query.count(),
        'borradores': Matricula.query.filter_by(estado='BORRADOR').count(),
        'enviadas': Matricula.query.filter_by(estado='ENVIADO').count(),
        'pendientes': Matricula.query.filter_by(estado='PENDIENTE').count(),
        'completas': Matricula.query.filter_by(estado='COMPLETO').count(),
        'prematriculas': Matricula.query.filter_by(estado='PREMATRICULA').count()
    }

    return render_template('admin/matriculas/list.html',
                         matriculas=matriculas,
                         colegios=colegios,
                         programas=programas,
                         grupos=grupos,
                         stats=stats,
                         estado_filtro=estado_filtro,
                         colegio_filtro=colegio_filtro)

@admin_bp.route('/matriculas/<int:matricula_id>')
@login_required
@admin_required
def ver_matricula(matricula_id):
    """Ver detalle de una matrícula"""
    matricula = Matricula.query.get_or_404(matricula_id)
    documentos = DocumentoService.get_documentos_activos(matricula.id)

    return render_template('admin/matriculas/detalle.html',
                         matricula=matricula,
                         documentos=documentos)

@admin_bp.route('/matriculas/validar/<int:matricula_id>', methods=['POST'])
@login_required
@admin_required
def validar_matricula(matricula_id):
    """Validar matrícula"""
    estado = request.form.get('estado')
    observaciones = request.form.get('observaciones')

    success, message = MatriculaService.validar_matricula_admin(
        matricula_id,
        current_user.id,
        estado,
        observaciones
    )

    if success:
        flash('Matrícula validada exitosamente', 'success')
    else:
        flash(message, 'danger')

    return redirect(url_for('admin.ver_matricula', matricula_id=matricula_id))

# ============================================
# REPORTES AVANZADOS
# ============================================
@admin_bp.route('/reportes')
@login_required
@admin_required
def reportes():
    """Página de reportes avanzados"""
    colegios = Colegio.query.filter_by(activo=True).all()
    programas = Programa.query.filter_by(activo=True).all()
    grupos = Grupo.query.filter_by(activo=True).all()

    return render_template('admin/reportes.html',
                         colegios=colegios,
                         programas=programas,
                         grupos=grupos)

@admin_bp.route('/reportes/generar-excel', methods=['POST'])
@login_required
@admin_required
def generar_reporte_excel():
    """Generar reporte Excel personalizado"""
    tipo_reporte = request.form.get('tipo_reporte', 'matriculas')

    # Si es formato SOFIA, usar el servicio SOFIA
    if tipo_reporte == 'sofia':
        try:
            # Determinar filtros
            filtro_tipo = 'todos'
            filtro_id = None

            if request.form.get('grupo_id'):
                filtro_tipo = 'ficha'
                filtro_id = int(request.form.get('grupo_id'))
            elif request.form.get('colegio_id'):
                filtro_tipo = 'colegio'
                filtro_id = int(request.form.get('colegio_id'))
            elif request.form.get('programa_id'):
                filtro_tipo = 'programa'
                filtro_id = int(request.form.get('programa_id'))

            # Generar formato SOFIA
            success, message, file_path = SofiaService.generar_formato_sofia(
                filtro_tipo=filtro_tipo,
                filtro_id=filtro_id,
                docente_colegio_id=None  # Admin no tiene restricciones
            )

            if success:
                return send_file(
                    file_path,
                    mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    as_attachment=True,
                    download_name=os.path.basename(file_path)
                )
            else:
                flash(message, 'danger')
                return redirect(url_for('admin.reportes'))

        except Exception as e:
            flash(f'Error al generar formato SOFIA: {str(e)}', 'danger')
            return redirect(url_for('admin.reportes'))

    # Para otros tipos de reportes, usar el servicio de reportes normal
    filtros = {}

    if request.form.get('colegio_id'):
        filtros['colegio_id'] = int(request.form.get('colegio_id'))

    if request.form.get('programa_id'):
        filtros['programa_id'] = int(request.form.get('programa_id'))

    if request.form.get('grupo_id'):
        filtros['grupo_id'] = int(request.form.get('grupo_id'))

    query = Matricula.query.join(Aprendiz)

    if 'colegio_id' in filtros:
        query = query.filter(Aprendiz.colegio_id == filtros['colegio_id'])

    if 'programa_id' in filtros:
        query = query.filter(Aprendiz.programa_id == filtros['programa_id'])

    if 'grupo_id' in filtros:
        query = query.filter(Aprendiz.grupo_id == filtros['grupo_id'])

    matriculas = query.all()

    try:
        excel_path = ReporteService.generar_excel_matriculas(matriculas)
        return send_file(excel_path, as_attachment=True, download_name='reporte_completo.xlsx')

    except Exception as e:
        flash(f'Error al generar reporte: {str(e)}', 'danger')
        return redirect(url_for('admin.reportes'))

@admin_bp.route('/reportes/descargar-documentos-grupo/<int:grupo_id>')
@login_required
@admin_required
def descargar_documentos_grupo(grupo_id):
    """Descargar todos los documentos de un grupo"""
    grupo = Grupo.query.get_or_404(grupo_id)

    try:
        # Crear carpeta temporal
        temp_folder = f'reports/documentos_{grupo.nombre}_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
        os.makedirs(temp_folder, exist_ok=True)

        # Obtener todas las matrículas del grupo
        matriculas = Matricula.query.join(Aprendiz).filter(Aprendiz.grupo_id == grupo_id).all()

        for matricula in matriculas:
            aprendiz = matricula.aprendiz
            usuario = aprendiz.usuario

            # Crear carpeta por aprendiz
            aprendiz_folder = os.path.join(
                temp_folder,
                f"{usuario.documento}_{usuario.nombres}_{usuario.apellidos}"
            )
            os.makedirs(aprendiz_folder, exist_ok=True)

            # Copiar documentos
            for doc in matricula.documentos:
                if not doc.reemplazado_por and os.path.exists(doc.ruta_archivo):
                    dest_path = os.path.join(aprendiz_folder, doc.nombre_archivo)
                    shutil.copy2(doc.ruta_archivo, dest_path)

        # Crear archivo ZIP
        shutil.make_archive(temp_folder, 'zip', temp_folder)

        # Enviar archivo
        return send_file(
            f'{temp_folder}.zip',
            as_attachment=True,
            download_name=f'documentos_{grupo.nombre}.zip'
        )

    except Exception as e:
        flash(f'Error al descargar documentos: {str(e)}', 'danger')
        return redirect(url_for('admin.grupos'))

# ============================================
# GESTIÓN DE NOVEDADES
# ============================================
@admin_bp.route('/novedades')
@login_required
@admin_required
def novedades():
    """Listado de novedades"""
    novedades = Novedad.query.order_by(Novedad.fecha_publicacion.desc()).all()
    return render_template('admin/novedades/list.html', novedades=novedades)

@admin_bp.route('/novedades/crear', methods=['GET', 'POST'])
@login_required
@admin_required
def crear_novedad():
    """Crear nueva novedad"""
    if request.method == 'POST':
        try:
            novedad = Novedad(
                titulo=request.form.get('titulo'),
                contenido=request.form.get('contenido'),
                fecha_publicacion=request.form.get('fecha_publicacion') or datetime.now().date(),
                destacado=request.form.get('destacado') == 'on',
                autor_id=current_user.id
            )

            # Manejar imagen si se cargó
            if 'imagen' in request.files:
                file = request.files['imagen']
                if file and file.filename:
                    # Guardar imagen (implementar lógica de guardado)
                    pass

            db.session.add(novedad)
            db.session.commit()

            flash('Novedad creada exitosamente', 'success')
            return redirect(url_for('admin.novedades'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear novedad: {str(e)}', 'danger')

    return render_template('admin/novedades/form.html', novedad=None, action='crear')

@admin_bp.route('/novedades/editar/<int:novedad_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_novedad(novedad_id):
    """Editar una novedad existente"""
    novedad = Novedad.query.get_or_404(novedad_id)

    if request.method == 'POST':
        try:
            novedad.titulo = request.form.get('titulo')
            novedad.contenido = request.form.get('contenido')
            novedad.fecha_publicacion = request.form.get('fecha_publicacion') or novedad.fecha_publicacion
            novedad.destacado = request.form.get('destacado') == 'on'

            # Manejar imagen si se cargó
            if 'imagen' in request.files:
                file = request.files['imagen']
                if file and file.filename:
                    # Guardar imagen (implementar lógica de guardado)
                    pass

            db.session.commit()

            flash('Novedad actualizada exitosamente', 'success')
            return redirect(url_for('admin.novedades'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar novedad: {str(e)}', 'danger')

    return render_template('admin/novedades/form.html', novedad=novedad, action='editar')

@admin_bp.route('/novedades/eliminar/<int:novedad_id>', methods=['POST'])
@login_required
@admin_required
def eliminar_novedad(novedad_id):
    """Eliminar una novedad"""
    try:
        novedad = Novedad.query.get_or_404(novedad_id)
        db.session.delete(novedad)
        db.session.commit()

        flash('Novedad eliminada exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar novedad: {str(e)}', 'danger')

    return redirect(url_for('admin.novedades'))

@admin_bp.route('/novedades/toggle-activo/<int:novedad_id>', methods=['POST'])
@login_required
@admin_required
def toggle_novedad_activo(novedad_id):
    """Activar/desactivar una novedad"""
    try:
        novedad = Novedad.query.get_or_404(novedad_id)
        novedad.activo = not novedad.activo
        db.session.commit()

        estado = 'activada' if novedad.activo else 'desactivada'
        flash(f'Novedad {estado} exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al cambiar estado: {str(e)}', 'danger')

    return redirect(url_for('admin.novedades'))

# ============================================
# MENSAJES DE CONTACTO
# ============================================
@admin_bp.route('/mensajes')
@login_required
@admin_required
def mensajes():
    """Ver mensajes de contacto"""
    mensajes = MensajeContacto.query.order_by(MensajeContacto.created_at.desc()).all()
    return render_template('admin/mensajes.html', mensajes=mensajes)

@admin_bp.route('/mensajes/marcar-leido/<int:mensaje_id>', methods=['POST'])
@login_required
@admin_required
def marcar_leido(mensaje_id):
    """Marcar mensaje como leído"""
    mensaje = MensajeContacto.query.get_or_404(mensaje_id)
    mensaje.leido = True
    db.session.commit()

    return jsonify({'success': True})

@admin_bp.route('/mensajes/marcar-respondido/<int:mensaje_id>', methods=['POST'])
@login_required
@admin_required
def marcar_respondido(mensaje_id):
    """Marcar mensaje como respondido"""
    mensaje = MensajeContacto.query.get_or_404(mensaje_id)
    mensaje.respondido = True
    mensaje.leido = True
    db.session.commit()

    return jsonify({'success': True})

@admin_bp.route('/mensajes/enviar-respuesta', methods=['POST'])
@login_required
@admin_required
def enviar_respuesta():
    """Enviar respuesta a un mensaje de contacto"""
    try:
        data = request.get_json()
        mensaje_id = data.get('mensaje_id')
        destinatario = data.get('destinatario')
        nombre = data.get('nombre')
        asunto = data.get('asunto')
        mensaje_texto = data.get('mensaje')

        # Validar datos
        if not all([mensaje_id, destinatario, asunto, mensaje_texto]):
            return jsonify({'success': False, 'message': 'Faltan datos requeridos'}), 400

        # Importar el servicio de email
        from app.services.email_service import EmailService

        # Enviar el email
        resultado = EmailService.enviar_respuesta_contacto(
            destinatario=destinatario,
            nombre=nombre,
            asunto=asunto,
            mensaje=mensaje_texto,
            remitente_nombre=current_user.nombre_completo,
            remitente_email=current_user.email
        )

        if resultado:
            # Marcar el mensaje como respondido
            mensaje = MensajeContacto.query.get(mensaje_id)
            if mensaje:
                mensaje.respondido = True
                mensaje.leido = True
                db.session.commit()

            return jsonify({'success': True, 'message': 'Respuesta enviada correctamente'})
        else:
            return jsonify({'success': False, 'message': 'Error al enviar el correo'}), 500

    except Exception as e:
        print(f"Error al enviar respuesta: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

# ============================================
# GESTIÓN DE DOCUMENTOS
# ============================================

@admin_bp.route('/ver-documento/<int:documento_id>')
@login_required
@admin_required
def ver_documento(documento_id):
    """Ver un documento específico en el navegador"""
    documento = Documento.query.get_or_404(documento_id)

    # Convertir ruta relativa a absoluta si es necesario
    file_path = documento.ruta_archivo
    if not os.path.isabs(file_path):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        file_path = os.path.join(base_dir, file_path)

    if not os.path.exists(file_path):
        flash(f'Archivo no encontrado: {os.path.basename(file_path)}', 'danger')
        return redirect(url_for('admin.matriculas'))

    # Detectar el tipo de archivo para usar el mimetype correcto
    extension = os.path.splitext(file_path)[1].lower()
    mimetype_map = {
        '.pdf': 'application/pdf',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg'
    }
    mimetype = mimetype_map.get(extension, 'application/pdf')

    return send_file(file_path, mimetype=mimetype)

@admin_bp.route('/descargar-documento/<int:documento_id>')
@login_required
@admin_required
def descargar_documento(documento_id):
    """Descargar un documento específico"""
    documento = Documento.query.get_or_404(documento_id)

    # Convertir ruta relativa a absoluta si es necesario
    file_path = documento.ruta_archivo
    if not os.path.isabs(file_path):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        file_path = os.path.join(base_dir, file_path)

    if not os.path.exists(file_path):
        flash(f'Archivo no encontrado: {os.path.basename(file_path)}', 'danger')
        return redirect(url_for('admin.matriculas'))

    return send_file(file_path, as_attachment=True, download_name=documento.nombre_archivo)

@admin_bp.route('/documentos/<int:documento_id>/aprobar', methods=['POST'])
@login_required
@admin_required
def aprobar_documento(documento_id):
    """Aprobar un documento"""
    documento = Documento.query.get_or_404(documento_id)

    documento.validado = True
    documento.validado_por = current_user.id
    documento.fecha_validacion = datetime.now()
    documento.observaciones = request.form.get('observaciones', '')
    db.session.commit()

    flash(f'Documento {documento.tipo_documento} aprobado exitosamente', 'success')

    # Verificar si todos los documentos están aprobados
    documentos_matricula = Documento.query.filter_by(matricula_id=documento.matricula_id).all()
    documentos_activos = [d for d in documentos_matricula if not d.reemplazado_por]
    todos_aprobados = all(d.validado == True for d in documentos_activos)

    # Obtener el aprendiz para verificar si es mayor de edad
    aprendiz = documento.matricula.aprendiz
    usuario = aprendiz.usuario
    es_mayor_de_edad = usuario.es_mayor_de_edad
    tipo_documento = usuario.tipo_documento

    # Determinar cantidad de documentos requeridos
    # Solo CC con 18+ es mayor de edad (5 docs), resto son menores (8 docs)
    documentos_requeridos = 5 if (tipo_documento == 'CC' and es_mayor_de_edad) else 8

    if todos_aprobados and len(documentos_activos) >= documentos_requeridos:
        matricula = Matricula.query.get(documento.matricula_id)
        matricula.estado = 'PREMATRICULA'
        db.session.commit()
        flash('Todos los documentos aprobados. El aprendiz pasa a estado PRE-MATRÍCULA', 'success')

    return redirect(url_for('admin.ver_matricula', matricula_id=documento.matricula_id))

@admin_bp.route('/documentos/<int:documento_id>/rechazar', methods=['POST'])
@login_required
@admin_required
def rechazar_documento(documento_id):
    """Rechazar un documento"""
    documento = Documento.query.get_or_404(documento_id)

    observaciones = request.form.get('observaciones', '')

    if not observaciones:
        flash('Debe proporcionar observaciones al rechazar un documento', 'warning')
        return redirect(url_for('admin.ver_matricula', matricula_id=documento.matricula_id))

    documento.validado = False
    documento.validado_por = current_user.id
    documento.fecha_validacion = datetime.now()
    documento.observaciones = observaciones
    db.session.commit()

    flash(f'Documento {documento.tipo_documento} rechazado. El aprendiz debe cargarlo nuevamente', 'warning')

    return redirect(url_for('admin.ver_matricula', matricula_id=documento.matricula_id))

@admin_bp.route('/matriculas/cambiar-estado/<int:matricula_id>', methods=['POST'])
@login_required
@admin_required
def cambiar_estado_matricula(matricula_id):
    """Cambiar el estado de una matrícula"""
    matricula = Matricula.query.get_or_404(matricula_id)

    nuevo_estado = request.form.get('nuevo_estado')
    observaciones = request.form.get('observaciones', '')

    if not nuevo_estado:
        flash('Debe seleccionar un estado', 'warning')
        return redirect(url_for('admin.ver_matricula', matricula_id=matricula_id))

    # Validar estados permitidos
    estados_validos = ['BORRADOR', 'ENVIADO', 'PENDIENTE', 'COMPLETO', 'PREMATRICULA', 'MATRICULADO', 'RECHAZADO']
    if nuevo_estado not in estados_validos:
        flash('Estado no válido', 'danger')
        return redirect(url_for('admin.ver_matricula', matricula_id=matricula_id))

    # Actualizar estado
    matricula.estado = nuevo_estado

    if nuevo_estado == 'COMPLETO' and not matricula.fecha_validacion:
        matricula.fecha_validacion = datetime.now()

    db.session.commit()

    flash(f'Estado de matrícula actualizado a {nuevo_estado}', 'success')

    return redirect(url_for('admin.ver_matricula', matricula_id=matricula_id))

@admin_bp.route('/matricular-aprendiz/<int:matricula_id>', methods=['POST'])
@login_required
@admin_required
def matricular_aprendiz(matricula_id):
    """Matricular definitivamente a un aprendiz (cambiar de PREMATRICULA a MATRICULADO)"""
    matricula = Matricula.query.get_or_404(matricula_id)

    # Verificar que está en PREMATRICULA
    if matricula.estado != 'PREMATRICULA':
        flash('Solo se pueden matricular aprendices en estado PRE-MATRÍCULA', 'warning')
        return redirect(url_for('admin.ver_matricula', matricula_id=matricula_id))

    # Verificar que todos los documentos están aprobados
    documentos = Documento.query.filter_by(matricula_id=matricula_id).all()
    documentos_activos = [d for d in documentos if not d.reemplazado_por]

    # Obtener el aprendiz para verificar documentos requeridos
    aprendiz = matricula.aprendiz
    usuario = aprendiz.usuario
    es_mayor_de_edad = usuario.es_mayor_de_edad
    tipo_documento = usuario.tipo_documento

    # Determinar cantidad de documentos requeridos
    documentos_requeridos = 5 if (tipo_documento in ['CC', 'PPT', 'CE', 'PEP'] and es_mayor_de_edad) else 8

    if len(documentos_activos) < documentos_requeridos:
        flash(f'El aprendiz debe tener los {documentos_requeridos} documentos requeridos', 'danger')
        return redirect(url_for('admin.ver_matricula', matricula_id=matricula_id))

    todos_aprobados = all(d.validado == True for d in documentos_activos)
    if not todos_aprobados:
        flash('Todos los documentos deben estar aprobados antes de matricular', 'danger')
        return redirect(url_for('admin.ver_matricula', matricula_id=matricula_id))

    # Cambiar estado a MATRICULADO
    matricula.estado = 'MATRICULADO'
    matricula.fecha_validacion_admin = datetime.now()
    matricula.validado_por_admin = current_user.id
    db.session.commit()

    flash('¡Aprendiz matriculado exitosamente! Se ha notificado al aprendiz y al docente enlace.', 'success')

    # TODO: Aquí se pueden agregar notificaciones por email

    return redirect(url_for('admin.ver_matricula', matricula_id=matricula_id))

# ============================================
# DESCARGAS ZIP
# ============================================

@admin_bp.route('/descargar-documentos-aprendiz/<int:aprendiz_id>')
@login_required
@admin_required
def descargar_documentos_aprendiz(aprendiz_id):
    """Descargar todos los formatos del aprendiz unidos en un solo PDF"""
    from app.services.formato_service import generar_pdf_unificado_aprendiz

    aprendiz = Aprendiz.query.get_or_404(aprendiz_id)
    matricula = Matricula.query.filter_by(aprendiz_id=aprendiz.id).first()

    if not matricula:
        flash('El aprendiz no tiene matrícula', 'warning')
        return redirect(url_for('admin.matriculas'))

    documentos = Documento.query.filter_by(matricula_id=matricula.id).filter(
        Documento.reemplazado_por == None
    ).all()

    if not documentos:
        flash('El aprendiz no tiene documentos para descargar', 'warning')
        return redirect(url_for('admin.ver_matricula', matricula_id=matricula.id))

    try:
        # Generar PDF unificado con todos los formatos
        pdf_path = generar_pdf_unificado_aprendiz(aprendiz, documentos)

        return send_file(
            pdf_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=os.path.basename(pdf_path)
        )

    except Exception as e:
        current_app.logger.error(f"Error al crear PDF unificado: {e}")
        flash(f'Error al crear PDF unificado: {str(e)}', 'danger')
        return redirect(url_for('admin.ver_matricula', matricula_id=matricula.id))

@admin_bp.route('/api/programas-por-colegio/<int:colegio_id>')
@login_required
@admin_required
def programas_por_colegio(colegio_id):
    """Obtener programas filtrados por colegio"""
    try:
        # Obtener los grupos del colegio
        grupos = Grupo.query.filter_by(colegio_id=colegio_id, activo=True).all()

        # Obtener los IDs únicos de programas de esos grupos
        programa_ids = list(set([g.programa_id for g in grupos if g.programa_id]))

        # Obtener los programas
        programas = Programa.query.filter(
            Programa.id.in_(programa_ids),
            Programa.activo == True
        ).all()

        return jsonify({
            'programas': [{
                'id': p.id,
                'nombre': p.nombre,
                'codigo': p.codigo
            } for p in programas]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/matriculas/descargar-documentos-grupo/<int:grupo_id>')
@login_required
@admin_required
def descargar_documentos_grupo_matriculas(grupo_id):
    """Descargar todos los documentos de un grupo en ZIP desde matrículas"""
    import zipfile
    from io import BytesIO
    from datetime import datetime

    grupo = Grupo.query.get_or_404(grupo_id)
    aprendices = Aprendiz.query.filter_by(grupo_id=grupo_id).all()

    if not aprendices:
        flash('No hay aprendices en este grupo', 'warning')
        return redirect(url_for('admin.matriculas'))

    try:
        memory_file = BytesIO()

        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            documentos_agregados = 0

            for aprendiz in aprendices:
                matricula = Matricula.query.filter_by(aprendiz_id=aprendiz.id).first()
                if not matricula:
                    continue

                documentos = Documento.query.filter_by(matricula_id=matricula.id).filter(
                    Documento.reemplazado_por == None
                ).all()

                if documentos:
                    carpeta_aprendiz = f"{aprendiz.usuario.nombres}_{aprendiz.usuario.apellidos}_{aprendiz.usuario.documento}"

                    for documento in documentos:
                        file_path = documento.ruta_archivo

                        if not os.path.isabs(file_path):
                            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                            file_path = os.path.join(base_dir, file_path)

                        if os.path.exists(file_path):
                            tipo_doc = documento.tipo_documento.replace('_', ' ').title()
                            nombre_en_zip = f"{carpeta_aprendiz}/{tipo_doc}_{documento.nombre_archivo}"
                            zipf.write(file_path, nombre_en_zip)
                            documentos_agregados += 1

            if documentos_agregados == 0:
                flash('No se encontraron documentos para descargar', 'warning')
                return redirect(url_for('admin.matriculas'))

        memory_file.seek(0)

        nombre_zip = f"Documentos_Grupo_{grupo.nombre}_{datetime.now().strftime('%Y%m%d')}.zip"

        return send_file(
            memory_file,
            mimetype='application/zip',
            as_attachment=True,
            download_name=nombre_zip
        )

    except Exception as e:
        current_app.logger.error(f"Error al crear ZIP grupal: {e}")
        flash(f'Error al crear archivo ZIP: {str(e)}', 'danger')
        return redirect(url_for('admin.matriculas'))

@admin_bp.route('/matriculas/descargar-todos-grupos')
@login_required
@admin_required
def descargar_todos_grupos():
    """Descargar todos los documentos de TODOS los grupos en un solo ZIP"""
    import zipfile
    from io import BytesIO
    from datetime import datetime

    grupos = Grupo.query.filter_by(activo=True).all()

    if not grupos:
        flash('No hay grupos activos en el sistema', 'warning')
        return redirect(url_for('admin.matriculas'))

    try:
        memory_file = BytesIO()

        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            documentos_agregados = 0

            for grupo in grupos:
                aprendices = Aprendiz.query.filter_by(grupo_id=grupo.id).all()

                if not aprendices:
                    continue

                for aprendiz in aprendices:
                    matricula = Matricula.query.filter_by(aprendiz_id=aprendiz.id).first()
                    if not matricula:
                        continue

                    documentos = Documento.query.filter_by(matricula_id=matricula.id).filter(
                        Documento.reemplazado_por == None
                    ).all()

                    if documentos:
                        # Estructura: Grupo_X/Aprendiz_Nombre/documentos
                        carpeta_grupo = f"Grupo_{grupo.nombre}"
                        carpeta_aprendiz = f"{aprendiz.usuario.nombres}_{aprendiz.usuario.apellidos}_{aprendiz.usuario.documento}"

                        for documento in documentos:
                            file_path = documento.ruta_archivo

                            if not os.path.isabs(file_path):
                                base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                                file_path = os.path.join(base_dir, file_path)

                            if os.path.exists(file_path):
                                tipo_doc = documento.tipo_documento.replace('_', ' ').title()
                                nombre_en_zip = f"{carpeta_grupo}/{carpeta_aprendiz}/{tipo_doc}_{documento.nombre_archivo}"
                                zipf.write(file_path, nombre_en_zip)
                                documentos_agregados += 1

            if documentos_agregados == 0:
                flash('No se encontraron documentos para descargar en ningún grupo', 'warning')
                return redirect(url_for('admin.matriculas'))

        memory_file.seek(0)

        nombre_zip = f"Documentos_Todos_Grupos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"

        return send_file(
            memory_file,
            mimetype='application/zip',
            as_attachment=True,
            download_name=nombre_zip
        )

    except Exception as e:
        current_app.logger.error(f"Error al crear ZIP de todos los grupos: {e}")
        flash(f'Error al crear archivo ZIP: {str(e)}', 'danger')
        return redirect(url_for('admin.matriculas'))

@admin_bp.route('/matricular-todos-prematricula', methods=['POST'])
@login_required
@admin_required
def matricular_todos_prematricula():
    """Matricular todos los aprendices en estado PREMATRICULA que tengan todos sus documentos aprobados"""
    from datetime import datetime

    # Obtener todas las matrículas en estado PREMATRICULA
    matriculas_prematricula = Matricula.query.filter_by(estado='PREMATRICULA').all()

    if not matriculas_prematricula:
        flash('No hay aprendices en estado PRE-MATRÍCULA para matricular', 'warning')
        return redirect(url_for('admin.matriculas'))

    matriculados_exitosos = 0
    matriculados_fallidos = 0
    errores = []

    for matricula in matriculas_prematricula:
        try:
            # Verificar que tenga todos los documentos aprobados
            documentos = Documento.query.filter_by(matricula_id=matricula.id).all()
            documentos_activos = [d for d in documentos if not d.reemplazado_por]

            # Obtener el aprendiz para verificar documentos requeridos
            aprendiz = matricula.aprendiz
            usuario = aprendiz.usuario
            es_mayor_de_edad = usuario.es_mayor_de_edad
            tipo_documento = usuario.tipo_documento

            # Determinar cantidad de documentos requeridos
            documentos_requeridos = 5 if (tipo_documento in ['CC', 'PPT', 'CE', 'PEP'] and es_mayor_de_edad) else 8

            # Verificar que tenga los documentos requeridos
            if len(documentos_activos) < documentos_requeridos:
                errores.append(f"{usuario.nombre_completo}: Solo tiene {len(documentos_activos)} de {documentos_requeridos} documentos requeridos")
                matriculados_fallidos += 1
                continue

            # Verificar que todos estén aprobados
            todos_aprobados = all(d.validado == True for d in documentos_activos)
            if not todos_aprobados:
                errores.append(f"{usuario.nombre_completo}: Tiene documentos sin aprobar")
                matriculados_fallidos += 1
                continue

            # Matricular
            matricula.estado = 'MATRICULADO'
            matricula.fecha_validacion_admin = datetime.now()
            matricula.validado_por_admin = current_user.id
            db.session.commit()

            matriculados_exitosos += 1

        except Exception as e:
            db.session.rollback()
            errores.append(f"{matricula.aprendiz.usuario.nombre_completo}: {str(e)}")
            matriculados_fallidos += 1
            from flask import current_app
            current_app.logger.error(f"Error al matricular {matricula.id}: {e}")

    # Mensajes de feedback
    if matriculados_exitosos > 0:
        flash(f'¡{matriculados_exitosos} aprendiz(es) matriculado(s) exitosamente!', 'success')

    if matriculados_fallidos > 0:
        flash(f'{matriculados_fallidos} aprendiz(es) NO pudieron ser matriculados', 'warning')
        for error in errores[:5]:  # Mostrar solo los primeros 5 errores
            flash(f'• {error}', 'danger')

    return redirect(url_for('admin.matriculas'))


@admin_bp.route('/generar-sofia', methods=['GET', 'POST'])
@login_required
@admin_required
def generar_sofia():
    """Página para generar formato SOFIA Plus con filtros"""
    if request.method == 'GET':
        # Obtener opciones de filtro
        opciones = SofiaService.get_opciones_filtro_admin()
        return render_template('admin/generar_sofia.html', **opciones)

    # POST: Generar archivo
    filtro_tipo = request.form.get('filtro_tipo')
    filtro_id = request.form.get('filtro_id')

    if not filtro_tipo:
        flash('Debe seleccionar un tipo de filtro', 'warning')
        return redirect(url_for('admin.generar_sofia'))

    # Convertir filtro_id a entero si existe
    if filtro_id:
        try:
            filtro_id = int(filtro_id)
        except ValueError:
            flash('ID de filtro inválido', 'danger')
            return redirect(url_for('admin.generar_sofia'))

    # Generar formato
    success, message, file_path = SofiaService.generar_formato_sofia(
        filtro_tipo=filtro_tipo,
        filtro_id=filtro_id,
        docente_colegio_id=None  # Admin no tiene restricciones
    )

    if success:
        # Descargar archivo
        return send_file(
            file_path,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=os.path.basename(file_path)
        )
    else:
        flash(message, 'danger')
        return redirect(url_for('admin.generar_sofia'))


# ============================================
# GESTIÓN DE DOCUMENTOS SIMAT (ADMIN)
# ============================================

@admin_bp.route('/simat')
@login_required
@admin_required
def simat():
    """Página de gestión de documentos SIMAT para administrador"""
    # Obtener todos los documentos SIMAT con filtros opcionales
    estado_filtro = request.args.get('estado', 'TODOS')
    colegio_filtro = request.args.get('colegio_id')

    query = DocumentoSIMAT.query

    if estado_filtro != 'TODOS':
        query = query.filter_by(estado=estado_filtro)

    if colegio_filtro:
        query = query.filter_by(colegio_id=int(colegio_filtro))

    documentos = query.order_by(DocumentoSIMAT.created_at.desc()).all()

    # Obtener colegios para el filtro
    colegios = Colegio.query.filter_by(activo=True).order_by(Colegio.nombre).all()

    # Estadísticas
    stats = {
        'total': DocumentoSIMAT.query.count(),
        'pendientes': DocumentoSIMAT.query.filter_by(estado='PENDIENTE').count(),
        'aprobados': DocumentoSIMAT.query.filter_by(estado='APROBADO').count(),
        'rechazados': DocumentoSIMAT.query.filter_by(estado='RECHAZADO').count()
    }

    return render_template('admin/simat.html',
                         documentos=documentos,
                         colegios=colegios,
                         stats=stats,
                         estado_filtro=estado_filtro,
                         colegio_filtro=colegio_filtro)


@admin_bp.route('/simat/<int:simat_id>/aprobar', methods=['POST'])
@login_required
@admin_required
def aprobar_simat(simat_id):
    """Aprobar documento SIMAT"""
    documento = DocumentoSIMAT.query.get_or_404(simat_id)

    observaciones = request.form.get('observaciones', '')

    try:
        documento.estado = 'APROBADO'
        documento.observaciones = observaciones if observaciones else None
        documento.revisado_por = current_user.id
        documento.fecha_revision = datetime.utcnow()

        db.session.commit()
        flash(f'Documento SIMAT aprobado exitosamente', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f'Error al aprobar documento: {str(e)}', 'danger')

    return redirect(url_for('admin.simat'))


@admin_bp.route('/simat/<int:simat_id>/rechazar', methods=['POST'])
@login_required
@admin_required
def rechazar_simat(simat_id):
    """Rechazar documento SIMAT"""
    documento = DocumentoSIMAT.query.get_or_404(simat_id)

    observaciones = request.form.get('observaciones', '')

    if not observaciones:
        flash('Debe proporcionar observaciones al rechazar un documento', 'warning')
        return redirect(url_for('admin.simat'))

    try:
        documento.estado = 'RECHAZADO'
        documento.observaciones = observaciones
        documento.revisado_por = current_user.id
        documento.fecha_revision = datetime.utcnow()

        db.session.commit()
        flash(f'Documento SIMAT rechazado', 'warning')

    except Exception as e:
        db.session.rollback()
        flash(f'Error al rechazar documento: {str(e)}', 'danger')

    return redirect(url_for('admin.simat'))


@admin_bp.route('/simat/<int:simat_id>/ver')
@login_required
@admin_required
def ver_simat_admin(simat_id):
    """Ver documento SIMAT (admin) - Solo PDFs se visualizan, otros se descargan"""
    documento = DocumentoSIMAT.query.get_or_404(simat_id)

    if not os.path.exists(documento.ruta_archivo):
        flash('El archivo no existe', 'danger')
        return redirect(url_for('admin.simat'))

    # Determinar extensión
    ext = documento.nombre_archivo_original.rsplit('.', 1)[1].lower() if '.' in documento.nombre_archivo_original else ''

    # Solo PDFs se pueden visualizar en navegador, otros formatos se descargan
    if ext == 'pdf':
        return send_file(
            documento.ruta_archivo,
            mimetype='application/pdf',
            as_attachment=False
        )
    else:
        # Para Excel/Word, redirigir directamente a descarga
        flash('Los archivos Excel/Word solo pueden descargarse. Use el botón de descarga.', 'info')
        return redirect(url_for('admin.simat'))

@admin_bp.route('/simat/<int:simat_id>/descargar')
@login_required
@admin_required
def descargar_simat_admin(simat_id):
    """Descargar documento SIMAT (admin)"""
    documento = DocumentoSIMAT.query.get_or_404(simat_id)

    if not os.path.exists(documento.ruta_archivo):
        flash('El archivo no existe', 'danger')
        return redirect(url_for('admin.simat'))

    return send_file(
        documento.ruta_archivo,
        as_attachment=True,
        download_name=documento.nombre_archivo_original
    )
