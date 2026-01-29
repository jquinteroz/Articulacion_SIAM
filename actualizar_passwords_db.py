"""
Script para actualizar las contraseñas directamente en la base de datos MySQL
"""
import mysql.connector
from werkzeug.security import generate_password_hash
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv('.env.production')

# Configuración de la base de datos
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

# Nueva contraseña
NUEVA_PASSWORD = "Sena123$"

# Documentos de los usuarios de prueba
DOCUMENTOS = ['1000000001', '1000000002', '1000000003', '1000000004', '1000000005']

def actualizar_passwords():
    """Actualiza las contraseñas de los usuarios de prueba"""

    print("=" * 80)
    print("ACTUALIZACIÓN AUTOMÁTICA DE CONTRASEÑAS")
    print("=" * 80)

    try:
        # Generar hash de la contraseña
        password_hash = generate_password_hash(NUEVA_PASSWORD)
        print(f"\n[OK] Hash generado para contrasena: {NUEVA_PASSWORD}")
        print(f"  Hash: {password_hash[:50]}...")

        # Conectar a la base de datos
        print(f"\n[CONECTANDO] a: {DB_CONFIG['host']}/{DB_CONFIG['database']}...")
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print("[OK] Conexion exitosa")

        # Verificar usuarios antes de actualizar
        print("\n[VERIFICANDO] Usuarios a actualizar:")
        placeholders = ','.join(['%s'] * len(DOCUMENTOS))
        query_verificar = f"SELECT documento, nombres, apellidos, rol FROM usuarios WHERE documento IN ({placeholders})"
        cursor.execute(query_verificar, DOCUMENTOS)
        usuarios = cursor.fetchall()

        if not usuarios:
            print("[ERROR] No se encontraron usuarios con esos documentos")
            return False

        for usuario in usuarios:
            print(f"  - {usuario[0]}: {usuario[1]} {usuario[2]} ({usuario[3]})")

        # Actualizar contraseñas
        print(f"\n[ACTUALIZANDO] contraseñas...")
        query_update = f"UPDATE usuarios SET password_hash = %s WHERE documento IN ({placeholders})"
        cursor.execute(query_update, [password_hash] + DOCUMENTOS)
        conn.commit()

        print(f"[OK] {cursor.rowcount} usuarios actualizados correctamente")

        # Verificar actualización
        print("\n[VERIFICANDO] actualizacion...")
        cursor.execute(query_verificar, DOCUMENTOS)
        usuarios_verificados = cursor.fetchall()

        print("\n[RESULTADO] Usuarios actualizados:")
        for usuario in usuarios_verificados:
            print(f"  [OK] {usuario[0]}: {usuario[1]} {usuario[2]} ({usuario[3]})")

        # Cerrar conexión
        cursor.close()
        conn.close()

        print("\n" + "=" * 80)
        print("[EXITO] ACTUALIZACION COMPLETADA EXITOSAMENTE")
        print("=" * 80)
        print("\n[CREDENCIALES] Contraseña para todos: " + NUEVA_PASSWORD)
        print("\n   Documentos disponibles:")
        print("   - 1000000001 (Administrador)")
        print("   - 1000000002 (Rector)")
        print("   - 1000000003 (Docente)")
        print("   - 1000000004 (Aprendiz 1)")
        print("   - 1000000005 (Aprendiz 2)")
        print("\n" + "=" * 80)

        return True

    except mysql.connector.Error as err:
        print(f"\n[ERROR] MySQL: {err}")
        return False
    except Exception as e:
        print(f"\n[ERROR] {e}")
        return False

if __name__ == "__main__":
    actualizar_passwords()
