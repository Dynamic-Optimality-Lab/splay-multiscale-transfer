"""WP-5 Phase-16 large-n adversarial falsification (frozen candidates only).

Generates structural histories at sizes far beyond exhaustive development
(n = 16,24,32,48,64,96,128,192,256) with fresh WP-5 seeds (never the WP-4
discovery seeds, never H3T residuals), evaluates every frozen candidate exactly
via the Phase-15 evaluator, and replays every claimed violation with the
clean-room evaluator. Heuristics propose; the exact evaluator disposes; only
exact-replayed witnesses count as kills. Console tag [WP5-STEP-07].
"""
from __future__ import annotations

import os
import random
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

from python.audit import cleanroom as cleanroom_mod  # noqa: E402
from python.holdout import h3t_evaluate as eval_mod  # noqa: E402
from python.splay_ref.splay import Node, build_balanced, build_spine, serialize  # noqa: E402

SIZES = [16, 24, 32, 48, 64, 96, 128, 192, 256]
LENGTH = 48
PER_SIZE = 6
KINDS = ["RANDOM_LEGAL", "SPINE_VS_BALANCED", "OPPOSITE_SPINE",
         "ALTERNATING_KEEP_DELETE", "DELETE_BURST_THEN_KEEP", "MIRROR_PAIRED"]


# WP5-STEP-07: structural history builders (fresh WP-5 seeds, target-blind).
def build_history(rng: random.Random, n: int, kind: str, length: int) -> list:
    """One (mode, key) history; structural pattern only, no candidate input."""
    hist: list = []
    if kind == "ALTERNATING_KEEP_DELETE":
        for i in range(length):
            hist.append(("KEEP" if i % 2 == 0 else "DELETE", rng.randint(1, n)))
    elif kind == "DELETE_BURST_THEN_KEEP":
        for i in range(length):
            hist.append(("DELETE" if i < length // 2 else "KEEP", rng.randint(1, n)))
    elif kind == "MIRROR_PAIRED":
        keys = [rng.randint(1, n) for _ in range((length + 1) // 2)]
        for i, x in enumerate(keys):
            hist.append(("KEEP", x))
            if len(hist) < length:
                hist.append(("KEEP", n + 1 - x))
        hist = hist[:length]
    else:
        for _ in range(length):
            hist.append(("KEEP" if rng.random() < 0.7 else "DELETE", rng.randint(1, n)))
    return hist


# WP5-STEP-07: initial tree by kind (balanced / spine / random insertion).
def initial_tree(rng: random.Random, n: int, kind: str):
    """Deterministic diagonal-start tree for the given kind."""
    keys = list(range(1, n + 1))
    if kind in ("SPINE_VS_BALANCED", "OPPOSITE_SPINE"):
        return build_spine(keys, left=True)
    if kind == "RANDOM_LEGAL" and rng.random() < 0.5:
        order = keys[:]
        rng.shuffle(order)
        root = None
        for kk in order:
            node = Node(kk)
            if root is None:
                root = node
                continue
            cur = root
            while True:
                if kk < cur.key:
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


# WP5-STEP-07: one large-n trial (primary evaluation + clean-room replay).
def trial(n: int, kind: str, seed: int, candidate: dict) -> dict:
    """Evaluate a frozen candidate on one fresh history; replay any kill."""
    rng = random.Random("WP5-LARGEN:%d:%s:%d" % (n, kind, seed))
    T0 = initial_tree(rng, n, kind)
    history = build_history(rng, n, kind, LENGTH)
    # NOTE: keyed serialization (clean-room parses exact keys 1..n; the primary
    # path assigns keys inorder, which reproduces the same BST for valid shapes).
    shape = serialize(T0)
    # NOTE: synthetic histories carry no recorded totals; episode_rotations
    # checks totals only when the episode record provides them (bank episodes).
    rots, _sa, _sy = eval_mod.episode_rotations(
        {"n": n, "init_shape": shape, "history": history,
         "episode_hash": "large-n-synthetic"})
    res = eval_mod.simulate(candidate["active_predicate"],
                            candidate["injection_rules"][0]["k"],
                            candidate["universal_constant_C"], rots)
    clean = cleanroom_mod.simulate_episode(
        n, shape, history,
        _predicate_name(candidate), candidate["injection_rules"][0]["k"],
        candidate["universal_constant_C"])
    # NOTE: primary returns Fractions, clean-room [num, den] lists.
    agree = ([res["max_res"].numerator, res["max_res"].denominator]
             == list(clean["max_res"])
             and res["feasible"] == clean["feasible"])
    return {"n": n, "kind": kind, "seed": seed,
            "feasible": res["feasible"],
            "max_res": [res["max_res"].numerator, res["max_res"].denominator],
            "first": res["first"], "agree": agree,
            "clean_max_res": list(clean["max_res"])}


# WP5-STEP-07: predicate name recovery from the frozen record (fail-closed).
def _predicate_name(candidate: dict) -> str:
    """Return P_all/P_keep for the frozen predicate; refuse anything else."""
    pred = candidate["active_predicate"]
    if pred == {"any_of": [{"mode_is": "KEEP"}, {"mode_is": "DELETE"}]}:
        return "P_all"
    if pred == {"mode_is": "KEEP"}:
        return "P_keep"
    raise ValueError("unknown frozen predicate (clean-room supports P_all/P_keep only)")
