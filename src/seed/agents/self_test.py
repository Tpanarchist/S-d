from seed.core.memory_log import MemoryLog

def audit_last(k: int):
    db = MemoryLog()
    rows = db._conn.execute(
        "SELECT delta, flag FROM events ORDER BY id DESC LIMIT ?", (k,)
    ).fetchall()

    deltas = [row['delta'] for row in rows]
    flags = [row['flag'] for row in rows]
    mean_delta = sum(deltas) / k
    boredom_states = set(flags)

    assert 0 <= min(deltas) <= max(deltas) <= 1, "Deltas are out of bounds."
    if flags.count(flags[0]) > 0.8 * k:
        print("Warning: More than 80% of the last k flags are identical.")

    if mean_delta <= 0:
        raise RuntimeError("Mean Δ is not greater than 0.")
    if len(boredom_states) == 1:
        raise RuntimeError("Boredom is stuck on a single state.")
    print("Audit passed.")
