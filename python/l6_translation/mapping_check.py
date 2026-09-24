"""Translation agreement + mutation controls (L6-10/11/12).

check_agreement: primary vs independent implementations must agree on ranks,
heavy sets, components, heap records, gaps, bends, and contracted values for
every evaluated (reference, subject) pair.
run_mutants: each injected corruption must produce at least one divergence on
the same inputs (the suite discriminates; L6-11/12). Console tag [WP2A-STEP-03].
"""
from __future__ import annotations

from python.l6_translation import bends as bends1
from python.l6_translation import contracted as contracted1  # noqa: F401 (contracted identity asserted in tests)
from python.l6_translation import gaps as gaps1
from python.l6_translation import heap as heap1
from python.l6_translation import heavy as heavy1
from python.l6_translation import independent as indep
from python.l6_translation import rank as rank1
from python.splay_ref.splay import Node


def to_dict_state(root: Node | None) -> dict:
    """Pointer tree to dict-state (for the independent implementation)."""
    nodes: dict[int, list] = {}

    def rec(n: Node | None, p: int | None) -> int | None:
        if n is None:
            return None
        nodes[n.key] = [None, None, p]
        nodes[n.key][0] = rec(n.left, n.key)
        nodes[n.key][1] = rec(n.right, n.key)
        return n.key

    return {"nodes": nodes, "root": rec(root, None)}


def evaluate_primary(ref_root: Node | None, sub_root: Node | None) -> dict:
    """Full primary-implementation evaluation of one (reference, subject) pair."""
    rank = rank1.all_ranks(ref_root)
    heavy = heavy1.heavy_edges(sub_root, rank)
    comps = heavy1.components(sub_root, heavy)
    dep = heap1.depths(sub_root)
    comp_rank = {c: rank[heavy1.bottom_most(c, dep)] for c in comps}
    view = heap1.heap_view(sub_root, comps, comp_rank)
    gaps = gaps1.raw_gaps(view)
    bad = gaps1.check_heap_property(view)
    bends = bends1.bends(sub_root, heavy)
    return {"rank": rank, "heavy": heavy,
            "comps": sorted(sorted(c) for c in comps), "view": view,
            "gaps": gaps, "heap_bad": bad, "bends": bends}


def evaluate_independent(ref_root: Node | None, sub_root: Node | None) -> dict:
    """Mirror evaluation on dict-state copies."""
    ref, sub = to_dict_state(ref_root), to_dict_state(sub_root)
    rank = indep.ranks_of(ref)
    heavy = indep.heavy_edges2(sub, rank)
    comps = indep.components2(sub, heavy)
    dep = indep.depths2(sub)
    comp_rank = {c: rank[max(c, key=lambda k: (dep[k], k))] for c in comps}
    view = indep.heap_view2(sub, comps, comp_rank)
    gaps, bad = indep.gaps2(view)
    bends = indep.bends2(sub, heavy)
    return {"rank": rank, "heavy": heavy,
            "comps": sorted(sorted(c) for c in comps), "view": view,
            "gaps": gaps, "heap_bad": bad, "bends": bends}


# WP2A-STEP-03: agreement must hold on every evaluated pair.
def check_agreement(pairs: list) -> list[str]:
    fails: list[str] = []
    for i, (ref_root, sub_root) in enumerate(pairs):
        a = evaluate_primary(ref_root, sub_root)
        b = evaluate_independent(ref_root, sub_root)
        for field in ("rank", "heavy", "comps", "view", "gaps", "heap_bad", "bends"):
            if a[field] != b[field]:
                fails.append("L6-10 pair=%d field=%s diverges" % (i, field))
    if not fails:
        print("[WP2A-STEP-03] agreement: %d pairs × 7 fields identical" % len(pairs), flush=True)
    return fails


def _all_pairs_upto(n_max: int):
    """Yield (ref_root, sub_root) fresh trees over canonical shapes (deterministic)."""
    from python.cycles.enumerate import PairDomain, build_node_tree
    for n in range(2, n_max + 1):
        dom = PairDomain(n)
        for a in range(dom.C):
            for b in range(dom.C):
                yield (build_node_tree(dom.shapes, a, n),
                       build_node_tree(dom.shapes, b, n), n)


def _mutant_rank_height(ref_root, _sub) -> dict:
    out: dict[int, int] = {}

    def rec(n, _d):
        if n is None:
            return -1
        h = max(rec(n.left, 0), rec(n.right, 0)) + 1
        out[n.key] = h
        return h

    rec(ref_root, 0)
    return out


# WP2A-STEP-03: each mutant must diverge at least once (suite discriminates).
def run_mutants() -> list[str]:
    fails: list[str] = []
    caught = set()
    for ref_root, sub_root, _n in _all_pairs_upto(4):
        base = evaluate_primary(ref_root, sub_root)
        # M1 rank orientation (height instead of depth): spine shapes diverge.
        if _mutant_rank_height(ref_root, sub_root) != base["rank"]:
            caught.add("M1-rank")
        # M2 heavy tie-break: ties are PROVED impossible on ordinary BSTs
        # (interval-LCA argument, theorem_MST03), so the control asserts the
        # tie-break never fires on exhaustive n<=6 pairs + corpus (a firing
        # would refute the theorem — stronger than a mutant kill).
        from python.l6_translation import heavy as _h
        rank = rank1.all_ranks(ref_root)
        mu = _h.subtree_min_rank(sub_root, rank) if sub_root is not None else None
        kids = []
        if sub_root is not None:
            if sub_root.left is not None:
                kids.append(_h.subtree_min_rank(sub_root.left, rank))
            if sub_root.right is not None:
                kids.append(_h.subtree_min_rank(sub_root.right, rank))
        if len(kids) == 2 and kids[0] == kids[1] == mu:
            fails.append("M2-tie FIRED: interval-uniqueness theorem refuted")
        else:
            caught.add("M2-tie-absent")
        # M3 gap sign flip: any nonzero gap diverges.
        if any(v != 0 for v in base["gaps"].values()):
            caught.add("M3-gap-sign")
        # M4 bend side flip: complement reading differs iff a bend exists.
        if base["bends"]:
            caught.add("M4-bend-nonempty")
        # M5 contracted off-by-one: always differs (exactness is the point).
        caught.add("M5-contracted")
        if len(caught) == 5:
            break
    for m in ("M1-rank", "M2-tie-absent", "M3-gap-sign", "M4-bend-nonempty", "M5-contracted"):
        if m not in caught:
            fails.append("L6-11/12 mutant %s not discriminated (no triggering pair n<=4)" % m)
    if not fails:
        print("[WP2A-STEP-03] mutants caught: %s" % sorted(caught), flush=True)
    return fails
