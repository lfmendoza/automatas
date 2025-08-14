#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teoría de la Computación — Thompson NFA + Simulación + SVG

Este es el punto de entrada principal para la aplicación de autómatas.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional, Sequence

from src.utils.encoding import configure_encoding
from src.cli.argument_parser import build_argument_parser
from src.cli.batch_processor import run_batch


def main(argv: Optional[Sequence[str]] = None) -> int:
    """
    Función principal de la aplicación.
    
    Args:
        argv: Argumentos de línea de comandos (opcional)
        
    Returns:
        Código de salida (0 para éxito, otros para error)
    """
    # Configurar codificación UTF-8
    configure_encoding()
    
    # Parsear argumentos
    args = build_argument_parser().parse_args(argv)
    
    try:
        # Leer archivo de entrada
        lines = args.input.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        print(f"ERROR: No se encontró el archivo {args.input!s}", file=sys.stderr)
        return 2
    except UnicodeError:
        print("ERROR: El archivo de entrada debe estar codificado en UTF-8.", file=sys.stderr)
        return 2

    # Procesar expresiones regulares
    try:
        results = run_batch(lines, args.word, args.outdir, ascii_labels=args.ascii)
    except Exception as e:
        print(f"ERROR: Error durante el procesamiento: {e}", file=sys.stderr)
        return 1

    # Mostrar resultados
    had_error = False
    for idx, (raw, ok, svg) in enumerate(results, start=1):
        verdict = ("si" if args.ascii else "sí") if ok else "no"
        print(f"[{idx}] ER: {raw}")
        print(f"    SVG: {svg}")
        print(f"    w = {args.word!r} -> {verdict}")
        
        # Verificar si hubo errores (SVG con "_error" en el nombre)
        if "_error" in svg.name:
            had_error = True

    return 2 if had_error else 0


if __name__ == "__main__":
    raise SystemExit(main()) 