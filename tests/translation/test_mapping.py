"""Translation test suite (L6-02..12 mechanics). Fast; corpus-free except agreement sample."""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

from python.l6_translation import bends as bends_mod  # noqa: E402
from python.l6_translation import contracted as contracted_mod  # noqa: E402
from python.l6_translation import gaps as gaps_mod  # noqa: E402
from python.l6_translation import heap as heap_mod  # noqa: E402
from python.l6_translation import heavy as heavy_mod  # noqa: E402
from python.l6_translation import lazy as lazy_mod  # noqa: E402
from python.l6_translation import mapping_check as mc_mod  # noqa: E402
from python.l6_translation import ops as ops_mod  # noqa: E402
from python.l6_translation import pairing as pairing_mod  # noqa: E402
from python.l6_translation import rank as rank_mod  # noqa: E402
from python.splay_ref.splay import build_balanced  # noqa: E402

FAILS: list[str] = []


def check(name: str, cond: bool) -> None:
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        FAILS.append(name)


def test_contracted_identity() -> None:
    check("L6-09 contracted identity 0..4999",
          all(contracted_mod.contracted(g) == contracted_mod.contracted_real(g)
              for g in range(5000)))
    try:
        contracted_mod.contracted(-1)
        check("L6-09 negative gap rejected", False)
    except ValueError:
        check("L6-09 negative gap rejected", True)


def test_heavy_uniqueness() -> None:
    from python.cycles.enumerate import PairDomain, build_node_tree
    ties = 0
    total = 0
    for n in (2, 3, 4):
        dom = PairDomain(n)
        for a in range(dom.C):
            for b in range(dom.C):
                total += 1
                ref = build_node_tree(dom.shapes, a, n)
                sub = build_node_tree(dom.shapes, b, n)
                rank = rank_mod.all_ranks(ref)
                stack = [sub]
                while stack:
                    u = stack.pop()
                    if u is None:
                        continue
                    mu = heavy_mod.subtree_min_rank(u, rank)
                    kids = [heavy_mod.subtree_min_rank(c, rank)
                            for c in (u.left, u.right) if c is not None]
                    if len(kids) == 2 and kids[0] == kids[1] == mu:
                        ties += 1
                    stack += [u.left, u.right]
    check("L6-11 no heavy ties n<=4 (%d pairs)" % total, ties == 0)


def test_heap_gaps() -> None:
    r = build_balanced([1, 2, 3, 4, 5])
    rank = rank_mod.all_ranks(r)
    heavy = heavy_mod.heavy_edges(r, rank)
    comps = heavy_mod.components(r, heavy)
    dep = heap_mod.depths(r)
    comp_rank = {c: rank[heavy_mod.bottom_most(c, dep)] for c in comps}
    view = heap_mod.heap_view(r, comps, comp_rank)
    check("L6-04 heap property holds (self-view)", gaps_mod.check_heap_property(view) == [])
    check("L6-04 root gap zero", gaps_mod.raw_gaps(view)[heavy_mod.bottom_most(
        next(c for c in comps if any(k == r.key for k in c)), dep)] == 0)


def test_lazy_ops() -> None:
    check("L6-06 contiguity", lazy_mod.check_contiguity([2, 3, 4], [1, 2, 3, 4, 5]))
    check("L6-06 non-contiguity", not lazy_mod.check_contiguity([2, 4], [1, 2, 3, 4, 5]))
    check("L6-06 growing", lazy_mod.transition_state([1, 2], [1, 2, 3]) == "GROWING")
    check("L6-06 shrinking", lazy_mod.transition_state([1, 2, 3], [1, 2]) == "SHRINKING")
    check("L6-06 broken", lazy_mod.transition_state([1, 2], []) == "BROKEN")
    check("L6-06 point gap", lazy_mod.point_gap(7, 3) == 4)
    check("L6-05 pairing classes",
          pairing_mod.classify_pairing({"hung": 1, "below": 2}, True, {1: 5, 2: 5}, (0, 0)) == "GOOD")
    check("L6-05 pairing bad",
          pairing_mod.classify_pairing({"hung": 1, "below": 2}, True, {1: 5, 2: 7}, (0, 0)) == "BAD")
    check("L6-05 pairing important",
          pairing_mod.classify_pairing({"hung": 1, "below": 2}, False, {1: 5, 2: 5}, (3, 5)) == "IMPORTANT")
    check("L6-05 pairing unimportant",
          pairing_mod.classify_pairing({"hung": 1, "below": 2}, False, {1: 5, 2: 5}, (3, 99)) == "UNIMPORTANT")
    op = ops_mod.make_op("PAIR_UP", "zigzig", [1], [2])
    check("L6-09 op unpaid", op["paid_free"] == "UNDETERMINED_PRE_WP6")
    try:
        ops_mod.make_op("NOPE", "x", [], [])
        check("L6-09 unknown op rejected", False)
    except ValueError:
        check("L6-09 unknown op rejected", True)


def test_mutants() -> None:
    check("L6-11/12 mutants discriminate", mc_mod.run_mutants() == [])


def test_bends_unit() -> None:
    r = build_balanced([1, 2, 3, 4, 5, 6, 7])
    from python.splay_ref.splay import splay
    r2, _e = splay(r, 1)
    rank = rank_mod.all_ranks(r2)
    heavy = heavy_mod.heavy_edges(r2, rank)
    bends = bends_mod.bends(r2, heavy)
    check("L6-08 bends computable", isinstance(bends, set))


if __name__ == "__main__":
    test_contracted_identity()
    test_heavy_uniqueness()
    test_heap_gaps()
    test_lazy_ops()
    test_mutants()
    test_bends_unit()
    print("FAILURES:", FAILS if FAILS else "none")
    sys.exit(1 if FAILS else 0)
