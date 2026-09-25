"""Frozen discovery masks (WP-4 entry requirement; pre-synthesis, development only).

Selection (synthesis may read): parent critical cycles (all sizes); near-critical
cycles = top-K exact-ratio simple cycles (n<=4 exhaustive Johnson, bounded length)
+ bounded closed-walk splicing around critical states (n5/n6) + scaled-slack filter
{0,1,2} at b=2; noncritical exact KEEP edges n2-5 (full); generated histories from
frozen DEV seeds (disjoint from validation seeds; sealed banks never opened here).
Validation (synthesis must NOT read): critical n7; noncritical n6-7 samples;
generated histories from frozen VALIDATION seeds.
All bounds deterministic and recorded in masks.json. Console tag [WP4-STEP-01].
"""
from __future__ import annotations

import json
import os
import random
import sys
from fractions import Fraction

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

from python.cycles.enumerate import PairDomain  # noqa: E402

TOP_K = 128
SLACK_SET = {0, 1, 2}
CYCLE_LEN_BOUND = 8
DEV_SEEDS = [101, 202, 303, 404, 505]
VAL_SEEDS = [606, 707, 808, 909, 1010]
DEV_SIZES = [8, 12, 16]
VAL_SIZES = [8, 12, 16]
DEV_HISTORIES_PER = 40
VAL_HISTORIES_PER = 40
N6_SAMPLE = 4000
N7_SAMPLE = 4000


def _keep_successors(dom: PairDomain, pid: int, n: int) -> list:
    """All (key, target, a, y) KEEP successors of a pair state."""
    out = []
    for x in range(1, n + 1):
        tgt, a, y = dom.edge(pid, x, "KEEP")
        out.append((x, tgt, a, y))
    return out


# WP4-STEP-01: Johnson simple cycles with length bound (exact, deterministic order).
def bounded_cycles(n: int, states: list[int], bound: int) -> list:
    """Enumerate simple KEEP cycles (length<=bound) over the given states."""
    dom = PairDomain(n)
    adj = {s: [(x, t) for x, t, _a, _y in _keep_successors(dom, s, n)] for s in states}
    cycles = []
    order = {s: i for i, s in enumerate(sorted(states))}
    sys.setrecursionlimit(10000)

    def dfs(start: int, cur: int, path: list, blocked: set, depth: int) -> None:
        if depth > bound:
            return
        for _x, nxt in adj.get(cur, []):
            if nxt == start and len(path) >= 1:
                cycles.append(list(path))
            elif nxt not in blocked and order[nxt] > order[start] and depth < bound:
                blocked.add(nxt)
                path.append(nxt)
                dfs(start, nxt, path, blocked, depth + 1)
                path.pop()
                blocked.discard(nxt)

    for s in sorted(states):
        dfs(s, s, [s], {s}, 1)
    return cycles


def _cycle_costs(dom: PairDomain, n: int, cyc: list) -> tuple | None:
    """(keys, sum_a, sum_y) for a closed state walk (lowest key on ties)."""
    sum_a = sum_y = 0
    keys = []
    for i in range(len(cyc)):
        src, tgt = cyc[i], cyc[(i + 1) % len(cyc)]
        found = None
        for x in range(1, n + 1):
            t, a, y = dom.edge(src, x, "KEEP")
            if t == tgt:
                found = (x, a, y)
                break
        if found is None:
            return None
        keys.append(found[0])
        sum_a += found[1]
        sum_y += found[2]
    return keys, sum_a, sum_y


def _rank_and_filter(dom: PairDomain, n: int, walks: list) -> tuple[list, dict]:
    """Rank closed walks by ratio; union top-K with slack-filtered set."""
    cands = []
    for cyc in walks:
        cc = _cycle_costs(dom, n, cyc)
        if cc is None:
            continue
        keys, sa, sy = cc
        if sa <= 0:
            continue
        cands.append({"states": cyc, "keys": keys, "sum_a": sa, "sum_y": sy,
                      "ratio": Fraction(sy, sa), "slack": sy - 2 * sa})
    cands.sort(key=lambda r: (-r["ratio"], r["slack"], len(r["states"])))
    topk = cands[:TOP_K]
    slackers = [c for c in cands if c["slack"] in SLACK_SET]
    seen = set()
    picked = []
    for c in topk + slackers:
        key = tuple(c["states"])
        if key not in seen:
            seen.add(key)
            rec = dict(c)
            rec["ratio"] = str(rec["ratio"])
            picked.append(rec)
    return picked, {"enumerated": len(walks), "ranked": len(cands), "picked": len(picked)}


# WP4-STEP-01: bounded closed walks from seed states (deterministic BFS, depth<=bound).
def bounded_walks(n: int, seeds: list[int], bound: int) -> list:
    """All closed walks (length 2..bound) rooted at seed states."""
    dom = PairDomain(n)
    out = []
    for s in sorted(seeds):
        stack = [(s, [s])]
        while stack:
            cur, path = stack.pop()
            if len(path) > bound:
                continue
            for _x, nxt in [(x, t) for x, t, _a, _y in _keep_successors(dom, cur, n)]:
                if nxt == s and len(path) >= 2:
                    out.append(list(path))
                elif len(path) < bound and nxt not in path:
                    stack.append((nxt, path + [nxt]))
    return out


# WP4-STEP-01: build the frozen near-critical selection set.
def near_critical_selection(imp: str) -> tuple[list, dict]:
    """Parent critical (all sizes in selection) + ranked extras (n4 exhaustive, n5/6 spliced)."""
    out: list = []
    info: dict = {}
    dom4 = PairDomain(4)
    raw4 = bounded_cycles(4, sorted(dom4.reachable()), CYCLE_LEN_BOUND)
    picked4, info4 = _rank_and_filter(dom4, 4, raw4)
    for c in picked4:
        c["n"] = 4
    out += picked4
    info["n4"] = info4
    print("[WP4-STEP-01] near-critical n4: %d simple cycles -> %d picked"
          % (len(raw4), len(picked4)), flush=True)
    for n in (5, 6):
        dom = PairDomain(n)
        cycles = json.load(open(os.path.join(imp, "v01baseline", "v01",
                                             "critical_n%d_canonical_cycles.json" % n),
                                encoding="utf-8"))
        seeds = sorted({e["source"] for c in cycles for e in c["edges"]})
        walks = bounded_walks(n, seeds, CYCLE_LEN_BOUND)
        picked, inf = _rank_and_filter(dom, n, walks)
        for c in picked:
            c["n"] = n
        out += picked
        info["n%d" % n] = inf
        print("[WP4-STEP-01] near-critical n=%d: %d spliced walks -> %d picked"
              % (n, len(walks), len(picked)), flush=True)
    return out, info


# WP4-STEP-01: noncritical exact edges (selection n2-5 full; validation n6-7 sampled).
def noncritical_edges(sizes_sel: list[int], sizes_val: list[int]) -> tuple[dict, dict]:
    """Deterministic noncritical KEEP-edge lists (critical states excluded)."""
    sel: dict = {}
    val: dict = {}
    for n in sizes_sel:
        dom = PairDomain(n)
        crit = set()
        try:
            cycles = json.load(open(os.path.join(
                ROOT, "artifacts", "v03", "parent_import", "v01baseline", "v01",
                "critical_n%d_canonical_cycles.json" % n), encoding="utf-8"))
            for c in cycles:
                crit.update(e["source"] for e in c["edges"])
        except OSError:
            pass
        rows = []
        for pid in sorted(dom.reachable()):
            if pid in crit:
                continue
            for x in range(1, n + 1):
                tgt, a, y = dom.edge(pid, x, "KEEP")
                rows.append([pid, x, tgt, a, y])
        sel[str(n)] = rows
        print("[WP4-STEP-01] noncritical selection n=%d: %d edges" % (n, len(rows)), flush=True)
    rng = random.Random(20260923)
    for n in sizes_val:
        dom = PairDomain(n)
        reached = sorted(dom.reachable())
        cap = N6_SAMPLE if n == 6 else N7_SAMPLE
        sample = rng.sample(reached, min(cap, len(reached)))
        rows = []
        for pid in sample:
            for x in range(1, n + 1):
                tgt, a, y = dom.edge(pid, x, "KEEP")
                rows.append([pid, x, tgt, a, y])
        val[str(n)] = rows
        print("[WP4-STEP-01] noncritical validation n=%d: %d edges" % (n, len(rows)), flush=True)
    return sel, val


# WP4-STEP-01: generated development/validation histories (frozen disjoint seeds).
def generated_histories(which: str) -> list:
    """Seeded paired histories (dev-only builder; separate seeds/modules from banks)."""
    from python.splay_ref.splay import build_balanced, build_spine
    from python.cycles.enumerate import node_shape_string
    seeds = DEV_SEEDS if which == "selection" else VAL_SEEDS
    sizes = DEV_SIZES if which == "selection" else VAL_SIZES
    per = DEV_HISTORIES_PER if which == "selection" else VAL_HISTORIES_PER
    out = []
    for n in sizes:
        for i in range(per):
            seed = seeds[i % len(seeds)] + i
            rng = random.Random("WP4-%s:%d:%d" % (which, n, seed))
            keys = list(range(1, n + 1))
            T0 = build_spine(keys) if (i % 2 == 0) else build_balanced(keys)
            length = [24, 48, 96][i % 3]
            hist = [[("KEEP" if rng.random() < 0.7 else "DELETE"), rng.randint(1, n)]
                    for _ in range(length)]
            out.append({"n": n, "seed": seed, "init_shape": node_shape_string(T0), "history": hist})
    print("[WP4-STEP-01] generated %s: %d histories" % (which, len(out)), flush=True)
    return out


# WP4-STEP-01: materialize rotation-level dev/validation corpora (frozen, pre-synthesis).
def _stepwise(n: int, root, x: int, side: str, mode: str):
    """Rotation events for one access side (case/keys/interval per rotation).

    Returns (events, new_root): splay mutates in place and only the returned
    root stays valid; callers MUST reassign (stale-root discipline).
    """
    from python.transfer import branchA as branchA_mod
    steps, top = branchA_mod.stepwise_access(root, x, n)
    return ([{"mode": mode, "side": side, "splay_case": s["splay_case"], "keys": s["keys"],
              "interval": s["interval"], "nkeys": n, "x": x,
              "a_edge": 0, "y_edge": 0, "w_num": 0, "w_den": 1} for s in steps], top)


def _edge_events(dom: PairDomain, n: int, pid: int, x: int, mode: str, c_const: int) -> list:
    """Rotation events for one pair edge; KEEP terminal B-rotation carries (a,y)."""
    from python.cycles.enumerate import build_node_tree
    from python.splay_ref.splay import cost
    a_id, b_id = dom.unpid(pid)
    A0 = build_node_tree(dom.shapes, a_id, n)
    B0 = build_node_tree(dom.shapes, b_id, n)
    a = cost(A0, x)
    events, _A1 = _stepwise(n, A0, x, "A", mode)
    if mode == "KEEP":
        y = cost(B0, x)
        B0b = build_node_tree(dom.shapes, b_id, n)
        bevents, _B1 = _stepwise(n, B0b, x, "B", mode)
        if bevents:
            bevents[-1]["a_edge"] = a
            bevents[-1]["y_edge"] = y
        events += bevents
    return events


def build_dev_corpus(imp: str, near: list, gen_histories: list, c_const: int = 2) -> dict:
    """Rotation-level development sequences (critical x3 rounds, near-critical, histories).

    w is NOT stored (C-dependent); terminal events carry (a_edge, y_edge) and the
    evaluator computes w = y - C*a exactly.
    """
    sequences = []
    for n in (4, 5, 6):
        dom = PairDomain(n)
        cycles = json.load(open(os.path.join(imp, "v01baseline", "v01",
                                             "critical_n%d_canonical_cycles.json" % n),
                                encoding="utf-8"))
        for cid, cyc in enumerate(cycles):
            rots = []
            for e in cyc["edges"]:
                rots += _edge_events(dom, n, e["source"], e["key"], e["mode"], c_const)
            sequences.append({"id": "crit-n%d-c%d" % (n, cid), "rotations": rots})
            sequences.append({"id": "crit-n%d-c%d-r2" % (n, cid), "rotations": list(rots)})
            sequences.append({"id": "crit-n%d-c%d-r3" % (n, cid), "rotations": list(rots)})
    for i, cyc in enumerate(near):
        n = cyc["n"]
        dom = PairDomain(n)
        rots = []
        cur_states = cyc["states"]
        for j, src in enumerate(cur_states):
            keys = cyc["keys"]
            rots += _edge_events(dom, n, src, keys[j % len(keys)], "KEEP", c_const)
        sequences.append({"id": "near-n%d-%d" % (n, i), "rotations": rots})
    for i, h in enumerate(gen_histories):
        n = h["n"]
        from python.cycles.enumerate import build_tree_from_shape
        from python.splay_ref.splay import cost
        A = build_tree_from_shape(h["init_shape"], n)
        B = build_tree_from_shape(h["init_shape"], n)
        rots = []
        for mode, x in h["history"]:
            a = cost(A, x)
            evs, A = _stepwise(n, A, x, "A", mode)
            rots += evs
            if mode == "KEEP":
                y = cost(B, x)
                brots, B = _stepwise(n, B, x, "B", mode)
                if brots:
                    brots[-1]["a_edge"] = a
                    brots[-1]["y_edge"] = y
                rots += brots
        sequences.append({"id": "gen-%d" % i, "rotations": rots})
    print("[WP4-STEP-01] dev corpus: %d sequences" % len(sequences), flush=True)
    return {"sequences": sequences}


# WP4-STEP-01: noncritical prefix sequences (seeded 8-access prefixes + edge).
def build_prefixes(noncritical_sel: dict) -> list:
    """Short-history prefixes ending at noncritical edges (deterministic seeds)."""
    import random as _random
    from python.cycles.enumerate import build_node_tree
    sequences = []
    for nstr, rows in sorted(noncritical_sel.items()):
        n = int(nstr)
        dom = PairDomain(n)
        for (pid, x, _t, _a, _y) in rows:
            rng = _random.Random("prefix:%d:%d:%d" % (n, pid, x))
            A = build_node_tree(dom.shapes, 0, n)
            B = build_node_tree(dom.shapes, 0, n)
            rots = []
            for _ in range(8):
                mode = "KEEP" if rng.random() < 0.7 else "DELETE"
                xk = rng.randint(1, n)
                evs, A, B = _prefix_step(dom, n, A, B, mode, xk)
                rots += evs
            rots += _edge_events(dom, n, pid, x, "KEEP", 2)
            sequences.append({"id": "pre-n%d-%d-%d" % (n, pid, x), "rotations": rots})
    print("[WP4-STEP-01] prefix corpus: %d sequences" % len(sequences), flush=True)
    return sequences


def _prefix_step(dom: PairDomain, n: int, A, B, mode: str, x: int) -> tuple[list, object, object]:
    from python.splay_ref.splay import cost
    a = cost(A, x)
    evs, A = _stepwise(n, A, x, "A", mode)
    rots = evs
    if mode == "KEEP":
        y = cost(B, x)
        brots, B = _stepwise(n, B, x, "B", mode)
        if brots:
            brots[-1]["a_edge"] = a
            brots[-1]["y_edge"] = y
        rots += brots
    return rots, A, B


if __name__ == "__main__":
    print("[WP4-STEP-01] discovery is library code; see run_phase10.py", flush=True)
