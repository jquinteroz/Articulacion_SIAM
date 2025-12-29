# GUÍA DE DEPLOY A PRODUCCIÓN
## Sistema de Articulación SENA
## Versión: 1.0.0
## Fecha: 2025-12-18

---

## ⚠️ IMPORTANTE - LEER ANTES DE CONTINUAR

La base de datos ha sido **limpiada y reinicializada** para producción:
- ✅ Todos los datos de prueba eliminados
- ✅ Estructura de base de datos verificada
- ✅ Usuario administrador inicial creado
- ✅ Archivos temporales limpiados

**NO ejecutar `init_production.py` nuevamente** a menos que quieras reiniciar todo.

---

## 🔐 CREDENCIALES DEL ADMINISTRADOR

```
Documento:  1000000000
Contraseña: [Ver archivo .admin_credentials]
```

**ACCIÓN INMEDIATA REQUERIDA**:
1. Guarda estas credenciales en un gestor de contraseñas seguro
2. Elimina el archivo `.admin_credentials` del servidor
3. En el primer login, cambia la contraseña del administrador

---

## 📋 CHECKLIST PRE-DEPLOY

### Configuración Local Completada
- [✅] Base de datos limpiada e inicializada
- [✅] Usuario administrador creado
- [✅] Archivos de prueba eliminados
- [✅] .gitignore configurado
- [✅] Archivo .env.production creado

### Pendiente (Hacer ANTES de subir a producción)
- [ ] Generar nueva SECRET_KEY para producción
- [ ] Generar nueva ENCRYPTION_KEY para producción
- [ ] Revisar y actualizar .env.production con valores reales
- [ ] Crear usuario de base de datos no-root
- [ ] Configurar backup automático de base de datos
- [ ] Probar sistema localmente con las nuevas credenciales

---

## 🚀 PASOS PARA DEPLOY

### PASO 1: Preparar Servidor

#### 1.1 Requisitos del Servidor
```
Sistema Operativo: Ubuntu 20.04+ / CentOS 8+ / Debian 11+
RAM: Mínimo 2GB, recomendado 4GB
Disco: Mínimo 20GB
Python: 3.8+
MySQL: 5.7+ o 8.0+
```

#### 1.2 Instalar Dependencias del Sistema
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3-pip python3-venv nginx mysql-server git

# CentOS/RHEL
sudo yum install python3 python3-pip nginx mysql-server git
```

#### 1.3 Instalar Microsoft Word (para conversión PDF)
```bash
# Nota: docx2pdf requiere MS Word o LibreOffice
# Alternativa: Instalar LibreOffice
sudo apt install libreoffice

# O configurar conversión en servidor sin Office
# (requiere modificar convert_docx_to_pdf para usar alternativa)
```

---

### PASO 2: Configurar Base de Datos

#### 2.1 Crear Usuario de Base de Datos
```sql
-- Conectar a MySQL como root
mysql -u root -p

-- Crear usuario para la aplicación
CREATE USER 'articulacion_user'@'localhost' IDENTIFIED BY 'CONTRASEÑA_SEGURA_AQUI';

-- Otorgar permisos
GRANT ALL PRIVILEGES ON articulacion_sena.* TO 'articulacion_user'@'localhost';
FLUSH PRIVILEGES;

-- Salir
EXIT;
```

#### 2.2 Importar Base de Datos
```bash
# Si ya tienes la base de datos local inicializada:
mysqldump -u root articulacion_sena > articulacion_sena_backup.sql

# En el servidor:
mysql -u root -p articulacion_sena < articulacion_sena_backup.sql
```

#### 2.3 Configurar Backup Automático
```bash
# Crear script de backup
sudo nano /usr/local/bin/backup_articulacion.sh
```

Contenido del script:
```bash
#!/bin/bash
BACKUP_DIR="/var/backups/articulacion"
DATE=$(date +%Y%m%d_%H%M%S)
FILENAME="articulacion_sena_$DATE.sql"

mkdir -p $BACKUP_DIR
mysqldump -u articulacion_user -pCONTRASEÑA articulacion_sena > $BACKUP_DIR/$FILENAME
gzip $BACKUP_DIR/$FILENAME

# Eliminar backups antiguos (más de 30 días)
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete
```

```bash
# Dar permisos de ejecución
sudo chmod +x /usr/local/bin/backup_articulacion.sh

# Configurar cron para ejecutar diariamente a las 2 AM
sudo crontab -e
# Agregar:
0 2 * * * /usr/local/bin/backup_articulacion.sh
```

---

### PASO 3: Configurar Aplicación en Servidor

#### 3.1 Crear Usuario del Sistema
```bash
sudo useradd -m -s /bin/bash articulacion
sudo usermod -aG www-data articulacion
```

#### 3.2 Clonar/Subir Proyecto
```bash
# Opción A: Con Git
sudo su - articulacion
cd /home/articulacion
git clone [URL_REPOSITORIO] articulacion_sena
cd articulacion_sena

# Opción B: Subir archivos con SCP/SFTP
# Desde tu máquina local:
scp -r /ruta/local/articulacion usuario@servidor:/home/articulacion/
```

#### 3.3 Crear Entorno Virtual
```bash
cd /home/articulacion/articulacion_sena
python3 -m venv venv
source venv/bin/activate
```

#### 3.4 Instalar Dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 3.5 Configurar Variables de Entorno
```bash
# Copiar template de producción
cp .env.production .env

# Editar con valores reales
nano .env
```

**Generar claves seguras**:
```python
# SECRET_KEY
python3 -c "import secrets; print(secrets.token_hex(32))"

# ENCRYPTION_KEY
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Ejemplo de `.env` final:
```
FLASK_APP=run.py
FLASK_ENV=production
DEBUG=False
SECRET_KEY=a9b8c7d6e5f4g3h2i1j0k9l8m7n6o5p4q3r2s1t0u9v8w7x6y5z4a3b2c1d0e9f8
DB_HOST=localhost
DB_PORT=3306
DB_USER=articulacion_user
DB_PASSWORD=TU_CONTRASEÑA_SEGURA_AQUI
DB_NAME=articulacion_sena
UPLOAD_FOLDER=uploads
MAX_FILE_SIZE=5242880
ALLOWED_EXTENSIONS=pdf,jpg,jpeg,png
ENCRYPTION_KEY=nueva_clave_fernet_generada_aqui
```

#### 3.6 Crear Directorios Necesarios
```bash
mkdir -p uploads temp logs
chmod 755 uploads temp
```

---

### PASO 4: Configurar Gunicorn

#### 4.1 Instalar Gunicorn
```bash
pip install gunicorn
```

#### 4.2 Crear Archivo de Configuración
```bash
nano gunicorn_config.py
```

Contenido:
```python
import multiprocessing

# Dirección y puerto
bind = "127.0.0.1:8000"

# Workers
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 5

# Logging
accesslog = "/home/articulacion/articulacion_sena/logs/gunicorn_access.log"
errorlog = "/home/articulacion/articulacion_sena/logs/gunicorn_error.log"
loglevel = "info"

# Process naming
proc_name = "articulacion_sena"

# Server mechanics
daemon = False
pidfile = "/home/articulacion/articulacion_sena/gunicorn.pid"
user = "articulacion"
group = "www-data"
```

#### 4.3 Probar Gunicorn
```bash
source venv/bin/activate
gunicorn -c gunicorn_config.py run:app
```

---

### PASO 5: Configurar Systemd

#### 5.1 Crear Servicio
```bash
sudo nano /etc/systemd/system/articulacion.service
```

Contenido:
```ini
[Unit]
Description=Sistema de Articulación SENA - Gunicorn
After=network.target mysql.service

[Service]
Type=notify
User=articulacion
Group=www-data
WorkingDirectory=/home/articulacion/articulacion_sena
Environment="PATH=/home/articulacion/articulacion_sena/venv/bin"
ExecStart=/home/articulacion/articulacion_sena/venv/bin/gunicorn -c gunicorn_config.py run:app
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

#### 5.2 Activar y Iniciar Servicio
```bash
sudo systemctl daemon-reload
sudo systemctl enable articulacion
sudo systemctl start articulacion
sudo systemctl status articulacion
```

---

### PASO 6: Configurar Nginx

#### 6.1 Crear Configuración del Sitio
```bash
sudo nano /etc/nginx/sites-available/articulacion
```

Contenido:
```nginx
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;

    client_max_body_size 10M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;

        # Timeouts
        proxy_connect_timeout 120s;
        proxy_send_timeout 120s;
        proxy_read_timeout 120s;
    }

    location /static {
        alias /home/articulacion/articulacion_sena/app/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /uploads {
        alias /home/articulacion/articulacion_sena/uploads;
        internal;
    }

    # Logs
    access_log /var/log/nginx/articulacion_access.log;
    error_log /var/log/nginx/articulacion_error.log;
}
```

#### 6.2 Activar Sitio
```bash
sudo ln -s /etc/nginx/sites-available/articulacion /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

### PASO 7: Configurar HTTPS con Let's Encrypt

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx

# Obtener certificado
sudo certbot --nginx -d tu-dominio.com -d www.tu-dominio.com

# Certbot configurará automáticamente Nginx para HTTPS
```

---

### PASO 8: Configurar Firewall

```bash
# UFW (Ubuntu)
sudo ufw allow 22/tcp  # SSH
sudo ufw allow 80/tcp  # HTTP
sudo ufw allow 443/tcp # HTTPS
sudo ufw enable

# Verificar
sudo ufw status
```

---

## 🔧 POST-DEPLOY

### Verificaciones Inmediatas

#### 1. Verificar Servicios
```bash
sudo systemctl status articulacion
sudo systemctl status nginx
sudo systemctl status mysql
```

#### 2. Verificar Logs
```bash
# Logs de la aplicación
tail -f /home/articulacion/articulacion_sena/logs/gunicorn_error.log

# Logs de Nginx
tail -f /var/log/nginx/articulacion_error.log
```

#### 3. Probar Aplicación
```
1. Acceder a: https://tu-dominio.com
2. Login con credenciales de administrador
3. Crear un colegio de prueba
4. Crear un programa de prueba
5. Crear un grupo de prueba
6. Cambiar contraseña del administrador
```

#### 4. Eliminar Archivo de Credenciales
```bash
rm /home/articulacion/articulacion_sena/.admin_credentials
```

---

## 📊 MONITOREO

### Configurar Logs Estructurados
```bash
# Rotación de logs
sudo nano /etc/logrotate.d/articulacion
```

Contenido:
```
/home/articulacion/articulacion_sena/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    create 0640 articulacion www-data
    sharedscripts
    postrotate
        systemctl reload articulacion > /dev/null
    endscript
}
```

### Monitoreo de Errores (Opcional)
- Instalar Sentry: https://sentry.io
- Configurar alerts por email
- Dashboard de métricas

---

## 🔄 MANTENIMIENTO

### Actualizar Aplicación
```bash
cd /home/articulacion/articulacion_sena
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart articulacion
```

### Backup Manual
```bash
/usr/local/bin/backup_articulacion.sh
```

### Ver Logs en Tiempo Real
```bash
sudo journalctl -u articulacion -f
```

---

## 🆘 TROUBLESHOOTING

### Aplicación no Inicia
```bash
# Verificar logs
sudo journalctl -u articulacion -n 50

# Verificar puerto
sudo netstat -tulpn | grep 8000

# Verificar permisos
ls -la /home/articulacion/articulacion_sena
```

### Error 502 Bad Gateway
```bash
# Verificar que Gunicorn esté corriendo
sudo systemctl status articulacion

# Verificar conexión
curl http://127.0.0.1:8000
```

### Error de Base de Datos
```bash
# Verificar MySQL
sudo systemctl status mysql

# Verificar conectividad
mysql -u articulacion_user -p -h localhost articulacion_sena
```

---

## 📞 SOPORTE

**Documentación Técnica**: Ver archivos en el proyecto
**Logs**: `/home/articulacion/articulacion_sena/logs/`
**Backups**: `/var/backups/articulacion/`

---

## ✅ CHECKLIST POST-DEPLOY

- [ ] Aplicación accesible vía HTTPS
- [ ] Login de administrador funciona
- [ ] Contraseña de administrador cambiada
- [ ] Archivo .admin_credentials eliminado
- [ ] Backup automático configurado y probado
- [ ] Logs rotando correctamente
- [ ] Firewall configurado
- [ ] SSL/HTTPS funcionando
- [ ] Todas las funcionalidades probadas

---

**Sistema listo para producción: 2025-12-18**
**Versión: 1.0.0**
**Desarrollado por: Claude Sonnet 4.5**
