from seed.core.memory_log import MemoryLog

def audit_last(k: int):
    db = MemoryLog()
    rows = db._conn.execute(
        "SELECT delta, flag FROM events ORDER BY id DESC LIMIT ?", (k,)
    ).fetchall()

    mean_delta = sum(row['delta'] for row in rows) / k
    boredom_states = set(row['flag'] for row in rows)

    if mean_delta <= 0:
        raise RuntimeError("Mean Δ is not greater than 0.")
    if len(boredom_states) == 1:
        raise RuntimeError("Boredom is stuck on a single state.")
    print("Audit passed.")
