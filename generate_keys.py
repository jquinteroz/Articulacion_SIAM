"""
Generador y Gestor de Claves de Seguridad
Sistema de Articulación SENA
"""
import os
import secrets
import argparse
from pathlib import Path
from cryptography.fernet import Fernet

def generar_clave_secreta(longitud=32):
    """Genera SECRET_KEY segura"""
    return secrets.token_hex(longitud)

def generar_clave_encriptacion():
    """Genera ENCRYPTION_KEY para Fernet"""
    return Fernet.generate_key().decode()

def crear_env_desde_ejemplo(env_type='development'):
    """Crea .env con claves generadas automáticamente"""
    
    # Rutas
    base_dir = Path(__file__).parent
    env_example = base_dir / '.env.example'
    env_file = base_dir / '.env'
    
    # Verificar si .env ya existe
    if env_file.exists():
        respuesta = input(f"⚠️  {env_file} ya existe. ¿Sobrescribir? (s/N): ")
        if respuesta.lower() != 's':
            print("❌ Operación cancelada")
            return False
    
    # Leer plantilla
    if not env_example.exists():
        print(f"❌ No se encontró {env_example}")
        return False
    
    with open(env_example, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Generar claves
    print("\n🔐 Generando claves de seguridad...\n")
    
    secret_key = generar_clave_secreta()
    encryption_key = generar_clave_encriptacion()
    
    print(f"✓ SECRET_KEY generada")
    print(f"✓ ENCRYPTION_KEY generada")
    
    # Reemplazar en plantilla
    contenido = contenido.replace(
        'SECRET_KEY=tu-secret-key-generada-con-generate_keys.py',
        f'SECRET_KEY={secret_key}'
    )
    contenido = contenido.replace(
        'ENCRYPTION_KEY=tu-encryption-key-generada-con-generate_keys.py',
        f'ENCRYPTION_KEY={encryption_key}'
    )
    
    # Configurar para desarrollo por defecto
    if env_type == 'development':
        contenido = contenido.replace('FLASK_ENV=production', 'FLASK_ENV=development')
        contenido = contenido.replace('DEBUG=False', 'DEBUG=True')
    
    # Guardar .env
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(contenido)
    
    # Establecer permisos restrictivos (solo en Unix/Linux/Mac)
    if os.name != 'nt':  # Si no es Windows
        os.chmod(env_file, 0o600)  # Solo lectura/escritura para el propietario
    
    print(f"\n✅ Archivo {env_file} creado exitosamente")
    print(f"🔒 Permisos establecidos (solo propietario puede leer)")
    
    # Mostrar siguiente paso
    print("\n" + "=" * 70)
    print("📝 SIGUIENTE PASO:")
    print("=" * 70)
    print(f"1. Edita {env_file} y configura:")
    print("   - DB_PASSWORD (tu contraseña de MySQL)")
    if env_type == 'production':
        print("   - DB_HOST (tu host de producción)")
        print("   - DB_NAME (tu base de datos de producción)")
    print(f"\n2. Verifica la conexión:")
    print(f"   python validate_config.py {env_type}")
    print("=" * 70)
    
    return True

def mostrar_claves_actuales():
    """Muestra las claves actuales del .env (ofuscadas)"""
    env_file = Path(__file__).parent / '.env'
    
    if not env_file.exists():
        print("❌ No existe archivo .env")
        return False
    
    print("\n" + "=" * 70)
    print("🔍 CLAVES ACTUALES (ofuscadas)")
    print("=" * 70)
    
    with open(env_file, 'r', encoding='utf-8') as f:
        for linea in f:
            linea = linea.strip()
            if linea.startswith('SECRET_KEY='):
                valor = linea.split('=', 1)[1]
                print(f"SECRET_KEY={'*' * min(len(valor), 40)}... ({len(valor)} caracteres)")
            elif linea.startswith('ENCRYPTION_KEY='):
                valor = linea.split('=', 1)[1]
                print(f"ENCRYPTION_KEY={'*' * min(len(valor), 40)}... ({len(valor)} caracteres)")
            elif linea.startswith('DB_PASSWORD='):
                valor = linea.split('=', 1)[1]
                print(f"DB_PASSWORD={'*' * min(len(valor), 20)} ({len(valor)} caracteres)")
    
    print("=" * 70)
    return True

def regenerar_claves():
    """Regenera solo las claves de seguridad manteniendo el resto de la config"""
    env_file = Path(__file__).parent / '.env'
    
    if not env_file.exists():
        print("❌ No existe archivo .env. Usa --init primero")
        return False
    
    print("⚠️  REGENERACIÓN DE CLAVES")
    print("Las claves SECRET_KEY y ENCRYPTION_KEY serán reemplazadas")
    respuesta = input("¿Continuar? (s/N): ")
    
    if respuesta.lower() != 's':
        print("❌ Operación cancelada")
        return False
    
    # Leer archivo actual
    with open(env_file, 'r', encoding='utf-8') as f:
        lineas = f.readlines()
    
    # Generar nuevas claves
    nuevo_secret = generar_clave_secreta()
    nuevo_encryption = generar_clave_encriptacion()
    
    # Reemplazar en el contenido
    nuevas_lineas = []
    for linea in lineas:
        if linea.startswith('SECRET_KEY='):
            nuevas_lineas.append(f'SECRET_KEY={nuevo_secret}\n')
            print("✓ SECRET_KEY regenerada")
        elif linea.startswith('ENCRYPTION_KEY='):
            nuevas_lineas.append(f'ENCRYPTION_KEY={nuevo_encryption}\n')
            print("✓ ENCRYPTION_KEY regenerada")
        else:
            nuevas_lineas.append(linea)
    
    # Guardar
    with open(env_file, 'w', encoding='utf-8') as f:
        f.writelines(nuevas_lineas)
    
    print(f"\n✅ Claves regeneradas en {env_file}")
    print("\n⚠️  IMPORTANTE:")
    print("   - Los datos encriptados con la clave anterior ya no se podrán desencriptar")
    print("   - Asegúrate de actualizar todos los entornos que usen este proyecto")
    
    return True

def main():
    parser = argparse.ArgumentParser(
        description='Gestor de Claves de Seguridad - Sistema Articulación SENA'
    )
    parser.add_argument(
        '--init',
        choices=['development', 'production'],
        help='Crear .env desde .env.example con claves generadas'
    )
    parser.add_argument(
        '--show',
        action='store_true',
        help='Mostrar claves actuales (ofuscadas)'
    )
    parser.add_argument(
        '--regenerate',
        action='store_true',
        help='Regenerar solo las claves de seguridad'
    )
    parser.add_argument(
        '--generate-only',
        action='store_true',
        help='Solo mostrar claves generadas (no crear archivo)'
    )
    
    args = parser.parse_args()
    
    if args.init:
        crear_env_desde_ejemplo(args.init)
    elif args.show:
        mostrar_claves_actuales()
    elif args.regenerate:
        regenerar_claves()
    elif args.generate_only:
        print("\n🔐 CLAVES GENERADAS (copiar manualmente)\n")
        print(f"SECRET_KEY={generar_clave_secreta()}")
        print(f"ENCRYPTION_KEY={generar_clave_encriptacion()}")
        print("\n💡 Copia estas claves a tu archivo .env")
    else:
        # Comportamiento por defecto - modo interactivo
        print("=" * 70)
        print("🔐 GESTOR DE CLAVES DE SEGURIDAD")
        print("Sistema de Articulación SENA")
        print("=" * 70)
        print("\n¿Qué deseas hacer?")
        print("1. Crear .env para desarrollo (con claves generadas)")
        print("2. Crear .env para producción (con claves generadas)")
        print("3. Mostrar claves actuales (ofuscadas)")
        print("4. Regenerar claves de seguridad")
        print("5. Solo generar claves nuevas (mostrar en pantalla)")
        print("0. Salir")
        
        opcion = input("\nSelecciona una opción: ")
        
        if opcion == '1':
            crear_env_desde_ejemplo('development')
        elif opcion == '2':
            crear_env_desde_ejemplo('production')
        elif opcion == '3':
            mostrar_claves_actuales()
        elif opcion == '4':
            regenerar_claves()
        elif opcion == '5':
            print(f"\nSECRET_KEY={generar_clave_secreta()}")
            print(f"ENCRYPTION_KEY={generar_clave_encriptacion()}")
        else:
            print("Saliendo...")

if __name__ == "__main__":
    main()