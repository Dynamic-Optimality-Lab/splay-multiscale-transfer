"""Branch-A raw-boundary candidate construction + exact evaluation (spec PHASE 10).

Candidate = (predicate P from the frozen menu, injection bound k, diagnostic C),
realized as rule records {TR-A-T7 inject, TR-A-T5 activate, TR-A-T6 repay} evaluated
THROUGH the ledger/update engine (discrete, exact). Granularity (documented choice,
spec-permitted): transfers T7/T5 per rotation; repayment aggregate per KEEP edge
(T6 looped exactly w times, w attached to the edge's terminal B-rotation).
Injection sites cycle deterministically over the affected interval's boundaries.
w = y - C*a (integers; Fractions exact). Console tag [WP4-STEP-03].
"""
from __future__ import annotations

from fractions import Fraction

from python.ledger import state as ledger_state
from python.ledger import update as update_mod
from python.splay_ref.splay import Node, _rotate_left, _rotate_right, cost

PREDICATES = {
    "P_all": {"any_of": [{"mode_is": "KEEP"}, {"mode_is": "DELETE"}]},
    "P_keep": {"mode_is": "KEEP"},
    "P_zigzig": {"all_of": [{"mode_is": "KEEP"}, {"any_of": [{"case_is": "LL"}, {"case_is": "RR"}]}]},
    "P_zigzag": {"all_of": [{"mode_is": "KEEP"},
                             {"any_of": [{"case_is": "LR"}, {"case_is": "RL"}, {"case_is": "ZIG"}]}]},
    "P_zigonly": {"all_of": [{"mode_is": "KEEP"}, {"case_is": "ZIG"}]},
    "P_never": {"all_of": [{"mode_is": "KEEP"}, {"mode_is": "DELETE"}]},
}
K_DOMAIN = range(0, 7)


def _snapshot(root: Node | None) -> Node | None:
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


def _subtree_span(node: Node | None) -> tuple[int, int]:
    """Key interval [lo, hi] of a subtree (inorder extremes)."""
    keys = []

    def rec(n: Node | None) -> None:
        if n is None:
            return
        rec(n.left)
        keys.append(n.key)
        rec(n.right)

    rec(node)
    return (min(keys), max(keys)) if keys else (0, 0)


def stepwise_access(root: Node, x: int, nkeys: int) -> tuple[list, Node]:
    """Replay one splay rotation-by-rotation, capturing (case, keys, interval) steps.

    Affected interval = key range of the ROTATED NODES (local site), not the
    rotated triple's whole subtree span: subtree spans go vacuous ([1,n], no
    interior boundaries) at root rotations, which would silence injection by
    construction. The local-keys range is the site-faithful reading (documented
    choice; deterministic either way). Returns (steps, final_root).
    """
    cur = root
    while cur is not None and cur.key != x:
        cur = cur.left if x < cur.key else cur.right
    if cur is None:
        raise KeyError(x)
    node = cur
    steps = []
    while node.parent is not None:
        p = node.parent
        g = p.parent
        if g is None:
            case = "ZIG"
            top = p
        elif p.left is node and g.left is p:
            case = "LL"
            top = g
        elif p.right is node and g.right is p:
            case = "RR"
            top = g
        elif p.left is node and g.right is p:
            case = "RL"
            top = g
        else:
            case = "LR"
            top = g
        keys = sorted({node.key, p.key} | ({g.key} if g is not None else set()))
        site = [min(keys), max(keys)]
        steps.append({"splay_case": case, "keys": keys, "interval": site})
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
    return steps, top


def build_rules(predicate: str, k: int) -> list:
    """Candidate (predicate, k) as frozen-schema rule records (no fitted targets)."""
    if predicate not in PREDICATES:
        raise ValueError("predicate outside frozen menu %r" % (predicate,))
    if k not in K_DOMAIN:
        raise ValueError("k outside domain")
    t7 = {"rule_id": "TR-A-T7", "template": "T7_A_rotation_injection",
          "branch": "RAW_BOUNDARY", "precondition": "A-side rotation",
          "trigger_event": "rotation", "match": {"side_is": "A"},
          "consume": [], "produce": [], "energy_delta_bound": "k=%d/rotation" % k,
          "regret_payment_bound": "0", "scale_movement": "none",
          "symmetry_behavior": "relabel-invariant"}
    t5 = {"rule_id": "TR-A-T5", "template": "T5_boundary_activation",
          "branch": "RAW_BOUNDARY", "precondition": "predicate fires on KEEP event",
          "trigger_event": "rotation", "match": PREDICATES[predicate],
          "consume": [{"type": "BOUNDARY_LATENT"}],
          "produce": [{"type": "BOUNDARY_ACTIVE", "support": "inherit",
                       "scale": ("S0", 0), "mass": Fraction(1),
                       "provenance": "B_ZIGZAG_EXPOSED"}],
          "energy_delta_bound": "0", "regret_payment_bound": "0",
          "scale_movement": "none", "symmetry_behavior": "relabel-invariant"}
    t6 = {"rule_id": "TR-A-T6", "template": "T6_repayment", "branch": "RAW_BOUNDARY",
          "precondition": "KEEP edge with w>0", "trigger_event": "rotation",
          "match": {"mode_is": "KEEP"},
          "consume": [{"type": "BOUNDARY_ACTIVE"}],
          "produce": [{"type": "SPENT", "support": ("key", 0), "scale": ("S0", 0),
                       "mass": Fraction(1), "provenance": "PAID_REGRET"}],
          "energy_delta_bound": "-paid", "regret_payment_bound": "min(pool,w)",
          "scale_movement": "none", "symmetry_behavior": "relabel-invariant"}
    t7["_k"] = k
    return [t7, t5, t6]


# WP4-STEP-03: exact candidate evaluation through the rule engine.
def evaluate(predicate: str, k: int, c_const: int, sequences, fail_fast: bool = False) -> dict:
    """Simulate the candidate over rotation-level sequences; exact residuals.

    Injection sites cycle deterministically over the affected interval's INTERIOR
    boundaries (i,i+1), oriented by the accessed key (documented site semantics).
    T5/T6 run through update() with validation precompiled once per candidate
    (_skip_validation per event). fail_fast=True returns on the first positive
    residual (verdict + first witness exact; max_residual then a lower bound).
    """
    from python.provenance import active as active_mod
    rules = build_rules(predicate, k)
    by_id = {r["rule_id"]: r for r in rules}
    t5 = dict(by_id["TR-A-T5"])
    t6 = dict(by_id["TR-A-T6"])
    active_mod.check_event_predicate(t5["match"])
    active_mod.check_event_predicate(t6["match"])
    if isinstance(sequences, dict):
        sequences = sequences["sequences"]
    # Evaluation paths: T7 injection via the exact site-cycling policy loop below
    # (sites are event-computed); T5/T6 through update() with the frozen records.
    max_res = Fraction(0)
    first = None
    paid_total = Fraction(0)
    injected_total = Fraction(0)
    for seq in sequences:
        ledger = []
        site_cursor = 0
        for ev in seq["rotations"]:
            if ev["side"] == "A":
                lo, hi = ev["interval"]
                sites = [("boundary", i, i + 1, "LEFT" if i + 1 <= ev["x"] else "RIGHT")
                         for i in range(lo, hi) if 1 <= i < ev["nkeys"]]
                for _ in range(k):
                    if not sites:
                        break
                    sup = sites[site_cursor % len(sites)]
                    site_cursor += 1
                    ledger = ledger_state.add(ledger, ledger_state.make_credit(
                        "BOUNDARY_LATENT", sup, ("S0", 0), Fraction(1),
                        "A_ROTATION_CREATED"))
                    injected_total += 1
            # T5 once per event through the engine (inherit support).
            ledger, _tr5 = update_mod.update(ledger, ev, [t5], _skip_validation=True)
            w = Fraction(0)
            if ev["mode"] == "KEEP" and ev.get("y_edge", 0) > 0:
                w = Fraction(ev["y_edge"] - c_const * ev["a_edge"], 1)
            if ev["mode"] == "KEEP" and w > 0:
                paid = 0
                for _ in range(int(w)):
                    ledger, tr6 = update_mod.update(ledger, ev, [t6], _skip_validation=True)
                    if tr6 and tr6[0]["applied"]:
                        paid += 1
                paid_total += paid
                res = w - paid
                if res > max_res:
                    max_res = res
                    first = {"seq": seq["id"], "w": [w.numerator, w.denominator],
                             "paid": paid, "res": [res.numerator, res.denominator]}
                    if fail_fast:
                        return {"feasible": False,
                                "max_residual": [max_res.numerator, max_res.denominator],
                                "first_violation": first,
                                "paid": [paid_total.numerator, paid_total.denominator],
                                "injected": [injected_total.numerator, injected_total.denominator],
                                "partial": True}
    feasible = max_res == 0
    return {"feasible": feasible,
            "max_residual": [max_res.numerator, max_res.denominator],
            "first_violation": first,
            "paid": [paid_total.numerator, paid_total.denominator],
            "injected": [injected_total.numerator, injected_total.denominator]}
