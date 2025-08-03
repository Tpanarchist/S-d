"""Smoke tests proving the minimal core loop wires together."""
from src.seed.core import boredom as _boredom  # noqa: D401 – underscore artsy
from src.seed.core import dyad_engine as de
from src.seed.core import memory_log as ml
from src.seed.core import sense_bus as sb


def test_delta_basic():
    assert de.delta("A", "A") == 0.0
    assert de.delta("A", "B") == 1.0


def test_memory_append_and_hash():
    log = ml.MemoryLog(":memory:")
    rowid = log.append({"inp": "A", "contrast": "B", "delta": 1.0, "flag": "explore"})
    assert rowid == 1


def test_boredom_states():
    thermo = _boredom.BoredomThermostat(low=0.3, high=0.7)
    assert thermo.update(0.1) == "explore"
    assert thermo.update(0.5) == "steady"
    assert thermo.update(0.9) == "exploit"


def test_sense_bus_cycle():
    first = sb.read()
    second = sb.read()
    assert first != second  # because the test corpus cycles
