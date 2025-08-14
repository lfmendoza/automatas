"""
Automatas - Teoría de la Computación
====================================

Paquete para crear y simular AFNs construidos con el algoritmo de Thompson
a partir de expresiones regulares.

Módulos principales:
- core: Constantes, tipos y excepciones base
- regex: Parsing y normalización de expresiones regulares
- nfa: Construcción y simulación de autómatas finitos no deterministas
- visualization: Generación de diagramas SVG
- utils: Utilidades de codificación y compatibilidad
- cli: Interfaz de línea de comandos
"""

__version__ = "1.0.0"
__author__ = "Fernando Mendoza"
__license__ = "MIT"

from .core.constants import *
from .core.types import *
from .core.exceptions import *
from .regex.normalizer import normalize_regex
from .regex.postfix_converter import insert_concat_ops, to_postfix
from .nfa.thompson import *
from .nfa.simulator import *
from .visualization.svg_renderer import *

__all__ = [
    # Core
    "OPERATORS",
    "UNARY", 
    "PRECEDENCE",
    "EPSILON",
    "Symbol",
    "StateId",
    "Transition",
    "TransitionMap",
    "MutableTransitionMap",
    "RegexSyntaxError",
    
    # Regex
    "normalize_regex",
    "insert_concat_ops", 
    "to_postfix",
    
    # NFA
    "State",
    "Fragment",
    "ThompsonNFA",
    "NFASimulator",
    
    # Visualization
    "draw_nfa_svg",
] 