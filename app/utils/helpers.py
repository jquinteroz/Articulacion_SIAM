import os
from datetime import datetime
from werkzeug.utils import secure_filename

def get_upload_path(aprendiz, tipo_documento):
    """
    Genera la ruta de carga estructurada para un documento
    Formato: uploads/[TipoDoc]_[Nombre]_[Apellido]_[Ficha]_[Programa]/
    """
    from app.models import Documento
    from flask import current_app

    usuario = aprendiz.usuario
    programa = aprendiz.programa.nombre if aprendiz.programa else "SinPrograma"
    grupo = aprendiz.grupo.nombre if aprendiz.grupo else "SinGrupo"

    # Sanitizar nombres
    nombres = usuario.nombres.replace(' ', '_')
    apellidos = usuario.apellidos.replace(' ', '_')
    programa_clean = programa.replace(' ', '_')
    tipo_clean = tipo_documento.replace('_', '')

    folder_name = f"{tipo_clean}_{nombres}_{apellidos}_{grupo}_{programa_clean}"

    # Crear ruta completa absoluta desde el directorio de la app
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    upload_folder = os.path.join(base_dir, 'uploads', folder_name)

    return upload_folder

def save_uploaded_file(file, aprendiz, tipo_documento):
    """
    Guarda un archivo cargado en la estructura correcta
    Retorna la ruta relativa del archivo guardado
    """
    if not file:
        return None

    # Obtener la ruta de destino
    upload_path = get_upload_path(aprendiz, tipo_documento)

    # Crear el directorio si no existe
    os.makedirs(upload_path, exist_ok=True)

    # Generar nombre único del archivo
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = secure_filename(file.filename)
    name, ext = os.path.splitext(filename)
    unique_filename = f"{name}_{timestamp}{ext}"

    # Ruta completa del archivo
    file_path = os.path.join(upload_path, unique_filename)

    # Guardar el archivo
    file.save(file_path)

    return file_path

def format_file_size(size_bytes):
    """Formatea el tamaño de archivo a formato legible"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.2f} MB"

def format_datetime(dt, format='%d/%m/%Y %H:%M'):
    """Formatea una fecha/hora"""
    if not dt:
        return ''
    if isinstance(dt, str):
        return dt
    return dt.strftime(format)

def get_estado_badge_class(estado):
    """Retorna la clase CSS para el badge según el estado"""
    badges = {
        'BORRADOR': 'secondary',
        'ENVIADO': 'info',
        'PENDIENTE': 'warning',
        'COMPLETO': 'success',
        'PREMATRICULA': 'primary',
        'RECHAZADO': 'danger'
    }
    return badges.get(estado, 'secondary')
