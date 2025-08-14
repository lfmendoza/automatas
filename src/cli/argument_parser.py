"""
Command-line argument parser for the automata CLI.
"""

import argparse
from pathlib import Path


def build_argument_parser() -> argparse.ArgumentParser:
    """
    Construye y configura el parser de argumentos de línea de comandos.
    
    Returns:
        Parser de argumentos configurado
    """
    parser = argparse.ArgumentParser(
        description="AFN (Thompson) + Simulación + SVG",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python main.py --input expresiones.txt --word abba --outdir output
  python main.py --input expresiones.txt --word "" --ascii
  python main.py --input expresiones.txt --word 1010 --outdir ./diagrams
        """
    )
    
    parser.add_argument(
        "--input", 
        required=True, 
        type=Path, 
        help="Archivo con una ER por línea"
    )
    
    parser.add_argument(
        "--word", 
        required=True, 
        help="Palabra w a evaluar contra cada ER"
    )
    
    parser.add_argument(
        "--outdir", 
        default=Path("./output"), 
        type=Path, 
        help="Directorio de salida para los SVG (default: ./output)"
    )
    
    parser.add_argument(
        "--ascii", 
        action="store_true", 
        help="Salida sin tildes y etiquetas 'eps' en vez de 'ε'"
    )
    
    return parser 