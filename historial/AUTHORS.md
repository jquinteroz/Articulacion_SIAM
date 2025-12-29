# Autoría del Proyecto

## Sistema de Articulación SENA
### Versión 1.0.0

---

## Desarrollador Principal

**Johann Quintero**
- Usuario: jsquinteroz
- GitHub: [@jsquinteroz](https://github.com/jsquinteroz)
- Rol: Desarrollador Full Stack
- Fecha de desarrollo: Diciembre 2025

---

## Contribuciones

### Arquitectura y Backend
- Diseño e implementación de la arquitectura MVC con Flask
- Desarrollo del sistema de autenticación y autorización
- Implementación de modelos de base de datos con SQLAlchemy
- Desarrollo de servicios de negocio y lógica de aplicación
- Sistema de generación de PDFs y formatos
- Exportación de datos a formato SOFIA Plus
- API REST y endpoints

### Frontend
- Diseño de interfaces de usuario responsivas
- Implementación de dashboards por rol (Admin, Docente, Rector, Aprendiz)
- Formularios dinámicos con validación
- Selectores dinámicos y filtros
- Sistema de mensajes flash y notificaciones

### Base de Datos
- Diseño del esquema de base de datos
- Implementación de migraciones con Flask-Migrate
- Optimización de consultas y relaciones
- Scripts de inicialización y limpieza

### Seguridad
- Implementación de hash de contraseñas con bcrypt
- Protección CSRF en formularios
- Control de acceso basado en roles
- Validaciones de entrada

### DevOps
- Scripts de inicialización para producción
- Configuración de variables de entorno
- Documentación de deployment
- Preparación para producción con Gunicorn y Nginx

---

## Tecnologías Utilizadas

- **Backend**: Python 3.8+, Flask 3.0, SQLAlchemy
- **Frontend**: HTML5, CSS3, JavaScript, Font Awesome
- **Base de Datos**: MySQL 8.0+
- **Generación de Documentos**: python-docx, docx2pdf, ReportLab
- **Exportación de Datos**: openpyxl
- **Autenticación**: Flask-Login, Werkzeug Security
- **Otros**: python-dotenv, PyMySQL, cryptography

---

## Líneas de Código

Aproximadamente:
- Python: ~15,000 líneas
- HTML/Jinja2: ~8,000 líneas
- CSS: ~6,000 líneas
- JavaScript: ~3,000 líneas
- **Total**: ~32,000 líneas de código

---

## Archivos Principales Desarrollados

### Core de la Aplicación
- `run.py` - Punto de entrada de la aplicación
- `config.py` - Configuración de la aplicación
- `app/__init__.py` - Factory de la aplicación Flask

### Modelos (app/models/)
- `user.py` - Modelo de usuarios
- `aprendiz.py` - Modelo de aprendices
- `colegio.py` - Modelo de colegios
- `programa.py` - Modelo de programas
- `grupo.py` - Modelo de grupos
- `matricula.py` - Modelo de matrículas
- `documento.py` - Modelo de documentos

### Servicios (app/services/)
- `auth_service.py` - Servicio de autenticación
- `matricula_service.py` - Servicio de matrículas
- `documento_service.py` - Servicio de documentos
- `formato_service.py` - Servicio de generación de formatos PDF
- `sofia_service.py` - Servicio de exportación SOFIA Plus
- `reporte_service.py` - Servicio de reportes

### Blueprints (app/blueprints/)
- `public/` - Rutas públicas (login, registro, contacto)
- `admin/` - Panel de administración
- `docente/` - Panel de docente enlace
- `aprendiz/` - Panel de aprendiz

### Scripts de Utilidad
- `init_production.py` - Inicialización para producción
- `app/utils/crypto.py` - Utilidades de encriptación
- `app/utils/decorators.py` - Decoradores personalizados
- `app/utils/validators.py` - Validadores
- `app/utils/helpers.py` - Funciones auxiliares

---

## Fechas Importantes

- **Inicio del Proyecto**: Diciembre 2025
- **Versión 1.0.0 Completada**: 18 de Diciembre de 2025
- **Listo para Producción**: 18 de Diciembre de 2025

---

## Agradecimientos

- **SENA** - Servicio Nacional de Aprendizaje
- **Centro de Gestión de Mercados, Logística y Tecnologías de la Información**

---

## Copyright

Copyright © 2025 Johann Quintero (jsquinteroz)

Todos los derechos reservados. Este software fue desarrollado para el SENA
(Servicio Nacional de Aprendizaje) como parte del Sistema de Articulación
con la Media Técnica.

---

**Johann Quintero** - Desarrollador Full Stack
GitHub: @jsquinteroz
