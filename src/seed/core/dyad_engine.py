"""Contrastive novelty metrics for SeeD."""
from __future__ import annotations

from typing import Union

Ascii = Union[str, bytes]


def delta(a: str, b: str) -> float:
    """0 ≤ Δ ≤ 1 based on ASCII distance."""
    max_ascii = max(ord(a), ord(b))
    return abs(ord(a) - ord(b)) / max_ascii
