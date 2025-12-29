# GUÍA DE DEPLOY EN PYTHONANYWHERE
## Sistema de Articulación SENA v1.0.0
## Fecha: 2025-12-18

---

## 📋 ÍNDICE

1. [Requisitos Previos](#requisitos-previos)
2. [Crear Cuenta en PythonAnywhere](#crear-cuenta)
3. [Configurar Base de Datos MySQL](#configurar-base-de-datos)
4. [Subir el Proyecto](#subir-proyecto)
5. [Configurar Aplicación Web](#configurar-aplicacion)
6. [Configurar Variables de Entorno](#variables-entorno)
7. [Inicializar Base de Datos](#inicializar-bd)
8. [Configurar WSGI](#configurar-wsgi)
9. [Verificación y Pruebas](#verificacion)
10. [Configuración de Dominio Personalizado](#dominio-personalizado)
11. [Mantenimiento](#mantenimiento)
12. [Troubleshooting](#troubleshooting)

---

## 🎯 REQUISITOS PREVIOS {#requisitos-previos}

### Cuenta de PythonAnywhere
- **Plan recomendado**: Hacker ($5/mes) o superior
- **Incluye**:
  - MySQL database
  - HTTPS automático
  - Dominio personalizado (en planes pagos)
  - SSH access

### Archivos del Proyecto
- ✅ Base de datos limpia (ya realizado)
- ✅ Usuario admin creado (ya realizado)
- ✅ Código listo para producción (ya realizado)

### Credenciales Admin del Sistema
```
Documento:  1000000000
Contraseña: 7u4DhMu3WcYmD5_c3eJRYg
```

---

## 🚀 PASO 1: CREAR CUENTA EN PYTHONANYWHERE {#crear-cuenta}

### 1.1 Registro
1. Ve a [https://www.pythonanywhere.com](https://www.pythonanywhere.com)
2. Click en **"Pricing & signup"**
3. Elige el plan **Hacker** ($5/mes) o superior
4. Completa el registro con tu email
5. Verifica tu email

### 1.2 Primer Login
1. Accede a tu dashboard: `https://www.pythonanywhere.com/user/TU_USUARIO/`
2. Familiarízate con el panel

---

## 💾 PASO 2: CONFIGURAR BASE DE DATOS MYSQL {#configurar-base-de-datos}

### 2.1 Crear Base de Datos

1. En el dashboard, ve a la pestaña **"Databases"**
2. En la sección **"MySQL"**, ingresa una contraseña para MySQL
3. Click en **"Initialize MySQL"**
4. Anota tu contraseña, la necesitarás después

### 2.2 Crear Base de Datos del Proyecto

En la sección **"Create database"**:
```
Database name: TU_USUARIO$articulacion_sena
```

Click en **"Create"**

### 2.3 Información de Conexión

Toma nota de:
```
Host:     TU_USUARIO.mysql.pythonanywhere-services.com
Usuario:  TU_USUARIO
Password: [la que creaste en el paso 2.1]
Database: TU_USUARIO$articulacion_sena
Port:     3306
```

---

## 📤 PASO 3: SUBIR EL PROYECTO {#subir-proyecto}

Tienes 3 opciones para subir tu proyecto:

### OPCIÓN A: Git (Recomendada)

#### 3.1 Preparar Repositorio Local

```bash
# En tu máquina local
cd c:\Users\johan\OneDrive\Documents\Flask\articulacion

# Inicializar git si no lo has hecho
git init

# Agregar archivos
git add .

# Commit
git commit -m "Versión 1.0.0 lista para producción"
```

#### 3.2 Subir a GitHub

```bash
# Crear repositorio en GitHub: https://github.com/new
# Nombre sugerido: articulacion-sena

# Agregar remote
git remote add origin https://github.com/TU_USUARIO/articulacion-sena.git

# Push
git branch -M main
git push -u origin main
```

#### 3.3 Clonar en PythonAnywhere

1. En PythonAnywhere, abre una consola **Bash**
2. Ejecuta:

```bash
cd ~
git clone https://github.com/TU_USUARIO/articulacion-sena.git articulacion
cd articulacion
```

### OPCIÓN B: Upload Manual (Alternativa)

1. En PythonAnywhere, ve a **"Files"**
2. Click en **"Upload a file"**
3. Sube el ZIP de tu proyecto
4. En la consola Bash:

```bash
cd ~
unzip articulacion.zip -d articulacion
cd articulacion
```

### OPCIÓN C: Via SCP (Avanzada)

```bash
# Desde tu máquina local
scp -r c:\Users\johan\OneDrive\Documents\Flask\articulacion TU_USUARIO@ssh.pythonanywhere.com:~/
```

---

## 🔧 PASO 4: CONFIGURAR APLICACIÓN WEB {#configurar-aplicacion}

### 4.1 Crear Entorno Virtual

En la consola Bash de PythonAnywhere:

```bash
cd ~/articulacion

# Crear virtualenv con Python 3.10
mkvirtualenv --python=/usr/bin/python3.10 articulacion-venv

# Activar (se activa automáticamente al crearlo)
workon articulacion-venv

# Actualizar pip
pip install --upgrade pip
```

### 4.2 Instalar Dependencias

```bash
# Asegúrate de estar en el virtualenv
workon articulacion-venv

# Instalar requirements
pip install -r requirements.txt

# Verificar instalación
pip list
```

### 4.3 Crear Web App

1. Ve a la pestaña **"Web"** en el dashboard
2. Click en **"Add a new web app"**
3. Click **"Next"**
4. Selecciona **"Manual configuration"**
5. Selecciona **"Python 3.10"**
6. Click **"Next"**

---

## ⚙️ PASO 5: CONFIGURAR VARIABLES DE ENTORNO {#variables-entorno}

### 5.1 Generar Claves Seguras

En la consola Bash de PythonAnywhere:

```bash
workon articulacion-venv
cd ~/articulacion

# Generar SECRET_KEY
python3 -c "import secrets; print(secrets.token_hex(32))"
# Copia el resultado

# Generar ENCRYPTION_KEY
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
# Copia el resultado
```

### 5.2 Crear Archivo .env

```bash
cd ~/articulacion
nano .env
```

**Contenido del archivo** (reemplaza los valores con los tuyos):

```env
# Flask
FLASK_APP=run.py
FLASK_ENV=production
DEBUG=False

# Seguridad
SECRET_KEY=tu_secret_key_generada_aqui

# Base de datos MySQL
DB_HOST=TU_USUARIO.mysql.pythonanywhere-services.com
DB_PORT=3306
DB_USER=TU_USUARIO
DB_PASSWORD=tu_password_mysql
DB_NAME=TU_USUARIO$articulacion_sena

# Archivos
UPLOAD_FOLDER=uploads
MAX_FILE_SIZE=5242880
ALLOWED_EXTENSIONS=pdf,jpg,jpeg,png

# Encriptación
ENCRYPTION_KEY=tu_encryption_key_generada_aqui
```

**Guardar**: `Ctrl+O`, `Enter`, `Ctrl+X`

### 5.3 Crear Directorios Necesarios

```bash
cd ~/articulacion
mkdir -p uploads temp logs
chmod 755 uploads temp
```

---

## 🗄️ PASO 6: INICIALIZAR BASE DE DATOS {#inicializar-bd}

### 6.1 Importar Estructura

Tienes dos opciones:

#### Opción A: Usar script de inicialización

```bash
workon articulacion-venv
cd ~/articulacion

# Ejecutar script de producción
python init_production.py
```

**IMPORTANTE**: El script creará un nuevo admin. Si quieres mantener las credenciales actuales, usa la Opción B.

#### Opción B: Importar desde tu BD local

En tu máquina local:

```bash
# Exportar BD local
mysqldump -u root -p articulacion_cgmlti > articulacion_backup.sql
```

Sube el archivo a PythonAnywhere (Files > Upload)

En PythonAnywhere:

```bash
cd ~/articulacion

# Importar
mysql -u TU_USUARIO -h TU_USUARIO.mysql.pythonanywhere-services.com -p 'TU_USUARIO$articulacion_sena' < articulacion_backup.sql
```

### 6.2 Verificar Datos

```bash
# Conectar a MySQL
mysql -u TU_USUARIO -h TU_USUARIO.mysql.pythonanywhere-services.com -p

# Dentro de MySQL
USE TU_USUARIO$articulacion_sena;
SHOW TABLES;
SELECT COUNT(*) FROM usuarios;
EXIT;
```

Deberías ver 1 usuario (el admin).

---

## 🌐 PASO 7: CONFIGURAR WSGI {#configurar-wsgi}

### 7.1 Editar archivo WSGI

1. En el dashboard, ve a **"Web"**
2. En la sección **"Code"**, click en el link del archivo WSGI
   - Ejemplo: `/var/www/tu_usuario_pythonanywhere_com_wsgi.py`

### 7.2 Reemplazar Contenido

**Elimina todo** el contenido y reemplázalo con:

```python
# -*- coding: utf-8 -*-
"""
WSGI Configuration para Sistema de Articulación SENA
PythonAnywhere Deployment

Desarrollado por: Johann Quintero (jsquinteroz)
"""

import sys
import os
from dotenv import load_dotenv

# Ruta del proyecto
project_home = '/home/TU_USUARIO/articulacion'  # ⚠️ CAMBIAR TU_USUARIO

# Agregar al path
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Cargar variables de entorno
load_dotenv(os.path.join(project_home, '.env'))

# Configurar encoding para Windows (si aplica)
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Importar la aplicación
from app import create_app

# Crear aplicación
application = create_app('production')

# Para debugging (remover en producción)
# print("WSGI loaded successfully!", file=sys.stderr)
```

**⚠️ IMPORTANTE**: Reemplaza `TU_USUARIO` con tu usuario de PythonAnywhere.

**Guardar**: Click en el botón **"Save"** o `Ctrl+S`

### 7.3 Configurar Virtualenv

1. En la pestaña **"Web"**, ve a la sección **"Virtualenv"**
2. En **"Enter path to a virtualenv"**, ingresa:
   ```
   /home/TU_USUARIO/.virtualenvs/articulacion-venv
   ```
3. Click en el checkmark azul

### 7.4 Configurar Archivos Estáticos

En la sección **"Static files"**:

| URL           | Directory                                    |
|---------------|----------------------------------------------|
| /static/      | /home/TU_USUARIO/articulacion/app/static    |
| /uploads/     | /home/TU_USUARIO/articulacion/uploads       |

Click en **"Add a new static file mapping"** para cada una.

---

## ✅ PASO 8: RECARGAR Y VERIFICAR {#verificacion}

### 8.1 Recargar Aplicación

1. En la pestaña **"Web"**, scroll hasta arriba
2. Click en el botón verde grande: **"Reload TU_USUARIO.pythonanywhere.com"**
3. Espera unos segundos

### 8.2 Acceder a la Aplicación

1. Click en el link: `https://TU_USUARIO.pythonanywhere.com`
2. Deberías ver la página de inicio del sistema

### 8.3 Probar Login de Administrador

```
URL:        https://TU_USUARIO.pythonanywhere.com/login
Documento:  1000000000
Contraseña: 7u4DhMu3WcYmD5_c3eJRYg
```

### 8.4 Verificar Funcionalidades

- ✅ Login funciona
- ✅ Dashboard admin se carga
- ✅ SENA logo aparece
- ✅ Puede crear colegio
- ✅ Puede crear programa
- ✅ Puede crear grupo

---

## 🌍 PASO 9: DOMINIO PERSONALIZADO (Opcional) {#dominio-personalizado}

### Solo en planes pagos (Hacker o superior)

1. Ve a **"Web"** > **"Custom domain"**
2. Agrega tu dominio: `articulacion.tudominio.com`
3. En tu proveedor de DNS, agrega:
   ```
   CNAME articulacion TU_USUARIO.pythonanywhere.com
   ```
4. Espera propagación DNS (hasta 24 horas)
5. Recarga la app

---

## 🔧 PASO 10: POST-DEPLOYMENT {#post-deployment}

### 10.1 Cambiar Contraseña Admin

1. Login como admin
2. Ve a tu perfil
3. Cambia la contraseña temporal

### 10.2 Eliminar Archivo de Credenciales

```bash
cd ~/articulacion
rm .admin_credentials
```

### 10.3 Crear Usuario de Prueba

Crea un colegio, programa y grupo de prueba para verificar el flujo completo.

### 10.4 Configurar Backups

```bash
# Crear script de backup
nano ~/backup_db.sh
```

Contenido:

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR=~/backups
mkdir -p $BACKUP_DIR

mysqldump -u TU_USUARIO -h TU_USUARIO.mysql.pythonanywhere-services.com -p'TU_PASSWORD' 'TU_USUARIO$articulacion_sena' > $BACKUP_DIR/backup_$DATE.sql

# Comprimir
gzip $BACKUP_DIR/backup_$DATE.sql

# Eliminar backups de más de 30 días
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete
```

```bash
chmod +x ~/backup_db.sh
```

Programa con cron:

```bash
# Editar crontab (solo en planes pagos)
crontab -e

# Agregar (ejecutar diariamente a las 2 AM)
0 2 * * * ~/backup_db.sh
```

---

## 🔄 MANTENIMIENTO {#mantenimiento}

### Actualizar Código

```bash
workon articulacion-venv
cd ~/articulacion

# Si usas Git
git pull origin main

# Reinstalar dependencias si cambiaron
pip install -r requirements.txt

# Recargar app
# Ve a Web > Reload
```

### Ver Logs de Errores

1. Ve a **"Web"** > **"Log files"**
2. Click en **"Error log"**
3. O en consola:

```bash
tail -f /var/log/TU_USUARIO.pythonanywhere.com.error.log
```

### Ver Logs del Sistema

```bash
cd ~/articulacion/logs
tail -f gunicorn_error.log
```

---

## 🆘 TROUBLESHOOTING {#troubleshooting}

### Error 500 - Internal Server Error

**Causa**: Error en el código o configuración

**Solución**:
```bash
# Ver error log
tail -50 /var/log/TU_USUARIO.pythonanywhere.com.error.log
```

Errores comunes:
- Ruta incorrecta en WSGI
- .env no encontrado
- Falta alguna dependencia

### Error de Conexión a Base de Datos

**Síntomas**: `Can't connect to MySQL server`

**Solución**:
1. Verificar host en .env:
   ```
   DB_HOST=TU_USUARIO.mysql.pythonanywhere-services.com
   ```
2. Verificar que la BD existe en **"Databases"**
3. Verificar password de MySQL

### Archivos Estáticos no Cargan

**Síntomas**: CSS/JS no aparece

**Solución**:
1. Verificar mappings en **"Web"** > **"Static files"**
2. Verificar rutas:
   ```
   /static/ → /home/TU_USUARIO/articulacion/app/static
   ```
3. Recargar app

### ImportError o ModuleNotFoundError

**Síntomas**: `ModuleNotFoundError: No module named 'flask'`

**Solución**:
```bash
workon articulacion-venv
pip install -r requirements.txt

# Verificar que virtualenv está configurado en Web
```

### Cambios no se Reflejan

**Solución**:
1. Ve a **"Web"**
2. Click en **"Reload"**
3. Limpia caché del navegador (`Ctrl+F5`)

### Error con Uploads

**Síntomas**: Documentos no se suben

**Solución**:
```bash
cd ~/articulacion
chmod 755 uploads
ls -la uploads  # Verificar permisos
```

---

## 📊 MONITOREO

### Dashboard de PythonAnywhere

Revisa regularmente:
- **Web**: Estado de la app
- **Databases**: Uso de disco
- **Files**: Espacio disponible
- **Consoles**: Sesiones activas

### Límites del Plan Hacker

- CPU time: 1000 segundos/día
- Disk space: 512 MB
- Consoles: 2 simultáneas
- MySQL: 1 database

Si necesitas más, considera actualizar a plan superior.

---

## ✅ CHECKLIST FINAL

- [ ] Cuenta de PythonAnywhere creada
- [ ] Base de datos MySQL configurada
- [ ] Proyecto subido a PythonAnywhere
- [ ] Virtualenv creado e instalado
- [ ] Archivo .env configurado con valores de producción
- [ ] Base de datos inicializada con admin
- [ ] WSGI configurado correctamente
- [ ] Archivos estáticos mapeados
- [ ] Aplicación recargada
- [ ] Login de admin funciona
- [ ] Contraseña de admin cambiada
- [ ] Archivo .admin_credentials eliminado
- [ ] SENA logo visible en todas las páginas
- [ ] Funcionalidades básicas probadas
- [ ] Backups configurados (opcional)

---

## 🎉 ¡LISTO PARA PRODUCCIÓN!

Tu Sistema de Articulación SENA está ahora desplegado en PythonAnywhere.

**URL de acceso**: `https://TU_USUARIO.pythonanywhere.com`

**Credenciales admin**:
```
Documento:  1000000000
Contraseña: [La que cambiaste después del primer login]
```

---

## 📞 SOPORTE

### PythonAnywhere
- Documentación: https://help.pythonanywhere.com/
- Forum: https://www.pythonanywhere.com/forums/
- Email: support@pythonanywhere.com

### Sistema de Articulación
- Documentación: Ver README.md y DEPLOY_PRODUCCION.md
- Desarrollador: Johann Quintero (jsquinteroz)

---

**Sistema de Articulación SENA v1.0.0**
**Desplegado en PythonAnywhere**
**Fecha: 2025-12-18**

Desarrollado por: Johann Quintero (jsquinteroz)
Copyright © 2025 - Todos los derechos reservados
