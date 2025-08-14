"""
Regular expression normalization utilities.
"""

from ..core.constants import EPSILON


def normalize_regex(expr: str) -> str:
    """
    Normaliza la ER: quita espacios y unifica epsilon en "ε".
    Acepta "eps", "epsilon", "EPS", "EPSILON" y "(e)".
    
    Args:
        expr: Expresión regular a normalizar
        
    Returns:
        Expresión regular normalizada
    """
    s = "".join(ch for ch in expr.strip() if not ch.isspace())
    s = (
        s.replace("EPSILON", EPSILON)
        .replace("EPS", EPSILON)
        .replace("epsilon", EPSILON)
        .replace("eps", EPSILON)
        .replace("(e)", f"({EPSILON})")
    )
    return s 