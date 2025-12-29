# Guía de Despliegue en Producción
## Sistema de Matrículas - Articulación SENA

Esta guía cubre el despliegue del sistema en un servidor de producción.

## Opción 1: Servidor Linux con Nginx + Gunicorn

### Requisitos
- Ubuntu 20.04 LTS o superior
- Acceso root o sudo
- Dominio configurado (opcional)

### Paso 1: Preparar el Servidor

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias
sudo apt install python3 python3-pip python3-venv nginx mysql-server -y
sudo apt install python3-dev default-libmysqlclient-dev build-essential -y
```

### Paso 2: Configurar MySQL

```bash
sudo mysql_secure_installation

sudo mysql
```

```sql
CREATE DATABASE articulacion_sena CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'articulacion'@'localhost' IDENTIFIED BY 'password_seguro';
GRANT ALL PRIVILEGES ON articulacion_sena.* TO 'articulacion'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Paso 3: Preparar la Aplicación

```bash
# Crear directorio
sudo mkdir -p /var/www/articulacion
cd /var/www/articulacion

# Copiar archivos del proyecto
# (usar git clone o scp)

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
pip install gunicorn
```

### Paso 4: Configurar Variables de Entorno

```bash
nano .env
```

```env
FLASK_APP=run.py
FLASK_ENV=production
SECRET_KEY=clave_muy_segura_de_producción

DB_HOST=localhost
DB_PORT=3306
DB_USER=articulacion
DB_PASSWORD=password_seguro
DB_NAME=articulacion_sena

UPLOAD_FOLDER=/var/www/articulacion/uploads
MAX_FILE_SIZE=5242880
ALLOWED_EXTENSIONS=pdf,jpg,jpeg,png

ENCRYPTION_KEY=clave_generada_con_flask_command
```

### Paso 5: Inicializar Base de Datos

```bash
# Cargar esquema
mysql -u articulacion -p articulacion_sena < database/schema.sql

# Cargar datos iniciales
mysql -u articulacion -p articulacion_sena < database/seed_data.sql

# Crear administrador
flask create-admin
```

### Paso 6: Configurar Permisos

```bash
# Crear usuario del sistema
sudo useradd -r -s /bin/false articulacion

# Establecer propietario
sudo chown -R articulacion:articulacion /var/www/articulacion

# Permisos especiales para uploads
sudo chmod 755 /var/www/articulacion/uploads
sudo chmod 755 /var/www/articulacion/reports
```

### Paso 7: Configurar Gunicorn como Servicio

```bash
sudo nano /etc/systemd/system/articulacion.service
```

```ini
[Unit]
Description=Sistema de Matrículas SENA
After=network.target mysql.service

[Service]
Type=notify
User=articulacion
Group=articulacion
WorkingDirectory=/var/www/articulacion
Environment="PATH=/var/www/articulacion/venv/bin"
EnvironmentFile=/var/www/articulacion/.env
ExecStart=/var/www/articulacion/venv/bin/gunicorn \
    --workers 4 \
    --bind unix:/var/www/articulacion/articulacion.sock \
    --timeout 120 \
    --access-logfile /var/log/articulacion/access.log \
    --error-logfile /var/log/articulacion/error.log \
    run:app

[Install]
WantedBy=multi-user.target
```

```bash
# Crear directorio de logs
sudo mkdir -p /var/log/articulacion
sudo chown articulacion:articulacion /var/log/articulacion

# Habilitar y arrancar servicio
sudo systemctl daemon-reload
sudo systemctl start articulacion
sudo systemctl enable articulacion

# Verificar estado
sudo systemctl status articulacion
```

### Paso 8: Configurar Nginx

```bash
sudo nano /etc/nginx/sites-available/articulacion
```

```nginx
server {
    listen 80;
    server_name tu_dominio.com www.tu_dominio.com;

    client_max_body_size 10M;

    location / {
        proxy_pass http://unix:/var/www/articulacion/articulacion.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 300s;
        proxy_read_timeout 300s;
    }

    location /static {
        alias /var/www/articulacion/app/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /uploads {
        internal;
        alias /var/www/articulacion/uploads;
    }

    location /reports {
        internal;
        alias /var/www/articulacion/reports;
    }

    access_log /var/log/nginx/articulacion_access.log;
    error_log /var/log/nginx/articulacion_error.log;
}
```

```bash
# Habilitar sitio
sudo ln -s /etc/nginx/sites-available/articulacion /etc/nginx/sites-enabled/

# Verificar configuración
sudo nginx -t

# Reiniciar Nginx
sudo systemctl restart nginx
```

### Paso 9: Configurar SSL con Let's Encrypt

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtener certificado
sudo certbot --nginx -d tu_dominio.com -d www.tu_dominio.com

# Verificar renovación automática
sudo certbot renew --dry-run
```

### Paso 10: Configurar Firewall

```bash
# Configurar UFW
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

## Opción 2: Docker

### Dockerfile

```dockerfile
FROM python:3.9-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Crear directorios necesarios
RUN mkdir -p uploads reports

# Exponer puerto
EXPOSE 5000

# Comando de inicio
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root_password
      MYSQL_DATABASE: articulacion_sena
      MYSQL_USER: articulacion
      MYSQL_PASSWORD: password_seguro
    volumes:
      - mysql_data:/var/lib/mysql
      - ./database:/docker-entrypoint-initdb.d
    ports:
      - "3306:3306"

  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - DB_HOST=db
      - DB_USER=articulacion
      - DB_PASSWORD=password_seguro
      - DB_NAME=articulacion_sena
    volumes:
      - ./uploads:/app/uploads
      - ./reports:/app/reports
    depends_on:
      - db

volumes:
  mysql_data:
```

```bash
# Construir y ejecutar
docker-compose up -d

# Ver logs
docker-compose logs -f app
```

## Mantenimiento en Producción

### Monitoreo

```bash
# Ver logs en tiempo real
sudo tail -f /var/log/articulacion/error.log

# Ver estado del servicio
sudo systemctl status articulacion

# Reiniciar servicio
sudo systemctl restart articulacion
```

### Respaldos Automáticos

```bash
# Crear script de respaldo
sudo nano /usr/local/bin/backup_articulacion.sh
```

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/articulacion"

mkdir -p $BACKUP_DIR

# Respaldar base de datos
mysqldump -u articulacion -p'password_seguro' articulacion_sena | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Respaldar archivos
tar -czf $BACKUP_DIR/uploads_$DATE.tar.gz /var/www/articulacion/uploads

# Eliminar respaldos antiguos (más de 30 días)
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete

echo "Respaldo completado: $DATE"
```

```bash
chmod +x /usr/local/bin/backup_articulacion.sh

# Programar respaldo diario a las 2 AM
sudo crontab -e
0 2 * * * /usr/local/bin/backup_articulacion.sh >> /var/log/articulacion/backup.log 2>&1
```

### Actualización

```bash
cd /var/www/articulacion

# Respaldar antes de actualizar
/usr/local/bin/backup_articulacion.sh

# Activar entorno
source venv/bin/activate

# Actualizar código
git pull origin main

# Actualizar dependencias
pip install -r requirements.txt

# Migrar base de datos si es necesario
flask db upgrade

# Reiniciar servicio
sudo systemctl restart articulacion
```

## Solución de Problemas

### Error 502 Bad Gateway

```bash
# Verificar que Gunicorn esté corriendo
sudo systemctl status articulacion

# Ver logs
sudo journalctl -u articulacion -n 100
```

### Error de Conexión a Base de Datos

```bash
# Verificar MySQL
sudo systemctl status mysql

# Probar conexión
mysql -u articulacion -p articulacion_sena
```

### Permisos de Archivos

```bash
# Restablecer permisos
sudo chown -R articulacion:articulacion /var/www/articulacion
sudo chmod 755 /var/www/articulacion/uploads
```

---

**Fin de la Guía de Despliegue**
