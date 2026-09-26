"""Rotation-trace refinement (§5): A-then-B KEEP order with frozen reference snapshot.

Analysis convention v1 (KEEP_REF_SNAPSHOT-v1):
  1. observe (A0,B0); 2. splay A -> A1; 3. freeze A1 hash as reference;
  4. splay B rotation-by-rotation against frozen snapshot;
  5. record (A1,B1). This convention does not change paired semantics.
"""
from __future__ import annotations

import hashlib

from python.rotations.reference import CONVENTION, snapshot_hash
from python.splay_ref.pair import delete, keep
from python.splay_ref.splay import Node, serialize

# Re-exported for backward compatibility; canonical home is reference.py.

SCHEMA_VERSION = "ROT-EVENT-v0.3"


def _trace_event(edge_id: str, mode: str, side: str, x: int, idx: int,
                 e: dict, ref: str) -> dict:
    """One §5.5 rotation event: identity + case + interval + orientation +
    neighborhood hashes + search-path position + frozen reference snapshot."""
    lo, hi = min(e["keys_local"]), max(e["keys_local"])
    return {"schema_version": SCHEMA_VERSION, "pair_edge_id": edge_id,
            "mode": mode, "side": side, "access_key": x,
            "rotation_index": idx, "splay_case": e["case"],
            "keys_local": e["keys_local"], "interval": [lo, hi],
            "orientation": e["orientation"], "depth_before": e["depth_before"],
            "nh_before": e["nh_before"], "nh_after": e["nh_after"],
            "reference_snapshot_hash": ref}


def trace_keep(A: Node, B: Node, x: int, edge_id: str) -> dict:
    A2, B2, info = keep(A, B, x)
    ref = snapshot_hash(A2)
    events = []
    for i, e in enumerate(info["events_A"]):
        events.append(_trace_event(edge_id, "KEEP", "A", x, i, e, ref))
    for j, e in enumerate(info["events_B"]):
        events.append(_trace_event(edge_id, "KEEP", "B", x, j, e, ref))
    return {"edge_id": edge_id, "convention": CONVENTION, "mode": "KEEP",
            "x": x, "a": info["a"], "y": info["y"],
            "reference_snapshot_hash": ref, "events": events,
            "A1": serialize(A2), "B1": serialize(B2)}


def trace_delete(A: Node, B: Node, x: int, edge_id: str) -> dict:
    A2, B2, info = delete(A, B, x)
    ref = snapshot_hash(A2)
    events = [_trace_event(edge_id, "DELETE", "A", x, i, e, ref)
              for i, e in enumerate(info["events_A"])]
    return {"edge_id": edge_id, "convention": CONVENTION, "mode": "DELETE",
            "x": x, "a": info["a"], "y": 0,
            "reference_snapshot_hash": ref, "events": events,
            "A1": serialize(A2), "B1": serialize(B2)}
