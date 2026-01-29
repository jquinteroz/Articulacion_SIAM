from cryptography.fernet import Fernet
from flask import current_app
import base64

class CryptoService:
    """Servicio para encriptar y desencriptar contraseñas de forma reversible"""

    @staticmethod
    def _get_cipher():
        """Obtiene el objeto Fernet para encriptación"""
        key = current_app.config.get('ENCRYPTION_KEY')
        if not key:
            # Generar una clave temporal si no existe (solo desarrollo)
            key = Fernet.generate_key()
        elif isinstance(key, str):
            key = key.encode()
        return Fernet(key)

    @staticmethod
    def encrypt_password(password):
        """
        Encripta una contraseña de forma reversible
        Args:
            password (str): Contraseña en texto plano
        Returns:
            str: Contraseña encriptada en base64
        """
        try:
            cipher = CryptoService._get_cipher()
            encrypted = cipher.encrypt(password.encode())
            return encrypted.decode()
        except Exception as e:
            current_app.logger.error(f"Error al encriptar: {e}")
            return None

    @staticmethod
    def decrypt_password(encrypted_password):
        """
        Desencripta una contraseña
        Args:
            encrypted_password (str): Contraseña encriptada
        Returns:
            str: Contraseña en texto plano
        """
        try:
            cipher = CryptoService._get_cipher()
            decrypted = cipher.decrypt(encrypted_password.encode())
            return decrypted.decode()
        except Exception as e:
            current_app.logger.error(f"Error al desencriptar: {e}")
            return None

    @staticmethod
    def generate_key():
        """Genera una nueva clave de encriptación"""
        return Fernet.generate_key().decode()
