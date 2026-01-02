# Instrucciones para Importar la Base de Datos

## Script: base_final.sql

Este script contiene la estructura completa de la base de datos y datos de prueba para el Sistema de Articulación SENA.

## Contenido del Script

### 1. Estructura de Tablas
- `usuarios` - Usuarios del sistema (Admin, Docentes, Aprendices, Rectores)
- `programas` - Programas técnicos disponibles
- `colegios` - Instituciones educativas
- `grupos` - Grupos de aprendices por colegio y programa
- `aprendices` - Información extendida de estudiantes
- `matriculas` - Proceso de matrícula
- `documentos` - Documentos de matrícula
- `documentos_simat` - Documentos SIMAT por colegio/grupo
- `novedades` - Noticias y avisos
- `mensajes_contacto` - Mensajes del formulario de contacto
- `auditoria` - Log de auditoría del sistema

### 2. Datos de Prueba Incluidos

#### Usuarios (Contraseña para todos: `Sena123$`)

| Rol | Email | Documento | Descripción |
|-----|-------|-----------|-------------|
| **ADMINISTRADOR** | admin@sena.edu.co | 1000000001 | Usuario administrador del sistema |
| **RECTOR** | rector@colegio1.edu.co | 1000000002 | Rector de colegio |
| **DOCENTE** | docente1@colegio1.edu.co | 1000000003 | Docente enlace |
| **APRENDIZ** | juan.perez@estudiante.edu.co | 1000000004 | Estudiante de prueba 1 |
| **APRENDIZ** | ana.martinez@estudiante.edu.co | 1000000005 | Estudiante de prueba 2 |

#### Programas Técnicos
- Técnico en Sistemas (1980 horas)
- Técnico en Administración (1760 horas)
- Técnico en Contabilidad (1760 horas)
- Técnico en Mecánica Industrial (2200 horas)
- Técnico en Electricidad (2000 horas)
- Técnico en Logística (1980 horas)

#### Colegios
- Institución Educativa Distrital San José
- Colegio Departamental La Esperanza
- Instituto Técnico Industrial

#### Grupos
- 5 grupos de prueba distribuidos en los colegios

#### Novedades
- 3 noticias de ejemplo

## Instrucciones de Importación

### Opción 1: MySQL Command Line

```bash
# 1. Acceder a MySQL
mysql -u root -p

# 2. Crear la base de datos (si no existe)
CREATE DATABASE IF NOT EXISTS articulacion_sena CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 3. Salir de MySQL
exit

# 4. Importar el script
mysql -u root -p articulacion_sena < base_final.sql
```

### Opción 2: phpMyAdmin

1. Abre phpMyAdmin
2. Selecciona la base de datos `articulacion_sena` (créala si no existe)
3. Ve a la pestaña "Importar"
4. Selecciona el archivo `base_final.sql`
5. Click en "Continuar"

### Opción 3: MySQL Workbench

1. Abre MySQL Workbench
2. Conecta al servidor
3. Ve a `Server` > `Data Import`
4. Selecciona "Import from Self-Contained File"
5. Busca el archivo `base_final.sql`
6. En "Default Target Schema" selecciona `articulacion_sena`
7. Click en "Start Import"

## Verificación Post-Importación

Después de importar, verifica que todo esté correcto:

```sql
-- Verificar usuarios
SELECT id, documento, nombre_completo, email, rol FROM usuarios;

-- Verificar programas
SELECT id, codigo, nombre, activo FROM programas WHERE activo = 1;

-- Verificar colegios
SELECT id, nombre, tipo_colegio FROM colegios WHERE activo = 1;

-- Verificar grupos
SELECT g.id, g.nombre, c.nombre as colegio, p.nombre as programa
FROM grupos g
JOIN colegios c ON g.colegio_id = c.id
JOIN programas p ON g.programa_id = p.id;
```

## Actualizar archivo .env

Asegúrate de que tu archivo `.env` tenga las credenciales correctas:

```env
# Base de datos MySQL LOCAL
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_password_aqui
DB_NAME=articulacion_sena
```

## Iniciar la Aplicación

Una vez importada la base de datos:

```bash
# 1. Activar entorno virtual (si usas uno)
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 2. Iniciar la aplicación
python run.py
```

## Acceso al Sistema

Puedes iniciar sesión con cualquiera de los usuarios de prueba:

### Como Administrador
- **Usuario:** 1000000001
- **Contraseña:** Sena123$

### Como Docente
- **Usuario:** 1000000003
- **Contraseña:** Sena123$

### Como Aprendiz
- **Usuario:** 1000000004
- **Contraseña:** Sena123$

## Notas Importantes

1. **Contraseñas:** Todos los usuarios de prueba tienen la misma contraseña: `Sena123$`

2. **Datos de Prueba:** Este script está diseñado para desarrollo y pruebas. En producción:
   - Cambia las contraseñas de todos los usuarios
   - Elimina los datos de prueba que no necesites
   - Configura usuarios reales

3. **Respaldo:** Antes de importar en un sistema existente, haz un respaldo:
   ```bash
   mysqldump -u root -p articulacion_sena > respaldo_$(date +%Y%m%d).sql
   ```

4. **Producción:** Para producción, genera una nueva clave de encriptación:
   ```bash
   python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
   ```
   Y actualiza `ENCRYPTION_KEY` en `.env`

## Solución de Problemas

### Error: Base de datos ya existe
Si necesitas reemplazar la base de datos existente:
```sql
DROP DATABASE IF EXISTS articulacion_sena;
CREATE DATABASE articulacion_sena CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Error: Permisos insuficientes
Asegúrate de que el usuario de MySQL tenga permisos:
```sql
GRANT ALL PRIVILEGES ON articulacion_sena.* TO 'tu_usuario'@'localhost';
FLUSH PRIVILEGES;
```

### La aplicación no carga los programas
Verifica que los programas estén activos:
```sql
SELECT * FROM programas WHERE activo = 1;
```

## Más Información

Para más detalles sobre el sistema, consulta:
- `README.md` - Documentación principal
- `historial/` - Documentación histórica y guías detalladas
