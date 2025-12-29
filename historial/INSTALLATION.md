# Guía de Instalación Detallada
## Sistema de Matrículas - Articulación SENA

Esta guía proporciona instrucciones paso a paso para la instalación y configuración del sistema.

## Tabla de Contenidos
1. [Requisitos Previos](#requisitos-previos)
2. [Instalación en Windows](#instalación-en-windows)
3. [Instalación en Linux](#instalación-en-linux)
4. [Configuración de la Base de Datos](#configuración-de-la-base-de-datos)
5. [Configuración de la Aplicación](#configuración-de-la-aplicación)
6. [Verificación de la Instalación](#verificación-de-la-instalación)
7. [Despliegue en Producción](#despliegue-en-producción)

---

## Requisitos Previos

### Software Requerido

1. **Python 3.8 o superior**
   - Descargar desde: https://www.python.org/downloads/
   - Verificar instalación: `python --version`

2. **MySQL 8.0 o superior**
   - Descargar desde: https://dev.mysql.com/downloads/installer/
   - Verificar instalación: `mysql --version`

3. **Git** (opcional, para control de versiones)
   - Descargar desde: https://git-scm.com/downloads

### Conocimientos Requeridos
- Línea de comandos básica
- Configuración de MySQL
- Conceptos básicos de Python y Flask

---

## Instalación en Windows

### Paso 1: Instalar Python

1. Descargar Python desde python.org
2. **IMPORTANTE**: Marcar "Add Python to PATH" durante la instalación
3. Verificar instalación:
```cmd
python --version
pip --version
```

### Paso 2: Instalar MySQL

1. Descargar MySQL Installer
2. Seleccionar "Developer Default"
3. Durante la configuración:
   - Root password: Elegir una contraseña segura y **anotarla**
   - Puerto: 3306 (predeterminado)
   - Windows Service: Dejar habilitado

4. Verificar instalación:
```cmd
mysql --version
```

### Paso 3: Preparar el Proyecto

1. Abrir CMD o PowerShell
2. Navegar a la carpeta del proyecto:
```cmd
cd C:\Users\johan\OneDrive\Documents\Flask\articulacion
```

3. Crear entorno virtual:
```cmd
python -m venv venv
```

4. Activar entorno virtual:
```cmd
venv\Scripts\activate
```

Tu prompt debe cambiar a mostrar `(venv)` al inicio.

### Paso 4: Instalar Dependencias

```cmd
pip install -r requirements.txt
```

**Nota**: Este proceso puede tomar varios minutos.

### Paso 5: Configurar Variables de Entorno

1. Copiar el archivo de ejemplo:
```cmd
copy .env.example .env
```

2. Abrir `.env` con un editor de texto (Notepad++, VS Code, etc.)

3. Editar las siguientes líneas:
```env
SECRET_KEY=genera_una_clave_aleatoria_segura_aqui_min_32_caracteres
DB_PASSWORD=tu_password_de_mysql_aqui
```

### Paso 6: Generar Clave de Encriptación

```cmd
flask generate-encryption-key
```

Copiar la salida y agregarla al archivo `.env`:
```env
ENCRYPTION_KEY=clave_generada_aqui
```

### Paso 7: Crear Base de Datos

1. Abrir MySQL:
```cmd
mysql -u root -p
```

2. Ingresar la contraseña de root

3. Ejecutar:
```sql
CREATE DATABASE articulacion_sena CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

4. Cargar el esquema:
```cmd
mysql -u root -p articulacion_sena < database\schema.sql
```

5. Cargar datos iniciales:
```cmd
mysql -u root -p articulacion_sena < database\seed_data.sql
```

### Paso 8: Crear Usuario Administrador

```cmd
flask create-admin
```

**Importante**: Guardar las credenciales mostradas:
- Usuario: 1000000000
- Contraseña: Admin123!

### Paso 9: Ejecutar la Aplicación

```cmd
python run.py
```

La aplicación estará disponible en: http://localhost:5000

---

## Instalación en Linux

### Paso 1: Actualizar el Sistema

```bash
sudo apt update
sudo apt upgrade -y
```

### Paso 2: Instalar Dependencias del Sistema

```bash
# Python y herramientas
sudo apt install python3 python3-pip python3-venv -y

# MySQL
sudo apt install mysql-server -y

# Librerías de desarrollo
sudo apt install python3-dev default-libmysqlclient-dev build-essential -y
```

### Paso 3: Configurar MySQL

```bash
# Ejecutar script de seguridad
sudo mysql_secure_installation

# Configurar contraseña de root si es necesario
sudo mysql
```

```sql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'tu_password';
FLUSH PRIVILEGES;
EXIT;
```

### Paso 4: Preparar el Proyecto

```bash
cd /home/usuario/articulacion

# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### Paso 5: Configurar Variables de Entorno

```bash
cp .env.example .env
nano .env  # o usar vim/vi
```

Editar los valores necesarios.

### Paso 6: Configurar Base de Datos

```bash
# Crear base de datos
mysql -u root -p <<EOF
CREATE DATABASE articulacion_sena CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EOF

# Cargar esquema
mysql -u root -p articulacion_sena < database/schema.sql

# Cargar datos iniciales
mysql -u root -p articulacion_sena < database/seed_data.sql
```

### Paso 7: Configurar Permisos

```bash
# Crear carpetas necesarias
mkdir -p uploads reports

# Establecer permisos
chmod 755 uploads reports
```

### Paso 8: Ejecutar la Aplicación

```bash
# Desarrollo
python run.py

# Producción con Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

---

## Configuración de la Base de Datos

### Verificar Conexión

```python
# test_db.py
from app import create_app
from app.models import db, Usuario

app = create_app()
with app.app_context():
    try:
        usuarios = Usuario.query.all()
        print(f"Conexión exitosa. Usuarios encontrados: {len(usuarios)}")
    except Exception as e:
        print(f"Error de conexión: {e}")
```

```bash
python test_db.py
```

### Problemas Comunes

**Error: Access denied for user 'root'@'localhost'**
```bash
# Reiniciar MySQL
sudo service mysql restart

# Verificar credenciales
mysql -u root -p
```

**Error: Can't connect to MySQL server**
```bash
# Verificar que MySQL esté corriendo
sudo service mysql status

# Iniciar si está detenido
sudo service mysql start
```

---

## Configuración de la Aplicación

### Variables de Entorno (.env)

```env
# Aplicación
FLASK_APP=run.py
FLASK_ENV=development  # Cambiar a 'production' en producción
SECRET_KEY=clave_muy_segura_de_al_menos_32_caracteres_aleatorios

# Base de Datos
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_password_mysql
DB_NAME=articulacion_sena

# Archivos
UPLOAD_FOLDER=uploads
MAX_FILE_SIZE=5242880  # 5MB en bytes
ALLOWED_EXTENSIONS=pdf,jpg,jpeg,png

# Encriptación (generar con: flask generate-encryption-key)
ENCRYPTION_KEY=tu_clave_de_encriptacion_en_base64
```

### Configuración de Producción

En `config.py`, la clase `ProductionConfig` incluye:
- `DEBUG = False`
- `SESSION_COOKIE_SECURE = True` (requiere HTTPS)
- Logging mejorado

---

## Verificación de la Instalación

### Checklist de Verificación

- [ ] Python 3.8+ instalado
- [ ] MySQL 8.0+ corriendo
- [ ] Entorno virtual activado
- [ ] Dependencias instaladas sin errores
- [ ] Archivo `.env` configurado
- [ ] Base de datos creada y poblada
- [ ] Administrador creado
- [ ] Aplicación ejecutándose sin errores
- [ ] Login funcional con admin
- [ ] Carpetas `uploads/` y `reports/` creadas

### Pruebas Básicas

1. **Acceder a la aplicación**: http://localhost:5000
2. **Iniciar sesión con admin**:
   - Usuario: 1000000000
   - Contraseña: Admin123!
3. **Crear un usuario de prueba** en el panel de administración
4. **Registrar un aprendiz** desde la página pública
5. **Subir un documento** como aprendiz

---

## Despliegue en Producción

### Usando Gunicorn (Linux)

```bash
# Instalar Gunicorn
pip install gunicorn

# Ejecutar con 4 workers
gunicorn -w 4 -b 0.0.0.0:5000 run:app

# Con systemd (servicio)
sudo nano /etc/systemd/system/articulacion.service
```

```ini
[Unit]
Description=Sistema de Matrículas SENA
After=network.target

[Service]
User=www-data
WorkingDirectory=/ruta/al/proyecto
Environment="PATH=/ruta/al/proyecto/venv/bin"
ExecStart=/ruta/al/proyecto/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 run:app

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl start articulacion
sudo systemctl enable articulacion
```

### Usando Nginx (Reverse Proxy)

```nginx
server {
    listen 80;
    server_name tu_dominio.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        alias /ruta/al/proyecto/app/static;
    }

    location /uploads {
        alias /ruta/al/proyecto/uploads;
    }
}
```

### Configurar HTTPS con Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d tu_dominio.com
```

---

## Mantenimiento

### Respaldos Automáticos

```bash
# Crear script de respaldo
nano backup.sh
```

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"

# Respaldar base de datos
mysqldump -u root -p articulacion_sena > $BACKUP_DIR/db_$DATE.sql

# Respaldar archivos
tar -czf $BACKUP_DIR/uploads_$DATE.tar.gz uploads/

# Eliminar respaldos antiguos (más de 30 días)
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
```

```bash
chmod +x backup.sh

# Agregar a crontab (todos los días a las 2 AM)
crontab -e
0 2 * * * /ruta/al/backup.sh
```

### Actualización del Sistema

```bash
# Respaldar primero
./backup.sh

# Actualizar código
git pull origin main

# Activar entorno
source venv/bin/activate

# Actualizar dependencias
pip install -r requirements.txt

# Reiniciar servicio
sudo systemctl restart articulacion
```

---

## Solución de Problemas

### La aplicación no inicia

```bash
# Verificar logs
tail -f /var/log/articulacion/error.log

# Verificar permisos
ls -la uploads/ reports/
```

### Error 500 en producción

```python
# Habilitar debug temporalmente (solo para diagnosticar)
# En config.py
DEBUG = True
```

### Base de datos no responde

```bash
sudo service mysql status
sudo service mysql restart
```

---

## Soporte

Para asistencia técnica:
- Revisar logs en `/var/log/`
- Consultar documentación de Flask: https://flask.palletsprojects.com/
- Consultar documentación de SQLAlchemy: https://docs.sqlalchemy.org/

---

**Fin de la Guía de Instalación**
