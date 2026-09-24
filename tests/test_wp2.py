"""WP-2 stress tests: scale behavior, hill-climb locality, idempotency, invalid inputs.

Probes run on seeded generated histories (development measurement, never holdouts)
and temp fixtures. Each test prints WP2STRESS-<id> lines; failure exits non-zero.
"""
import json
import os
import random
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from python.cycles.enumerate import PairDomain, build_node_tree  # noqa: E402
from python.cycles import stratify as strat_mod  # noqa: E402
from python.l6_translation import heavy as heavy_mod  # noqa: E402
from python.l6_translation import rank as rank_mod  # noqa: E402
from python.splay_ref.splay import build_balanced  # noqa: E402
from scripts.run_phase05 import _apply_single_rotation, _rotatable_edges  # noqa: E402

FAILS: list[str] = []


def check(name: str, cond: bool) -> None:
    print(("WP2STRESS-PASS " if cond else "WP2STRESS-FAIL ") + name)
    if not cond:
        FAILS.append(name)


def _random_tree(rng: random.Random, n: int):
    """Random BST by seeded insertion order (no Catalan enumeration)."""
    from python.splay_ref.splay import Node
    keys = list(range(1, n + 1))
    rng.shuffle(keys)
    root = None
    for k in keys:
        node = Node(k)
        if root is None:
            root = node
            continue
        cur = root
        while True:
            if k < cur.key:
                if cur.left is None:
                    cur.left = node
                    node.parent = cur
                    break
                cur = cur.left
            else:
                if cur.right is None:
                    cur.right = node
                    node.parent = cur
                    break
                cur = cur.right
    return root


def _flips_after_rotation(n: int, ref_tree, key: int, direction: str) -> int:
    """Heavy-flip count for one raw rotation of the given reference tree."""
    B = build_balanced(list(range(1, n + 1)))
    r0 = rank_mod.all_ranks(ref_tree)
    h0 = heavy_mod.heavy_edges(strat_mod._snapshot(B), r0)
    A2 = _apply_single_rotation(strat_mod._snapshot(ref_tree), key, direction)
    if A2 is None:
        return -1
    r1 = rank_mod.all_ranks(A2)
    h1 = heavy_mod.heavy_edges(strat_mod._snapshot(B), r1)
    return len(set(h0) ^ set(h1))


def test_hillclimb_locality() -> None:
    rng = random.Random(20260923)
    best = {"n": 0, "flips": 0}
    t0 = time.time()
    for n in (8, 16, 32, 64):
        cur_flips = 0
        elite = _random_tree(rng, n)
        for _step in range(120):
            if rng.random() < 0.5 and elite is not None:
                # Mutate the elite: one random raw rotation of the current best.
                cand = strat_mod._snapshot(elite)
                edges = _rotatable_edges(cand)
                if edges:
                    key, direction = rng.choice(edges)
                    moved = _apply_single_rotation(cand, key, direction)
                    if moved is not None:
                        cand = moved
                else:
                    cand = _random_tree(rng, n)
            else:
                cand = _random_tree(rng, n)
            edges = _rotatable_edges(cand)
            if not edges:
                continue
            key, direction = rng.choice(edges)
            f = _flips_after_rotation(n, cand, key, direction)
            if f > cur_flips:
                cur_flips = f
                elite = cand
        print("WP2STRESS-HILL n=%d maxflips=%d" % (n, cur_flips))
        if cur_flips > best["flips"]:
            best = {"n": n, "flips": cur_flips}
    dt = time.time() - t0
    print("WP2STRESS-HILL seconds=%.1f" % dt)
    check("WP2STRESS-HILL flips bounded small (<=6 to n=64)", best["flips"] <= 6)


def test_stratify_idempotent() -> None:
    import hashlib
    dom = PairDomain(4)
    h = lambda: hashlib.sha256(json.dumps(
        strat_mod.analyze_edge(dom, 4, 87, 1), sort_keys=True, default=str
    ).encode()).hexdigest()
    check("WP2STRESS-IDEM stratify deterministic", h() == h())


def test_invalid_inputs() -> None:
    from python.l6_translation import contracted as cmod
    from python.l6_translation import pairing as pmod
    try:
        pmod.decompose_zigzig([1, 2], {1: 0, 2: 0})
        check("WP2STRESS-INV triple arity enforced", False)
    except ValueError:
        check("WP2STRESS-INV triple arity enforced", True)
    try:
        rank_mod.rank_in_reference(build_balanced([1, 2]), 99)
        check("WP2STRESS-INV absent key raises", False)
    except KeyError:
        check("WP2STRESS-INV absent key raises", True)
    check("WP2STRESS-INV contracted monotonic",
          all(cmod.contracted(g + 1) >= cmod.contracted(g) for g in range(200)))


if __name__ == "__main__":
    test_hillclimb_locality()
    test_stratify_idempotent()
    test_invalid_inputs()
    print("WP2STRESS-FAILURES:", FAILS if FAILS else "none")
    sys.exit(1 if FAILS else 0)
