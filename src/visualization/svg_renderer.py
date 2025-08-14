"""
SVG renderer for NFA diagrams (no external dependencies).
"""

from pathlib import Path
from typing import Dict, List, Set, Tuple
from ..core.constants import EPSILON
from ..nfa.models import Fragment, State


def _svg_escape(text: str) -> str:
    """
    Escapa caracteres especiales para SVG.
    
    Args:
        text: Texto a escapar
        
    Returns:
        Texto escapado para SVG
    """
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def draw_nfa_svg(fragment: Fragment, out_path: Path, ascii_labels: bool = False) -> None:
    """
    Dibuja el AFN en un archivo SVG.
    
    Args:
        fragment: Fragmento NFA a dibujar
        out_path: Ruta del archivo SVG de salida
        ascii_labels: Si es True, usa etiquetas ASCII en lugar de Unicode
    """
    # Recopilar todos los estados
    states: List[int] = sorted(
        set(fragment.transitions.keys())
        | {fragment.start.id, fragment.accept.id}
        | {t for lst in fragment.transitions.values() for _, t in lst}
    )
    
    n = len(states)
    cols = min(6, max(3, int((n ** 0.5) * 1.5)))
    cell_w, cell_h = 140, 120
    r = 22
    width = cols * cell_w + 60
    rows = (n + cols - 1) // cols
    height = rows * cell_h + 80

    # Calcular posiciones de los estados
    pos: Dict[int, Tuple[int, int]] = {}
    for i, s in enumerate(states):
        row, col = divmod(i, cols)
        x = 40 + col * cell_w + 40
        y = 40 + row * cell_h + 40
        pos[s] = (x, y)

    def edge_path(x1: int, y1: int, x2: int, y2: int, offset: int = 0) -> str:
        """
        Genera el path SVG para una arista con offset.
        
        Args:
            x1, y1: Coordenadas del punto origen
            x2, y2: Coordenadas del punto destino
            offset: Offset para evitar superposición de aristas
            
        Returns:
            Path SVG para la arista
        """
        cx = (x1 + x2) / 2
        cy = min(y1, y2) - 40 - abs(offset) * 10
        return f"M{x1},{y1} Q{cx},{cy} {x2},{y2}"

    # Construir el SVG
    parts: List[str] = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">')
    
    # Definiciones (flechas)
    parts.append(
        "<defs>"
        '<marker id="arrow" markerWidth="10" markerHeight="10" refX="10" refY="3" orient="auto" markerUnits="strokeWidth">'
        '<path d="M0,0 L0,6 L9,3 z" />'
        "</marker>"
        "</defs>"
    )

    # Dibujar aristas
    drawn: Set[Tuple[int, int, str, int]] = set()
    for a, lst in fragment.transitions.items():
        for k, (sym, b) in enumerate(lst):
            x1, y1 = pos[a]
            x2, y2 = pos[b]
            
            if a == b:  # Auto-loop
                loop_r = r + 8 + 6 * k
                path = f"M{x1},{y1 - r} C{x1 - loop_r},{y1 - loop_r*2} {x1 + loop_r},{y1 - loop_r*2} {x1},{y1 - r}"
                parts.append(f'<path d="{path}" fill="none" stroke="black" marker-end="url(#arrow)"/>')
                
                label = "eps" if (sym is None and ascii_labels) else (EPSILON if sym is None else sym)
                parts.append(f'<text x="{x1}" y="{y1 - loop_r*2 - 5}" text-anchor="middle" font-size="12">{_svg_escape(label)}</text>')
            else:  # Arista normal
                key = (a, b, sym, k)
                if key in drawn:
                    continue
                drawn.add(key)
                
                path = edge_path(x1, y1, x2, y2, offset=k)
                parts.append(f'<path d="{path}" fill="none" stroke="black" marker-end="url(#arrow)"/>')
                
                label = "eps" if (sym is None and ascii_labels) else (EPSILON if sym is None else sym)
                lx = (x1 + x2) / 2
                ly = min(y1, y2) - 40 - abs(k) * 10
                parts.append(f'<text x="{lx}" y="{ly}" text-anchor="middle" font-size="12">{_svg_escape(label)}</text>')

    # Dibujar estados
    for s in states:
        x, y = pos[s]
        is_accept = s == fragment.accept.id
        
        # Círculo del estado
        parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" stroke="black" fill="white"/>')
        
        # Círculo doble para estado de aceptación
        if is_accept:
            parts.append(f'<circle cx="{x}" cy="{y}" r="{r-5}" stroke="black" fill="none"/>')
        
        # Etiqueta del estado
        parts.append(f'<text x="{x}" y="{y+4}" text-anchor="middle" font-size="12">q{s}</text>')

    # Flecha de inicio
    sx, sy = pos[fragment.start.id]
    parts.append(f'<line x1="{sx-40}" y1="{sy}" x2="{sx - r}" y2="{sy}" stroke="black" marker-end="url(#arrow)"/>')
    parts.append(f'<text x="{sx-52}" y="{sy-8}" font-size="12">start</text>')

    parts.append("</svg>")
    
    # Escribir el archivo SVG
    out_path.write_text("\n".join(parts), encoding="utf-8") 