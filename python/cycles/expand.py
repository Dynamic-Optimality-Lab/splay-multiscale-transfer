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
def expand_cycle(dom: PairDomain, n: int, cid: int, cycle: dict) -> dict:
    """Expand each edge; verify chained closure on our evaluator."""
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
        tr = trace_keep(A, B, e["key"], "n%dc%d-e%d" % (n, cid, i))
        if tr["A1"] is None:
            ok = False
            break
        edges_out.append({"edge_index": i, "mode": e["mode"], "x": e["key"],
                          "a": tr["a"], "y": tr["y"],
                          "reference_snapshot_hash": tr["reference_snapshot_hash"],
                          "events": tr["events"]})
        cur = dom.edge(cur, e["key"], e["mode"])[0]
        if cur != e["target"]:
            ok = False
            break
    closed = ok and cur == cycle["edges"][0]["source"]
    return {"n": n, "cycle_index": cid, "edge_count": len(edges_out),
            "closed": closed, "edges": edges_out}


def main() -> int:
    print("[WP1-STEP-05] expansion needs imported corpus; see run_phase03.py", flush=True)
    return 2


if __name__ == "__main__":
    sys.exit(main())
