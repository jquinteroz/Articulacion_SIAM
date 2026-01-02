"""
Script para actualizar las contraseñas de los usuarios de prueba a Sena123$
"""
from werkzeug.security import generate_password_hash

# Nueva contraseña
nueva_password = "Sena123$"

# Generar hash
password_hash = generate_password_hash(nueva_password)

print("=" * 80)
print("ACTUALIZACIÓN DE CONTRASEÑAS - BASE DE DATOS")
print("=" * 80)
print(f"\nNueva contraseña: {nueva_password}")
print(f"\nHash generado:\n{password_hash}")
print("\n" + "=" * 80)
print("INSTRUCCIONES:")
print("=" * 80)
print("\n1. Copia el siguiente comando SQL y ejecútalo en MySQL/phpMyAdmin:")
print("\n" + "-" * 80)
print(f"""
UPDATE usuarios
SET password_hash = '{password_hash}'
WHERE documento IN ('1000000001', '1000000002', '1000000003', '1000000004', '1000000005');
""")
print("-" * 80)
print("\n2. Verifica que se actualizaron los 5 usuarios:")
print("\nSELECT documento, CONCAT(nombres, ' ', apellidos) as nombre, rol FROM usuarios;")
print("\n" + "=" * 80)
print("CREDENCIALES DE ACCESO:")
print("=" * 80)
print("\nTodos los usuarios tienen la misma contraseña: Sena123$")
print("\nDocumentos disponibles:")
print("  - 1000000001 (Administrador)")
print("  - 1000000002 (Rector)")
print("  - 1000000003 (Docente)")
print("  - 1000000004 (Aprendiz 1)")
print("  - 1000000005 (Aprendiz 2)")
print("\n" + "=" * 80)
