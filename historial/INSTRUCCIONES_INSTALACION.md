# 📋 Instrucciones de Instalación - Sistema de Matrículas SENA

## 🗄️ Instalación de la Base de Datos

### Opción 1: MySQL Workbench (Recomendado)

1. Abre **MySQL Workbench**
2. Conecta a tu servidor MySQL
3. Ve a **File** → **Open SQL Script**
4. Selecciona el archivo: `database/articulacion_completo.sql`
5. Presiona el botón **Execute** (rayo) o presiona `Ctrl + Shift + Enter`
6. Espera a que termine la ejecución (verás mensajes de confirmación al final)

### Opción 2: Línea de Comandos MySQL

```bash
mysql -u root -p < database/articulacion_completo.sql
```

O si prefieres ejecutarlo desde dentro de MySQL:

```bash
mysql -u root -p
```

Luego dentro de MySQL:

```sql
source C:/Users/johan/OneDrive/Documents/Flask/articulacion/database/articulacion_completo.sql
```

### Opción 3: phpMyAdmin

1. Accede a **phpMyAdmin**
2. Ve a la pestaña **Importar**
3. Selecciona el archivo `database/articulacion_completo.sql`
4. Presiona **Continuar**

---

## ⚙️ Configuración del Proyecto

### 1. Crear archivo .env

Crea un archivo llamado `.env` en la raíz del proyecto con el siguiente contenido:

```env
# Flask Configuration
SECRET_KEY=tu_clave_secreta_muy_segura_cambiala_en_produccion
FLASK_ENV=development

# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_password_mysql
DB_NAME=articulacion_sena

# Encryption Key (IMPORTANTE: Esta es la clave generada para los usuarios de prueba)
ENCRYPTION_KEY=cXNkL8qstj6vaRFTfJRqihhA1RBX-gi6PqJBdBWutJs=
```

**⚠️ IMPORTANTE:**
- La `ENCRYPTION_KEY` debe ser exactamente la que aparece arriba para que funcionen las contraseñas de los usuarios de prueba
- En producción, debes generar una nueva clave y regenerar todos los hashes

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

Si tienes problemas con Pillow en Windows:

```bash
pip install -r requirements_sin_pillow.txt
```

### 3. Ejecutar la aplicación

```bash
python run.py
```

La aplicación estará disponible en: **http://localhost:5000**

---

## 🔑 Credenciales de Acceso

### Administrador
- **Usuario:** 1000000000
- **Contraseña:** Admin123!
- **Permisos:** Acceso total al sistema

### Docente Enlace
- **Usuario:** 1000000001
- **Contraseña:** Docente123!
- **Permisos:** Gestión de estudiantes y validación de documentos

### Aprendiz
- **Usuario:** 1000000002
- **Contraseña:** Aprendiz123!
- **Permisos:** Completar perfil y subir documentos de matrícula

---

## 📊 Datos Incluidos en la Base de Datos

El archivo SQL completo incluye:

✅ **5 Programas de formación:**
- Técnico en Sistemas
- Técnico en Contabilidad
- Técnico en Administración
- Técnico en Logística
- Técnico en Mecánica

✅ **3 Colegios de ejemplo:**
- Institución Educativa Técnico Industrial
- Colegio Integrado Comercial
- Instituto Técnico Empresarial

✅ **5 Grupos activos** para el año lectivo 2025

✅ **3 Novedades** para la página principal

✅ **3 Usuarios de prueba** (Admin, Docente, Aprendiz)

---

## 🔒 Seguridad en Producción

**ANTES DE LLEVAR A PRODUCCIÓN:**

1. **Cambiar todas las contraseñas de prueba**
2. **Generar nueva ENCRYPTION_KEY:**
   ```bash
   flask generate-encryption-key
   ```
3. **Generar nuevo SECRET_KEY:**
   ```python
   import secrets
   print(secrets.token_hex(32))
   ```
4. **Actualizar archivo .env** con las nuevas claves
5. **Deshabilitar o eliminar usuarios de prueba** que no necesites
6. **Configurar HTTPS** en el servidor
7. **Configurar respaldos automáticos** de la base de datos

---

## 🐛 Solución de Problemas

### Error: "Can't connect to MySQL server"
- Verifica que MySQL esté ejecutándose
- Confirma las credenciales en el archivo `.env`
- Verifica el puerto (por defecto 3306)

### Error: "Table doesn't exist"
- Asegúrate de haber ejecutado el archivo `articulacion_completo.sql`
- Verifica que la base de datos `articulacion_sena` exista

### Error: "Invalid hash method"
- Verifica que la ENCRYPTION_KEY en `.env` sea exactamente:
  `cXNkL8qstj6vaRFTfJRqihhA1RBX-gi6PqJBdBWutJs=`

### Error al subir archivos
- Verifica que exista la carpeta `uploads/` en la raíz del proyecto
- Verifica permisos de escritura en la carpeta

---

## 📁 Estructura del Proyecto

```
articulacion/
├── app/
│   ├── blueprints/        # Módulos de la aplicación
│   ├── models/            # Modelos de base de datos
│   ├── services/          # Lógica de negocio
│   ├── static/            # CSS, JS, imágenes
│   ├── templates/         # Plantillas HTML
│   └── utils/             # Utilidades
├── database/
│   └── articulacion_completo.sql  # ⭐ Archivo SQL completo
├── uploads/               # Documentos subidos (crear si no existe)
├── .env                   # Configuración (crear manualmente)
├── config.py              # Configuraciones de Flask
├── requirements.txt       # Dependencias Python
└── run.py                 # Punto de entrada
```

---

## 📞 Soporte

Si encuentras algún problema:

1. Verifica que todas las dependencias estén instaladas
2. Confirma que el archivo `.env` esté correctamente configurado
3. Revisa los logs de la aplicación para más detalles
4. Verifica que MySQL esté ejecutándose y accesible

---

**¡Listo! Tu sistema de matrículas está instalado y funcionando.** 🎉
