# Guía de Contribución

¡Gracias por tu interés en contribuir al proyecto Automatas!

## Cómo Contribuir

### 1. Configuración del Entorno

```bash
# Clonar el repositorio
git clone https://github.com/automatas/automatas.git
cd automatas

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias de desarrollo
make install-dev
```

### 2. Estructura del Proyecto

- **src/**: Código fuente principal
- **tests/**: Pruebas unitarias e integración
- **examples/**: Ejemplos de uso
- **docs/**: Documentación adicional

### 3. Estándares de Código

#### Formato
- Usar **Black** para formateo automático
- Longitud de línea máxima: 88 caracteres
- Docstrings en formato Google/NumPy

#### Linting
- **Flake8** para verificación de estilo
- **MyPy** para verificación de tipos
- **Pre-commit hooks** configurados automáticamente

#### Ejecutar verificaciones
```bash
make format      # Formatear código
make lint        # Verificar estilo
make type-check  # Verificar tipos
```

### 4. Escribiendo Pruebas

- Cada nuevo módulo debe tener pruebas correspondientes
- Usar **pytest** como framework de testing
- Meta de cobertura: 90%+

```bash
make test        # Ejecutar todas las pruebas
pytest tests/ -v --cov=src  # Con cobertura
```

### 5. Flujo de Trabajo

#### 1. Crear una rama
```bash
git checkout -b feature/nueva-funcionalidad
```

#### 2. Hacer cambios
- Escribir código siguiendo estándares
- Agregar pruebas para nueva funcionalidad
- Actualizar documentación si es necesario

#### 3. Verificar calidad
```bash
make format
make lint
make type-check
make test
```

#### 4. Commit y Push
```bash
git add .
git commit -m "feat: agregar nueva funcionalidad"
git push origin feature/nueva-funcionalidad
```

#### 5. Crear Pull Request
- Describir cambios claramente
- Referenciar issues relacionados
- Asegurar que todas las pruebas pasen

### 6. Convenciones de Commit

Usar [Conventional Commits](https://www.conventionalcommits.org/):

- **feat**: Nueva funcionalidad
- **fix**: Corrección de bug
- **docs**: Cambios en documentación
- **style**: Cambios de formato
- **refactor**: Refactorización de código
- **test**: Agregar o modificar pruebas
- **chore**: Tareas de mantenimiento

### 7. Reportando Bugs

Usar el template de issue y incluir:
- Descripción del problema
- Pasos para reproducir
- Comportamiento esperado vs actual
- Información del sistema
- Capturas de pantalla si aplica

### 8. Sugiriendo Mejoras

Para nuevas funcionalidades:
- Describir el caso de uso
- Explicar beneficios
- Proponer implementación si es posible
- Considerar impacto en código existente

### 9. Revisión de Código

#### Como Autor
- Responder a comentarios de revisión
- Hacer cambios solicitados
- Mantener conversación constructiva

#### Como Revisor
- Ser constructivo y respetuoso
- Enfocarse en el código, no en la persona
- Sugerir alternativas cuando sea apropiado

### 10. Recursos Adicionales

- **Documentación**: `README.md`, `ARCHITECTURE.md`
- **Issues**: Para reportar bugs y sugerir mejoras
- **Discussions**: Para preguntas y discusiones generales

### 11. Reconocimiento

Los contribuyentes serán reconocidos en:
- Archivo `CONTRIBUTORS.md`
- README del proyecto
- Releases de GitHub

## ¿Necesitas Ayuda?

- Abrir un issue para preguntas
- Usar Discussions para discusiones generales
- Contactar al equipo de mantenimiento

¡Gracias por contribuir a hacer Automatas mejor! 