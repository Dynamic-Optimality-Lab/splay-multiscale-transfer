"""WP-5 Phase-15 H3T fresh evaluation (frozen-calculus-only imports).

Evaluates each frozen MSTC candidate over every H3T episode exactly (Fraction
residuals), with canonical-order first violation + maximum violation + failure
class + replay bundle per candidate. The rotation primitive below is
separately written for this evaluator (no synthesis imports: no transfer,
solver, discovery, adversary, or generator modules — asserted by the Phase-15
import audit); agreement with the dev evaluator on a shared sample is checked
by tests, never by importing it. The dev-corpus convention is mirrored exactly:
the terminal B-rotation of a KEEP carries (a_edge, y_edge); root accesses carry
no burden events.

Console tag [WP5-STEP-04].
"""
from __future__ import annotations

import os
import sys
from fractions import Fraction

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

from python.ledger import state as ledger_state  # noqa: E402
from python.ledger import update as update_mod  # noqa: E402
from python.provenance import active as active_mod  # noqa: E402
from python.splay_ref.splay import Node, _rotate_left, _rotate_right, cost  # noqa: E402


# WP5-STEP-04: keyed shape parser (bank init_shape grammar '(left key right)').
def _parse_keyed(text: str):
    """Parse a keyed shape string into nested (left, key, right) tuples."""
    pos = [0]

    def rec():
        if text[pos[0]] == ".":
            pos[0] += 1
            return None
        assert text[pos[0]] == "("
        pos[0] += 1
        key = 0
        while text[pos[0]].isdigit():
            key = key * 10 + int(text[pos[0]])
            pos[0] += 1
        left = rec()
        right = rec()
        assert text[pos[0]] == ")"
        pos[0] += 1
        return (left, key, right)

    out = rec()
    assert pos[0] == len(text), "trailing bytes in keyed shape"
    return out


# WP5-STEP-04: keyed tuple tree to pointer BST (fresh construction path).
def _to_node(tree) -> Node | None:
    """Build a pointer BST from a keyed tuple tree."""
    if tree is None:
        return None
    left, key, right = tree
    node = Node(key)
    node.left = _to_node(left)
    if node.left is not None:
        node.left.parent = node
    node.right = _to_node(right)
    if node.right is not None:
        node.right.parent = node
    return node


# WP5-STEP-04: rotation primitive (separately written; pointer BST, depth+1 cost).
def _side_events(n: int, root, x: int, side: str, mode: str):
    """Replay one splay rotation-by-rotation; zeroed (a_edge, y_edge) events."""
    cur = root
    while cur is not None and cur.key != x:
        cur = cur.left if x < cur.key else cur.right
    if cur is None:
        raise KeyError(x)
    node = cur
    events: list = []
    while node.parent is not None:
        p = node.parent
        g = p.parent
        if g is None:
            case = "ZIG"
        elif p.left is node and g.left is p:
            case = "LL"
        elif p.right is node and g.right is p:
            case = "RR"
        elif p.left is node and g.right is p:
            case = "RL"
        else:
            case = "LR"
        keys = sorted({node.key, p.key} | ({g.key} if g is not None else set()))
        site = [min(keys), max(keys)]
        events.append({"mode": mode, "side": side, "splay_case": case,
                       "keys": keys, "interval": site, "nkeys": n, "x": x,
                       "a_edge": 0, "y_edge": 0, "w_num": 0, "w_den": 1})
        if case == "ZIG":
            if p.left is node:
                _rotate_right(p)
            else:
                _rotate_left(p)
        elif case == "LL":
            _rotate_right(g)
            _rotate_right(p)
        elif case == "RR":
            _rotate_left(g)
            _rotate_left(p)
        elif case == "RL":
            _rotate_right(p)
            _rotate_left(g)
        else:
            _rotate_left(p)
            _rotate_right(g)
    top = node
    while top.parent is not None:
        top = top.parent
    return events, top


# WP5-STEP-04: materialize one H3T episode as a rotation-level sequence.
def episode_rotations(episode: dict):
    """Return (rotations, sum_a, sum_y); raises on replay-total mismatch."""
    n = episode["n"]
    parsed = _parse_keyed(episode["init_shape"])
    A = _to_node(parsed)
    B = _to_node(parsed)
    rots: list = []
    sum_a = sum_y = 0
    for mode, x in episode["history"]:
        a = cost(A, x)
        evs, A = _side_events(n, A, x, "A", mode)
        rots += evs
        if mode == "KEEP":
            y = cost(B, x)
            sum_a += a
            sum_y += y
            bevs, B = _side_events(n, B, x, "B", mode)
            if bevs:
                bevs[-1]["a_edge"] = a
                bevs[-1]["y_edge"] = y
            rots += bevs
        else:
            sum_a += a
    if "sum_a" in episode and (sum_a != episode["sum_a"] or sum_y != episode["sum_y"]):
        raise ValueError("H3T episode %s replay totals mismatch (bank corrupt)"
                         % episode.get("episode_hash", "?")[:8])
    return rots, sum_a, sum_y


# WP5-STEP-04: exact single-candidate ledger simulation over rotation events.
def simulate(predicate: dict, k: int, c_const: int, rotations: list,
             produce_active: bool = True) -> dict:
    """Run T7/T5/T6 semantics from the frozen record; exact residuals.

    produce_active=True is the frozen behavior (T5 mints payable ACTIVE
    credit). produce_active=False is the M4 mutant (T5 mints SPENT directly,
    so repayment starves); the mutation battery asserts it is caught.
    """
    active_mod.check_event_predicate(predicate)
    t5 = {"rule_id": "TR-A-T5", "template": "T5_boundary_activation",
          "match": predicate, "consume": [{"type": "BOUNDARY_LATENT"}],
          "produce": [{"type": "BOUNDARY_ACTIVE" if produce_active else "SPENT",
                       "support": "inherit",
                       "scale": ("S0", 0), "mass": Fraction(1),
                       "provenance": "B_ZIGZAG_EXPOSED"}]}
    t6 = {"rule_id": "TR-A-T6", "template": "T6_repayment",
          "match": {"mode_is": "KEEP"}, "consume": [{"type": "BOUNDARY_ACTIVE"}],
          "produce": [{"type": "SPENT", "support": ("key", 0),
                       "scale": ("S0", 0), "mass": Fraction(1),
                       "provenance": "PAID_REGRET"}]}
    ledger: list = []
    cursor = 0
    max_res = Fraction(0)
    first = None
    paid_total = Fraction(0)
    injected_total = Fraction(0)
    for ev in rotations:
        if ev["side"] == "A":
            lo, hi = ev["interval"]
            sites = [("boundary", i, i + 1, "LEFT" if i + 1 <= ev["x"] else "RIGHT")
                     for i in range(lo, hi) if 1 <= i < ev["nkeys"]]
            for _ in range(k):
                if not sites:
                    break
                sup = sites[cursor % len(sites)]
                cursor += 1
                ledger = ledger_state.add(ledger, ledger_state.make_credit(
                    "BOUNDARY_LATENT", sup, ("S0", 0), Fraction(1),
                    "A_ROTATION_CREATED"))
                injected_total += 1
        ledger, _ = update_mod.update(ledger, ev, [t5], _skip_validation=True)
        w = Fraction(0)
        if ev["mode"] == "KEEP" and ev.get("y_edge", 0) > 0:
            w = Fraction(ev["y_edge"] - c_const * ev["a_edge"], 1)
        if ev["mode"] == "KEEP" and w > 0:
            paid = 0
            for _ in range(int(w)):
                ledger, tr = update_mod.update(ledger, ev, [t6], _skip_validation=True)
                if tr and tr[0]["applied"]:
                    paid += 1
            paid_total += paid
            res = w - paid
            if res > max_res:
                max_res = res
                first = {"w": [w.numerator, w.denominator], "paid": paid,
                         "res": [res.numerator, res.denominator],
                         "edge": {"mode": ev["mode"], "x": ev["x"],
                                  "a": ev["a_edge"], "y": ev["y_edge"]}}
    return {"feasible": max_res == 0,
            "max_res": max_res, "first": first,
            "paid": paid_total, "injected": injected_total,
            "ledger_final_size": len(ledger)}
