"""Contrastive novelty metrics for SeeD."""
from __future__ import annotations

from typing import Union, Callable, Dict

Ascii = Union[str, bytes]


DELTA_REGISTRY: Dict[str, Callable[[str, str], float]] = {}

def register(name: str) -> Callable[[Callable[[str, str], float]], Callable[[str, str], float]]:
    def deco(fn):
        DELTA_REGISTRY[name] = fn
        return fn
    return deco

@register("ascii")
def ascii_distance(a: str, b: str) -> float:
    """0 ≤ Δ ≤ 1 based on ASCII distance."""
    max_ascii = max(ord(a), ord(b))
    return abs(ord(a) - ord(b)) / max_ascii

def load_delta(name: str) -> Callable[[str, str], float]:
    return DELTA_REGISTRY.get(name, ascii_distance)
