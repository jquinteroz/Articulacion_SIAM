from werkzeug.security import generate_password_hash

# Generar hash para la contraseña Admin123!
password = "Admin123!"
hash_correcto = generate_password_hash(password, method='pbkdf2:sha256')

print("=" * 60)
print("HASH GENERADO PARA LA CONTRASEÑA: Admin123!")
print("=" * 60)
print(hash_correcto)
print("=" * 60)
print("\nCopia este hash y úsalo en tu base de datos.")
print("Ejecuta en MySQL:")
print(f"UPDATE usuarios SET password_hash = '{hash_correcto}' WHERE id > 0;")
