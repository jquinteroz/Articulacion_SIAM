# -*- coding: utf-8 -*-
"""
Sistema de Articulación SENA
Versión: 1.0.0
Fecha: 2025-12-18

Desarrollado por: Johann Quintero (jsquinteroz)
GitHub: @jsquinteroz
Email: jsquinteroz@example.com

Copyright (c) 2025 - Todos los derechos reservados
"""
print("=== INICIO DEL SCRIPT ===", flush=True)

import os
import sys

# Configurar encoding para la consola de Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from app import create_app
from app.models import db
from sqlalchemy import text
from sqlalchemy.exc import OperationalError, DatabaseError

# Crear la aplicación
config_name = os.getenv('FLASK_ENV', 'development')
app = create_app(config_name)

# Verificar conexión a la base de datos al iniciar
def check_database_connection():
    """Verif-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ica si la base de datos está disponible"""
    try:
        with app.app_context():
            # Intentar una consulta simple
            db.session.execute(text('SELECT 1'))
            db.session.commit()
            print("✓ Conexión a la base de datos exitosa")
            return True
    except OperationalError as e:
        error_msg = str(e.orig) if hasattr(e, 'orig') else str(e)
        print("\n" + "=" * 70)
        print("⚠️  ERROR: NO SE PUDO CONECTAR A LA BASE DE DATOS")
        print("=" * 70)
        print("\n🔴 ¿Olvidaste encender el servidor de MySQL/XAMPP?")
        print("\nPosibles causas:")
        print("  1. El servidor MySQL no está ejecutándose")
        print("  2. XAMPP no está iniciado")
        print("  3. Las credenciales de la base de datos son incorrectas")
        print("  4. El puerto de MySQL está ocupado o bloqueado")
        print("\n📋 Pasos para solucionar:")
        print("  1. Abre XAMPP Control Panel")
        print("  2. Haz clic en 'Start' en MySQL")
        print("  3. Espera a que aparezca el fondo verde")
        print("  4. Intenta ejecutar la aplicación nuevamente")
        print(f"\n🔧 Detalles técnicos del error:")
        print(f"  {error_msg}")
        print("\n" + "=" * 70)
        return False
    except DatabaseError as e:
        print("\n" + "=" * 70)
        print("⚠️  ERROR DE BASE DE DATOS")
        print("=" * 70)
        print(f"\nError: {str(e)}")
        print("\nVerifica:")
        print("  - Que la base de datos 'articulacion' exista")
        print("  - Que las credenciales en el archivo .env sean correctas")
        print("=" * 70)
        return False
    except Exception as e:
        print(f"\n⚠️  Error inesperado al conectar con la base de datos: {str(e)}")
        return False

@app.cli.command()
def init_db():
    """Inicializa la base de datos"""
    db.create_all()
    print("Base de datos inicializada")

@app.cli.command()
def create_admin():
    """Crea usuarios de prueba para todos los roles"""
    from app.models import Usuario, Aprendiz
    from app.utils.crypto import CryptoService

    usuarios_prueba = [
        {
            'documento': '1000000000',
            'tipo_documento': 'CC',
            'nombres': 'Administrador',
            'apellidos': 'Sistema',
            'email': 'admin@sena.edu.co',
            'telefono': '3001234567',
            'password': 'Admin123!',
            'rol': 'ADMINISTRADOR'
        },
        {
            'documento': '1000000001',
            'tipo_documento': 'CC',
            'nombres': 'Juan Carlos',
            'apellidos': 'Pérez Gómez',
            'email': 'docente@colegio.edu.co',
            'telefono': '3001234568',
            'password': 'Docente123!',
            'rol': 'DOCENTE'
        },
        {
            'documento': '1000000002',
            'tipo_documento': 'TI',
            'nombres': 'María Fernanda',
            'apellidos': 'López Martínez',
            'email': 'aprendiz@estudiante.com',
            'telefono': '3001234569',
            'password': 'Aprendiz123!',
            'rol': 'APRENDIZ'
        }
    ]

    print("=" * 60)
    print("CREANDO USUARIOS DE PRUEBA")
    print("=" * 60)

    for user_data in usuarios_prueba:
        # Verificar si ya existe
        if Usuario.query.filter_by(documento=user_data['documento']).first():
            print(f"[OK] {user_data['rol']}: Ya existe (documento: {user_data['documento']})")
            continue

        # Crear usuario
        usuario = Usuario(
            documento=user_data['documento'],
            tipo_documento=user_data['tipo_documento'],
            nombres=user_data['nombres'],
            apellidos=user_data['apellidos'],
            email=user_data['email'],
            telefono=user_data['telefono'],
            rol=user_data['rol'],
            activo=True
        )
        usuario.set_password(user_data['password'])

        try:
            usuario.password_cipher = CryptoService.encrypt_password(user_data['password'])
        except Exception as e:
            print(f"[!] Advertencia: No se pudo encriptar la contrasena para {user_data['rol']}")
            print(f"  Error: {e}")
            print(f"  El usuario se creara sin encriptacion reversible")
            usuario.password_cipher = None

        db.session.add(usuario)
        db.session.flush()

        # Si es aprendiz, crear perfil
        if user_data['rol'] == 'APRENDIZ':
            aprendiz = Aprendiz(usuario_id=usuario.id)
            db.session.add(aprendiz)

        print(f"[OK] {user_data['rol']} creado: {user_data['nombres']} {user_data['apellidos']}")
        print(f"  Usuario: {user_data['documento']}")
        print(f"  Contrasena: {user_data['password']}")

    db.session.commit()

    print("\n" + "=" * 60)
    print("CREDENCIALES DE PRUEBA:")
    print("=" * 60)
    for user_data in usuarios_prueba:
        print(f"\n{user_data['rol']}:")
        print(f"  Usuario: {user_data['documento']}")
        print(f"  Contrasena: {user_data['password']}")
    print("\n" + "=" * 60)

@app.cli.command()
def generate_encryption_key():
    """Genera una clave de encriptación para el .env"""
    from app.utils.crypto import CryptoService
    key = CryptoService.generate_key()
    print(f"Clave de encriptación generada:")
    print(f"ENCRYPTION_KEY={key}")
    print("\nAgregue esta línea a su archivo .env")

if __name__ == '__main__':
    # Verificar conexión a la base de datos antes de iniciar el servidor
    if not check_database_connection():
        print("\n❌ No se puede iniciar la aplicación sin conexión a la base de datos")
        print("   Por favor, soluciona el problema e intenta nuevamente.\n")
        exit(1)

    print("\n" + "=" * 70)
    print("🚀 Iniciando servidor Flask...")
    print("=" * 70)
    print(f"📍 URL: http://localhost:5000")
    print(f"🔧 Modo: Debug")
    print("=" * 70 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
