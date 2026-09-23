"""Rotation-trace refinement (§5): A-then-B KEEP order with frozen reference snapshot.

Analysis convention v1 (KEEP_REF_SNAPSHOT-v1):
  1. observe (A0,B0); 2. splay A -> A1; 3. freeze A1 hash as reference;
  4. splay B rotation-by-rotation against frozen snapshot;
  5. record (A1,B1). This convention does not change paired semantics.
"""
from __future__ import annotations

import hashlib

from python.splay_ref.pair import delete, keep
from python.splay_ref.splay import Node, serialize

CONVENTION = "KEEP_REF_SNAPSHOT-v1"


def snapshot_hash(A1: Node | None) -> str:
    return hashlib.sha256(serialize(A1).encode()).hexdigest()


def trace_keep(A: Node, B: Node, x: int, edge_id: str) -> dict:
    A2, B2, info = keep(A, B, x)
    ref = snapshot_hash(A2)
    events = []
    for i, e in enumerate(info["events_A"]):
        events.append({"pair_edge_id": edge_id, "mode": "KEEP", "side": "A",
                       "access_key": x, "rotation_index": i,
                       "splay_case": e["case"], "keys_local": e["keys_local"],
                       "reference_snapshot_hash": ref})
    base = len(events)
    for j, e in enumerate(info["events_B"]):
        events.append({"pair_edge_id": edge_id, "mode": "KEEP", "side": "B",
                       "access_key": x, "rotation_index": j,
                       "splay_case": e["case"], "keys_local": e["keys_local"],
                       "reference_snapshot_hash": ref})
    return {"edge_id": edge_id, "convention": CONVENTION, "mode": "KEEP",
            "x": x, "a": info["a"], "y": info["y"],
            "reference_snapshot_hash": ref, "events": events,
            "A1": serialize(A2), "B1": serialize(B2)}


def trace_delete(A: Node, B: Node, x: int, edge_id: str) -> dict:
    A2, B2, info = delete(A, B, x)
    ref = snapshot_hash(A2)
    events = [{"pair_edge_id": edge_id, "mode": "DELETE", "side": "A",
               "access_key": x, "rotation_index": i,
               "splay_case": e["case"], "keys_local": e["keys_local"],
               "reference_snapshot_hash": ref}
              for i, e in enumerate(info["events_A"])]
    return {"edge_id": edge_id, "convention": CONVENTION, "mode": "DELETE",
            "x": x, "a": info["a"], "y": 0,
            "reference_snapshot_hash": ref, "events": events,
            "A1": serialize(A2), "B1": serialize(B2)}
