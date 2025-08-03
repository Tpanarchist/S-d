from hypothesis import given, strategies as st
from seed.core.dyad_engine import delta
from seed.core.boredom import BoredomThermostat

@given(st.text(min_size=1, max_size=1), st.text(min_size=1, max_size=1))
def test_delta_range(a, b):
    """Test that delta returns a value between 0 and 1 for any ASCII characters."""
    result = delta(a, b)
    assert 0 <= result <= 1

@given(st.lists(st.floats(min_value=0, max_value=1), min_size=200, max_size=200))
def test_boredom_thermostat(deltas):
    """Test that after feeding 200 random events, thermo.low < thermo.high."""
    thermo = BoredomThermostat()
    for delta in deltas:
        thermo.update(delta)
    assert thermo.low < thermo.high
