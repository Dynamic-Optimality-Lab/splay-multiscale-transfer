"""Structural stratification of critical KEEP edges (WP-2B step 1, target-joined).

For every expanded critical edge: zig-class context, B-path heavy fraction under
the A1 reference, bend/gap/contracted deltas across the B splay, per-rotation
pairing classes (GOOD/BAD/IMPORTANT/UNIMPORTANT) via stepwise heap views, lazy
state transitions, intervals created per rotation, regret across the C ladder.
Pure structural measurement; no transfer synthesis. Console tag [WP2B-STEP-01].
"""
from __future__ import annotations

import sys

from python.cycles.enumerate import PairDomain, build_node_tree
from python.l6_translation import bends as bends_mod
from python.l6_translation import contracted as contracted_mod
from python.l6_translation import gaps as gaps_mod
from python.l6_translation import heap as heap_mod
from python.l6_translation import heavy as heavy_mod
from python.l6_translation import lazy as lazy_mod
from python.l6_translation import pairing as pairing_mod
from python.l6_translation import rank as rank_mod
from python.ontology import scales as scales_mod
from python.splay_ref.splay import Node, inorder, serialize

DIAGNOSTIC_LADDER = (2, 3, 4, 6, 8, 12, 16, 24, 32, 64)


def _path_keys(root: Node | None, x: int) -> list[int]:
    path = []
    cur = root
    while cur is not None:
        path.append(cur.key)
        if x == cur.key:
            return path
        cur = cur.left if x < cur.key else cur.right
    raise KeyError(x)


def _snapshot(root: Node | None) -> Node | None:
    """Deep copy a pointer tree (for stepwise replay)."""
    if root is None:
        return None
    n = Node(root.key)
    n.left = _snapshot(root.left)
    if n.left is not None:
        n.left.parent = n
    n.right = _snapshot(root.right)
    if n.right is not None:
        n.right.parent = n
    return n


def translated_view(ref_root: Node | None, sub_root: Node | None) -> dict:
    """Full translated snapshot: ranks, heavy, components, heap, gaps, bends."""
    rank = rank_mod.all_ranks(ref_root)
    heavy = heavy_mod.heavy_edges(sub_root, rank)
    comps = heavy_mod.components(sub_root, heavy)
    dep = heap_mod.depths(sub_root)
    comp_rank = {c: rank[heavy_mod.bottom_most(c, dep)] for c in comps}
    view = heap_mod.heap_view(sub_root, comps, comp_rank)
    gaps = gaps_mod.raw_gaps(view)
    heap_bad = gaps_mod.check_heap_property(view)
    bends = bends_mod.bends(sub_root, heavy)
    csum = sum(contracted_mod.contracted(g) for g in gaps.values())
    return {"rank": rank, "heavy": sorted(heavy), "n_components": len(comps),
            "gaps": gaps, "gap_sum": sum(gaps.values()), "heap_violations": heap_bad,
            "bends": sorted(bends), "contracted_sum": csum, "view": view}


def stepwise_b_splay(B0: Node | None, x: int) -> list[dict]:
    """Replay the B splay one rotation at a time, snapshotting (tree, case) steps."""
    from python.splay_ref.splay import _rotate_left, _rotate_right
    B = _snapshot(B0)
    cur = B
    while cur is not None and cur.key != x:
        cur = cur.left if x < cur.key else cur.right
    if cur is None:
        raise KeyError(x)
    node = cur
    steps = [{"tree": serialize(B), "case": "ROOT", "nodes": []}]
    while node.parent is not None:
        p = node.parent
        g = p.parent
        triple_keys = [node.key] if g is None else [node.key, p.key, g.key]
        if g is None:
            case = "ZIG"
            if p.left is node:
                _rotate_right(p)
            else:
                _rotate_left(p)
        elif p.left is node and g.left is p:
            case = "LL"
            _rotate_right(g)
            _rotate_right(p)
        elif p.right is node and g.right is p:
            case = "RR"
            _rotate_left(g)
            _rotate_left(p)
        elif p.left is node and g.right is p:
            case = "RL"
            _rotate_right(p)
            _rotate_left(g)
        else:
            case = "LR"
            _rotate_left(p)
            _rotate_right(g)
        # Re-root handle: find current root for snapshot.
        top = node
        while top.parent is not None:
            top = top.parent
        steps.append({"tree": serialize(top), "case": case, "nodes": triple_keys})
    return steps


def _parse_serialized(ss: str) -> Node | None:
    """Rebuild a pointer tree from a keyed serialization (keys fixed by inorder)."""
    pos = [0]

    def rec() -> Node | None:
        if ss[pos[0]] == ".":
            pos[0] += 1
            return None
        assert ss[pos[0]] == "("
        pos[0] += 1
        key = 0
        while ss[pos[0]].isdigit():
            key = key * 10 + int(ss[pos[0]])
            pos[0] += 1
        left = rec()
        right = rec()
        assert ss[pos[0]] == ")"
        pos[0] += 1
        n = Node(key)
        n.left = left
        if left is not None:
            left.parent = n
        n.right = right
        if right is not None:
            right.parent = n
        return n

    return rec()


# WP2B-STEP-01: analyze one critical KEEP edge structurally.
def analyze_edge(dom: PairDomain, n: int, source_pid: int, x: int) -> dict:
    """Full structural stratification of one KEEP edge (A0,B0) -x-> (A1,B1)."""
    from python.splay_ref.splay import cost, splay
    a_id, b_id = dom.unpid(source_pid)
    A0 = build_node_tree(dom.shapes, a_id, n)
    B0 = build_node_tree(dom.shapes, b_id, n)
    # Snapshot BEFORE splays: splay() mutates in place and only the returned
    # root stays valid; the input variable becomes a detached subtree.
    B0pre = _snapshot(B0)
    a, y = cost(A0, x), cost(B0, x)
    A1, evA = splay(A0, x)
    B1, evB = splay(B0, x)
    ref = A1
    before = translated_view(ref, _snapshot(B0pre))
    after = translated_view(ref, _snapshot(B1))
    # B-path heavy fraction under the A1 reference.
    path = _path_keys(_snapshot(B0pre), x)
    rank = rank_mod.all_ranks(ref)
    heavy = heavy_mod.heavy_edges(_snapshot(B0pre), rank)
    heavy_set = set(heavy)
    path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
    heavy_on_path = sum(1 for e in path_edges if e in heavy_set)
    light_positions = [i for i, e in enumerate(path_edges) if e not in heavy_set]
    # Per-rotation pairing classes via stepwise heap views.
    steps = stepwise_b_splay(_snapshot(B0pre), x)
    pairings = []
    created_per_rotation = []
    prev_members: dict[int, list] = {}
    # Initial lazy intervals: one per component over its heap-children.
    v0 = translated_view(ref, _snapshot(B0pre))
    interval_of = {}
    for b, rec0 in v0["view"].items():
        for k in rec0["heap_children"]:
            interval_of[k] = b
    for s in steps[1:]:
        tree = _parse_serialized(s["tree"])
        v = translated_view(ref, tree)
        cur_members = {b: sorted(v["view"][b]["heap_children"]) for b in v["view"]}
        created = sum(1 for b, m in cur_members.items()
                      if b not in prev_members or prev_members[b] != m)
        created_per_rotation.append(created)
        prev_members = cur_members
        if s["case"] in ("LL", "RR") and len(s["nodes"]) == 3:
            # Actual rotation triple -> heap-component bottoms (pairing correspondence).
            owner = {}
            for b, rec0 in v["view"].items():
                for k in rec0["members"]:
                    owner[k] = b
            triple = sorted({owner[k] for k in s["nodes"] if k in owner})
            if len(triple) == 3:
                dec = pairing_mod.decompose_zigzig(triple, rank)
                contracted_of = {b: contracted_mod.contracted(v["gaps"][b])
                                 for b in v["gaps"]}
                same = len({interval_of.get(k, k) for k in triple}) == 1
                for pr in dec:
                    cls = pairing_mod.classify_pairing(pr, same, contracted_of, (0, 0))
                    pairings.append({"case": s["case"], "class": cls,
                                     "same_interval": same})
            else:
                pairings.append({"case": s["case"], "class": "DEGENERATE_merged",
                                 "same_interval": False})
    bends_before, bends_after = set(before["bends"]), set(after["bends"])
    rec = {"x": x, "a": a, "y": y,
           "zig": {"ZIG": sum(1 for e in evB if e["case"] == "ZIG"),
                   "LL": sum(1 for e in evB if e["case"] == "LL"),
                   "RR": sum(1 for e in evB if e["case"] == "RR"),
                   "LR": sum(1 for e in evB if e["case"] == "LR"),
                   "RL": sum(1 for e in evB if e["case"] == "RL")},
           "b_path": {"length": len(path), "heavy": heavy_on_path,
                      "light_positions": light_positions},
           "bends": {"before": len(bends_before), "after": len(bends_after),
                     "destroyed": len(bends_before - bends_after),
                     "created": len(bends_after - bends_before)},
           "gap_sum": {"before": before["gap_sum"], "after": after["gap_sum"],
                       "delta": after["gap_sum"] - before["gap_sum"]},
           "contracted_sum": {"before": before["contracted_sum"],
                              "after": after["contracted_sum"],
                              "delta": after["contracted_sum"] - before["contracted_sum"]},
           "heap_violations": {"before": len(before["heap_violations"]),
                               "after": len(after["heap_violations"])},
           "pairings": pairings,
           "intervals_created_per_rotation": created_per_rotation,
           "max_intervals_per_rotation": max(created_per_rotation) if created_per_rotation else 0,
           "regret": {c: y - c * a for c in DIAGNOSTIC_LADDER},
           "s0_scale_path": [scales_mod.s0_subtree(len(path) - i) for i in range(len(path))]}
    rec["zig"]["zigzig"] = rec["zig"]["LL"] + rec["zig"]["RR"]
    rec["zig"]["zigzag"] = rec["zig"]["LR"] + rec["zig"]["RL"]
    return rec


def main() -> int:
    print("[WP2B-STEP-01] stratification needs corpus driver; see run_phase04.py", flush=True)
    return 2


if __name__ == "__main__":
    sys.exit(main())
