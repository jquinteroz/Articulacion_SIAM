# Documentación de la API del Sistema
## Sistema de Matrículas - Articulación SENA

Este documento describe los endpoints disponibles en el sistema, organizados por módulo.

---

## Autenticación

Todas las rutas protegidas requieren autenticación mediante sesión de Flask-Login.

---

## Módulo Público

### 1. Landing Page
```
GET /
```
**Descripción**: Página principal del sitio
**Autenticación**: No requerida
**Respuesta**: HTML

---

### 2. Login
```
GET  /login
POST /login
```
**Descripción**: Inicio de sesión
**Autenticación**: No requerida

**POST Parámetros**:
```json
{
  "documento": "string",
  "password": "string",
  "remember": "boolean"
}
```

**Respuesta exitosa**: Redirect a dashboard según rol

---

### 3. Registro
```
GET  /registro
POST /registro
```
**Descripción**: Registro de nuevo aprendiz
**Autenticación**: No requerida

**POST Parámetros**:
```json
{
  "documento": "string",
  "tipo_documento": "CC|TI|CE|PEP|PPT",
  "nombres": "string",
  "apellidos": "string",
  "email": "string",
  "telefono": "string",
  "password": "string",
  "password_confirm": "string"
}
```

---

### 4. Logout
```
GET /logout
```
**Descripción**: Cerrar sesión
**Autenticación**: Requerida

---

### 5. Contacto
```
GET  /contacto
POST /contacto
```
**POST Parámetros**:
```json
{
  "nombre": "string",
  "email": "string",
  "telefono": "string",
  "asunto": "string",
  "mensaje": "text"
}
```

---

## Módulo Aprendiz

**Prefijo**: `/aprendiz`
**Autenticación**: Requerida (Rol: APRENDIZ)

### 1. Dashboard
```
GET /aprendiz/dashboard
```
**Respuesta**: Vista del dashboard con estado de matrícula

---

### 2. Perfil
```
GET  /aprendiz/perfil
POST /aprendiz/perfil
```

**POST Parámetros**:
```json
{
  "nombres": "string",
  "apellidos": "string",
  "email": "string",
  "telefono": "string",
  "direccion": "string",
  "ciudad": "string",
  "departamento": "string",
  "acudiente_tipo_doc": "CC|TI|CE",
  "acudiente_documento": "string",
  "acudiente_nombres": "string",
  "acudiente_apellidos": "string",
  "acudiente_telefono": "string",
  "acudiente_email": "string",
  "colegio_id": "integer",
  "grupo_id": "integer",
  "programa_id": "integer"
}
```

---

### 3. Matrícula
```
GET /aprendiz/matricula
```
**Respuesta**: Formulario completo de matrícula

---

### 4. Documentos
```
GET  /aprendiz/documentos
POST /aprendiz/documentos
```

**POST Parámetros** (multipart/form-data):
```
tipo_documento: DOCUMENTO_IDENTIDAD|REGISTRO_CIVIL|CERTIFICADO_SALUD|...
archivo: File (PDF, JPG, JPEG, PNG - Max 5MB)
```

---

### 5. Enviar Matrícula
```
POST /aprendiz/enviar-matricula
```
**Descripción**: Envía la matrícula para validación
**Validaciones**:
- Perfil completo
- Todos los documentos cargados

---

### 6. Descargar Resumen
```
GET /aprendiz/descargar-resumen
```
**Respuesta**: PDF con resumen de matrícula

---

### 7. Descargar Documento
```
GET /aprendiz/descargar-documento/<int:documento_id>
```
**Parámetros**: ID del documento
**Respuesta**: Archivo descargable

---

## Módulo Docente

**Prefijo**: `/docente`
**Autenticación**: Requerida (Rol: DOCENTE o ADMINISTRADOR)

### 1. Dashboard
```
GET /docente/dashboard
```
**Respuesta**: Estadísticas del colegio asignado

---

### 2. Listar Matrículas
```
GET /docente/matriculas
```
**Query Params**:
- `estado`: todos|ENVIADO|PENDIENTE|COMPLETO
- `grupo`: todos|<grupo_id>

---

### 3. Ver Matrícula
```
GET /docente/matricula/<int:matricula_id>
```
**Parámetros**: ID de la matrícula
**Respuesta**: Detalle completo con documentos

---

### 4. Validar Matrícula
```
POST /docente/validar-matricula/<int:matricula_id>
```

**POST Parámetros**:
```json
{
  "estado": "COMPLETO|PENDIENTE|RECHAZADO",
  "observaciones": "text"
}
```

---

### 5. Reemplazar Documento
```
POST /docente/reemplazar-documento/<int:documento_id>
```

**POST Parámetros** (multipart/form-data):
```
archivo: File
```

---

### 6. Reportes
```
GET /docente/reportes
```
**Respuesta**: Página de generación de reportes

---

### 7. Generar Reporte Excel
```
POST /docente/generar-reporte-excel
```

**POST Parámetros**:
```json
{
  "filtro_tipo": "grupo|programa",
  "filtro_valor": "integer"
}
```

**Respuesta**: Archivo Excel

---

## Módulo Administrador

**Prefijo**: `/admin`
**Autenticación**: Requerida (Rol: ADMINISTRADOR)

### CRUD Usuarios

#### 1. Listar Usuarios
```
GET /admin/usuarios
```
**Query Params**:
- `rol`: todos|APRENDIZ|DOCENTE|ADMINISTRADOR|RECTOR

---

#### 2. Crear Usuario
```
GET  /admin/usuarios/crear
POST /admin/usuarios/crear
```

**POST Parámetros**:
```json
{
  "documento": "string",
  "tipo_documento": "CC|TI|CE|PEP|PPT",
  "nombres": "string",
  "apellidos": "string",
  "email": "string",
  "telefono": "string",
  "password": "string",
  "rol": "APRENDIZ|DOCENTE|ADMINISTRADOR|RECTOR"
}
```

---

#### 3. Editar Usuario
```
GET  /admin/usuarios/editar/<int:user_id>
POST /admin/usuarios/editar/<int:user_id>
```

**POST Parámetros**: Mismos que crear (password opcional)

---

#### 4. Eliminar Usuario
```
POST /admin/usuarios/eliminar/<int:user_id>
```

---

#### 5. Obtener Contraseña (AJAX)
```
GET /admin/usuarios/get-password/<int:user_id>
```

**Respuesta**:
```json
{
  "success": true,
  "password": "string"
}
```

---

### CRUD Colegios

#### 1. Listar Colegios
```
GET /admin/colegios
```

---

#### 2. Crear Colegio
```
GET  /admin/colegios/crear
POST /admin/colegios/crear
```

**POST Parámetros**:
```json
{
  "nombre": "string",
  "tipo_colegio": "PUBLICO|PRIVADO|MIXTO",
  "direccion": "string",
  "telefono": "string",
  "email": "string",
  "rector_id": "integer",
  "docente_enlace_id": "integer"
}
```

---

#### 3. Editar Colegio
```
GET  /admin/colegios/editar/<int:colegio_id>
POST /admin/colegios/editar/<int:colegio_id>
```

---

#### 4. Eliminar Colegio
```
POST /admin/colegios/eliminar/<int:colegio_id>
```

---

### CRUD Programas

#### 1. Listar Programas
```
GET /admin/programas
```

---

#### 2. Crear Programa
```
GET  /admin/programas/crear
POST /admin/programas/crear
```

**POST Parámetros**:
```json
{
  "codigo": "string",
  "nombre": "string",
  "descripcion": "text",
  "duracion_horas": "integer"
}
```

---

#### 3. Editar Programa
```
GET  /admin/programas/editar/<int:programa_id>
POST /admin/programas/editar/<int:programa_id>
```

---

#### 4. Eliminar Programa
```
POST /admin/programas/eliminar/<int:programa_id>
```

---

### CRUD Grupos

#### 1. Listar Grupos
```
GET /admin/grupos
```

---

#### 2. Crear Grupo
```
GET  /admin/grupos/crear
POST /admin/grupos/crear
```

**POST Parámetros**:
```json
{
  "nombre": "string",
  "colegio_id": "integer",
  "programa_id": "integer",
  "jornada": "MAÑANA|TARDE|NOCHE|UNICA",
  "año_lectivo": "integer"
}
```

---

### Gestión de Matrículas

#### 1. Listar Matrículas
```
GET /admin/matriculas
```
**Query Params**:
- `estado`: todos|BORRADOR|ENVIADO|PENDIENTE|COMPLETO|PREMATRICULA
- `colegio`: todos|<colegio_id>

---

#### 2. Ver Matrícula
```
GET /admin/matriculas/<int:matricula_id>
```

---

#### 3. Validar Matrícula
```
POST /admin/matriculas/validar/<int:matricula_id>
```

**POST Parámetros**:
```json
{
  "estado": "PREMATRICULA|PENDIENTE|RECHAZADO",
  "observaciones": "text"
}
```

---

### Reportes Avanzados

#### 1. Página de Reportes
```
GET /admin/reportes
```

---

#### 2. Generar Reporte Excel
```
POST /admin/reportes/generar-excel
```

**POST Parámetros**:
```json
{
  "colegio_id": "integer",
  "programa_id": "integer",
  "grupo_id": "integer"
}
```

**Respuesta**: Archivo Excel

---

#### 3. Descargar Documentos de Grupo
```
GET /admin/reportes/descargar-documentos-grupo/<int:grupo_id>
```

**Respuesta**: Archivo ZIP con todos los documentos

---

### Novedades

#### 1. Listar Novedades
```
GET /admin/novedades
```

---

#### 2. Crear Novedad
```
GET  /admin/novedades/crear
POST /admin/novedades/crear
```

**POST Parámetros** (multipart/form-data):
```
titulo: string
contenido: text
fecha_publicacion: date
destacado: boolean
imagen: File (opcional)
```

---

### Mensajes

#### 1. Ver Mensajes de Contacto
```
GET /admin/mensajes
```

---

#### 2. Marcar como Leído
```
POST /admin/mensajes/marcar-leido/<int:mensaje_id>
```

**Respuesta** (JSON):
```json
{
  "success": true
}
```

---

## Códigos de Estado HTTP

- **200 OK**: Solicitud exitosa
- **302 Found**: Redirección
- **400 Bad Request**: Datos inválidos
- **403 Forbidden**: Sin permisos
- **404 Not Found**: Recurso no encontrado
- **500 Internal Server Error**: Error del servidor

---

## Formatos de Respuesta

### HTML
La mayoría de endpoints devuelven páginas HTML renderizadas.

### JSON
Endpoints AJAX devuelven JSON:
```json
{
  "success": boolean,
  "message": "string",
  "data": object
}
```

### Archivos
- PDF: `application/pdf`
- Excel: `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
- ZIP: `application/zip`

---

## Ejemplos de Uso

### Ejemplo 1: Login con cURL
```bash
curl -X POST http://localhost:5000/login \
  -d "documento=1000000000" \
  -d "password=Admin123!" \
  -c cookies.txt
```

### Ejemplo 2: Obtener contraseña (JavaScript)
```javascript
async function obtenerPassword(userId) {
  const response = await fetch(`/admin/usuarios/get-password/${userId}`);
  const data = await response.json();

  if (data.success) {
    console.log('Contraseña:', data.password);
  }
}
```

### Ejemplo 3: Subir documento (HTML Form)
```html
<form method="POST" enctype="multipart/form-data" action="/aprendiz/documentos">
  <select name="tipo_documento">
    <option value="DOCUMENTO_IDENTIDAD">Documento de Identidad</option>
  </select>
  <input type="file" name="archivo" accept=".pdf,.jpg,.jpeg,.png">
  <button type="submit">Subir</button>
</form>
```

---

**Fin de la Documentación de la API**
