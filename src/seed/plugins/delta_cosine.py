import math
from seed.core.dyad_engine import register

@register("cosine")
def cosine_delta(a: str, b: str) -> float:
    v = [ord(a), ord(b)]
    return 1 - (v[0] * v[1]) / (math.sqrt(v[0]**2) * math.sqrt(v[1]**2) + 1e-9)
