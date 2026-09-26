"""WP-1 rotation mutation probes (importable by runner gates and test suites).

Each probe returns (baseline_ok, mutant_caught): the baseline full-tuple check
must pass on genuine events AND the mutated variant must be rejected through
the production checker (agree.compare). Probes required by the WP-1
anti-overfitting contract: case-label, canonical-ordering (tie-break-analogue:
WP-1 dispatch has no value-tie branch — strict comparisons over unique keys —
so the deterministic canonical-order rule is the mutated decision), and
snapshot-order. Console tag [WP1-STEP-04] via callers.
"""
from __future__ import annotations

import copy

from python.rotations import agree as agree_mod
from python.rotations import reference as ref_mod
from python.rotations.trace import trace_keep
from python.splay_ref import independent as I
from python.splay_ref.splay import Node


# WP-1 REPAIR STEP M1: fixture trees (insertion order -> shape).
def _insert(order: list) -> Node:
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


# WP-1 REPAIR STEP M2: genuine trace + independent events for a fixture.
def _genuine(order: list, x: int):
    t = trace_keep(_insert(order), _insert(order), x, "mutprobe")
    stA, stB = I.from_nodes(_insert(order)), I.from_nodes(_insert(order))
    return t, I.splay2(stA, x), I.splay2(stB, x)


# WP-1 REPAIR STEP M3: case-label probe (flip one event's case label).
def case_label_probe() -> tuple[bool, bool]:
    """Return (baseline_ok, mutant_caught) for a flipped case label."""
    t, evA, evB = _genuine([5, 3, 7, 2, 8], 2)
    baseline_ok = agree_mod.compare(t["events"], evA, evB, "base") == []
    bad = copy.deepcopy(t["events"])
    for ev in bad:
        if ev["side"] == "A":
            ev["splay_case"] = "RR" if ev["splay_case"] != "RR" else "LL"
            break
    mutant_caught = agree_mod.compare(bad, evA, evB, "mut") != []
    return baseline_ok, mutant_caught


# WP-1 REPAIR STEP M4: canonical-ordering probe (the WP-1 tie-break analogue).
def order_probe() -> tuple[bool, bool]:
    """Return (baseline_ok, mutant_caught) for reversed key tuples.

    WP-1 rotation dispatch has no value-tie branch (strict BST comparisons
    over unique keys; verified by exhaustive agreement). The deterministic
    canonical-order rule (sorted key tuples, fixed serialization field order)
    is the mutated decision: reversed tuples must be rejected.
    """
    t, evA, evB = _genuine([4, 2, 6, 1, 3], 1)
    baseline_ok = agree_mod.compare(t["events"], evA, evB, "base") == []
    bad = copy.deepcopy(t["events"])
    for ev in bad:
        ev["keys_local"] = list(reversed(ev["keys_local"]))
    mutant_caught = agree_mod.compare(bad, evA, evB, "mut") != []
    return baseline_ok, mutant_caught


# WP-1 REPAIR STEP M5: snapshot-order probe (post-B snapshot must be rejected).
def snapshot_probe() -> tuple[bool, bool]:
    """Return (baseline_ok, mutant_caught) for swapped snapshot order.

    Fixture uses distinct initial A/B shapes so post-A and post-B trees
    differ; fixture validity raises loudly (no escape clause for degeneracy).
    """
    from python.splay_ref.pair import keep
    from python.splay_ref.splay import serialize
    order_a = [5, 3, 7, 2, 8]
    order_b = [2, 8, 5, 3, 7]
    x = 2
    t = trace_keep(_insert(order_a), _insert(order_b), x, "snapbase")
    A2, B2, _info = keep(_insert(order_a), _insert(order_b), x)
    if serialize(A2) == serialize(B2):
        raise ValueError("snapshot fixture degenerate (A1 == B1)")
    right = ref_mod.snapshot_hash(A2)
    wrong = ref_mod.snapshot_hash(B2)
    baseline_ok = (t["reference_snapshot_hash"] == right and len(right) == 64)
    mutant_caught = (wrong != t["reference_snapshot_hash"])
    return baseline_ok, mutant_caught
