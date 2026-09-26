"""Rotation-trace expansion of imported critical cycles (WP-1 prerequisite mechanics).

For every imported KEEP edge: full A-then-B rotation trace under KEEP_REF_SNAPSHOT-v1
(via python.rotations.trace), plus the translated-L6 event stream placeholder (WP-2
fills translation content; the placeholder records only raw rotation events).
Target-blind: reads edge structure only, never regret/criticality values.
Console lines prefixed [WP1-STEP-05] are the audit record.
"""
from __future__ import annotations

import json
import os
import sys

from python.cycles.enumerate import PairDomain, build_node_tree
from python.rotations.trace import trace_keep


# WP1-STEP-05: expand one imported cycle into rotation-level traces.
def _placeholder(schema: str, owner: str) -> dict:
    """Explicit empty downstream stream (schema-declared, never silent)."""
    return {"schema": schema, "status": "PLACEHOLDER_%s_PENDING" % owner,
            "events": [], "entries": []}


# WP-1 REPAIR STEP E2: expansion record with the full §9.4 field set.
def expand_cycle(dom: PairDomain, n: int, cid: int, cycle: dict) -> dict:
    """Expand each edge; verify chained closure on our evaluator.

    Per-edge record: canonical edge ID, edge index, A trace, snapshot (the
    frozen post-A tree), B trace, translated-L6 stream placeholder, ledger
    placeholder stream. Combined events additionally retained. Cycle identity
    preserves the authoritative parent position (n, index, source, key word).
    """
    edges_out = []
    cur = cycle["edges"][0]["source"]
    ok = True
    for i, e in enumerate(cycle["edges"]):
        if cur != e["source"]:
            ok = False
            break
        a_id, b_id = dom.unpid(cur)
        A = build_node_tree(dom.shapes, a_id, n)
        B = build_node_tree(dom.shapes, b_id, n)
        edge_id = dom.edge_id(cur, e["mode"], e["key"])
        tr = trace_keep(A, B, e["key"], edge_id)
        if tr["A1"] is None:
            ok = False
            break
        a_trace = [ev for ev in tr["events"] if ev["side"] == "A"]
        b_trace = [ev for ev in tr["events"] if ev["side"] == "B"]
        edges_out.append({"edge_id": edge_id, "edge_index": i, "mode": e["mode"],
                          "x": e["key"], "a": tr["a"], "y": tr["y"],
                          "reference_snapshot_hash": tr["reference_snapshot_hash"],
                          "snapshot": tr["A1"],
                          "A_trace": a_trace, "B_trace": b_trace,
                          "translated_l6_stream": _placeholder("L6-EVENT-v0.3", "WP2"),
                          "ledger_placeholder": _placeholder("LEDGER-STREAM-v0.3", "WP3"),
                          "events": tr["events"]})
        cur = dom.edge(cur, e["key"], e["mode"])[0]
        if cur != e["target"]:
            ok = False
            break
    closed = ok and cur == cycle["edges"][0]["source"]
    key_word = [e["key"] for e in cycle["edges"]]
    return {"n": n, "cycle_index": cid,
            "cycle_id": {"n": n, "cycle_index": cid,
                         "source": cycle["edges"][0]["source"],
                         "key_word": key_word},
            "edge_count": len(edges_out),
            "closed": closed, "edges": edges_out}


# WP-1 REPAIR STEP E3: frozen canonical order key for expansion tasks.
def canonical_key(n: int, cycle: dict, cid: int) -> tuple:
    """[n, source_state_id, cycle_length, key_word_lex] (§9.4/WorkPlan)."""
    edges = cycle["edges"]
    return (n, edges[0]["source"], len(edges), tuple(e["key"] for e in edges))


def main() -> int:
    print("[WP1-STEP-05] expansion needs imported corpus; see run_phase03.py", flush=True)
    return 2


if __name__ == "__main__":
    sys.exit(main())
