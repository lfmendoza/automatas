# Automatas - Teoría de la Computación

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Este proyecto implementa la construcción y simulación de autómatas finitos no deterministas (NFA) usando el algoritmo de Thompson a partir de expresiones regulares, siguiendo principios de ingeniería de software de empresas tecnológicas grandes.

## 🚀 Características

- **Algoritmo de Thompson**: Construcción eficiente de NFA desde expresiones regulares
- **Simulación de NFA**: Evaluación de cadenas con soporte para transiciones epsilon
- **Generación de Diagramas**: Visualización automática en formato SVG
- **Arquitectura Modular**: Código desacoplado y fácilmente extensible
- **Sin Dependencias Externas**: Solo utiliza la biblioteca estándar de Python
- **Testing Completo**: Suite de pruebas con cobertura alta
- **Herramientas de Desarrollo**: Formateo, linting y verificación de tipos automática

## 📁 Estructura del Proyecto

```
automatas/
├── src/                    # Código fuente principal
│   ├── core/              # Constantes, tipos y excepciones base
│   ├── regex/             # Parsing y procesamiento de expresiones regulares
│   ├── nfa/               # Construcción y simulación de NFA
│   ├── visualization/     # Generación de diagramas SVG
│   ├── utils/             # Utilidades de codificación y compatibilidad
│   └── cli/               # Interfaz de línea de comandos
├── tests/                 # Suite de pruebas
├── examples/              # Ejemplos de uso
├── output/                # Archivos de salida generados
├── docs/                  # Documentación adicional
├── main.py                # Punto de entrada principal
├── setup.py               # Configuración de instalación
├── pyproject.toml         # Configuración moderna de Python
└── Makefile               # Automatización de tareas
```

## 🛠️ Instalación

### Requisitos

- Python 3.8 o superior
- Git (para clonar el repositorio)

### Instalación desde Fuente

```bash
# Clonar el repositorio
git clone https://github.com/automatas/automatas.git
cd automatas

# Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar en modo desarrollo
pip install -e .

# O instalar con dependencias de desarrollo
make install-dev
```

### Instalación Rápida

```bash
# Instalar directamente
pip install git+https://github.com/automatas/automatas.git
```

## 🚀 Uso Rápido

### Ejemplo Básico

```bash
# Procesar expresiones regulares desde un archivo
python main.py --input examples/expresiones.txt --word abba --outdir output
```

### Ejemplos de Expresiones Regulares

El archivo `examples/expresiones.txt` contiene ejemplos para probar:

1. **`(a*|b*)+`** - Bloques homogéneos de a's o b's
2. **`((ε|a)|b*)*`** - Cadenas que pueden contener a's y b's
3. **`(a|b)*abb(a|b)*`** - Cadenas que contienen "abb" como subcadena
4. **`0?(1?)?0*`** - Patrón específico de ceros y unos

### Pruebas Sugeridas

```bash
# ER: (a*|b*)+
python main.py --input examples/expresiones.txt --word aaaa --outdir output
python main.py --input examples/expresiones.txt --word ab --outdir output

# ER: ((ε|a)|b*)*
python main.py --input examples/expresiones.txt --word "" --outdir output
python main.py --input examples/expresiones.txt --word bbbba --outdir output

# ER: (a|b)*abb(a|b)*
python main.py --input examples/expresiones.txt --word abb --outdir output
python main.py --input examples/expresiones.txt --word ababa --outdir output
```

## 📖 Uso Detallado

### Argumentos de Línea de Comandos

```bash
python main.py [OPCIONES]

Opciones:
  --input INPUT           Archivo con una ER por línea (requerido)
  --word WORD            Palabra w a evaluar contra cada ER (requerido)
  --outdir OUTDIR        Directorio de salida para los SVG (default: ./output)
  --ascii                Salida sin tildes y etiquetas 'eps' en vez de 'ε'
  -h, --help            Mostrar mensaje de ayuda
```

### Ejemplos de Uso

```bash
# Generar diagramas SVG con etiquetas Unicode
python main.py --input expresiones.txt --word "hello" --outdir diagrams

# Usar etiquetas ASCII para compatibilidad
python main.py --input expresiones.txt --word "test" --ascii

# Especificar directorio de salida personalizado
python main.py --input expresiones.txt --word "example" --outdir ./my_diagrams
```

## 🧪 Testing y Desarrollo

### Ejecutar Pruebas

```bash
# Ejecutar todas las pruebas
make test

# Ejecutar con cobertura
pytest tests/ -v --cov=src

# Ejecutar pruebas específicas
pytest tests/test_regex/ -v
```

### Verificación de Calidad

```bash
# Formatear código
make format

# Verificar estilo
make lint

# Verificar tipos
make type-check

# Limpiar archivos generados
make clean
```

### Configuración de Pre-commit

```bash
# Instalar pre-commit hooks
pre-commit install

# Ejecutar manualmente
pre-commit run --all-files
```

## 🏗️ Arquitectura

### Principios de Diseño

- **Separación de Responsabilidades**: Cada módulo tiene una función específica
- **Inversión de Dependencias**: Módulos de alto nivel no dependen de implementaciones
- **Principio de Responsabilidad Única**: Cada clase tiene una sola razón para cambiar
- **Open/Closed Principle**: Extensible sin modificar código existente

### Módulos Principales

- **Core**: Definiciones base, tipos y excepciones
- **Regex**: Normalización y conversión a notación postfija
- **NFA**: Construcción Thompson y simulación
- **Visualization**: Generación de diagramas SVG
- **CLI**: Interfaz de línea de comandos

## 📊 Salida

### Archivos SVG Generados

El programa genera diagramas SVG para cada expresión regular:
- `afn_01.svg` - Primera expresión regular
- `afn_02.svg` - Segunda expresión regular
- etc.

### Formato de Salida

```
[1] ER: (a*|b*)+
    SVG: output/afn_01.svg
    w = 'abba' -> no

[2] ER: ((ε|a)|b*)*
    SVG: output/afn_02.svg
    w = 'abba' -> sí
```

## 🔧 Configuración

### Variables de Entorno

```bash
# Configurar codificación (opcional)
export PYTHONIOENCODING=utf-8
```

### Configuración de IDE

El proyecto incluye configuraciones para:
- **VS Code**: Configuración automática de Python, testing y linting
- **PyCharm**: Configuración de proyecto y testing
- **Vim/Neovim**: Configuración de LSP y formateo

## 🐛 Solución de Problemas

### Errores Comunes

1. **"No module named 'src'"**: Asegúrate de estar en el directorio raíz del proyecto
2. **"FileNotFoundError"**: Verifica que el archivo de entrada existe
3. **"UnicodeError"**: Asegúrate de que el archivo esté en UTF-8

### Logs y Debugging

```bash
# Ejecutar con más información
python -v main.py --input examples/expresiones.txt --word test

# Verificar estructura del proyecto
tree src/  # o dir src/ en Windows
```

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Consulta [CONTRIBUTING.md](CONTRIBUTING.md) para detalles sobre:

- Configuración del entorno de desarrollo
- Estándares de código
- Proceso de Pull Request
- Guías de testing

## 📚 Documentación Adicional

- [ARCHITECTURE.md](ARCHITECTURE.md) - Documentación detallada de la arquitectura
- [CONTRIBUTING.md](CONTRIBUTING.md) - Guía de contribución
- [Ejemplos](examples/) - Casos de uso y expresiones de prueba

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.
