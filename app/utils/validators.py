import re
from flask import current_app

class Validators:
    """Clase con validadores personalizados"""

    @staticmethod
    def validate_documento(documento):
        """Valida que el documento solo contenga números"""
        if not documento:
            return False
        return bool(re.match(r'^\d+$', str(documento)))

    @staticmethod
    def validate_email(email):
        """Valida formato de email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    @staticmethod
    def validate_telefono(telefono):
        """Valida formato de teléfono colombiano"""
        if not telefono:
            return True  # Es opcional
        # Permite 10 dígitos o 7 dígitos
        return bool(re.match(r'^[3]\d{9}$|^\d{7}$', str(telefono)))

    @staticmethod
    def validate_password_strength(password):
        """
        Valida la fortaleza de la contraseña
        Retorna (bool, str) - (es_valida, mensaje_error)
        """
        if len(password) < 8:
            return False, "La contraseña debe tener al menos 8 caracteres"

        if not re.search(r'[A-Z]', password):
            return False, "La contraseña debe contener al menos una mayúscula"

        if not re.search(r'[a-z]', password):
            return False, "La contraseña debe contener al menos una minúscula"

        if not re.search(r'\d', password):
            return False, "La contraseña debe contener al menos un número"

        return True, "Contraseña válida"

    @staticmethod
    def allowed_file(filename):
        """Verifica si la extensión del archivo está permitida"""
        if not filename:
            return False
        allowed_extensions = current_app.config.get('ALLOWED_EXTENSIONS', {'pdf', 'jpg', 'jpeg', 'png'})
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

    @staticmethod
    def get_file_extension(filename):
        """Obtiene la extensión de un archivo"""
        if not filename or '.' not in filename:
            return ''
        return filename.rsplit('.', 1)[1].lower()

    @staticmethod
    def sanitize_filename(filename):
        """Sanitiza el nombre del archivo para evitar problemas"""
        # Elimina caracteres especiales y espacios
        filename = re.sub(r'[^\w\s.-]', '', filename)
        filename = re.sub(r'\s+', '_', filename)
        return filename
