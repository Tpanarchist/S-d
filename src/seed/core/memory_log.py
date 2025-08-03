"""Append‑only, tamper‑evident event ledger for SeeD."""
from __future__ import annotations

import json
import pathlib
import sqlite3
import time
from hashlib import sha256
from typing import Any, Dict, Union, List
from dataclasses import dataclass, astuple

_DB_PATH = pathlib.Path(__file__).parent.parent.parent / "memory_log.db"

_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS events (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    ts       TEXT    NOT NULL,
    inp      TEXT    NOT NULL,
    contrast TEXT    NOT NULL,
    delta    REAL    NOT NULL,
    flag     TEXT    NOT NULL,
    hash     TEXT    NOT NULL UNIQUE
);
"""


@dataclass
class Event:
    id: int
    ts: str
    inp: str
    contrast: str
    delta: float
    flag: str

    def as_row(self):
        return map(str, astuple(self))

class MemoryLog:
    """Lightweight wrapper around an SQLite WAL ledger."""

    def __init__(self, db_path: pathlib.Path | str = _DB_PATH) -> None:
        self.db_path = pathlib.Path(db_path)
        self._conn = sqlite3.connect(self.db_path, isolation_level=None, check_same_thread=False)
        self._conn.execute("PRAGMA journal_mode=WAL;")
        self._conn.execute(_SCHEMA_SQL)

    # ── Public API ────────────────────────────────────────────────────
    def append(self, record: Dict[str, Any]) -> Event:
        """Insert *record* and return the row‑id.

        The input *record* **must** contain keys: inp, contrast, delta, flag.
        A UTC timestamp and SHA‑256 integrity hash are injected automatically.
        """
        required = {"inp", "contrast", "delta", "flag"}
        if not required.issubset(record):
            missing = required - record.keys()
            raise ValueError(f"Missing mandatory keys: {missing}")

        # Normalize & enrich record
        enriched: Dict[str, Union[str, float]] = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            **record,
        }
        # Deterministic hash (sorted keys)
        payload = json.dumps(enriched, separators=(",", ":"), sort_keys=True)
        enriched["hash"] = sha256(payload.encode()).hexdigest()

        with self._conn as conn:  # type: ignore
            cur = conn.cursor()
            cur.execute(
                """INSERT INTO events (ts, inp, contrast, delta, flag, hash)
                   VALUES (:ts, :inp, :contrast, :delta, :flag, :hash)""",
                enriched,
            )
            event_id = cur.lastrowid
            return Event(event_id, enriched["ts"], enriched["inp"], enriched["contrast"], enriched["delta"], enriched["flag"])

    def get_last_n_events(self, n: int) -> List[Event]:
        """Retrieve the last n events from the log."""
        with self._conn as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, ts, inp, contrast, delta, flag FROM events ORDER BY id DESC LIMIT ?",
                (n,)
            )
            rows = cur.fetchall()
            return [Event(id, ts, inp, contrast, delta, flag) for id, ts, inp, contrast, delta, flag in rows]

    def __del__(self):  # noqa: D401 – destructor to close handle
        try:
            self._conn.close()
        except Exception:  # pragma: no cover
            pass
