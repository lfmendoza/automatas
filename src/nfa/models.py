"""
Data models for NFA components.
"""

from dataclasses import dataclass
from typing import Mapping, Sequence
from ..core.types import StateId, Transition, TransitionMap


@dataclass(frozen=True)
class State:
    """
    Estado del AFN (identificador entero).
    
    Attributes:
        id: Identificador único del estado
    """
    id: StateId


@dataclass(frozen=True)
class Fragment:
    """
    Fragmento de NFA con estado inicial y de aceptación y su mapa de transiciones.
    
    Attributes:
        start: Estado inicial del fragmento
        accept: Estado de aceptación del fragmento
        transitions: Mapa de transiciones del fragmento
    """
    start: State
    accept: State
    transitions: TransitionMap 