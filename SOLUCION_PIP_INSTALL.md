# SOLUCIÓN: ERROR AL INSTALAR REQUIREMENTS
## Sistema de Articulación SENA

---

## ❌ Error Recibido

```
ERROR: You must give at least one requirement to install
(maybe you meant "pip install /usr/share/pip-wheels"?)
```

---

## 🔍 POSIBLES CAUSAS Y SOLUCIONES

### CAUSA 1: Ruta Incorrecta del Archivo

Si estás en PythonAnywhere o Linux, asegúrate de estar en el directorio correcto:

```bash
# Verificar directorio actual
pwd

# Debe mostrar algo como: /home/TU_USUARIO/articulacion

# Listar archivos
ls -la

# Debes ver requirements.txt en la lista
```

**Solución**:
```bash
cd ~/articulacion
pip install -r requirements.txt
```

---

### CAUSA 2: Archivo con Formato Windows (CRLF)

En sistemas Linux, los archivos de Windows pueden tener problemas de formato.

**Solución - Convertir formato**:
```bash
# Instalar dos2unix si no está instalado
sudo apt-get install dos2unix

# Convertir el archivo
dos2unix requirements.txt

# Ahora instalar
pip install -r requirements.txt
```

**Solución Alternativa - Crear archivo nuevo**:
```bash
# Crear nuevo requirements.txt limpio
cat > requirements.txt << 'EOF'
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Migrate==4.0.5
Flask-Login==0.6.3
Flask-WTF==1.2.1
WTForms==3.1.1
PyMySQL==1.1.0
cryptography==41.0.7
python-dotenv==1.0.0
Pillow>=10.0.0
reportlab==4.0.7
openpyxl==3.1.2
xlrd==2.0.1
xlwt==1.3.0
email-validator==2.1.0
werkzeug==3.0.1
pandas>=2.0.0
python-docx==1.1.0
PyPDF2==3.0.1
pycryptodome==3.23.0
EOF

# Instalar
pip install -r requirements.txt
```

---

### CAUSA 3: Virtualenv No Activado

Debes estar dentro del entorno virtual.

**Verificar**:
```bash
# Ver si el virtualenv está activo
which python

# Debe mostrar algo como:
# /home/TU_USUARIO/.virtualenvs/articulacion-venv/bin/python
```

**Solución**:
```bash
# Activar virtualenv
workon articulacion-venv

# O si usas venv estándar:
source venv/bin/activate

# Ahora instalar
pip install -r requirements.txt
```

---

### CAUSA 4: Pip Desactualizado

**Solución**:
```bash
# Actualizar pip primero
pip install --upgrade pip

# Luego instalar requirements
pip install -r requirements.txt
```

---

### CAUSA 5: Problemas con docx2pdf en Linux

`docx2pdf` requiere Microsoft Word o LibreOffice en el sistema.

**Solución - Usar requirements sin docx2pdf**:

```bash
# Crear requirements_linux.txt (sin docx2pdf)
cat > requirements_linux.txt << 'EOF'
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Migrate==4.0.5
Flask-Login==0.6.3
Flask-WTF==1.2.1
WTForms==3.1.1
PyMySQL==1.1.0
cryptography==41.0.7
python-dotenv==1.0.0
Pillow>=10.0.0
reportlab==4.0.7
openpyxl==3.1.2
xlrd==2.0.1
xlwt==1.3.0
email-validator==2.1.0
werkzeug==3.0.1
pandas>=2.0.0
python-docx==1.1.0
PyPDF2==3.0.1
pycryptodome==3.23.0
EOF

# Instalar sin docx2pdf
pip install -r requirements_linux.txt
```

**Nota**: El sistema NO usa docx2pdf en producción, así que es seguro omitirlo.

---

### CAUSA 6: Instalar Paquete por Paquete

Si todo lo demás falla, instala uno por uno:

```bash
pip install Flask==3.0.0
pip install Flask-SQLAlchemy==3.1.1
pip install Flask-Migrate==4.0.5
pip install Flask-Login==0.6.3
pip install Flask-WTF==1.2.1
pip install WTForms==3.1.1
pip install PyMySQL==1.1.0
pip install cryptography==41.0.7
pip install python-dotenv==1.0.0
pip install Pillow>=10.0.0
pip install reportlab==4.0.7
pip install openpyxl==3.1.2
pip install xlrd==2.0.1
pip install xlwt==1.3.0
pip install email-validator==2.1.0
pip install werkzeug==3.0.1
pip install pandas>=2.0.0
pip install python-docx==1.1.0
pip install PyPDF2==3.0.1
pip install pycryptodome==3.23.0
```

---

## 🎯 SOLUCIÓN RECOMENDADA PARA PYTHONANYWHERE

```bash
# 1. Ir al directorio
cd ~/articulacion

# 2. Activar virtualenv
workon articulacion-venv

# 3. Actualizar pip
pip install --upgrade pip

# 4. Verificar que requirements.txt existe
cat requirements.txt

# 5. Instalar requirements
pip install -r requirements.txt

# 6. Si falla con docx2pdf, usar versión sin docx2pdf
pip install Flask==3.0.0 Flask-SQLAlchemy==3.1.1 Flask-Migrate==4.0.5 Flask-Login==0.6.3 Flask-WTF==1.2.1 WTForms==3.1.1 PyMySQL==1.1.0 cryptography==41.0.7 python-dotenv==1.0.0 "Pillow>=10.0.0" reportlab==4.0.7 openpyxl==3.1.2 xlrd==2.0.1 xlwt==1.3.0 email-validator==2.1.0 werkzeug==3.0.1 "pandas>=2.0.0" python-docx==1.1.0 PyPDF2==3.0.1 pycryptodome==3.23.0
```

---

## ✅ VERIFICAR INSTALACIÓN

Después de instalar, verifica:

```bash
# Ver paquetes instalados
pip list

# Verificar que Flask esté instalado
python -c "import flask; print(flask.__version__)"

# Debe mostrar: 3.0.0

# Verificar que SQLAlchemy funciona
python -c "import flask_sqlalchemy; print('OK')"

# Verificar que PyMySQL funciona
python -c "import pymysql; print('OK')"
```

---

## 📋 DEPENDENCIAS MÍNIMAS REQUERIDAS

Si quieres instalar solo lo esencial:

```bash
pip install Flask==3.0.0 \
    Flask-SQLAlchemy==3.1.1 \
    Flask-Login==0.6.3 \
    PyMySQL==1.1.0 \
    python-dotenv==1.0.0 \
    werkzeug==3.0.1
```

Luego instala el resto según necesites.

---

## 🐍 VERIFICAR VERSIÓN DE PYTHON

```bash
python --version
# Debe ser Python 3.8 o superior

# Si no, usar python3
python3 --version
python3 -m pip install -r requirements.txt
```

---

## 💡 TIPS ADICIONALES

### En Windows (Desarrollo Local)

```powershell
# Activar virtualenv
venv\Scripts\activate

# Instalar
pip install -r requirements.txt
```

### En Linux/Mac

```bash
# Activar virtualenv
source venv/bin/activate

# Instalar
pip install -r requirements.txt
```

### En PythonAnywhere

```bash
# Usar workon
workon articulacion-venv

# Instalar con timeout mayor
pip install --timeout=1000 -r requirements.txt
```

---

## 🆘 SI NADA FUNCIONA

Contacta con soporte indicando:

1. Sistema operativo: `uname -a`
2. Versión de Python: `python --version`
3. Versión de pip: `pip --version`
4. Contenido de requirements.txt: `cat requirements.txt`
5. Error completo al instalar

---

## 📞 SOPORTE

- **GitHub Issues**: https://github.com/jquinteroz/Articulacion_SIAM/issues
- **Documentación**: Ver DEPLOY_PYTHONANYWHERE.md
- **Desarrollador**: Johann Quintero (jsquinteroz)

---

**Sistema de Articulación SENA v1.0.0**
**Fecha**: 2025-12-18
