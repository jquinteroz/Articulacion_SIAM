from app.models import db, Usuario, Aprendiz
from app.utils.crypto import CryptoService
from flask import current_app

class AuthService:
    """Servicio para manejo de autenticación y usuarios"""

    @staticmethod
    def register_aprendiz(documento, tipo_documento, nombres, apellidos, email, telefono, password,
                         colegio_id=None, grupo_id=None, programa_id=None, fecha_nacimiento=None):
        """
        Registra un nuevo aprendiz
        Returns: (success, message, user)
        """
        try:
            # Verificar si ya existe el documento
            if Usuario.query.filter_by(documento=documento).first():
                return False, 'El documento ya está registrado', None

            # Verificar si ya existe el email
            if Usuario.query.filter_by(email=email).first():
                return False, 'El email ya está registrado', None

            # Convertir fecha_nacimiento de string a date si es necesario
            if fecha_nacimiento and isinstance(fecha_nacimiento, str):
                from datetime import datetime as dt
                fecha_nacimiento = dt.strptime(fecha_nacimiento, '%Y-%m-%d').date()

            # Encriptar contraseña
            password_cipher = CryptoService.encrypt_password(password)

            # Crear usuario
            usuario = Usuario(
                documento=documento,
                tipo_documento=tipo_documento,
                nombres=nombres,
                apellidos=apellidos,
                fecha_nacimiento=fecha_nacimiento,
                email=email,
                telefono=telefono,
                password_cipher=password_cipher,
                rol='APRENDIZ'
            )
            usuario.set_password(password)

            db.session.add(usuario)
            db.session.flush()

            # Crear perfil de aprendiz con colegio, grupo y programa
            aprendiz = Aprendiz(
                usuario_id=usuario.id,
                colegio_id=colegio_id,
                grupo_id=grupo_id,
                programa_id=programa_id
            )
            db.session.add(aprendiz)

            db.session.commit()

            return True, 'Registro exitoso', usuario

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error en registro: {e}")
            return False, 'Error al registrar usuario', None

    @staticmethod
    def create_user(documento, tipo_documento, nombres, apellidos, email, telefono, password, rol='APRENDIZ', fecha_nacimiento=None):
        """
        Crea un nuevo usuario (para uso administrativo)
        Returns: (success, message, user)
        """
        try:
            # Verificar duplicados
            if Usuario.query.filter_by(documento=documento).first():
                return False, 'El documento ya está registrado', None

            if Usuario.query.filter_by(email=email).first():
                return False, 'El email ya está registrado', None

            # Convertir fecha_nacimiento de string a date si es necesario
            if fecha_nacimiento and isinstance(fecha_nacimiento, str):
                from datetime import datetime as dt
                fecha_nacimiento = dt.strptime(fecha_nacimiento, '%Y-%m-%d').date()

            # Encriptar contraseña
            password_cipher = CryptoService.encrypt_password(password)

            # Crear usuario
            usuario = Usuario(
                documento=documento,
                tipo_documento=tipo_documento,
                nombres=nombres,
                apellidos=apellidos,
                fecha_nacimiento=fecha_nacimiento,
                email=email,
                telefono=telefono,
                password_cipher=password_cipher,
                rol=rol
            )
            usuario.set_password(password)

            db.session.add(usuario)

            # Si es aprendiz, crear el perfil
            if rol == 'APRENDIZ':
                db.session.flush()
                aprendiz = Aprendiz(usuario_id=usuario.id)
                db.session.add(aprendiz)

            db.session.commit()

            return True, 'Usuario creado exitosamente', usuario

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error al crear usuario: {e}")
            return False, f'Error al crear usuario: {str(e)}', None

    @staticmethod
    def update_user(user_id, **kwargs):
        """Actualiza los datos de un usuario"""
        try:
            usuario = Usuario.query.get(user_id)
            if not usuario:
                return False, 'Usuario no encontrado'

            # Actualizar campos permitidos
            allowed_fields = ['nombres', 'apellidos', 'email', 'telefono', 'tipo_documento', 'fecha_nacimiento', 'activo', 'rol']

            for field in allowed_fields:
                if field in kwargs:
                    value = kwargs[field]
                    # Convertir fecha_nacimiento de string a date si es necesario
                    if field == 'fecha_nacimiento' and value and isinstance(value, str):
                        from datetime import datetime as dt
                        value = dt.strptime(value, '%Y-%m-%d').date()
                    setattr(usuario, field, value)

            # Si se proporciona nueva contraseña
            if 'password' in kwargs and kwargs['password']:
                usuario.set_password(kwargs['password'])
                usuario.password_cipher = CryptoService.encrypt_password(kwargs['password'])

            # Si es aprendiz, actualizar colegio_id, grupo_id y programa_id en el perfil
            if usuario.rol == 'APRENDIZ':
                aprendiz = Aprendiz.query.filter_by(usuario_id=usuario.id).first()
                if aprendiz:
                    if 'colegio_id' in kwargs:
                        aprendiz.colegio_id = kwargs['colegio_id'] if kwargs['colegio_id'] else None
                    if 'grupo_id' in kwargs:
                        aprendiz.grupo_id = kwargs['grupo_id'] if kwargs['grupo_id'] else None
                    if 'programa_id' in kwargs:
                        aprendiz.programa_id = kwargs['programa_id'] if kwargs['programa_id'] else None

            db.session.commit()
            return True, 'Usuario actualizado exitosamente'

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error al actualizar usuario: {e}")
            return False, f'Error al actualizar usuario: {str(e)}'

    @staticmethod
    def delete_user(user_id):
        """Elimina un usuario"""
        try:
            usuario = Usuario.query.get(user_id)
            if not usuario:
                return False, 'Usuario no encontrado'

            db.session.delete(usuario)
            db.session.commit()
            return True, 'Usuario eliminado exitosamente'

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error al eliminar usuario: {e}")
            return False, f'Error al eliminar usuario: {str(e)}'

    @staticmethod
    def get_decrypted_password(user_id):
        """Obtiene la contraseña desencriptada de un usuario"""
        try:
            usuario = Usuario.query.get(user_id)
            if not usuario or not usuario.password_cipher:
                return None

            return CryptoService.decrypt_password(usuario.password_cipher)

        except Exception as e:
            current_app.logger.error(f"Error al desencriptar contraseña: {e}")
            return None
