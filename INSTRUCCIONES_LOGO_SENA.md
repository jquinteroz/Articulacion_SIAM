# Instrucciones para Quitar el Fondo del Logo SENA

El logo SENA actual tiene fondo blanco. Para tener un logo profesional con fondo transparente, sigue estos pasos:

## Opción 1: Online (Más Rápido)

### Usando remove.bg
1. Ve a https://www.remove.bg/
2. Sube el archivo `app/static/img/sena.png`
3. Descarga la versión sin fondo
4. Guárdalo como `sena.png` en `app/static/img/`

### Usando PhotoScissors
1. Ve a https://photoscissors.com/
2. Sube el logo
3. Descarga PNG con transparencia
4. Reemplaza el archivo actual

## Opción 2: Con Photoshop/GIMP

### Photoshop
1. Abre `sena.png`
2. Usa "Magic Wand Tool" (W)
3. Click en el fondo blanco
4. Delete
5. Guardar como PNG (File > Export > Save for Web)
6. Asegurar que "Transparency" esté marcado

### GIMP (Gratis)
1. Abre `sena.png`
2. Layer > Transparency > Add Alpha Channel
3. Herramienta "Select by Color"
4. Click en el fondo blanco
5. Delete
6. Export As PNG

## Opción 3: Usar el Logo Oficial SENA

El logo oficial del SENA ya viene con fondo transparente:
- Descarga desde: https://www.sena.edu.co/
- O usa el logo vectorial (SVG/EPS) oficial

## Resultado Esperado

✅ Formato: PNG
✅ Fondo: Transparente
✅ Tamaño recomendado: 500x500px o similar
✅ Resolución: 72-150 DPI

---

Una vez tengas el logo sin fondo, reemplaza el archivo en:
`app/static/img/sena.png`

Y el sistema automáticamente lo usará en todas las páginas.
