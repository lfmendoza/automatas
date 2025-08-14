"""
NFA simulator with epsilon closure and symbol transitions.
"""

from typing import Set
from ..core.types import StateId, TransitionMap
from .models import Fragment


class NFASimulator:
    """
    Simulador de AFN con cierres epsilon y movimientos por símbolo.
    
    Esta clase implementa la simulación de autómatas finitos no deterministas,
    incluyendo el manejo de transiciones epsilon y la evaluación de cadenas.
    """

    __slots__ = ("_start", "_accept", "_trans")

    def __init__(self, fragment: Fragment) -> None:
        """
        Inicializa el simulador con un fragmento NFA.
        
        Args:
            fragment: Fragmento NFA a simular
        """
        self._start: StateId = fragment.start.id
        self._accept: StateId = fragment.accept.id
        self._trans: TransitionMap = fragment.transitions

    def _epsilon_closure(self, states: Set[StateId]) -> Set[StateId]:
        """
        Calcula el cierre epsilon de un conjunto de estados.
        
        Args:
            states: Conjunto de estados inicial
            
        Returns:
            Conjunto de estados alcanzables por transiciones epsilon
        """
        stack = list(states)
        closure = set(states)
        
        while stack:
            s = stack.pop()
            for sym, t in self._trans.get(s, ()):
                if sym is None and t not in closure:  # Transición epsilon
                    closure.add(t)
                    stack.append(t)
        
        return closure

    def _move(self, states: Set[StateId], sym: str) -> Set[StateId]:
        """
        Calcula los estados alcanzables desde un conjunto de estados
        mediante transiciones con un símbolo específico.
        
        Args:
            states: Conjunto de estados origen
            sym: Símbolo de la transición
            
        Returns:
            Conjunto de estados destino
        """
        out: Set[StateId] = set()
        
        for s in states:
            for label, t in self._trans.get(s, ()):
                if label == sym:
                    out.add(t)
        
        return out

    def accepts(self, w: str) -> bool:
        """
        Decide si el AFN acepta la palabra w.
        
        Args:
            w: Palabra a evaluar
            
        Returns:
            True si la palabra es aceptada, False en caso contrario
        """
        # Estado inicial con cierre epsilon
        current = self._epsilon_closure({self._start})
        
        # Procesar cada símbolo de la palabra
        for ch in w:
            # Mover por el símbolo y calcular cierre epsilon
            current = self._epsilon_closure(self._move(current, ch))
            
            # Si no hay estados activos, la palabra es rechazada
            if not current:
                return False
        
        # Verificar si algún estado activo es de aceptación
        return self._accept in current 