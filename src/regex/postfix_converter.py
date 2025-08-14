"""
Regular expression to postfix notation converter.
"""

from typing import List
from ..core.constants import OPERATORS, UNARY, PRECEDENCE, EPSILON
from ..core.exceptions import RegexSyntaxError


def _is_symbol(ch: str) -> bool:
    """
    Retorna True si `ch` es símbolo del alfabeto (no operador/paréntesis).
    
    Args:
        ch: Carácter a verificar
        
    Returns:
        True si es símbolo, False si es operador o paréntesis
    """
    return ch not in OPERATORS


def insert_concat_ops(regex: str) -> str:
    """
    Inserta el operador explícito de concatenación '.' donde corresponda.

    Reglas: insertar '.' entre X e Y cuando
      - X ∈ {símbolo, ')', '*', '+', '?'}
      - Y ∈ {símbolo, '(', 'ε'}
      
    Args:
        regex: Expresión regular sin operadores de concatenación explícitos
        
    Returns:
        Expresión regular con operadores de concatenación explícitos
    """
    out: List[str] = []
    for i, ch in enumerate(regex):
        out.append(ch)
        if ch in {"(", "|"}:
            continue
        if ch in UNARY:
            if i + 1 < len(regex):
                nxt = regex[i + 1]
                if _is_symbol(nxt) or nxt == "(":
                    out.append(".")
            continue
        if _is_symbol(ch) or ch == ")":
            if i + 1 < len(regex):
                nxt = regex[i + 1]
                if _is_symbol(nxt) or nxt == "(" or nxt == EPSILON:
                    out.append(".")
    return "".join(out)


def to_postfix(regex: str) -> str:
    """
    Convierte la ER (con '.') a notación postfija (Shunting-yard).
    
    Args:
        regex: Expresión regular con operadores de concatenación explícitos
        
    Returns:
        Expresión regular en notación postfija
        
    Raises:
        RegexSyntaxError: Si hay errores de sintaxis en la ER
    """
    output: List[str] = []
    stack: List[str] = []
    
    for i, ch in enumerate(regex):
        if _is_symbol(ch) and ch not in {"(", ")"}:
            output.append(ch)
        elif ch == "(":
            stack.append(ch)
        elif ch == ")":
            while stack and stack[-1] != "(":
                output.append(stack.pop())
            if not stack:
                raise RegexSyntaxError("Paréntesis desbalanceados", i)
            stack.pop()  # '('
        elif ch in PRECEDENCE:
            while stack and stack[-1] != "(" and PRECEDENCE[stack[-1]] >= PRECEDENCE[ch]:
                output.append(stack.pop())
            stack.append(ch)
        else:
            raise RegexSyntaxError(f"Carácter no reconocido en ER: {ch!r}", i)
    
    while stack:
        op = stack.pop()
        if op in {"(", ")"}:
            raise RegexSyntaxError("Paréntesis desbalanceados")
        output.append(op)
    
    return "".join(output) 