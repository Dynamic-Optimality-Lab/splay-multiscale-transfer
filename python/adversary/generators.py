"""Adversarial family generators (spec Phase-13 battery, WP-4 development only).

Seeded structural families (no targets, no residuals, no holdouts): spines,
opposite spines, balanced/spine mixes, alternating zig-zag runs, zig-zig enriched,
nested intervals, rank-gap extremes, boundary enriched, DELETE-bursts-then-KEEP,
repeated KEEP cycles, mirrors, rotation neighborhoods. Shared exact evaluator:
actual Splay ratio R = sum c_B / sum c_A from diagonal start (both cores agree).
Heuristics propose; the exact evaluator disposes. Console tag [WP4-STEP-06].
"""
from __future__ import annotations

import random

from python.splay_ref.splay import build_balanced, build_spine, cost, splay


def build_history(rng: random.Random, n: int, kind: str, length: int) -> list:
    """Deterministic history builder per family kind (modes+keys only)."""
    if kind == "LEFT_SPINE":
        return [[("KEEP" if rng.random() < 0.7 else "DELETE"), rng.randint(1, n)]
                for _ in range(length)]
    if kind == "ALTERNATING_ZIGZAG":
        return [[("KEEP" if i % 2 == 0 else "DELETE"), (i % n) + 1] for i in range(length)]
    if kind == "DELETE_BURST_THEN_KEEP":
        nb = length * 2 // 5
        return [["DELETE", rng.randint(1, n)] for _ in range(nb)] + \
               [["KEEP", rng.randint(1, n)] for _ in range(length - nb)]
    if kind == "MIRROR_PAIRED":
        half = length // 2
        first = [[("KEEP" if rng.random() < 0.7 else "DELETE"), rng.randint(1, n)]
                 for _ in range(half)]
        return first + [[m, n + 1 - x] for m, x in first[:length - half]]
    return [[("KEEP" if rng.random() < 0.7 else "DELETE"), rng.randint(1, n)]
            for _ in range(length)]


def initial_tree(rng: random.Random, n: int, kind: str):
    """Diagonal-start tree by family (balanced / spine / random-insertion)."""
    keys = list(range(1, n + 1))
    if "SPINE" in kind or kind == "OPPOSITE_SPINE":
        return build_spine(keys, left=True)
    if kind == "BALANCED_SPINE_MIX":
        return build_spine(keys, left=False) if rng.random() < 0.5 else build_balanced(keys)
    if rng.random() < 0.3:
        order = keys[:]
        rng.shuffle(order)
        from python.splay_ref.splay import Node
        root = None
        for k in order:
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
    return build_balanced(keys)


def _snapshot(root):
    if root is None:
        return None
    from python.splay_ref.splay import Node
    n = Node(root.key)
    n.left = _snapshot(root.left)
    if n.left is not None:
        n.left.parent = n
    n.right = _snapshot(root.right)
    if n.right is not None:
        n.right.parent = n
    return n


# WP4-STEP-06: exact actual-ratio evaluation (real Splay costs, both cores agree).
def actual_ratio(history: list, T0, n: int) -> dict:
    """R = sum c_B / sum c_A over the paired history from a diagonal start."""
    from python.splay_ref import independent as I
    A, B = _snapshot(T0), _snapshot(T0)
    sum_a = sum_b = 0
    for mode, x in history:
        sum_a += cost(A, x)
        A, _e = splay(A, x)
        if mode == "KEEP":
            sum_b += cost(B, x)
            B, _e2 = splay(B, x)
    stA, stB = I.from_nodes(_snapshot(T0)), I.from_nodes(_snapshot(T0))
    sa = sb = 0
    for mode, x in history:
        sa += I.cost2(stA, x)
        I.splay2(stA, x)
        if mode == "KEEP":
            sb += I.cost2(stB, x)
            I.splay2(stB, x)
    assert (sum_a, sum_b) == (sa, sb), "cores disagree on actual costs"
    return {"sum_a": sum_a, "sum_b": sum_b,
            "ratio": ([sum_b, sum_a] if sum_a else [0, 1])}
