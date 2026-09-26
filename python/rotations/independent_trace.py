"""Independent ROT-EVENT-v0.3 trace serializer (§5.5/PHASE 03, F9).

Builds canonical rotation-trace records from independent-core (dict-state)
outputs only. Imports the independent core plus hashlib — never trace.py,
reference.py, or pair.py — so end-to-end byte comparison against trace_keep
output proves the serializer itself is independently reproduced, not merely
the Splay mechanics. Console tag [WP1-STEP-04] via callers.
"""
from __future__ import annotations

import hashlib
import json

from python.splay_ref import independent as I

SCHEMA_VERSION = "ROT-EVENT-v0.3"


# WP-1 REPAIR STEP S1: snapshot identity over dict-state (reference contract).
def dict_snapshot_hash(st: dict) -> str:
    """SHA-256 of the keyed serialization (same contract as snapshot_hash)."""
    return hashlib.sha256(I.serialize2(st).encode("utf-8")).hexdigest()


# WP-1 REPAIR STEP S2: canonical KEEP trace from dict-states (separate code).
def trace_keep_independent(stA: dict, stB: dict, x: int, edge_id: str,
                           a: int, y: int, convention: str) -> dict:
    """Replay both sides on dict-states; return the ROT-EVENT record.

    stA/stB are consumed (splayed). a/y are caller-measured pre-splay costs;
    convention is caller-supplied (never imported here).
    """
    evA = I.splay2(stA, x)
    ref = dict_snapshot_hash(stA)
    evB = I.splay2(stB, x)
    events = []
    for i, e in enumerate(evA):
        events.append(_event(edge_id, "KEEP", "A", x, i, e, ref))
    for j, e in enumerate(evB):
        events.append(_event(edge_id, "KEEP", "B", x, j, e, ref))
    return {"edge_id": edge_id, "convention": convention,
            "mode": "KEEP", "x": x, "a": a, "y": y,
            "reference_snapshot_hash": ref, "events": events,
            "A1": I.serialize2(stA), "B1": I.serialize2(stB)}


# WP-1 REPAIR STEP S3: one canonical event from an independent-core event.
def _event(edge_id: str, mode: str, side: str, x: int, idx: int,
           e: dict, ref: str) -> dict:
    """Map a splay2 event onto the ROT-EVENT-v0.3 record shape."""
    lo, hi = min(e["keys_local"]), max(e["keys_local"])
    return {"schema_version": SCHEMA_VERSION, "pair_edge_id": edge_id,
            "mode": mode, "side": side, "access_key": x,
            "rotation_index": idx, "splay_case": e["case"],
            "keys_local": list(e["keys_local"]), "interval": [lo, hi],
            "orientation": e["orientation"], "depth_before": e["depth_before"],
            "nh_before": e["nh_before"], "nh_after": e["nh_after"],
            "reference_snapshot_hash": ref}


# WP-1 REPAIR STEP S4: end-to-end canonical-bytes comparison.
def compare_canonical(primary: dict, independent: dict, tag: str) -> list[str]:
    """Return mismatches between canonical JSON bytes (empty iff identical)."""
    a = json.dumps(primary, sort_keys=True)
    b = json.dumps(independent, sort_keys=True)
    if a != b:
        return ["%s independent serializer bytes differ" % tag]
    return []
