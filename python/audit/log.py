"""Append-only run logger (§27): every execution record carries the full field set."""
from __future__ import annotations

import datetime
import hashlib
import json
import os


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def write_log(path: str, rec: dict) -> dict:
    required = ["experiment_id", "phase", "branch", "command", "scientific_status"]
    for k in required:
        if k not in rec:
            raise ValueError(f"log missing {k}")
    rec = dict(rec)
    rec.setdefault("utc", datetime.datetime.now(datetime.timezone.utc).isoformat())
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    lines = []
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, sort_keys=True) + "\n")
    return rec
