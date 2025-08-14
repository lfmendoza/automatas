
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Teoría de la Computación — Thompson NFA + Simulación + SVG
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from collections import defaultdict
from typing import DefaultDict, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Set, Tuple
import argparse
import sys

# --------------------------------------------------------------------------------------
# Compatibilidad de salida UTF-8 (Windows)
# --------------------------------------------------------------------------------------
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

# --------------------------------------------------------------------------------------
# Constantes y tipos
# --------------------------------------------------------------------------------------
OPERATORS: Set[str] = {"|", ".", "*", "+", "?", "(", ")"}
UNARY: Set[str] = {"*", "+", "?"}
PRECEDENCE: Mapping[str, int] = {"|": 1, ".": 2, "*": 3, "+": 3, "?": 3}
EPSILON: str = "ε"  # Símbolo de epsilon

Symbol = Optional[str]  # None en transiciones epsilon
StateId = int
Transition = Tuple[Symbol, StateId]
TransitionMap = Mapping[StateId, Sequence[Transition]]
MutableTransitionMap = MutableMapping[StateId, List[Transition]]

__all__ = [
    "RegexSyntaxError",
    "normalize_regex",
    "insert_concat_ops",
    "to_postfix",
    "State",
    "Fragment",
    "ThompsonNFA",
    "NFASimulator",
    "draw_nfa_svg",
    "run_batch",
    "main",
]


# --------------------------------------------------------------------------------------
# Errores
# --------------------------------------------------------------------------------------
class RegexSyntaxError(ValueError):
    """Error de sintaxis en la expresión regular."""


# --------------------------------------------------------------------------------------
# Utilidades de ER
# --------------------------------------------------------------------------------------
def normalize_regex(expr: str) -> str:
    """Normaliza la ER: quita espacios y unifica epsilon en “ε”.
    Acepta “eps”, “epsilon”, “EPS”, “EPSILON” y “(e)”.
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


def _is_symbol(ch: str) -> bool:
    """Retorna True si `ch` es símbolo del alfabeto (no operador/paréntesis)."""
    return ch not in OPERATORS


def insert_concat_ops(regex: str) -> str:
    """Inserta el operador explícito de concatenación '.' donde corresponda.

    Reglas: insertar '.' entre X e Y cuando
      - X ∈ {símbolo, ')', '*', '+', '?'}
      - Y ∈ {símbolo, '(', 'ε'}
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
    """Convierte la ER (con '.') a notación postfija (Shunting-yard)."""
    output: List[str] = []
    stack: List[str] = []
    for ch in regex:
        if _is_symbol(ch) and ch not in {"(", ")"}:
            output.append(ch)
        elif ch == "(":
            stack.append(ch)
        elif ch == ")":
            while stack and stack[-1] != "(":
                output.append(stack.pop())
            if not stack:
                raise RegexSyntaxError("Paréntesis desbalanceados")
            stack.pop()  # '('
        elif ch in PRECEDENCE:
            while stack and stack[-1] != "(" and PRECEDENCE[stack[-1]] >= PRECEDENCE[ch]:
                output.append(stack.pop())
            stack.append(ch)
        else:
            raise RegexSyntaxError(f"Carácter no reconocido en ER: {ch!r}")
    while stack:
        op = stack.pop()
        if op in {"(", ")"}:
            raise RegexSyntaxError("Paréntesis desbalanceados")
        output.append(op)
    return "".join(output)


# --------------------------------------------------------------------------------------
# Thompson NFA
# --------------------------------------------------------------------------------------
@dataclass(frozen=True)
class State:
    """Estado del AFN (identificador entero)."""
    id: StateId


@dataclass(frozen=True)
class Fragment:
    """Fragmento de NFA con estado inicial y de aceptación y su mapa de transiciones."""
    start: State
    accept: State
    transitions: TransitionMap


class ThompsonNFA:
    """Constructor de AFN por el algoritmo de Thompson."""

    __slots__ = ("_next_id",)

    def __init__(self) -> None:
        self._next_id: StateId = 0

    def _new_state(self) -> State:
        sid = self._next_id
        self._next_id += 1
        return State(sid)

    @staticmethod
    def _add(trans: MutableTransitionMap, a: StateId, sym: Symbol, b: StateId) -> None:
        trans[a].append((sym, b))

    @staticmethod
    def _freeze(trans: MutableTransitionMap) -> TransitionMap:
        return {k: tuple(v) for k, v in trans.items()}

    def build_from_postfix(self, postfix: str) -> Fragment:
        """Construye un AFN a partir de la ER en notación postfija."""
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
        s, t = self._new_state(), self._new_state()
        trans: DefaultDict[StateId, List[Transition]] = defaultdict(list)
        label: Symbol = None if ch == EPSILON else ch
        self._add(trans, s.id, label, t.id)
        return Fragment(s, t, self._freeze(trans))

    def _concat(self, a: Fragment, b: Fragment) -> Fragment:
        trans: DefaultDict[StateId, List[Transition]] = defaultdict(list)
        for src, lst in a.transitions.items():
            trans[src].extend(lst)
        for src, lst in b.transitions.items():
            trans[src].extend(lst)
        self._add(trans, a.accept.id, None, b.start.id)
        return Fragment(a.start, b.accept, self._freeze(trans))

    def _union(self, a: Fragment, b: Fragment) -> Fragment:
        s, t = self._new_state(), self._new_state()
        trans: DefaultDict[StateId, List[Transition]] = defaultdict(list)
        for src, lst in a.transitions.items():
            trans[src].extend(lst)
        for src, lst in b.transitions.items():
            trans[src].extend(lst)
        self._add(trans, s.id, None, a.start.id)
        self._add(trans, s.id, None, b.start.id)
        self._add(trans, a.accept.id, None, t.id)
        self._add(trans, b.accept.id, None, t.id)
        return Fragment(s, t, self._freeze(trans))

    def _apply_unary(self, op: str, f: Fragment) -> Fragment:
        s, t = self._new_state(), self._new_state()
        trans: DefaultDict[StateId, List[Transition]] = defaultdict(list)
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


# --------------------------------------------------------------------------------------
# Simulador de AFN (ε-NFA)
# --------------------------------------------------------------------------------------
class NFASimulator:
    """Simulador de AFN con cierres epsilon y movimientos por símbolo."""

    __slots__ = ("_start", "_accept", "_trans")

    def __init__(self, fragment: Fragment) -> None:
        self._start: StateId = fragment.start.id
        self._accept: StateId = fragment.accept.id
        self._trans: TransitionMap = fragment.transitions

    def _epsilon_closure(self, states: Set[StateId]) -> Set[StateId]:
        stack = list(states)
        closure = set(states)
        while stack:
            s = stack.pop()
            for sym, t in self._trans.get(s, ()):
                if sym is None and t not in closure:
                    closure.add(t)
                    stack.append(t)
        return closure

    def _move(self, states: Set[StateId], sym: str) -> Set[StateId]:
        out: Set[StateId] = set()
        for s in states:
            for label, t in self._trans.get(s, ()):
                if label == sym:
                    out.add(t)
        return out

    def accepts(self, w: str) -> bool:
        """Decide si el AFN acepta la palabra w."""
        current = self._epsilon_closure({self._start})
        for ch in w:
            current = self._epsilon_closure(self._move(current, ch))
            if not current:
                return False
        return self._accept in current


# --------------------------------------------------------------------------------------
# SVG (sin dependencias externas)
# --------------------------------------------------------------------------------------
def _svg_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def draw_nfa_svg(fragment: Fragment, out_path: Path, ascii_labels: bool = False) -> None:
    """Dibuja el AFN en un archivo SVG."""
    states: List[StateId] = sorted(
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

    pos: Dict[StateId, Tuple[int, int]] = {}
    for i, s in enumerate(states):
        row, col = divmod(i, cols)
        x = 40 + col * cell_w + 40
        y = 40 + row * cell_h + 40
        pos[s] = (x, y)

    def edge_path(x1: int, y1: int, x2: int, y2: int, offset: int = 0) -> str:
        cx = (x1 + x2) / 2
        cy = min(y1, y2) - 40 - abs(offset) * 10
        return f"M{x1},{y1} Q{cx},{cy} {x2},{y2}"

    parts: List[str] = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">')
    parts.append(
        "<defs>"
        '<marker id="arrow" markerWidth="10" markerHeight="10" refX="10" refY="3" orient="auto" markerUnits="strokeWidth">'
        '<path d="M0,0 L0,6 L9,3 z" />'
        "</marker>"
        "</defs>"
    )

    drawn: Set[Tuple[StateId, StateId, Symbol, int]] = set()
    for a, lst in fragment.transitions.items():
        for k, (sym, b) in enumerate(lst):
            x1, y1 = pos[a]
            x2, y2 = pos[b]
            if a == b:
                loop_r = r + 8 + 6 * k
                path = f"M{x1},{y1 - r} C{x1 - loop_r},{y1 - loop_r*2} {x1 + loop_r},{y1 - loop_r*2} {x1},{y1 - r}"
                parts.append(f'<path d="{path}" fill="none" stroke="black" marker-end="url(#arrow)"/>')
                label = "eps" if (sym is None and ascii_labels) else (EPSILON if sym is None else sym)
                parts.append(f'<text x="{x1}" y="{y1 - loop_r*2 - 5}" text-anchor="middle" font-size="12">{_svg_escape(label)}</text>')
            else:
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

    for s in states:
        x, y = pos[s]
        is_accept = s == fragment.accept.id
        parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" stroke="black" fill="white"/>')
        if is_accept:
            parts.append(f'<circle cx="{x}" cy="{y}" r="{r-5}" stroke="black" fill="none"/>')
        parts.append(f'<text x="{x}" y="{y+4}" text-anchor="middle" font-size="12">q{s}</text>')

    sx, sy = pos[fragment.start.id]
    parts.append(f'<line x1="{sx-40}" y1="{sy}" x2="{sx - r}" y2="{sy}" stroke="black" marker-end="url(#arrow)"/>')
    parts.append(f'<text x="{sx-52}" y="{sy-8}" font-size="12">start</text>')

    parts.append("</svg>")
    out_path.write_text("\n".join(parts), encoding="utf-8")


# --------------------------------------------------------------------------------------
# Lógica de ejecución
# --------------------------------------------------------------------------------------
def run_batch(regex_lines: Iterable[str], word: str, outdir: Path, ascii_labels: bool = False) -> List[Tuple[str, bool, Path]]:
    """Procesa una lista de ERs, genera SVG para cada una y evalúa la palabra `word`.
    Retorna tuplas (regex_original, aceptada, ruta_svg).
    """
    outdir.mkdir(parents=True, exist_ok=True)
    results: List[Tuple[str, bool, Path]] = []
    for i, raw in enumerate((line for line in (ln.strip() for ln in regex_lines) if line), start=1):
        reg = insert_concat_ops(normalize_regex(raw))
        postfix = to_postfix(reg)
        frag = ThompsonNFA().build_from_postfix(postfix)
        svg_path = outdir / f"afn_{i:02d}.svg"
        draw_nfa_svg(frag, svg_path, ascii_labels=ascii_labels)
        ok = NFASimulator(frag).accepts(word)
        results.append((raw, ok, svg_path))
    return results


def _build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="AFN (Thompson) + Simulación + SVG")
    p.add_argument("--input", required=True, type=Path, help="Archivo con una ER por línea")
    p.add_argument("--word", required=True, help="Palabra w a evaluar contra cada ER")
    p.add_argument("--outdir", default=Path("./output"), type=Path, help="Directorio de salida para los SVG")
    p.add_argument("--ascii", action="store_true", help="Salida sin tildes y etiquetas 'eps' en vez de 'ε'")
    return p


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = _build_arg_parser().parse_args(argv)
    try:
        lines = args.input.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        print(f"ERROR: No se encontró el archivo {args.input!s}", file=sys.stderr)
        return 2
    except UnicodeError:
        print("ERROR: El archivo de entrada debe estar codificado en UTF-8.", file=sys.stderr)
        return 2

    had_error = False
    for idx, (raw, ok, svg) in enumerate(run_batch(lines, args.word, args.outdir, ascii_labels=args.ascii), start=1):
        verdict = ("si" if args.ascii else "sí") if ok else "no"
        print(f"[{idx}] ER: {raw}")
        print(f"    SVG: {svg}")
        print(f"    w = {args.word!r} -> {verdict}")
    return 2 if had_error else 0


if __name__ == "__main__":
    raise SystemExit(main())
