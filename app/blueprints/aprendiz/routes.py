from flask import render_template, redirect, url_for, flash, request, send_file, current_app
from flask_login import login_required, current_user
from app.models import db, Aprendiz, Colegio, Grupo, Programa
from app.services.matricula_service import MatriculaService
from app.services.documento_service import DocumentoService
from app.services.reporte_service import ReporteService
from app.utils.decorators import aprendiz_required
from app.utils.validators import Validators
from werkzeug.utils import secure_filename
from . import aprendiz_bp
import os

@aprendiz_bp.route('/dashboard')
@login_required
@aprendiz_required
def dashboard():
    """Dashboard del aprendiz"""
    aprendiz = current_user.aprendiz

    if not aprendiz:
        flash('Perfil de aprendiz no encontrado', 'danger')
        return redirect(url_for('public.logout'))

    # Obtener o crear matrícula
    matricula = MatriculaService.get_or_create_matricula(aprendiz.id)

    # Obtener documentos activos con su estado
    documentos = DocumentoService.get_documentos_activos(matricula.id) if matricula else []
    documentos_subidos = len(documentos)

    # Contar documentos por estado
    docs_aprobados = len([d for d in documentos if d.estado == 'APROBADO'])
    docs_pendientes = len([d for d in documentos if d.estado == 'PENDIENTE'])
    docs_rechazados = len([d for d in documentos if d.estado == 'RECHAZADO'])

    return render_template('aprendiz/dashboard.html',
                         aprendiz=aprendiz,
                         matricula=matricula,
                         documentos=documentos,
                         documentos_subidos=documentos_subidos,
                         docs_aprobados=docs_aprobados,
                         docs_pendientes=docs_pendientes,
                         docs_rechazados=docs_rechazados)

@aprendiz_bp.route('/perfil', methods=['GET', 'POST'])
@login_required
@aprendiz_required
def perfil():
    """Editar perfil del aprendiz"""
    aprendiz = current_user.aprendiz

    if request.method == 'POST':
        # Actualizar datos del usuario
        current_user.nombres = request.form.get('nombres')
        current_user.apellidos = request.form.get('apellidos')
        current_user.email = request.form.get('email')
        current_user.telefono = request.form.get('telefono')

        # Actualizar datos del aprendiz
        # Convertir strings vacíos a None para campos de clave foránea
        colegio_id = request.form.get('colegio_id')
        grupo_id = request.form.get('grupo_id')
        programa_id = request.form.get('programa_id')

        data = {
            'ciudad': request.form.get('ciudad'),
            'departamento': request.form.get('departamento'),
            'acudiente_tipo_doc': request.form.get('acudiente_tipo_doc'),
            'acudiente_documento': request.form.get('acudiente_documento'),
            'acudiente_lugar_expedicion': request.form.get('acudiente_lugar_expedicion'),
            'acudiente_nombres': request.form.get('acudiente_nombres'),
            'acudiente_apellidos': request.form.get('acudiente_apellidos'),
            'acudiente_direccion': request.form.get('acudiente_direccion'),
            'acudiente_telefono': request.form.get('acudiente_telefono'),
            'acudiente_email': request.form.get('acudiente_email'),
            'colegio_id': int(colegio_id) if colegio_id and colegio_id.strip() else None,
            'grupo_id': int(grupo_id) if grupo_id and grupo_id.strip() else None,
            'programa_id': int(programa_id) if programa_id and programa_id.strip() else None
        }

        try:
            db.session.commit()
            success, message = MatriculaService.update_aprendiz_data(aprendiz.id, **data)

            if success:
                flash('Perfil actualizado exitosamente', 'success')
                return redirect(url_for('aprendiz.perfil'))
            else:
                flash(message, 'danger')

        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar perfil: {str(e)}', 'danger')

    colegios = Colegio.query.filter_by(activo=True).all()
    # Cargar todos los grupos con sus relaciones para filtrar en frontend
    grupos = Grupo.query.filter_by(activo=True).options(
        db.joinedload(Grupo.colegio),
        db.joinedload(Grupo.programa)
    ).all()
    programas = Programa.query.filter_by(activo=True).all()

    return render_template('aprendiz/perfil.html',
                         aprendiz=aprendiz,
                         colegios=colegios,
                         grupos=grupos,
                         programas=programas)

@aprendiz_bp.route('/matricula')
@login_required
@aprendiz_required
def matricula():
    """Formulario de matrícula"""
    aprendiz = current_user.aprendiz
    matricula = MatriculaService.get_or_create_matricula(aprendiz.id)

    colegios = Colegio.query.filter_by(activo=True).all()
    # Cargar todos los grupos con sus relaciones para filtrar en frontend
    grupos = Grupo.query.filter_by(activo=True).options(
        db.joinedload(Grupo.colegio),
        db.joinedload(Grupo.programa)
    ).all()
    programas = Programa.query.filter_by(activo=True).all()

    return render_template('aprendiz/matricula.html',
                         aprendiz=aprendiz,
                         matricula=matricula,
                         colegios=colegios,
                         grupos=grupos,
                         programas=programas)

@aprendiz_bp.route('/guardar-matricula', methods=['POST'])
@login_required
@aprendiz_required
def guardar_matricula():
    """Guardar datos de matrícula del aprendiz"""
    try:
        aprendiz = current_user.aprendiz

        # Datos de residencia
        aprendiz.ciudad = request.form.get('ciudad')
        aprendiz.departamento = request.form.get('departamento')

        # Datos del acudiente
        aprendiz.acudiente_tipo_doc = request.form.get('acudiente_tipo_doc')
        aprendiz.acudiente_documento = request.form.get('acudiente_documento')
        aprendiz.acudiente_lugar_expedicion = request.form.get('acudiente_lugar_expedicion')
        aprendiz.acudiente_nombres = request.form.get('acudiente_nombres')
        aprendiz.acudiente_apellidos = request.form.get('acudiente_apellidos')
        aprendiz.acudiente_direccion = request.form.get('acudiente_direccion')
        aprendiz.acudiente_telefono = request.form.get('acudiente_telefono')
        aprendiz.acudiente_email = request.form.get('acudiente_email')

        # Datos académicos (convertir strings vacíos a None)
        colegio_id = request.form.get('colegio_id')
        grupo_id = request.form.get('grupo_id')
        programa_id = request.form.get('programa_id')

        aprendiz.colegio_id = int(colegio_id) if colegio_id and colegio_id.strip() else None
        aprendiz.grupo_id = int(grupo_id) if grupo_id and grupo_id.strip() else aprendiz.grupo_id  # Preservar valor existente si viene vacío
        aprendiz.programa_id = int(programa_id) if programa_id and programa_id.strip() else None

        # Marcar perfil como completo
        aprendiz.perfil_completo = True

        db.session.commit()
        flash('Datos de matrícula guardados exitosamente', 'success')
        return redirect(url_for('aprendiz.dashboard'))

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error al guardar matrícula: {e}")
        flash(f'Error al guardar los datos: {str(e)}', 'danger')
        return redirect(url_for('aprendiz.matricula'))

@aprendiz_bp.route('/documentos', methods=['GET', 'POST'])
@login_required
@aprendiz_required
def documentos():
    """Gestión de documentos"""
    aprendiz = current_user.aprendiz
    matricula = MatriculaService.get_or_create_matricula(aprendiz.id)

    if request.method == 'POST':
        tipo_documento = request.form.get('tipo_documento')
        file = request.files.get('archivo')

        if not file or not file.filename:
            flash('Debe seleccionar un archivo', 'danger')
            return redirect(url_for('aprendiz.documentos'))

        if not Validators.allowed_file(file.filename):
            flash('Tipo de archivo no permitido. Solo PDF, JPG, JPEG, PNG', 'danger')
            return redirect(url_for('aprendiz.documentos'))

        # Subir documento
        success, message, documento = DocumentoService.upload_documento(file, matricula, tipo_documento)

        if success:
            flash('Documento cargado exitosamente', 'success')
        else:
            flash(message, 'danger')

        return redirect(url_for('aprendiz.documentos'))

    # Obtener documentos activos
    documentos = DocumentoService.get_documentos_activos(matricula.id)

    # Tipos de documentos requeridos según edad y tipo de documento
    # Si tiene CC, PPT, CE o PEP y es mayor de edad, no necesita: registro civil, tratamiento de datos, documento acudiente
    if current_user.tipo_documento in ['CC', 'PPT', 'CE', 'PEP'] and current_user.es_mayor_de_edad:
        tipos_requeridos = [
            ('DOCUMENTO_IDENTIDAD', 'Documento de Identidad'),
            ('CERTIFICADO_SALUD', 'Certificado de Afiliación a Salud'),
            ('CERTIFICADO_SOFIA', 'Certificado SOFIA Plus'),
            ('CERTIFICADO_APE', 'Certificado APE'),
            ('ACUERDO_APRENDIZ', 'Acuerdo del Aprendiz')
        ]
    else:
        # Menores de edad o con TI requieren todos los documentos
        tipos_requeridos = [
            ('DOCUMENTO_IDENTIDAD', 'Documento de Identidad'),
            ('REGISTRO_CIVIL', 'Registro Civil'),
            ('CERTIFICADO_SALUD', 'Certificado de Afiliación a Salud'),
            ('CERTIFICADO_SOFIA', 'Certificado SOFIA Plus'),
            ('CERTIFICADO_APE', 'Certificado APE'),
            ('DOCUMENTO_ACUDIENTE', 'Documento del Acudiente'),
            ('TRATAMIENTO_DATOS', 'Tratamiento de Datos'),
            ('ACUERDO_APRENDIZ', 'Acuerdo del Aprendiz')
        ]

    return render_template('aprendiz/documentos.html',
                         aprendiz=aprendiz,
                         matricula=matricula,
                         documentos=documentos,
                         tipos_requeridos=tipos_requeridos)

@aprendiz_bp.route('/subir-documento', methods=['POST'])
@login_required
@aprendiz_required
def subir_documento():
    """Subir un documento individual"""
    aprendiz = current_user.aprendiz
    matricula = MatriculaService.get_or_create_matricula(aprendiz.id)

    tipo_documento = request.form.get('tipo_documento')
    file = request.files.get('archivo')

    if not file or not file.filename:
        flash('Debe seleccionar un archivo', 'danger')
        return redirect(url_for('aprendiz.documentos'))

    if not Validators.allowed_file(file.filename):
        flash('Tipo de archivo no permitido. Solo PDF', 'danger')
        return redirect(url_for('aprendiz.documentos'))

    # Subir documento
    success, message, documento = DocumentoService.upload_documento(file, matricula, tipo_documento)

    if success:
        flash('Documento cargado exitosamente', 'success')
    else:
        flash(message, 'danger')

    return redirect(url_for('aprendiz.documentos'))

@aprendiz_bp.route('/reemplazar-documento/<int:documento_id>', methods=['POST'])
@login_required
@aprendiz_required
def reemplazar_documento(documento_id):
    """Reemplazar un documento existente"""
    from app.models import Documento

    documento = Documento.query.get_or_404(documento_id)

    # Verificar que el documento pertenece al aprendiz actual
    if documento.matricula.aprendiz_id != current_user.aprendiz.id:
        flash('No tiene permisos para modificar este documento', 'danger')
        return redirect(url_for('aprendiz.documentos'))

    # Verificar que el documento no esté aprobado
    if documento.validado == True:
        flash('No puede reemplazar un documento que ya ha sido aprobado por el docente. Contacte al administrador si necesita cambiarlo.', 'danger')
        return redirect(url_for('aprendiz.documentos'))

    file = request.files.get('archivo')

    if not file or not file.filename:
        flash('Debe seleccionar un archivo', 'danger')
        return redirect(url_for('aprendiz.documentos'))

    if not Validators.allowed_file(file.filename):
        flash('Tipo de archivo no permitido. Solo PDF', 'danger')
        return redirect(url_for('aprendiz.documentos'))

    # Reemplazar documento
    success, message, nuevo_doc = DocumentoService.replace_documento(documento.id, file, current_user.id)

    if success:
        flash('Documento reemplazado exitosamente', 'success')
    else:
        flash(message, 'danger')

    return redirect(url_for('aprendiz.documentos'))

@aprendiz_bp.route('/enviar-matricula', methods=['POST'])
@login_required
@aprendiz_required
def enviar_matricula():
    """Enviar matrícula para validación"""
    aprendiz = current_user.aprendiz
    matricula = MatriculaService.get_or_create_matricula(aprendiz.id)

    success, message = MatriculaService.enviar_matricula(matricula.id)

    if success:
        flash('Matrícula enviada exitosamente para validación', 'success')
    else:
        flash(message, 'danger')

    return redirect(url_for('aprendiz.dashboard'))

@aprendiz_bp.route('/descargar-resumen')
@login_required
@aprendiz_required
def descargar_resumen():
    """Descargar PDF con resumen de matrícula"""
    aprendiz = current_user.aprendiz
    matricula = MatriculaService.get_or_create_matricula(aprendiz.id)

    try:
        pdf_path = ReporteService.generar_pdf_resumen_aprendiz(aprendiz, matricula)
        return send_file(pdf_path, as_attachment=True, download_name=f'resumen_{current_user.documento}.pdf')

    except Exception as e:
        flash(f'Error al generar PDF: {str(e)}', 'danger')
        return redirect(url_for('aprendiz.dashboard'))

@aprendiz_bp.route('/descargar-documento/<int:documento_id>')
@login_required
@aprendiz_required
def descargar_documento(documento_id):
    """Descargar un documento específico"""
    from app.models import Documento

    documento = Documento.query.get_or_404(documento_id)

    # Verificar que el documento pertenece al aprendiz actual
    if documento.matricula.aprendiz_id != current_user.aprendiz.id:
        flash('No tiene permisos para descargar este documento', 'danger')
        return redirect(url_for('aprendiz.dashboard'))

    if not os.path.exists(documento.ruta_archivo):
        flash('Archivo no encontrado', 'danger')
        return redirect(url_for('aprendiz.documentos'))

    return send_file(documento.ruta_archivo, as_attachment=True, download_name=documento.nombre_archivo)

@aprendiz_bp.route('/ver-documento/<int:documento_id>')
@login_required
@aprendiz_required
def ver_documento(documento_id):
    """Ver un documento específico en el navegador"""
    from app.models import Documento

    documento = Documento.query.get_or_404(documento_id)

    # Verificar que el documento pertenece al aprendiz actual
    if documento.matricula.aprendiz_id != current_user.aprendiz.id:
        flash('No tiene permisos para ver este documento', 'danger')
        return redirect(url_for('aprendiz.dashboard'))

    # Convertir ruta relativa a absoluta si es necesario
    file_path = documento.ruta_archivo
    if not os.path.isabs(file_path):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        file_path = os.path.join(base_dir, file_path)

    if not os.path.exists(file_path):
        flash(f'Archivo no encontrado: {os.path.basename(file_path)}', 'danger')
        return redirect(url_for('aprendiz.documentos'))

    # Detectar el tipo de archivo para usar el mimetype correcto
    extension = os.path.splitext(file_path)[1].lower()
    mimetype_map = {
        '.pdf': 'application/pdf',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg'
    }
    mimetype = mimetype_map.get(extension, 'application/pdf')

    # Enviar archivo para visualizar en navegador (no descargar)
    return send_file(file_path, mimetype=mimetype)

@aprendiz_bp.route('/descargar-documentos-pdf')
@login_required
@aprendiz_required
def descargar_documentos_pdf():
    """Descargar todos los documentos del aprendiz en un PDF unificado"""
    from app.services.formato_service import generar_pdf_unificado_aprendiz

    aprendiz = current_user.aprendiz
    matricula = MatriculaService.get_or_create_matricula(aprendiz.id)
    documentos = DocumentoService.get_documentos_activos(matricula.id)

    if not documentos:
        flash('No tiene documentos para descargar', 'warning')
        return redirect(url_for('aprendiz.documentos'))

    try:
        # Generar PDF unificado
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
        return redirect(url_for('aprendiz.documentos'))


@aprendiz_bp.route('/descargar-formato-tratamiento-datos')
@login_required
@aprendiz_required
def descargar_formato_tratamiento_datos():
    """Descargar formato de tratamiento de datos auto-generado con los datos del aprendiz"""
    from app.services.formato_service import generar_formato_tratamiento_datos

    try:
        aprendiz = current_user.aprendiz

        # Generar el formato (los datos del acudiente están en el modelo Aprendiz)
        file_path = generar_formato_tratamiento_datos(aprendiz)

        # Enviar el archivo
        return send_file(
            file_path,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            as_attachment=True,
            download_name=os.path.basename(file_path)
        )

    except Exception as e:
        current_app.logger.error(f"Error al generar formato de tratamiento de datos: {e}")
        flash(f'Error al generar el formato: {str(e)}', 'danger')
        return redirect(url_for('aprendiz.documentos'))


@aprendiz_bp.route('/descargar-formato-compromiso-aprendiz')
@login_required
@aprendiz_required
def descargar_formato_compromiso_aprendiz():
    """Descargar formato de compromiso del aprendiz auto-generado con los datos del aprendiz"""
    from app.services.formato_service import generar_formato_compromiso_aprendiz

    try:
        aprendiz = current_user.aprendiz

        # Generar el formato (los datos del acudiente están en el modelo Aprendiz)
        file_path = generar_formato_compromiso_aprendiz(aprendiz)

        # Enviar el archivo
        return send_file(
            file_path,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            as_attachment=True,
            download_name=os.path.basename(file_path)
        )

    except Exception as e:
        current_app.logger.error(f"Error al generar formato de compromiso del aprendiz: {e}")
        flash(f'Error al generar el formato: {str(e)}', 'danger')
        return redirect(url_for('aprendiz.documentos'))
