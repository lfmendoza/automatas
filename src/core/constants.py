"""
Constants used throughout the automata package.
"""

from typing import Set, Mapping

# Set of regex operators
OPERATORS: Set[str] = {"|", ".", "*", "+", "?", "(", ")"}

# Set of unary operators
UNARY: Set[str] = {"*", "+", "?"}

# Operator precedence mapping
PRECEDENCE: Mapping[str, int] = {"|": 1, ".": 2, "*": 3, "+": 3, "?": 3}

# Epsilon symbol
EPSILON: str = "ε" 