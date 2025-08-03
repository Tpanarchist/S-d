import pytest
from seed.plugins import autodiscover_plugins
from seed.core.sense_bus import SENSE_REGISTRY
from seed.core.dyad_engine import DELTA_REGISTRY

autodiscover_plugins()

def test_sense_registry():
    assert "jsonl" in SENSE_REGISTRY

def test_delta_registry():
    assert "cosine" in DELTA_REGISTRY

def test_jsonl_reader():
    reader = SENSE_REGISTRY["jsonl"]()
    a, b = next(reader)
    assert isinstance(a, str) and isinstance(b, str)

def test_cosine_delta():
    delta_fn = DELTA_REGISTRY["cosine"]
    result = delta_fn('a', 'b')
    assert 0 <= result <= 1
