from hypothesis import given, strategies as st
from seed.core.dyad_engine import delta

@given(st.text(min_size=1, max_size=1), st.text(min_size=1, max_size=1))
def test_delta_range(a, b):
    """Test that delta returns a value between 0 and 1 for any ASCII characters."""
    result = delta(a, b)
    assert 0 <= result <= 1
