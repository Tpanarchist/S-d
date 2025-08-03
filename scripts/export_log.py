from seed.core.memory_log import MemoryLog
import json
import pathlib

def export_log():
    out = pathlib.Path("seeD_export.jsonl")
    db = MemoryLog()
    rows = db.get_last_n_events(1000)  # Adjust the number as needed
    with out.open("w") as f:
        for r in rows:
            event_dict = {
                "id": r[0],
                "inp": r[1],
                "contrast": r[2],
                "delta": r[3],
                "flag": r[4]
            }
            json.dump(event_dict, f)
            f.write("\n")
    print(f"Dumped {len(rows)} rows → {out}")

if __name__ == "__main__":
    export_log()
