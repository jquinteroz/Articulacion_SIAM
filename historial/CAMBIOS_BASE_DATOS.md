# Cambios en la Base de Datos - Validación de Edad

## Cambios Realizados

### 1. Nueva Columna: `fecha_nacimiento`

**Tabla afectada**: `usuarios`

**SQL aplicado**:
```sql
ALTER TABLE usuarios
ADD COLUMN fecha_nacimiento DATE NULL
AFTER apellidos;
```

**Detalles**:
- **Tipo**: DATE
- **Nullable**: Sí (NULL permitido para usuarios existentes)
- **Posición**: Después de la columna `apellidos`
- **Estado**: ✅ **YA APLICADO** - La migración se ejecutó exitosamente

**Propósito**:
- Almacenar la fecha de nacimiento del usuario
- Permitir cálculo de edad automático
- Validar tipo de documento según edad
- Determinar si requiere acudiente
- Ajustar documentos requeridos según mayoría de edad

---

## Verificar si el cambio está aplicado

Ejecuta en MySQL:

```sql
-- Verificar estructura de la tabla
DESCRIBE usuarios;

-- Ver datos de ejemplo
SELECT id, documento, nombres, apellidos, fecha_nacimiento, tipo_documento
FROM usuarios
LIMIT 5;
```

**Resultado esperado**: Deberías ver la columna `fecha_nacimiento` entre `apellidos` y `email`.

---

## Nuevas Propiedades en el Modelo Usuario

Aunque no son cambios en la base de datos, estas propiedades calculadas se agregaron al modelo Python:

```python
@property
def edad(self):
    """Calcula edad actual basada en fecha_nacimiento"""
    # Retorna edad en años o None si no hay fecha

@property
def es_mayor_de_edad(self):
    """True si tiene 18 años o más"""

@property
def tiene_documento_desactualizado(self):
    """True si tiene TI pero ya es mayor de edad"""

@property
def requiere_acudiente(self):
    """True si es menor de 18 años"""
```

---

## Resumen

✅ **Un solo cambio en la base de datos**: Columna `fecha_nacimiento` agregada a tabla `usuarios`

✅ **Estado**: Aplicado exitosamente

✅ **Usuarios existentes**: No afectados (columna nullable)

✅ **Nuevos usuarios**: Deberán proporcionar fecha de nacimiento en el registro

---

## Archivo de Migración

El script SQL completo está en: `migrations/add_fecha_nacimiento.sql`
