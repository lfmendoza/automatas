"""
Thompson NFA construction algorithm implementation.
"""

from collections import defaultdict
from typing import List, DefaultDict
from ..core.constants import UNARY, EPSILON
from ..core.exceptions import RegexSyntaxError
from ..core.types import Symbol, StateId, Transition, TransitionMap, MutableTransitionMap
from .models import State, Fragment


class ThompsonNFA:
    """
    Constructor de AFN por el algoritmo de Thompson.
    
    Esta clase implementa el algoritmo de Thompson para construir autómatas
    finitos no deterministas a partir de expresiones regulares en notación postfija.
    """

    __slots__ = ("_next_id",)

    def __init__(self) -> None:
        """Inicializa el constructor de Thompson NFA."""
        self._next_id: StateId = 0

    def _new_state(self) -> State:
        """
        Crea un nuevo estado con un identificador único.
        
        Returns:
            Nuevo estado con identificador único
        """
        sid = self._next_id
        self._next_id += 1
        return State(sid)

    @staticmethod
    def _add(trans: MutableTransitionMap, a: StateId, sym: Symbol, b: StateId) -> None:
        """
        Agrega una transición al mapa de transiciones.
        
        Args:
            trans: Mapa de transiciones mutable
            a: Estado origen
            sym: Símbolo de la transición (None para epsilon)
            b: Estado destino
        """
        trans[a].append((sym, b))

    @staticmethod
    def _freeze(trans: MutableTransitionMap) -> TransitionMap:
        """
        Convierte un mapa de transiciones mutable a inmutable.
        
        Args:
            trans: Mapa de transiciones mutable
            
        Returns:
            Mapa de transiciones inmutable
        """
        return {k: tuple(v) for k, v in trans.items()}

    def build_from_postfix(self, postfix: str) -> Fragment:
        """
        Construye un AFN a partir de la ER en notación postfija.
        
        Args:
            postfix: Expresión regular en notación postfija
            
        Returns:
            Fragmento NFA construido
            
        Raises:
            RegexSyntaxError: Si la expresión regular es inválida
        """
        stack: List[Fragment] = []
        
        for ch in postfix:
            if ch in UNARY or ch in (".", "|"):
                if ch in UNARY:
                    if not stack:
                        raise RegexSyntaxError("Operador unario sin operando")
                    stack.append(self._apply_unary(ch, stack.pop()))
                elif ch == ".":
                    if len(stack) < 2:
                        raise RegexSyntaxError("Concatenación sin operandos")
                    b, a = stack.pop(), stack.pop()
                    stack.append(self._concat(a, b))
                else:  # '|'
                    if len(stack) < 2:
                        raise RegexSyntaxError("Unión sin operandos")
                    b, a = stack.pop(), stack.pop()
                    stack.append(self._union(a, b))
            else:
                stack.append(self._symbol(ch))
        
        if len(stack) != 1:
            raise RegexSyntaxError("ER inválida (sobran operandos/u operadores)")
        
        return stack[0]

    def _symbol(self, ch: str) -> Fragment:
        """
        Crea un fragmento NFA para un símbolo individual.
        
        Args:
            ch: Símbolo del alfabeto
            
        Returns:
            Fragmento NFA para el símbolo
        """
        s, t = self._new_state(), self._new_state()
        trans: DefaultDict[StateId, List[Transition]] = defaultdict(list)
        label: Symbol = None if ch == EPSILON else ch
        self._add(trans, s.id, label, t.id)
        return Fragment(s, t, self._freeze(trans))

    def _concat(self, a: Fragment, b: Fragment) -> Fragment:
        """
        Concatena dos fragmentos NFA.
        
        Args:
            a: Primer fragmento
            b: Segundo fragmento
            
        Returns:
            Fragmento NFA concatenado
        """
        trans: DefaultDict[StateId, List[Transition]] = defaultdict(list)
        
        # Copiar transiciones del primer fragmento
        for src, lst in a.transitions.items():
            trans[src].extend(lst)
        
        # Copiar transiciones del segundo fragmento
        for src, lst in b.transitions.items():
            trans[src].extend(lst)
        
        # Conectar estados de aceptación
        self._add(trans, a.accept.id, None, b.start.id)
        
        return Fragment(a.start, b.accept, self._freeze(trans))

    def _union(self, a: Fragment, b: Fragment) -> Fragment:
        """
        Une dos fragmentos NFA.
        
        Args:
            a: Primer fragmento
            b: Segundo fragmento
            
        Returns:
            Fragmento NFA unido
        """
        s, t = self._new_state(), self._new_state()
        trans: DefaultDict[StateId, List[Transition]] = defaultdict(list)
        
        # Copiar transiciones de ambos fragmentos
        for src, lst in a.transitions.items():
            trans[src].extend(lst)
        for src, lst in b.transitions.items():
            trans[src].extend(lst)
        
        # Conectar estados iniciales
        self._add(trans, s.id, None, a.start.id)
        self._add(trans, s.id, None, b.start.id)
        
        # Conectar estados de aceptación
        self._add(trans, a.accept.id, None, t.id)
        self._add(trans, b.accept.id, None, t.id)
        
        return Fragment(s, t, self._freeze(trans))

    def _apply_unary(self, op: str, f: Fragment) -> Fragment:
        """
        Aplica un operador unario a un fragmento NFA.
        
        Args:
            op: Operador unario ('*', '+', '?')
            f: Fragmento al que aplicar el operador
            
        Returns:
            Fragmento NFA con el operador aplicado
            
        Raises:
            RegexSyntaxError: Si el operador es desconocido
        """
        s, t = self._new_state(), self._new_state()
        trans: DefaultDict[StateId, List[Transition]] = defaultdict(list)
        
        # Copiar transiciones del fragmento original
        for src, lst in f.transitions.items():
            trans[src].extend(lst)
        
        if op == "*":  # Cierre de Kleene
            self._add(trans, s.id, None, f.start.id)
            self._add(trans, s.id, None, t.id)
            self._add(trans, f.accept.id, None, f.start.id)
            self._add(trans, f.accept.id, None, t.id)
        elif op == "+":  # Una o más
            self._add(trans, s.id, None, f.start.id)
            self._add(trans, f.accept.id, None, f.start.id)
            self._add(trans, f.accept.id, None, t.id)
        elif op == "?":  # Cero o una
            self._add(trans, s.id, None, f.start.id)
            self._add(trans, s.id, None, t.id)
            self._add(trans, f.accept.id, None, t.id)
        else:
            raise RegexSyntaxError(f"Operador unario desconocido: {op}")
        
        return Fragment(s, t, self._freeze(trans)) 