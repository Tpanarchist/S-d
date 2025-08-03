"""
Module for the curator agent responsible for managing dyadic interactions.

This agent oversees the dyadic interactions and ensures that
the learning process is optimized.
"""

from typing import List
from seed.core.memory_log import Event, MemoryLog

class Curator:
    def __init__(self, memory_log: MemoryLog):
        self.memory_log = memory_log

    def top_n(self, n: int = 5) -> List[Event]:
        """Retrieve the top n events."""
        return self.memory_log.get_last_n_events(n)
