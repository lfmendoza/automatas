"""
Type definitions used throughout the automata package.
"""

from typing import Optional, Sequence, Mapping, MutableMapping

# Symbol type - None for epsilon transitions
Symbol = Optional[str]

# State identifier type
StateId = int

# Transition tuple (symbol, target_state)
Transition = tuple[Symbol, StateId]

# Immutable transition map
TransitionMap = Mapping[StateId, Sequence[Transition]]

# Mutable transition map
MutableTransitionMap = MutableMapping[StateId, list[Transition]] 