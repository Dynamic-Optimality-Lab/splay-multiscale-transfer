"""Spec PHASE 03 runner (REAL): rotation-trace certification + expansion mechanics.

Requires run_phase01 outputs (import ledger, replay). Steps: WP1-STEP-04 rotation
verification (dual-core agreement on every imported corpus edge, reference-snapshot
determinism, block-partition exact-once coverage), WP1-STEP-05 expansion of all
imported critical cycles to A/B rotation traces + circulation tables (prerequisite
artifacts for WP-2-owned Phase 04 science). Emits ROTATION_TRACE_CERTIFIED
(mechanics scope; MST0-02/04 theorem reviews remain pending human verdicts).
Console lines prefixed [WP1-STEP-0x] are the audit record.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from python.cycles import expand as expand_mod  # noqa: E402
from python.cycles import circulation as circ_mod  # noqa: E402
from python.cycles.enumerate import PairDomain  # noqa: E402
from python.rotations import blocks as blocks_mod  # noqa: E402
from python.rotations import reference as ref_mod  # noqa: E402
from python.rotations.trace import trace_keep  # noqa: E402
from python.splay_ref import independent as I  # noqa: E402
from python.splay_ref.splay import build_balanced  # noqa: E402


# WP1-STEP-04: dual-core agreement on every imported corpus edge + convention checks.
def step_rotation_verification(imp: str, sizes: list[int]) -> list[str]:
    fails: list[str] = []
    checked = 0
    for n in sizes:
        dom = PairDomain(n)
        cycles = json.load(open(os.path.join(imp, "v01baseline", "v01",
                                             "critical_n%d_canonical_cycles.json" % n),
                                encoding="utf-8"))
        for cid, cyc in enumerate(cycles):
            for i, e in enumerate(cyc["edges"]):
                a_id, b_id = dom.unpid(e["source"])
                A = build_node_tree_outer(dom, a_id, n)
                B = build_node_tree_outer(dom, b_id, n)
                t1 = trace_keep(A, B, e["key"], "agree-%d-%d-%d" % (n, cid, i))
                # Independent core on structurally identical trees.
                A2 = build_node_tree_outer(dom, a_id, n)
                B2 = build_node_tree_outer(dom, b_id, n)
                stA, stB = I.from_nodes(A2), I.from_nodes(B2)
                a2, y2 = I.cost2(stA, e["key"]), I.cost2(stB, e["key"])
                evA, evB = I.splay2(stA, e["key"]), I.splay2(stB, e["key"])
                if a2 != t1["a"] or y2 != t1["y"]:
                    fails.append("ROT-02 n=%d c=%d e=%d cost mismatch" % (n, cid, i))
                mine = [ev["splay_case"] for ev in t1["events"]]
                theirs = [ev["case"] for ev in evA] + [ev["case"] for ev in evB]
                if mine != theirs:
                    fails.append("ROT-10 n=%d c=%d e=%d case-sequence mismatch" % (n, cid, i))
                if I.serialize2(stA) != t1["A1"] or I.serialize2(stB) != t1["B1"]:
                    fails.append("ROT-01 n=%d c=%d e=%d final-tree mismatch" % (n, cid, i))
                if len(t1["reference_snapshot_hash"]) != 64:
                    fails.append("ROT-11 n=%d c=%d e=%d snapshot malformed" % (n, cid, i))
                checked += 1
    print("[WP1-STEP-04] dual-core agreement on %d corpus edges (costs+cases+trees)" % checked,
          flush=True)
    # Reference determinism: same KEEP twice gives identical snapshot + event stream.
    A = build_balanced([1, 2, 3, 4, 5])
    B = build_balanced([1, 2, 3, 4, 5])
    t1 = trace_keep(A, B, 3, "det-a")
    A = build_balanced([1, 2, 3, 4, 5])
    B = build_balanced([1, 2, 3, 4, 5])
    t2 = trace_keep(A, B, 3, "det-b")
    if t1["reference_snapshot_hash"] != t2["reference_snapshot_hash"]:
        fails.append("ROT-11 reference snapshot not deterministic")
    elif [ev["splay_case"] for ev in t1["events"]] != [ev["splay_case"] for ev in t2["events"]]:
        fails.append("ROT-11 event stream not deterministic")
    else:
        print("[WP1-STEP-04] reference snapshot deterministic; convention %s"
              % ref_mod.CONVENTION, flush=True)
    # Block partition exact-once coverage on synthetic histories (incl. empty/edge cases).
    cases = [[], [{"mode": "KEEP", "x": 1}],
             [{"mode": "DELETE", "x": 1}, {"mode": "DELETE", "x": 2},
              {"mode": "KEEP", "x": 1}, {"mode": "KEEP", "x": 3},
              {"mode": "DELETE", "x": 2}, {"mode": "KEEP", "x": 1}]]
    for h in cases:
        bl = blocks_mod.partition(h)
        if not blocks_mod.check_coverage(h, bl):
            fails.append("BLOCK-01 partition coverage failed for %s" % h)
    # Determinism of partition itself.
    h = cases[2]
    if blocks_mod.partition(h) != blocks_mod.partition([dict(z) for z in h]):
        fails.append("BLOCK-02 partition not a pure function of history")
    else:
        print("[WP1-STEP-04] block partition exact-once on %d histories" % len(cases), flush=True)
    if not fails:
        print("[WP1-STEP-04] rotation core verified (dual-core agreement via foundation suite)", flush=True)
    return fails


def build_node_tree_outer(dom: PairDomain, idx: int, n: int):
    """Fresh pointer tree for tree_id (import here to keep runner dependency-light)."""
    from python.cycles.enumerate import build_node_tree
    return build_node_tree(dom.shapes, idx, n)


# WP1-STEP-05: expand all imported cycles (prerequisite mechanics for WP-2 science).
def step_expand(imp: str, outdir: str, sizes: list[int], b_map: dict) -> list[str]:
    fails: list[str] = []
    os.makedirs(outdir, exist_ok=True)
    for n in sizes:
        dom = PairDomain(n)
        cycles = json.load(open(os.path.join(imp, "v01baseline", "v01",
                                             "critical_n%d_canonical_cycles.json" % n),
                                encoding="utf-8"))
        p, q = b_map[n]
        expanded = []
        table = []
        for cid, cyc in enumerate(cycles):
            ex = expand_mod.expand_cycle(dom, n, cid, cyc)
            if not ex["closed"]:
                fails.append("EXPAND-01 n=%d cycle=%d did not close" % (n, cid))
            expanded.append(ex)
            table.append(circ_mod.circulate(ex, p, q))
        blob = json.dumps({"n": n, "b": [p, q], "cycles": expanded,
                           "circulation": table}, sort_keys=True)
        digest = hashlib.sha256(blob.encode("utf-8")).hexdigest().upper()
        with open(os.path.join(outdir, "expanded_n%d.json" % n), "w",
                  encoding="utf-8", newline="\n") as f:
            f.write(blob + "\n")
        print("[WP1-STEP-05] n=%d expanded %d cycles sha=%s..."
              % (n, len(expanded), digest[:16]), flush=True)
    return fails


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sizes", default="4,5,6,7")
    args = ap.parse_args()
    print("[WP1-STEP-00] PHASE 03: rotation verification + expansion mechanics", flush=True)
    imp = os.path.join(ROOT, "artifacts", "v03", "parent_import")
    if not os.path.exists(os.path.join(imp, "replay.json")):
        print("[WP1-STEP-00] PHASE03_FAIL: run_phase01 outputs missing", flush=True)
        return 1
    sizes = [int(s) for s in args.sizes.split(",")]
    fails: list[str] = []
    fails += step_rotation_verification(imp, sizes)
    fact = json.load(open(os.path.join(imp, "v02baseline", "v02", "fact_table.json"),
                          encoding="utf-8"))
    b_map = {row["n"]: (int(row["b"][0]), int(row["b"][1])) for row in fact}
    fails += step_expand(imp, os.path.join(ROOT, "artifacts", "v03", "cycles", "expanded"),
                         sizes, b_map)
    if fails:
        print("[WP1-STEP-00] PHASE03_FAIL (%d)" % len(fails), flush=True)
        for x in fails:
            print(" -", x, flush=True)
        return 1
    print("[WP1-STEP-00] ROTATION_TRACE_CERTIFIED (mechanics scope; MST0-02/04 reviews pending human)", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
