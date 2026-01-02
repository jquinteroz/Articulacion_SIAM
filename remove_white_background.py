"""
Script para eliminar el fondo blanco del logo SENA
Requiere: pip install pillow
"""
from PIL import Image
import os

def remove_white_background(input_path, output_path, threshold=240):
    """
    Elimina el fondo blanco de una imagen PNG

    Args:
        input_path: Ruta de la imagen de entrada
        output_path: Ruta de la imagen de salida
        threshold: Umbral de blanco (0-255). Pixeles más claros que este valor se vuelven transparentes
    """
    try:
        # Abrir la imagen
        img = Image.open(input_path)

        # Convertir a RGBA si no lo está
        img = img.convert("RGBA")

        # Obtener los datos de la imagen
        datas = img.getdata()

        new_data = []
        for item in datas:
            # Si el pixel es blanco o casi blanco, hacerlo transparente
            if item[0] > threshold and item[1] > threshold and item[2] > threshold:
                new_data.append((255, 255, 255, 0))  # Transparente
            else:
                new_data.append(item)

        # Actualizar los datos de la imagen
        img.putdata(new_data)

        # Guardar con transparencia
        img.save(output_path, "PNG")
        print(f"[OK] Imagen guardada exitosamente en: {output_path}")
        print(f"   Fondo blanco eliminado (threshold: {threshold})")

        return True

    except Exception as e:
        print(f"[ERROR] Error al procesar la imagen: {e}")
        return False

if __name__ == "__main__":
    # Rutas
    input_image = r"app\static\img\sena.png"
    output_image = r"app\static\img\sena_transparent.png"
    backup_image = r"app\static\img\sena_backup.png"

    print("=" * 60)
    print("ELIMINADOR DE FONDO BLANCO - LOGO SENA")
    print("=" * 60)

    # Verificar que existe la imagen
    if not os.path.exists(input_image):
        print(f"[ERROR] No se encontro la imagen: {input_image}")
        exit(1)

    # Crear backup
    print(f"\n[BACKUP] Creando backup en: {backup_image}")
    img = Image.open(input_image)
    img.save(backup_image)
    print("[OK] Backup creado")

    # Procesar imagen
    print(f"\n[PROCESANDO] Procesando imagen...")
    print(f"   Entrada: {input_image}")
    print(f"   Salida: {output_image}")

    success = remove_white_background(input_image, output_image, threshold=240)

    if success:
        print("\n" + "=" * 60)
        print("[OK] PROCESO COMPLETADO")
        print("=" * 60)
        print(f"\nArchivos generados:")
        print(f"  1. {backup_image} (backup original)")
        print(f"  2. {output_image} (sin fondo)")
        print(f"\n[INSTRUCCIONES]:")
        print(f"  1. Revisa {output_image}")
        print(f"  2. Si se ve bien, reemplaza el original:")
        print(f"     - Renombra 'sena.png' a 'sena_old.png'")
        print(f"     - Renombra 'sena_transparent.png' a 'sena.png'")
        print(f"  3. Si no se ve bien, ajusta el threshold en el script")
    else:
        print("\n[ERROR] Error al procesar la imagen")
        print("Revisa el mensaje de error arriba")
