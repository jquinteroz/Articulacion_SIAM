# Sistema de Articulación SENA
## Versión 1.0.0 - Producción

Sistema web completo para la gestión de articulación educativa entre instituciones y el SENA.

## Características Principales

- **Gestión de Usuarios**: Sistema completo de autenticación y autorización con 4 roles diferenciados
- **Formulario de Matrícula**: Formulario completo para aprendices con validación
- **Gestión Documental**: Carga, validación y descarga de documentos obligatorios
- **Reportes**: Generación de reportes en PDF y Excel con múltiples filtros
- **Panel Administrativo**: CRUD completo de usuarios, colegios, programas, grupos
- **Seguridad**: Contraseñas encriptadas con visualización controlada para administradores
- **Diseño Responsivo**: Interfaz adaptable a todos los dispositivos

## Roles del Sistema

### 1. Aprendiz
- Registro y autenticación
- Edición de perfil personal
- Completar formulario de matrícula
- Carga de documentos obligatorios
- Envío de matrícula para validación
- Descarga de resumen en PDF

### 2. Docente Enlace
- Visualización de matrículas del colegio asignado
- Validación de información de aprendices
- Reemplazo de documentos incorrectos
- Cambio de estados (Completo, Pendiente)
- Generación de reportes por grupo y programa

### 3. Administrador
- CRUD completo de usuarios (con visualización de contraseñas)
- CRUD de colegios, programas y grupos
- Gestión completa de matrículas
- Validación final (Prematrícula, Pendiente)
- Reportes avanzados en PDF y Excel
- Descarga masiva de documentos por grupo
- Gestión de novedades y mensajes de contacto

### 4. Rector
- Visualización de información del colegio
- Consulta de matrículas

## Tecnologías Utilizadas

### Backend
- **Flask 3.0.0**: Framework web de Python
- **SQLAlchemy**: ORM para manejo de base de datos
- **Flask-Login**: Gestión de sesiones y autenticación
- **Flask-Migrate**: Migraciones de base de datos
- **PyMySQL**: Conector para MySQL

### Frontend
- **HTML5, CSS3, JavaScript**: Tecnologías web estándar
- **Font Awesome**: Iconografía
- **Diseño personalizado**: Paleta verde corporativa SENA

### Base de Datos
- **MySQL 8.0+**: Base de datos relacional

### Librerías Adicionales
- **ReportLab**: Generación de PDF
- **OpenPyXL**: Generación de Excel
- **Cryptography**: Encriptación reversible de contraseñas
- **Pillow**: Procesamiento de imágenes

## Requisitos del Sistema

- Python 3.8+
- MySQL 8.0+
- 2GB RAM mínimo
- 10GB espacio en disco

## Instalación

### 1. Clonar o descargar el proyecto

```bash
cd articulacion
```

### 2. Crear entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copiar el archivo `.env.example` a `.env` y configurar:

```bash
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac
```

Editar el archivo `.env`:

```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=tu_clave_secreta_muy_segura_aqui

DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_password_mysql
DB_NAME=articulacion_sena

UPLOAD_FOLDER=uploads
MAX_FILE_SIZE=5242880
ALLOWED_EXTENSIONS=pdf,jpg,jpeg,png
```

### 5. Generar clave de encriptación

```bash
flask generate-encryption-key
```

Copiar la clave generada y agregarla al archivo `.env`:

```env
ENCRYPTION_KEY=clave_generada_aqui
```

### 6. Crear base de datos MySQL

```sql
mysql -u root -p

CREATE DATABASE articulacion_sena CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

### 7. Ejecutar scripts SQL

```bash
mysql -u root -p articulacion_sena < database/schema.sql
mysql -u root -p articulacion_sena < database/seed_data.sql
```

### 8. Crear administrador por defecto

```bash
flask create-admin
```

Credenciales por defecto:
- **Usuario**: 1000000000
- **Contraseña**: Admin123!

### 9. Ejecutar la aplicación

```bash
# Desarrollo
python run.py

# Producción
flask run --host=0.0.0.0 --port=5000
```

La aplicación estará disponible en: [http://localhost:5000](http://localhost:5000)

## Estructura del Proyecto

```
articulacion/
├── app/
│   ├── __init__.py              # Factory de la aplicación
│   ├── models/                   # Modelos de base de datos
│   │   ├── user.py
│   │   ├── aprendiz.py
│   │   ├── colegio.py
│   │   ├── programa.py
│   │   ├── grupo.py
│   │   ├── matricula.py
│   │   ├── documento.py
│   │   └── ...
│   ├── blueprints/              # Módulos de rutas
│   │   ├── public/              # Sitio público
│   │   ├── aprendiz/            # Dashboard aprendiz
│   │   ├── docente/             # Dashboard docente
│   │   └── admin/               # Panel administración
│   ├── services/                # Lógica de negocio
│   │   ├── auth_service.py
│   │   ├── matricula_service.py
│   │   ├── documento_service.py
│   │   └── reporte_service.py
│   ├── utils/                   # Utilidades
│   │   ├── crypto.py
│   │   ├── validators.py
│   │   ├── decorators.py
│   │   └── helpers.py
│   ├── static/                  # Archivos estáticos
│   │   ├── css/
│   │   ├── js/
│   │   └── img/
│   └── templates/               # Plantillas HTML
│       ├── base.html
│       ├── public/
│       ├── aprendiz/
│       ├── docente/
│       └── admin/
├── database/                    # Scripts SQL
│   ├── schema.sql
│   └── seed_data.sql
├── uploads/                     # Archivos subidos
├── reports/                     # Reportes generados
├── config.py                    # Configuración
├── requirements.txt             # Dependencias
├── run.py                       # Punto de entrada
└── README.md                    # Este archivo
```

## Funcionalidades Detalladas

### Gestión de Documentos

El sistema requiere 8 documentos obligatorios:

1. Documento de identidad del aprendiz
2. Registro civil
3. Certificado de afiliación a salud
4. Certificado SOFIA Plus
5. Certificado APE
6. Documento del acudiente
7. Tratamiento de datos
8. Acuerdo del aprendiz

**Estructura de archivos:**
```
uploads/
└── [TipoDoc]_[Nombre]_[Apellido]_[Ficha]_[Programa]/
    ├── documento1.pdf
    ├── documento2.pdf
    └── ...
```

### Sistema de Encriptación de Contraseñas

**Característica especial**: Las contraseñas se almacenan de dos formas:
1. **Hash bcrypt**: Para autenticación (no reversible)
2. **Cifrado Fernet**: Para visualización por administradores (reversible)

En el CRUD de usuarios, el administrador puede:
- Ver contraseñas como `********`
- Click en el ícono de ojo (👁) para mostrar la contraseña real
- Click nuevamente para ocultarla

**Implementación en templates:**
```html
<div class="password-container">
    <span class="password-display">********</span>
    <i class="fas fa-eye password-toggle"
       onclick="togglePassword({{ usuario.id }}, this)"></i>
</div>
```

### Estados de Matrícula

1. **BORRADOR**: Matrícula en proceso de llenado
2. **ENVIADO**: Aprendiz envió para validación
3. **PENDIENTE**: Docente marcó como pendiente
4. **COMPLETO**: Docente validó como completa
5. **PREMATRICULA**: Administrador aprobó
6. **RECHAZADO**: Fue rechazada

### Reportes

**PDF:**
- Resumen individual de aprendiz
- Listado por grupo
- Listado por programa
- Combinaciones personalizadas

**Excel:**
- Exportación completa de matrículas
- Filtros múltiples (colegio, programa, grupo)
- Formato profesional con estilos

### Paleta de Colores Corporativa

```css
--sena-verde-principal: #39A900
--sena-verde-oscuro: #2E7D32
--sena-verde-claro: #66BB6A
--sena-verde-muy-claro: #A5D6A7
--sena-verde-fondo: #E8F5E9
```

## Comandos Flask CLI

```bash
# Inicializar base de datos
flask init-db

# Crear administrador
flask create-admin

# Generar clave de encriptación
flask generate-encryption-key

# Ejecutar servidor
flask run
```

## Seguridad

- **Contraseñas**: Hasheadas con bcrypt + encriptación Fernet
- **Sesiones**: Cookies seguras con expiración
- **CSRF**: Protección habilitada
- **SQL Injection**: Prevenido por ORM
- **XSS**: Templates con auto-escape
- **Roles**: Decoradores para control de acceso

## Validaciones

**Campos requeridos en registro:**
- Documento (único)
- Nombres y apellidos
- Email (único, formato válido)
- Contraseña (mínimo 6 caracteres)

**Archivos:**
- Formatos permitidos: PDF, JPG, JPEG, PNG
- Tamaño máximo: 5MB por archivo

## Troubleshooting

### Error de conexión a MySQL
```bash
# Verificar que MySQL esté corriendo
mysql -u root -p

# Verificar credenciales en .env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=tu_password
```

### Error de importación de módulos
```bash
# Reinstalar dependencias
pip install --force-reinstall -r requirements.txt
```

### Carpetas de uploads no se crean
```bash
# Crear manualmente
mkdir uploads
mkdir reports
```

## Mantenimiento

### Respaldo de base de datos
```bash
mysqldump -u root -p articulacion_sena > backup_$(date +%Y%m%d).sql
```

### Limpiar archivos temporales
```bash
# Windows
rmdir /s /q uploads\temp
rmdir /s /q reports

# Linux
rm -rf uploads/temp reports/*
```

## Soporte

Para soporte técnico o consultas:
- Email: soporte@sena.edu.co
- Documentación: Este archivo README

## Desarrollador

**Johann Quintero** (jsquinteroz)
- GitHub: [@jsquinteroz](https://github.com/jsquinteroz)
- Versión: 1.0.0
- Fecha: 2025-12-18

## Licencia

Propiedad del SENA - Servicio Nacional de Aprendizaje
Todos los derechos reservados © 2025

Desarrollado por: Johann Quintero (jsquinteroz)

---

**Sistema de Articulación SENA v1.0.0**
Desarrollado para el SENA - Servicio Nacional de Aprendizaje
Copyright © 2025 - Johann Quintero (jsquinteroz)
