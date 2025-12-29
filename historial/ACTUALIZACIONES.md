# Actualizaciones del Sistema - Diciembre 2025

## Resumen de Cambios

Se han implementado múltiples mejoras en el sistema de gestión de articulación SENA-Universidad de Cundinamarca:

### ✅ Correcciones de Errores

1. **Error de Directorio de Reportes**
   - Los reportes ahora se guardan en el directorio temporal del sistema
   - No más errores de permisos al generar reportes

2. **Estado de Documentos Mejorado**
   - Los documentos subidos sin validar ahora muestran estado 'ENVIADO' en lugar de 'PENDIENTE'
   - Mejor consistencia en el flujo de estados

3. **Prevención de Reemplazo de Documentos Aprobados**
   - Los aprendices ya NO pueden reemplazar documentos aprobados por el docente
   - Solo el administrador puede modificar documentos aprobados

4. **Mejoras en Generación de Formatos Word**
   - Mejor manejo de texto dividido en múltiples runs
   - Los marcadores como [NOMBRE_APRENDIZ] ahora se reemplazan correctamente

### 🎨 Modernización de Interfaz

Se aplicó un diseño moderno consistente en todas las páginas con:
- Headers con gradiente azul/morado
- Tarjetas de estadísticas con iconos coloridos
- Filtros modernos y responsivos
- Tablas mejoradas con hover effects
- Badges coloridos para estados
- Animaciones suaves en botones

**Páginas modernizadas:**
- ✅ Página de reportes del docente
- ✅ Página de reportes del admin
- ✅ Página de gestión de grupos

### ⚙️ Nuevas Funcionalidades

1. **Estado MATRICULADO**
   - Nuevo estado para aprendices que completaron todo el proceso
   - Flujo: BORRADOR → ENVIADO → PREMATRICULA → **MATRICULADO**

2. **Botón de Aprobación Final para Admin**
   - Botón destacado "MATRICULAR APRENDIZ" en la página de detalle de matrícula
   - Solo visible cuando el aprendiz está en estado PREMATRICULA
   - Valida que todos los documentos estén aprobados antes de matricular
   - Registra fecha y usuario que aprobó

3. **Gestión de Grupos de Formación SENA**
   - Interfaz moderna para crear y gestionar grupos de formación
   - Los grupos son identificados por un número único generado por el administrador (Ej: 2824345, 2824346)
   - Relación: Un programa de formación puede tener MUCHOS grupos, pero un grupo solo pertenece a UN programa
   - Cada grupo también está asociado a un colegio específico y tiene una jornada (mañana, tarde, noche)
   - **Filtrado Inteligente**: Los aprendices SOLO ven grupos que pertenezcan a:
     - Su colegio actual
     - El programa de formación que seleccionen
   - Filtrado dinámico en tiempo real con JavaScript (sin recargar página)

3. **Aprobación y Matriculación Masiva**
   - Botón individual "Matricular" en cada fila de la lista de matrículas para aprendices en PREMATRICULA
   - Botón "Matricular Todos" para aprobar masivamente todos los aprendices en PREMATRICULA
   - Validación automática: verifica que tengan 8 documentos aprobados antes de matricular
   - Feedback detallado con número de aprobados/fallidos y razones de errores

4. **Descarga Masiva de Documentos**
   - Nuevo botón "Descargar Todos" que descarga documentos de TODOS los grupos de formación en un solo ZIP
   - Estructura organizada: Grupo_2824345/Aprendiz_Nombre/documentos
   - Facilita respaldo completo de los documentos por grupos de formación SENA

5. **Edición de Datos por Docente Enlace**
   - Los docentes pueden editar el grupo y programa del aprendiz desde la página de detalle de matrícula
   - Formulario integrado en el sidebar con validación en tiempo real
   - Solo muestra grupos del colegio del docente
   - Filtrado automático de grupos según el programa seleccionado
   - Útil para corregir errores de inscripción o cambios de última hora

## 🗄️ Migración de Base de Datos

### IMPORTANTE: Ejecutar esta migración

Para agregar el nuevo estado MATRICULADO a la base de datos existente, ejecute:

```bash
mysql -u root -p articulacion < database/migrations/add_matriculado_estado.sql
```

O manualmente en MySQL:

```sql
ALTER TABLE matriculas
MODIFY COLUMN estado ENUM('BORRADOR', 'ENVIADO', 'PENDIENTE', 'COMPLETO', 'PREMATRICULA', 'MATRICULADO', 'RECHAZADO')
NOT NULL DEFAULT 'BORRADOR';
```

### Verificar la migración

```sql
SELECT COLUMN_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = DATABASE()
  AND TABLE_NAME = 'matriculas'
  AND COLUMN_NAME = 'estado';
```

Debería ver: `enum('BORRADOR','ENVIADO','PENDIENTE','COMPLETO','PREMATRICULA','MATRICULADO','RECHAZADO')`

## 📁 Archivos Modificados

### Modelos
- `app/models/matricula.py` - Agregado estado MATRICULADO al enum
- `app/models/documento.py` - Cambio de estado PENDIENTE a ENVIADO para docs sin validar

### Servicios
- `app/services/reporte_service.py` - Uso de directorio temporal
- `app/services/formato_service.py` - Mejor reemplazo en documentos Word

### Rutas
- `app/blueprints/admin/routes.py` - Nuevas rutas:
  - `matricular_aprendiz` - Matriculación individual
  - `matricular_todos_prematricula` - Matriculación masiva (NUEVO)
  - `descargar_todos_grupos` - Descarga ZIP de todos los grupos (NUEVO)
- `app/blueprints/aprendiz/routes.py` - Prevención de reemplazo de docs aprobados + filtrado de grupos
- `app/blueprints/docente/routes.py` - Nueva ruta:
  - `editar_datos_aprendiz` - Editar grupo y programa del aprendiz (NUEVO)

### Templates
- `app/templates/admin/matriculas/detalle.html` - Botón MATRICULAR APRENDIZ
- `app/templates/admin/matriculas/list.html` - Botones individuales y masivos de matriculación + descarga (NUEVO)
- `app/templates/admin/reportes.html` - Estado MATRICULADO en filtros
- `app/templates/admin/grupos/list.html` - Diseño moderno completo
- `app/templates/admin/grupos/form.html` - Formulario crear/editar grupo (NUEVO)
- `app/templates/docente/reportes.html` - Diseño moderno completo
- `app/templates/docente/ver_matricula.html` - Formulario de edición de datos del aprendiz (NUEVO)
- `app/templates/aprendiz/matricula.html` - Filtrado dinámico de grupos por colegio y programa
- `app/templates/aprendiz/perfil.html` - Filtrado dinámico de grupos por colegio y programa

### Base de Datos
- `database/articulacion.sql` - Schema actualizado con MATRICULADO y grupos SENA
- `database/migrations/add_matriculado_estado.sql` - Script de migración (NUEVO)
- `database/migrations/insert_grupos_formacion.sql` - Script para insertar grupos de formación SENA (NUEVO)
- `database/migrations/update_aprendices_grupos.sql` - Script para actualizar aprendices con grupos SENA (NUEVO)

## 🚀 Próximos Pasos

### Para Base de Datos Nueva (Instalación desde cero):
```bash
# 1. Crear base de datos completa con grupos SENA
mysql -u root -p articulacion < database/articulacion.sql
```

### Para Base de Datos Existente (Migración):
```bash
# 1. Agregar estado MATRICULADO
mysql -u root -p articulacion < database/migrations/add_matriculado_estado.sql

# 2. Reemplazar grupos antiguos con grupos SENA
mysql -u root -p articulacion < database/migrations/insert_grupos_formacion.sql

# 3. Actualizar aprendices existentes con grupos SENA
mysql -u root -p articulacion < database/migrations/update_aprendices_grupos.sql
```

### Luego:
3. **Reiniciar la aplicación Flask**
4. **Verificar que el sistema funciona correctamente**
5. **Probar el flujo completo de matrícula:**
   - Aprendiz selecciona colegio y programa
   - Solo ve grupos de su colegio y programa (números SENA como 2824345)
   - Completa matrícula y sube documentos
   - Docente aprueba documentos
   - Admin matricula al aprendiz

## 🔄 Flujo Completo de Matrícula

1. **Aprendiz** - Completa perfil y sube 8 documentos (estado: BORRADOR → ENVIADO)
2. **Docente Enlace** - Revisa y aprueba/rechaza documentos (estado: ENVIADO → PREMATRICULA)
3. **Administrador** - Matrícula definitiva del aprendiz (estado: PREMATRICULA → **MATRICULADO**)

## 📞 Soporte

Si encuentra algún problema después de aplicar estas actualizaciones, verifique:
1. ✅ La migración de base de datos se ejecutó correctamente
2. ✅ Todos los archivos están en su lugar
3. ✅ La aplicación se reinició después de los cambios
4. ✅ No hay errores en los logs de Flask

---

**Fecha de actualización:** 8 de Diciembre, 2025
**Versión:** 2.0.0
