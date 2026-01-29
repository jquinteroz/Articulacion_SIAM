# Actualización de Contraseñas - Usuarios de Prueba

## Problema
Los usuarios de prueba en la base de datos tienen una contraseña incorrecta (`Admin123!`) que no funciona.

## Solución
Actualizar las contraseñas a `Sena123$` para todos los usuarios de prueba.

---

## Método 1: Comando SQL Directo (Recomendado)

### Paso 1: Acceder a MySQL
```bash
mysql -u root -p
```

### Paso 2: Seleccionar la base de datos
```sql
USE articulacion_sena;
```

### Paso 3: Ejecutar el UPDATE
```sql
UPDATE usuarios
SET password_hash = 'scrypt:32768:8:1$vLNKgu9372NUqF6B$76813a769148e099d99edc8dc80e8222d09f7bd6bb8ec7a4e0d973627f07ea19344badfb6e6ca62218543d2322ff0a70d0eab1c5e1080a0b70a7e34de482f668'
WHERE documento IN ('1000000001', '1000000002', '1000000003', '1000000004', '1000000005');
```

### Paso 4: Verificar la actualización
```sql
SELECT documento, CONCAT(nombres, ' ', apellidos) as nombre, rol
FROM usuarios
WHERE documento IN ('1000000001', '1000000002', '1000000003', '1000000004', '1000000005');
```

Deberías ver 5 usuarios actualizados.

---

## Método 2: Usando phpMyAdmin

1. Abre **phpMyAdmin**
2. Selecciona la base de datos `articulacion_sena`
3. Ve a la pestaña **SQL**
4. Pega el siguiente comando:
   ```sql
   UPDATE usuarios
   SET password_hash = 'scrypt:32768:8:1$vLNKgu9372NUqF6B$76813a769148e099d99edc8dc80e8222d09f7bd6bb8ec7a4e0d973627f07ea19344badfb6e6ca62218543d2322ff0a70d0eab1c5e1080a0b70a7e34de482f668'
   WHERE documento IN ('1000000001', '1000000002', '1000000003', '1000000004', '1000000005');
   ```
5. Click en **Continuar**

---

## Método 3: Usando el Script Python

### Opción A: Solo ver las instrucciones
```bash
python actualizar_passwords.py
```

Este script mostrará:
- El hash generado para `Sena123$`
- El comando SQL completo para copiar y pegar
- Instrucciones de verificación

---

## Credenciales Actualizadas

Después de ejecutar la actualización, estas son las credenciales correctas:

### 👤 Administrador
- **Documento:** `1000000001`
- **Contraseña:** `Sena123$`
- **Email:** admin@sena.edu.co

### 👤 Rector
- **Documento:** `1000000002`
- **Contraseña:** `Sena123$`
- **Email:** rector@colegio1.edu.co

### 👤 Docente
- **Documento:** `1000000003`
- **Contraseña:** `Sena123$`
- **Email:** docente1@colegio1.edu.co

### 👤 Aprendiz 1
- **Documento:** `1000000004`
- **Contraseña:** `Sena123$`
- **Email:** juan.perez@estudiante.edu.co

### 👤 Aprendiz 2
- **Documento:** `1000000005`
- **Contraseña:** `Sena123$`
- **Email:** ana.martinez@estudiante.edu.co

---

## Verificación Post-Actualización

### 1. Verifica que las contraseñas se actualizaron
```sql
SELECT documento,
       CONCAT(nombres, ' ', apellidos) as nombre,
       rol,
       LEFT(password_hash, 20) as hash_preview
FROM usuarios
WHERE documento IN ('1000000001', '1000000002', '1000000003', '1000000004', '1000000005');
```

El `hash_preview` debería comenzar con: `scrypt:32768:8:1$vL`

### 2. Prueba el inicio de sesión
1. Abre la aplicación: http://localhost:5000/login
2. Ingresa:
   - **Documento:** `1000000001`
   - **Contraseña:** `Sena123$`
3. Deberías poder iniciar sesión correctamente

---

## ⚠️ Notas Importantes

1. **La contraseña es Case Sensitive**
   - Debe ser exactamente: `Sena123$`
   - **NO** funcionará: `sena123$`, `SENA123$`, `Sena123!`

2. **Símbolo del Dólar**
   - Asegúrate de incluir el `$` al final
   - El símbolo es parte de la contraseña

3. **Usuarios Nuevos**
   - Si creas un nuevo usuario desde la aplicación, puedes usar cualquier contraseña
   - Esta actualización solo afecta a los 5 usuarios de prueba

4. **Producción**
   - Para producción, cambia TODAS las contraseñas
   - Usa contraseñas únicas para cada usuario
   - Elimina los usuarios de prueba que no necesites

---

## Solución de Problemas

### ❌ Error: "Usuario o contraseña incorrectos"
**Causa:** La contraseña no se actualizó correctamente

**Solución:**
1. Verifica que ejecutaste el comando UPDATE
2. Asegúrate de escribir exactamente: `Sena123$`
3. Verifica que el hash en la base de datos comience con `scrypt:32768:8:1$vL`

### ❌ Error: "0 rows affected"
**Causa:** Los documentos no existen en la base de datos

**Solución:**
```sql
-- Verifica que existan los usuarios
SELECT * FROM usuarios WHERE documento IN ('1000000001', '1000000002', '1000000003', '1000000004', '1000000005');

-- Si no existen, reimporta base_final.sql
```

### ❌ La contraseña no funciona después de actualizar
**Solución:**
1. Limpia la caché del navegador
2. Cierra todas las pestañas de la aplicación
3. Abre una nueva pestaña de incógnito
4. Intenta iniciar sesión de nuevo con `Sena123$`

---

## Archivos Relacionados

- `actualizar_passwords.py` - Script Python para generar el hash
- `INSTRUCCIONES_BASE_DATOS.md` - Documentación completa de la base de datos
- `base_final.sql` - Script SQL con la estructura y datos de prueba

---

## Contacto y Soporte

Si tienes problemas con la actualización:
1. Verifica que la base de datos sea `articulacion_sena`
2. Verifica que los usuarios existan
3. Revisa los logs de la aplicación para errores específicos
