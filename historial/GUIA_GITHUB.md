# GUÍA PARA SUBIR EL PROYECTO A GITHUB
## Sistema de Articulación SENA v1.0.0

---

## ✅ PASOS YA COMPLETADOS

- ✅ Git configurado con tu información
- ✅ Repositorio local inicializado
- ✅ Todos los archivos agregados
- ✅ Commit inicial creado con 199 archivos

---

## 📝 PASOS PENDIENTES

### PASO 1: Crear Repositorio en GitHub

1. **Inicia sesión en GitHub**
   - Ve a: https://github.com
   - Si no tienes cuenta, créala primero

2. **Crear Nuevo Repositorio**
   - Click en el botón **"+"** en la esquina superior derecha
   - Selecciona **"New repository"**

3. **Configurar el Repositorio**
   ```
   Repository name:        articulacion-sena
   Description:            Sistema de Articulación SENA - Gestión de matrículas y programas de formación
   Visibility:             🔒 Private (recomendado para producción)
                          o
                          🌐 Public (si quieres que sea público)

   ⚠️ NO MARQUES:
   [ ] Add a README file
   [ ] Add .gitignore
   [ ] Choose a license

   (Ya los tenemos en el proyecto local)
   ```

4. **Click en "Create repository"**

---

### PASO 2: Conectar y Subir el Código

Después de crear el repositorio, GitHub te mostrará instrucciones. Usaremos la opción:
**"…or push an existing repository from the command line"**

#### Opción A: Con HTTPS (Más fácil)

Copia y pega ESTOS comandos en PowerShell o CMD (dentro de la carpeta del proyecto):

```bash
cd "c:\Users\johan\OneDrive\Documents\Flask\articulacion"

# Agregar el remoto (reemplaza TU_USUARIO con tu usuario de GitHub)
git remote add origin https://github.com/TU_USUARIO/articulacion-sena.git

# Cambiar rama a main
git branch -M main

# Subir el código
git push -u origin main
```

**Importante**:
- Reemplaza `TU_USUARIO` con tu nombre de usuario de GitHub
- Te pedirá autenticación. Usa **Personal Access Token** (no contraseña)

#### Opción B: Con SSH (Si ya tienes SSH configurado)

```bash
cd "c:\Users\johan\OneDrive\Documents\Flask\articulacion"

# Agregar el remoto (reemplaza TU_USUARIO)
git remote add origin git@github.com:TU_USUARIO/articulacion-sena.git

# Cambiar rama a main
git branch -M main

# Subir el código
git push -u origin main
```

---

### PASO 3: Generar Personal Access Token (Si usas HTTPS)

Si Git te pide autenticación:

1. Ve a GitHub > Settings
2. Developer settings > Personal access tokens > Tokens (classic)
3. Click **"Generate new token"**
4. Nombre: `Git Access desde Windows`
5. Selecciona: `repo` (todos los permisos de repositorio)
6. Genera y **COPIA EL TOKEN** (no lo volverás a ver)
7. Usa el token como contraseña cuando Git lo pida

---

### PASO 4: Verificar que se Subió

1. Ve a tu repositorio en GitHub
2. Deberías ver:
   - 199 archivos
   - Commit inicial: "Versión 1.0.0 lista para producción"
   - README.md con la documentación

---

## 🎯 COMANDOS RÁPIDOS

### Para verificar el estado actual:

```bash
cd "c:\Users\johan\OneDrive\Documents\Flask\articulacion"
git status
git log --oneline
```

### Para hacer cambios futuros:

```bash
# Después de modificar archivos
git add .
git commit -m "Descripción de los cambios"
git push
```

---

## 🔒 ARCHIVOS QUE NO SE SUBIRÁN

El `.gitignore` ya está configurado para NO subir:

- ✅ `.env` (variables de entorno con contraseñas)
- ✅ `.admin_credentials` (credenciales admin)
- ✅ `uploads/*` (archivos de usuarios)
- ✅ `temp/*` (archivos temporales)
- ✅ `__pycache__/` (archivos Python compilados)
- ✅ `*.pyc` (bytecode Python)
- ✅ Archivos de prueba y documentación de desarrollo

---

## 📋 INFORMACIÓN DEL REPOSITORIO

### Detalles del Commit Inicial

```
Commit:  af9d893
Autor:   Johann Quintero <jsquinteroz@example.com>
Fecha:   2025-12-18
Mensaje: Versión 1.0.0 lista para producción - Sistema de Articulación SENA

Estadísticas:
- 199 archivos creados
- 44,239 líneas de código añadidas
```

### Estructura del Proyecto Subido

```
articulacion-sena/
├── app/                    # Aplicación Flask
├── database/               # Scripts SQL
├── formatos/               # Plantillas de documentos
├── migrations/             # Migraciones de BD
├── .gitignore             # Archivos ignorados
├── AUTHORS.md             # Autoría del proyecto
├── README.md              # Documentación principal
├── DEPLOY_PRODUCCION.md   # Guía de deploy tradicional
├── DEPLOY_PYTHONANYWHERE.md  # Guía de deploy PythonAnywhere
├── config.py              # Configuración
├── init_production.py     # Script de inicialización
├── requirements.txt       # Dependencias Python
└── run.py                 # Punto de entrada
```

---

## 🆘 SOLUCIÓN DE PROBLEMAS

### Error: "remote origin already exists"

```bash
git remote remove origin
git remote add origin https://github.com/TU_USUARIO/articulacion-sena.git
git push -u origin main
```

### Error: "Authentication failed"

- Asegúrate de usar un **Personal Access Token**, no tu contraseña de GitHub
- Los tokens se generan en: GitHub > Settings > Developer settings > Personal access tokens

### Error: "Repository not found"

- Verifica que el nombre del repositorio sea correcto
- Asegúrate de haber creado el repositorio en GitHub primero
- Verifica que el usuario sea correcto en la URL

### El push es muy lento

Es normal. El proyecto tiene 199 archivos y puede tardar varios minutos dependiendo de tu conexión.

---

## ✅ CHECKLIST FINAL

Una vez subido, verifica:

- [ ] El repositorio existe en GitHub
- [ ] Se ve el README.md con la documentación
- [ ] Hay 199 archivos en el repositorio
- [ ] El commit dice "Versión 1.0.0 lista para producción"
- [ ] NO se subieron archivos sensibles (.env, .admin_credentials)
- [ ] La estructura de carpetas es correcta

---

## 🔄 MANTENER EL REPOSITORIO ACTUALIZADO

### Cada vez que hagas cambios:

```bash
# Ver cambios
git status

# Agregar cambios
git add .

# Commit
git commit -m "Descripción breve de los cambios"

# Subir a GitHub
git push
```

### Para clonar en otro lugar (ej: PythonAnywhere):

```bash
git clone https://github.com/TU_USUARIO/articulacion-sena.git
cd articulacion-sena
```

---

## 📞 RECURSOS

- **GitHub Docs**: https://docs.github.com
- **Git Cheatsheet**: https://training.github.com/downloads/github-git-cheat-sheet/
- **Personal Access Tokens**: https://github.com/settings/tokens

---

## 🎉 ¡LISTO!

Una vez completados estos pasos, tu proyecto estará en GitHub y podrás:

1. ✅ Clonarlo en PythonAnywhere
2. ✅ Compartir el código con tu equipo
3. ✅ Mantener un historial de cambios
4. ✅ Hacer backups automáticos
5. ✅ Colaborar con otros desarrolladores

---

**Sistema de Articulación SENA v1.0.0**
**Desarrollado por**: Johann Quintero (jsquinteroz)
**Fecha**: 2025-12-18

¡Éxito con el deploy! 🚀
