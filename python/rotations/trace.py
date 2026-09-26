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


def _key_multiset(serialized: str) -> list:
    """Key multiset of a keyed serialization (permutation check)."""
    import re as _re
    return sorted(int(k) for k in _re.findall(r"(?<=\()(\d+)", serialized))


# WP-1 REPAIR STEP T5: trace-owned assertions (fail-closed, every certified trace).
def _assert_trace(mode: str, t: dict, a0: int, y0: int) -> None:
    """Assert final-tree presence, key integrity, and reported costs.

    A1/B1 serialize the ACTUAL post-splay objects (never reconstructions);
    reported costs equal independently recomputed pre-splay costs.
    """
    if t["A1"] is None or (mode == "KEEP" and t["B1"] is None):
        raise ValueError("trace missing final tree for %s" % t["edge_id"])
    for tag, serial in (("A1", t["A1"]), ("B1", t["B1"])):
        keys = _key_multiset(serial)
        if not keys or len(set(keys)) != len(keys):
            raise ValueError("trace %s %s keys malformed" % (t["edge_id"], tag))
    if t["a"] != a0 or (mode == "KEEP" and t["y"] != y0):
        raise ValueError("trace %s cost mismatch (trace-layer refinement)" % t["edge_id"])


# WP-1 REPAIR STEP T6: trace-owned independent validator (every certified trace).
def certify_keep(A: Node, B: Node, x: int, edge_id: str) -> dict:
    """Build the KEEP trace and certify it against the independent core.

    Runs trace_keep on the given trees plus a full-tuple independent replay on
    structurally identical dict-states; raises on any divergence (fail-closed).
    Returns the certified trace.
    """
    from python.rotations import agree as agree_mod
    from python.splay_ref import independent as I
    from python.splay_ref.splay import cost
    a0, y0 = cost(A, x), cost(B, x)
    stA, stB = I.from_nodes(A), I.from_nodes(B)
    t = trace_keep(A, B, x, edge_id)
    _assert_trace("KEEP", t, a0, y0)
    evA, evB = I.splay2(stA, x), I.splay2(stB, x)
    desc = agree_mod.compare(t["events"], evA, evB, edge_id)
    if desc:
        raise ValueError("trace certification failed %s: %r" % (edge_id, desc))
    if I.serialize2(stA) != t["A1"] or I.serialize2(stB) != t["B1"]:
        raise ValueError("trace successor mismatch %s" % edge_id)
    return t


# WP-1 REPAIR STEP T6: DELETE counterpart of the trace-owned validator.
def certify_delete(A: Node, B: Node, x: int, edge_id: str) -> dict:
    """Build the DELETE trace and certify it against the independent core."""
    from python.rotations import agree as agree_mod
    from python.splay_ref import independent as I
    from python.splay_ref.splay import cost
    a0 = cost(A, x)
    stA = I.from_nodes(A)
    t = trace_delete(A, B, x, edge_id)
    _assert_trace("DELETE", t, a0, 0)
    evA = I.splay2(stA, x)
    desc = agree_mod.compare(t["events"], evA, [], edge_id)
    if desc:
        raise ValueError("trace certification failed %s: %r" % (edge_id, desc))
    if I.serialize2(stA) != t["A1"]:
        raise ValueError("trace successor mismatch %s" % edge_id)
    return t
