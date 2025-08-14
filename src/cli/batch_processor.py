"""
Batch processor for multiple regular expressions.
"""

from pathlib import Path
from typing import Iterable, List, Tuple
from ..regex.normalizer import normalize_regex
from ..regex.postfix_converter import insert_concat_ops, to_postfix
from ..nfa.thompson import ThompsonNFA
from ..nfa.simulator import NFASimulator
from ..visualization.svg_renderer import draw_nfa_svg


def run_batch(
    regex_lines: Iterable[str], 
    word: str, 
    outdir: Path, 
    ascii_labels: bool = False
) -> List[Tuple[str, bool, Path]]:
    """
    Procesa una lista de ERs, genera SVG para cada una y evalúa la palabra `word`.
    
    Args:
        regex_lines: Iterable de líneas con expresiones regulares
        word: Palabra a evaluar contra cada ER
        outdir: Directorio de salida para los archivos SVG
        ascii_labels: Si es True, usa etiquetas ASCII en lugar de Unicode
        
    Returns:
        Lista de tuplas (regex_original, aceptada, ruta_svg)
    """
    # Crear directorio de salida si no existe
    outdir.mkdir(parents=True, exist_ok=True)
    
    results: List[Tuple[str, bool, Path]] = []
    
    # Procesar cada expresión regular
    for i, raw in enumerate(
        (line for line in (ln.strip() for ln in regex_lines) if line), 
        start=1
    ):
        try:
            # Normalizar y convertir la ER
            reg = insert_concat_ops(normalize_regex(raw))
            postfix = to_postfix(reg)
            
            # Construir el NFA
            frag = ThompsonNFA().build_from_postfix(postfix)
            
            # Generar SVG
            svg_path = outdir / f"afn_{i:02d}.svg"
            draw_nfa_svg(frag, svg_path, ascii_labels=ascii_labels)
            
            # Evaluar la palabra
            ok = NFASimulator(frag).accepts(word)
            
            results.append((raw, ok, svg_path))
            
        except Exception as e:
            # En caso de error, agregar resultado con error
            svg_path = outdir / f"afn_{i:02d}_error.svg"
            results.append((raw, False, svg_path))
            # TODO: Log del error
    
    return results 