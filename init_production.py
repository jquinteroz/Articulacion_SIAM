# -*- coding: utf-8 -*-
"""
Script de Inicialización para Producción
Sistema de Articulación SENA
Versión: 1.0.0

Este script:
1. Limpia todos los datos de prueba
2. Crea un usuario administrador inicial
3. Inicializa la base de datos con la estructura correcta

ADVERTENCIA: Este script eliminará TODOS los datos existentes

Desarrollado por: Johann Quintero (jsquinteroz)
GitHub: @jsquinteroz
Copyright (c) 2025 - Todos los derechos reservados
"""

import sys
import os
import io

# Configurar encoding para Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import secrets
from datetime import datetime

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Usuario, Aprendiz, Colegio, Programa, Grupo, Matricula, Documento
from werkzeug.security import generate_password_hash

def limpiar_base_datos():
    """Elimina todos los datos de las tablas"""
    print("\n🗑️  Limpiando base de datos...")

    try:
        # Eliminar en orden correcto (respetando foreign keys)
        Documento.query.delete()
        print("   ✓ Documentos eliminados")

        Matricula.query.delete()
        print("   ✓ Matrículas eliminadas")

        Aprendiz.query.delete()
        print("   ✓ Aprendices eliminados")

        Grupo.query.delete()
        print("   ✓ Grupos eliminados")

        Programa.query.delete()
        print("   ✓ Programas eliminados")

        Colegio.query.delete()
        print("   ✓ Colegios eliminados")

        Usuario.query.delete()
        print("   ✓ Usuarios eliminados")

        db.session.commit()
        print("\n✅ Base de datos limpiada exitosamente\n")
        return True

    except Exception as e:
        db.session.rollback()
        print(f"\n❌ Error al limpiar base de datos: {str(e)}\n")
        return False

def crear_usuario_admin(documento, password):
    """Crea el usuario administrador inicial"""
    print("👤 Creando usuario administrador...")

    try:
        # Verificar que no exista
        admin_existente = Usuario.query.filter_by(documento=documento).first()
        if admin_existente:
            print("   ⚠️  Ya existe un administrador con este documento")
            return None

        # Crear usuario admin
        from datetime import datetime as dt, timezone
        admin = Usuario(
            documento=documento,
            tipo_documento='CC',
            nombres='Administrador',
            apellidos='Sistema',
            email='admin@articulacion.sena.edu.co',
            password_hash=generate_password_hash(password),
            rol='ADMINISTRADOR',
            activo=True,
            created_at=dt.now(timezone.utc)
        )

        db.session.add(admin)
        db.session.commit()

        print("   ✓ Usuario administrador creado exitosamente")
        print(f"   📋 Documento: {documento}")
        print(f"   🔑 Contraseña: {password}")
        print("\n⚠️  IMPORTANTE: Guarda estas credenciales en un lugar seguro\n")

        return admin

    except Exception as e:
        db.session.rollback()
        print(f"\n❌ Error al crear administrador: {str(e)}\n")
        return None

def inicializar_tablas():
    """Crea las tablas si no existen"""
    print("🔧 Verificando estructura de base de datos...")

    try:
        db.create_all()
        print("   ✓ Estructura de base de datos verificada\n")
        return True
    except Exception as e:
        print(f"\n❌ Error al crear tablas: {str(e)}\n")
        return False

def limpiar_archivos_temporales():
    """Limpia archivos temporales y de prueba"""
    print("🧹 Limpiando archivos temporales...")

    import shutil

    # Directorio temporal
    temp_dir = os.path.join(os.path.dirname(__file__), 'temp')
    if os.path.exists(temp_dir):
        try:
            # Eliminar todos los archivos dentro de temp
            for filename in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, filename)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            print("   ✓ Archivos temporales eliminados")
        except Exception as e:
            print(f"   ⚠️  Error al limpiar temp: {str(e)}")
    else:
        # Crear directorio temp si no existe
        os.makedirs(temp_dir)
        print("   ✓ Directorio temp creado")

    # Directorio de uploads (si existe)
    uploads_dir = os.path.join(os.path.dirname(__file__), 'uploads')
    if os.path.exists(uploads_dir):
        try:
            for filename in os.listdir(uploads_dir):
                file_path = os.path.join(uploads_dir, filename)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            print("   ✓ Archivos de uploads eliminados")
        except Exception as e:
            print(f"   ⚠️  Error al limpiar uploads: {str(e)}")

    print()

def main():
    """Función principal"""
    print("\n" + "="*70)
    print("   INICIALIZACIÓN DE BASE DE DATOS PARA PRODUCCIÓN")
    print("   Sistema de Articulación SENA")
    print("="*70)

    print("\n⚠️  ADVERTENCIA: Este script eliminará TODOS los datos existentes")
    print("   - Usuarios de prueba")
    print("   - Aprendices")
    print("   - Colegios")
    print("   - Programas")
    print("   - Grupos")
    print("   - Matrículas")
    print("   - Documentos")

    # Confirmación (comentar en producción automatizada)
    # respuesta = input("\n¿Está seguro de continuar? (escriba 'SI' para confirmar): ")
    # if respuesta != 'SI':
    #     print("\n❌ Operación cancelada\n")
    #     return

    # Crear aplicación
    app = create_app('production')

    with app.app_context():
        # 1. Inicializar estructura
        if not inicializar_tablas():
            print("❌ Error en la inicialización. Abortando.\n")
            return

        # 2. Limpiar datos existentes
        if not limpiar_base_datos():
            print("❌ Error al limpiar datos. Abortando.\n")
            return

        # 3. Generar credenciales seguras para admin
        admin_documento = "1000000000"  # Documento del admin
        admin_password = secrets.token_urlsafe(16)  # Contraseña aleatoria segura

        # 4. Crear usuario administrador
        admin = crear_usuario_admin(admin_documento, admin_password)

        if not admin:
            print("❌ Error al crear administrador. Abortando.\n")
            return

        # 5. Limpiar archivos temporales
        limpiar_archivos_temporales()

        # 6. Guardar credenciales en archivo seguro
        credentials_file = os.path.join(os.path.dirname(__file__), '.admin_credentials')
        with open(credentials_file, 'w') as f:
            f.write(f"ADMIN_DOCUMENTO={admin_documento}\n")
            f.write(f"ADMIN_PASSWORD={admin_password}\n")
            f.write(f"CREATED_AT={datetime.now().isoformat()}\n")

        print("="*70)
        print("✅ INICIALIZACIÓN COMPLETADA EXITOSAMENTE")
        print("="*70)
        print(f"\n📄 Credenciales guardadas en: {credentials_file}")
        print("\n⚠️  IMPORTANTE:")
        print("   1. Guarda las credenciales en un lugar seguro")
        print("   2. Elimina el archivo .admin_credentials después de guardarlas")
        print("   3. Cambia la contraseña del administrador después del primer login")
        print("\n🔐 CREDENCIALES DEL ADMINISTRADOR:")
        print(f"   Documento: {admin_documento}")
        print(f"   Contraseña: {admin_password}")
        print("\n" + "="*70 + "\n")

if __name__ == '__main__':
    main()
