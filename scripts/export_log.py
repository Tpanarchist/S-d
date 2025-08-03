from seed.core.memory_log import MemoryLog
import json
import pathlib
import argparse
import gzip

def export_log(rows: int, out: pathlib.Path):
    db = MemoryLog()
    events = db.get_last_n_events(rows)
    open_func = gzip.open if out.suffix == ".gz" else open
    with open_func(out, "wt", encoding="utf-8") as f:
        for event in events:
            event_dict = {
                "id": event.id,
                "inp": event.inp,
                "contrast": event.contrast,
                "delta": event.delta,
                "flag": event.flag
            }
            json.dump(event_dict, f)
            f.write("\n")
    print(f"Dumped {len(events)} rows → {out}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export the event log.")
    parser.add_argument("--rows", type=int, default=1000, help="Number of rows to export")
    parser.add_argument("--out", type=pathlib.Path, default=pathlib.Path("seeD_export.jsonl"), help="Output file path")
    args = parser.parse_args()
    export_log(args.rows, args.out)
