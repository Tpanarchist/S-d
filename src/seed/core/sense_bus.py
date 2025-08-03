"""Minimal IO adapter for SeeD.

Exports:
    read(stdin: bool=False) -> str  – return a single ASCII symbol.

The function purposefully stays <20 LOC so it can be swapped out later.
"""
from __future__ import annotations

import itertools
import sys
from typing import Iterator

# Cyclic fallback corpus for quick unit tests.
_TEST_STRING: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
_cycle: Iterator[str] = itertools.cycle(_TEST_STRING)

def read_pair(*, stdin: bool = False) -> tuple[str, str]:  # noqa: D401 – we like imperative style
    """Yield a pair of ASCII characters.

    If *stdin* is True and there is data waiting, pop one byte from STDIN.
    Otherwise return the next char from an infinite test‑string cycle.
    """
    if stdin and not sys.stdin.closed and not sys.stdin.isatty():
        char = sys.stdin.read(1)
        if char:
            return char[0], next(_cycle)

    return next(_cycle), next(_cycle)

__all__ = ["read_pair"]

# Fallback to test corpus
