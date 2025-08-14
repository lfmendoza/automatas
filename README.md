# Laboratorio 4

Este demo crea y simula AFNs construidos con el algoritmo de Thompson a partir de expresiones regulares.

## 1) Requisitos

- Python 3.8+ instalado.
- **No** requiere librerías externas.

## 2) Archivos provistos

- `lab4.py` — Script principal (solo librerías estándar).
- `expresiones.txt` — Archivo de ejemplo con una ER por línea (las del enunciado).
- Directorio de salida: `./output/` (se crea automáticamente) con imágenes SVG de los AFNs.

## 3) Ejecutar

Desde el directorio donde están los archivos:

```bash
python lab4.py --input expresiones.txt --word abba --outdir output --ascii
```

- Genera `output/afn_01.svg`, `output/afn_02.svg`, etc.
- Imprime por consola **sí**/**no** según si `w` pertenece al lenguaje de cada ER.

Pruebas sugeridas para el video (una por expresión del enunciado):

1. ER: `(a*|b*)+`
   - `--word aaaa` → **sí**
   - `--word ab` → **no** (porque obliga a bloques homogéneos, no mezcla)
2. ER: `((ε|a)|b*)*`
   - `--word ""` (cadena vacía) → **sí**
   - `--word bbbba` → **sí**
3. ER: `(a|b)*abb(a|b)*`
   - `--word abb` → **sí**
   - `--word ababa` → **sí** (contiene `abb` como subcadena)
   - `--word ababaabb` → **sí**
   - `--word aba` → **no**
4. ER: `0?(1?)?0*`
   - `--word ""` → **sí**
   - `--word 0` → **sí**
   - `--word 10` → **sí**
   - `--word 110` → **no**
   - `--word 001` → **no**

> Nota: el script acepta `ε` como símbolo de epsilon (también `eps` o `epsilon`).

## 4) ¿Dónde están las imágenes?

Se guardan en el directorio indicado con `--outdir` (por defecto `./output`). Son archivos **SVG** que puedes abrir en el navegador (Chrome/Firefox) para mostrarlos en el video.

## 5) Errores comunes

- **Paréntesis desbalanceados**: el parser lo detecta.
- **Espacios**: el script los ignora automáticamente.
- **Epsilon**: usa `ε`, `eps` o `epsilon`.

¡Éxitos en tu presentación!
