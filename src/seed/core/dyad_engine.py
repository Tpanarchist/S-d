"""Contrastive novelty metrics for SeeD."""
from __future__ import annotations

from typing import Union

Ascii = Union[str, bytes]


def delta(a: Ascii, b: Ascii) -> float:  # noqa: D401
    """Return a simple Hamming‑distance novelty score between *a* and *b*.

    * If the inputs are exactly equal → 0.0
    * Otherwise → 1.0  (placeholder for richer metrics later)
    """
    if isinstance(a, bytes):
        a = a.decode()
    if isinstance(b, bytes):
        b = b.decode()
    return 0.0 if a == b else 1.0
