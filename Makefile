.PHONY: help install test clean format lint type-check run-example

help:  ## Mostrar esta ayuda
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Instalar el paquete en modo desarrollo
	pip install -e .

test:  ## Ejecutar las pruebas
	python -m pytest tests/ -v

clean:  ## Limpiar archivos generados
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf __pycache__/
	rm -rf src/__pycache__/
	rm -rf src/*/__pycache__/
	rm -rf tests/__pycache__/
	rm -rf tests/*/__pycache__/
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

format:  ## Formatear código con black
	black src/ tests/ main.py

lint:  ## Verificar estilo con flake8
	flake8 src/ tests/ main.py

type-check:  ## Verificar tipos con mypy
	mypy src/ main.py

run-example:  ## Ejecutar ejemplo básico
	python main.py --input examples/expresiones.txt --word abba --outdir output --ascii

build:  ## Construir el paquete
	python setup.py sdist bdist_wheel

install-dev:  ## Instalar dependencias de desarrollo
	pip install -e ".[dev]" 