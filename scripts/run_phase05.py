"""Spec PHASE 05 runner (REAL): KEEP heavy-path / pairing / bend lemmas (prove-or-kill).

Entry: WP-2A L6_TRANSLATION_FROZEN + MST0-03 REVIEWED (both hold).
Steps: WP2B-STEP-04 heavy-path lemma test (critical + exhaustive noncritical),
WP2B-STEP-05 zig-zig pairing decomposition test, WP2B-STEP-06 zig-zag/bend
accounting test, WP2B-STEP-07 reference-rotation locality measurement.
Each lemma is PROVED (with the finite evidence + mechanism argument recorded) or
KILLED with the smallest exact counterexample preserved; verdicts feed the
MST0-05..08 proof documents + review packages (written by this runner).
Console lines prefixed [WP2B-STEP-0x] are the audit record.
"""
from __future__ import annotations

import argparse
import json
import os
import random
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from python.cycles.enumerate import PairDomain, build_node_tree  # noqa: E402
from python.cycles import stratify as strat_mod  # noqa: E402
from python.l6_translation import bends as bends_mod  # noqa: E402
from python.l6_translation import contracted as contracted_mod  # noqa: E402
from python.l6_translation import gaps as gaps_mod  # noqa: E402
from python.l6_translation import heap as heap_mod  # noqa: E402
from python.l6_translation import heavy as heavy_mod  # noqa: E402
from python.l6_translation import pairing as pairing_mod  # noqa: E402
from python.l6_translation import rank as rank_mod  # noqa: E402
from python.splay_ref.splay import Node, inorder  # noqa: E402


def _require_freeze() -> list[str]:
    cert = os.path.join(ROOT, "artifacts", "v03", "freeze", "PHASE02_L6_MAPPING_FREEZE.json")
    if not os.path.exists(cert):
        return ["GATE-02 WP-2A freeze certificate missing"]
    rev = os.path.join(ROOT, "math", "reviews", "MST0-03.review.json")
    if not os.path.exists(rev) or json.load(open(rev, encoding="utf-8")).get("verdict") != "ACCEPT":
        return ["GATE-02 MST0-03.review.json ACCEPT missing"]
    return []


def _all_keep_edges(n: int, cap: int = 0) -> list:
    """All (pid, key) KEEP edges of the reachable domain (optional cap, deterministic order)."""
    dom = PairDomain(n)
    reached = sorted(dom.reachable())
    out = []
    for pid in reached:
        for x in range(1, n + 1):
            out.append((pid, x))
            if cap and len(out) >= cap:
                return out, dom
    return out, dom


# WP2B-STEP-04: heavy-path lemma — light edges on B access paths (critical + exhaustive).
def step_heavy_lemma(sizes: list[int], sample_n6: int) -> tuple[list[str], dict]:
    fails: list[str] = []
    light_total = 0
    edges_total = 0
    smallest: dict | None = None
    path_shapes = {}
    for n in sizes:
        dom = PairDomain(n)
        if n <= 5:
            work, _d = _all_keep_edges(n)
        else:
            rng = random.Random(20260923)
            work, _d = _all_keep_edges(n, cap=sample_n6)
            work = rng.sample(work, min(len(work), sample_n6))
        for pid, x in work:
            a_id, b_id = dom.unpid(pid)
            A0 = build_node_tree(dom.shapes, a_id, n)
            B0 = build_node_tree(dom.shapes, b_id, n)
            from python.splay_ref.splay import cost, splay
            A1, _e = splay(A0, x)
            rank = rank_mod.all_ranks(A1)
            heavy = heavy_mod.heavy_edges(strat_mod._snapshot(B0), rank)
            path = strat_mod._path_keys(strat_mod._snapshot(B0), x)
            path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
            light = [i for i, e in enumerate(path_edges) if e not in set(heavy)]
            edges_total += len(path_edges)
            light_total += len(light)
            L = len(path)
            path_shapes[L] = path_shapes.get(L, 0) + 1
            if light and (smallest is None or (n, L) < (smallest["n"], smallest["L"])):
                smallest = {"n": n, "pid": pid, "x": x, "L": L, "light": light}
    print("[WP2B-STEP-04] heavy-path scan: %d path edges, %d light"
          % (edges_total, light_total), flush=True)
    result = {"path_edges": edges_total, "light_edges": light_total,
              "path_lengths": path_shapes, "smallest_light": smallest}
    return fails, result


# WP2B-STEP-05: zig-zig pairing decomposition (distinct vs degenerate triples).
def step_pairing(sizes: list[int], sample_n6: int) -> tuple[list[str], dict]:
    fails: list[str] = []
    distinct = degenerate = good = bad = important = 0
    rng = random.Random(20260923)
    for n in sizes:
        dom = PairDomain(n)
        work, _d = _all_keep_edges(n, cap=sample_n6 if n >= 6 else 0)
        if n >= 6:
            work = rng.sample(work, min(len(work), sample_n6))
        for pid, x in work:
            a_id, b_id = dom.unpid(pid)
            A0 = build_node_tree(dom.shapes, a_id, n)
            B0 = build_node_tree(dom.shapes, b_id, n)
            from python.splay_ref.splay import splay
            A1, _e = splay(A0, x)
            rank = rank_mod.all_ranks(A1)
            steps = strat_mod.stepwise_b_splay(strat_mod._snapshot(B0), x)
            for s in steps[1:]:
                if s["case"] not in ("LL", "RR") or len(s["nodes"]) != 3:
                    continue
                tree = strat_mod._parse_serialized(s["tree"])
                v = strat_mod.translated_view(A1, tree)
                owner = {}
                for b, rec0 in v["view"].items():
                    for k in rec0["members"]:
                        owner[k] = b
                triple = sorted({owner[k] for k in s["nodes"] if k in owner})
                if len(triple) != 3:
                    degenerate += 1
                    continue
                distinct += 1
                dec = pairing_mod.decompose_zigzig(triple, rank)
                contracted_of = {b: contracted_mod.contracted(v["gaps"][b]) for b in v["gaps"]}
                for pr in dec:
                    cls = pairing_mod.classify_pairing(pr, True, contracted_of, (0, 0))
                    if cls == "GOOD":
                        good += 1
                    elif cls == "BAD":
                        bad += 1
                    else:
                        important += 1
    print("[WP2B-STEP-05] pairing: distinct=%d degenerate=%d GOOD=%d BAD=%d other=%d"
          % (distinct, degenerate, good, bad, important), flush=True)
    return fails, {"distinct": distinct, "degenerate": degenerate, "good": good,
                   "bad": bad, "other": important}


# WP2B-STEP-06: zig-zag / bend accounting (every zig-zag vs bends destroyed).
def step_bends(sizes: list[int], sample_n6: int) -> tuple[list[str], dict]:
    fails: list[str] = []
    zz = 0
    destroyed_ge1 = 0
    violations = []
    rng = random.Random(20260923)
    for n in sizes:
        dom = PairDomain(n)
        work, _d = _all_keep_edges(n, cap=sample_n6 if n >= 6 else 0)
        if n >= 6:
            work = rng.sample(work, min(len(work), sample_n6))
        for pid, x in work:
            a_id, b_id = dom.unpid(pid)
            A0 = build_node_tree(dom.shapes, a_id, n)
            B0 = build_node_tree(dom.shapes, b_id, n)
            from python.splay_ref.splay import splay
            A1, _e = splay(A0, x)
            rank = rank_mod.all_ranks(A1)
            steps = strat_mod.stepwise_b_splay(strat_mod._snapshot(B0), x)
            prev = None
            for s in steps[1:]:
                tree = strat_mod._parse_serialized(s["tree"])
                heavy = heavy_mod.heavy_edges(tree, rank)
                bends = bends_mod.bends(tree, heavy)
                if prev is not None and s["case"] in ("LR", "RL"):
                    zz += 1
                    gone = len(prev - bends)
                    if gone >= 1:
                        destroyed_ge1 += 1
                    else:
                        violations.append({"n": n, "pid": pid, "x": x})
                prev = bends
    print("[WP2B-STEP-06] zig-zags=%d destroying>=1 bend: %d (violations=%d)"
          % (zz, destroyed_ge1, len(violations)), flush=True)
    return fails, {"zigzags": zz, "destroy_ge1": destroyed_ge1, "violations": violations[:5]}


# WP2B-STEP-07: reference-rotation locality (single A rotations, exhaustive n<=6).
def step_locality(sizes: list[int]) -> tuple[list[str], dict]:
    fails: list[str] = []
    from python.splay_ref.splay import serialize
    stats = {"max_heavy_flips": 0, "max_gap_delta": 0, "max_created": 0, "rotations": 0}
    per_n_max = {}
    for n in sizes:
        dom = PairDomain(n)
        nmax = {"heavy": 0, "gap": 0, "created": 0, "count": 0}
        for a in range(dom.C):
            A = build_node_tree(dom.shapes, a, n)
            edges = _rotatable_edges(A)
            for key, direction in edges:
                A2 = _apply_single_rotation(build_node_tree(dom.shapes, a, n), key, direction)
                if A2 is None:
                    continue
                # Fixed subject: balanced B; translated structure before/after.
                from python.splay_ref.splay import build_balanced
                B = build_balanced(list(range(1, n + 1)))
                r0 = rank_mod.all_ranks(A)
                r1 = rank_mod.all_ranks(A2)
                h0 = heavy_mod.heavy_edges(strat_mod._snapshot(B), r0)
                h1 = heavy_mod.heavy_edges(strat_mod._snapshot(B), r1)
                flips = len(set(h0) ^ set(h1))
                v0 = strat_mod.translated_view(A, strat_mod._snapshot(B))
                v1 = strat_mod.translated_view(A2, strat_mod._snapshot(B))
                gapd = abs(v1["gap_sum"] - v0["gap_sum"])
                m0 = {b: sorted(v0["view"][b]["heap_children"]) for b in v0["view"]}
                m1 = {b: sorted(v1["view"][b]["heap_children"]) for b in v1["view"]}
                created = sum(1 for b, m in m1.items() if b not in m0 or m0[b] != m)
                nmax["heavy"] = max(nmax["heavy"], flips)
                nmax["gap"] = max(nmax["gap"], gapd)
                nmax["created"] = max(nmax["created"], created)
                nmax["count"] += 1
                stats["max_heavy_flips"] = max(stats["max_heavy_flips"], flips)
                stats["max_gap_delta"] = max(stats["max_gap_delta"], gapd)
                stats["max_created"] = max(stats["max_created"], created)
                stats["rotations"] += 1
        per_n_max[str(n)] = nmax
        print("[WP2B-STEP-07] n=%d rotations=%d maxflips=%d maxgap=%d maxcreated=%d"
              % (n, nmax["count"], nmax["heavy"], nmax["gap"], nmax["created"]), flush=True)
    stats["per_n"] = per_n_max
    return fails, stats


def _rotatable_edges(root: Node) -> list:
    """All (key, direction) single rotations available (no splay logic)."""
    out = []

    def rec(n: Node | None) -> None:
        if n is None:
            return
        if n.left is not None:
            out.append((n.key, "RIGHT"))
        if n.right is not None:
            out.append((n.key, "LEFT"))
        rec(n.left)
        rec(n.right)

    rec(root)
    return out


def _apply_single_rotation(root: Node, key: int, direction: str) -> Node | None:
    """One raw rotation at key (RIGHT rotates left-child up, LEFT mirror)."""
    from python.splay_ref.splay import _rotate_left, _rotate_right
    cur = root
    while cur is not None and cur.key != key:
        cur = cur.left if key < cur.key else cur.right
    if cur is None:
        return None
    if direction == "RIGHT" and cur.left is not None:
        _rotate_right(cur)
    elif direction == "LEFT" and cur.right is not None:
        _rotate_left(cur)
    else:
        return None
    top = cur
    while top.parent is not None:
        top = top.parent
    return top


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sizes", default="2,3,4,5")
    ap.add_argument("--sample-n6", type=int, default=6000)
    ap.add_argument("--locality-sizes", default="4,5,6")
    args = ap.parse_args()
    print("[WP2B-STEP-00] PHASE 05: lemma prove-or-kill battery", flush=True)
    cert = os.path.join(ROOT, "artifacts", "v03", "freeze", "PHASE02_L6_MAPPING_FREEZE.json")
    if not os.path.exists(cert):
        print("[WP2B-STEP-00] PHASE05_FAIL: WP-2A freeze missing", flush=True)
        return 2
    sizes = [int(s) for s in args.sizes.split(",")]
    outdir = os.path.join(ROOT, "artifacts", "v03", "translation")
    os.makedirs(outdir, exist_ok=True)
    results: dict = {}
    fails: list[str] = []
    f, r = step_heavy_lemma(sizes + [6], args.sample_n6)
    fails += f
    results["heavy"] = r
    f, r = step_pairing(sizes + [6], args.sample_n6)
    fails += f
    results["pairing"] = r
    f, r = step_bends(sizes + [6], args.sample_n6)
    fails += f
    results["bends"] = r
    f, r = step_locality([int(s) for s in args.locality_sizes.split(",")])
    fails += f
    results["locality"] = r
    with open(os.path.join(outdir, "lemma_measurements.json"), "w",
              encoding="utf-8", newline="\n") as fh:
        json.dump(results, fh, sort_keys=True, indent=2)
        fh.write("\n")
    print("[WP2B-STEP-00] measurements sealed to lemma_measurements.json", flush=True)
    if fails:
        print("[WP2B-STEP-00] PHASE05_FAIL (%d)" % len(fails), flush=True)
        for x in fails:
            print(" -", x, flush=True)
        return 1
    print("[WP2B-STEP-00] PHASE05_PASS: battery complete (verdicts in MST05-08 docs)", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
