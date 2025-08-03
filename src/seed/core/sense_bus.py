"""Minimal IO adapter for SeeD.

Exports:
    read(stdin: bool=False) -> str  – return a single ASCII symbol.

The function purposefully stays <20 LOC so it can be swapped out later.
"""
from __future__ import annotations

import itertools
import sys
from typing import Iterator, Callable

# Cyclic fallback corpus for quick unit tests.
_TEST_STRING: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
_cycle: Iterator[str] = itertools.cycle(_TEST_STRING)

SENSE_REGISTRY: dict[str, Callable[[], Iterator[tuple[str, str]]]] = {}

def register(name: str) -> Callable[[Callable[[], Iterator[tuple[str, str]]]], Callable[[], Iterator[tuple[str, str]]]]:
    def deco(fn):
        SENSE_REGISTRY[name] = fn
        return fn
    return deco

@register("default")
def read_pair(*, stdin: bool = False) -> Iterator[tuple[str, str]]:  # noqa: D401 – we like imperative style
    """Yield a pair of ASCII characters.

    If *stdin* is True and there is data waiting, pop one byte from STDIN.
    Otherwise return the next char from an infinite test‑string cycle.
    """
    if stdin and not sys.stdin.closed and not sys.stdin.isatty():
        char = sys.stdin.read(1)
        if char:
            yield char[0], next(_cycle)
    while True:
        yield next(_cycle), next(_cycle)

from pathlib import Path

@register("file")
def file_reader(path: Path = Path("sample.txt")) -> Iterator[tuple[str, str]]:
    with path.open('r') as f:
        while True:
            char = f.read(1)
            if not char:
                f.seek(0)  # Loop when EOF
                continue
            yield char, next(_cycle)

@register("stdin")
def stdin_reader() -> Iterator[tuple[str, str]]:
    while True:
        if not sys.stdin.closed and not sys.stdin.isatty():
            char = sys.stdin.read(1)
            if char:
                yield char[0], next(_cycle)
        else:
            yield next(_cycle), next(_cycle)

__all__ = ["read_pair", "file_reader", "stdin_reader"]

# Fallback to test corpus
