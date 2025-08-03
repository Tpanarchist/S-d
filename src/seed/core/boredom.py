"""Intrinsic‑motivation dial for SeeD."""
from __future__ import annotations

import collections
import statistics

class BoredomThermostat:
    """Regulates exploration ↔ exploitation via two novelty thresholds."""

    def __init__(self, *, low: float = 0.2, high: float = 0.8) -> None:
        assert 0.0 <= low < high <= 1.0, "Thresholds must satisfy 0 ≤ low < high ≤ 1"
        self.low = low
        self.high = high
        self.deltas: collections.deque[float] = collections.deque(maxlen=50)

    def update(self, delta: float) -> str:
        """Return one of **explore | steady | exploit** based on *delta*."""
        self.deltas.append(delta)
        if len(self.deltas) == 50:
            mu = statistics.mean(self.deltas)
            sigma = statistics.stdev(self.deltas) or 1e-6
            self.low = max(0.0, mu - sigma)
            self.high = min(1.0, mu + sigma)
        """Return one of **explore | steady | exploit** based on *delta*."""
        if delta < self.low:
            return "explore"
        if delta > self.high:
            return "exploit"
        return "steady"
