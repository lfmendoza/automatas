# Arquitectura del Proyecto Automatas

## Visión General

Este proyecto implementa la construcción y simulación de autómatas finitos no deterministas (NFA) usando el algoritmo de Thompson, siguiendo principios de ingeniería de software de empresas tecnológicas grandes.

## Estructura de Directorios

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
└── docs/                  # Documentación adicional
```

## Principios de Diseño

### 1. Separación de Responsabilidades (SRP)
- **Core**: Definiciones base y tipos
- **Regex**: Procesamiento de expresiones regulares
- **NFA**: Lógica de autómatas
- **Visualization**: Generación de diagramas
- **CLI**: Interfaz de usuario

### 2. Inversión de Dependencias (DIP)
- Los módulos de alto nivel no dependen de implementaciones específicas
- Uso de interfaces y tipos abstractos
- Inyección de dependencias a través de constructores

### 3. Principio de Responsabilidad Única
- Cada clase tiene una sola razón para cambiar
- Métodos pequeños y enfocados
- Cohesión alta, acoplamiento bajo

### 4. Open/Closed Principle
- Extensible para nuevas funcionalidades
- Cerrado para modificaciones existentes
- Uso de herencia y composición

## Módulos Principales

### Core Module
- **constants.py**: Constantes globales del sistema
- **types.py**: Definiciones de tipos TypeScript
- **exceptions.py**: Jerarquía de excepciones personalizadas

### Regex Module
- **normalizer.py**: Normalización de expresiones regulares
- **postfix_converter.py**: Conversión a notación postfija

### NFA Module
- **models.py**: Modelos de datos (State, Fragment)
- **thompson.py**: Algoritmo de construcción de Thompson
- **simulator.py**: Simulación de NFA

### Visualization Module
- **svg_renderer.py**: Generación de diagramas SVG

### CLI Module
- **argument_parser.py**: Parsing de argumentos de línea de comandos
- **batch_processor.py**: Procesamiento por lotes

## Patrones de Diseño Utilizados

### 1. Factory Pattern
- `ThompsonNFA` actúa como fábrica para crear fragmentos NFA

### 2. Strategy Pattern
- Diferentes estrategias de renderizado (SVG, ASCII)

### 3. Builder Pattern
- Construcción paso a paso de autómatas

### 4. Command Pattern
- Procesamiento por lotes de expresiones regulares

## Manejo de Errores

- **RegexSyntaxError**: Errores de sintaxis en expresiones regulares
- Manejo robusto de archivos de entrada
- Logging de errores para debugging
- Códigos de salida apropiados

## Testing Strategy

- **Unit Tests**: Pruebas individuales de cada módulo
- **Integration Tests**: Pruebas de flujo completo
- **Property-Based Testing**: Para validar propiedades matemáticas
- **Coverage**: Meta de cobertura del 90%+

## Configuración y Despliegue

- **setup.py**: Configuración de instalación
- **pyproject.toml**: Configuración moderna de Python
- **Makefile**: Automatización de tareas comunes
- **Pre-commit hooks**: Calidad de código automática

## Escalabilidad

### 1. Modularidad
- Fácil agregar nuevos algoritmos de construcción
- Soporte para diferentes formatos de salida
- Extensibilidad para nuevos tipos de autómatas

### 2. Performance
- Algoritmos optimizados para NFA grandes
- Lazy evaluation donde sea apropiado
- Caching de resultados intermedios

### 3. Mantenibilidad
- Código bien documentado
- Estándares de codificación consistentes
- Refactoring automático con herramientas

## Monitoreo y Logging

- Logging estructurado para debugging
- Métricas de performance
- Trazabilidad de operaciones
- Manejo de errores robusto

## Seguridad

- Validación de entrada robusta
- Sanitización de archivos SVG
- Manejo seguro de rutas de archivo
- Prevención de ataques de inyección

## Documentación

- Docstrings en formato Google/NumPy
- README detallado con ejemplos
- Documentación de API
- Guías de contribución 