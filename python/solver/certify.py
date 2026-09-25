"""Solver certificate independence (spec S12.5): replay + agreement enforcement.

A solver verdict is authoritative only if: feasible assignments are replayed by an
INDEPENDENT exact checker, and infeasibility is confirmed by a second formulation.
Here the independent checker is a direct pool-accounting simulator (straight-line
credit-pool semantics, ~40 lines, no rule engine), and the second formulation is
exhaustive enumeration over the same finite space. Both must agree with the
CEGIS/z3 verdict. Console tag [WP4-STEP-02].
"""
from __future__ import annotations

from fractions import Fraction


# WP4-STEP-02: independent direct-pool replay of one (predicate, k, C) verdict.
def replay_candidate(predicate: str, k: int, c_const: int, corpus: dict) -> dict:
    """Straight-line pool semantics mirroring the rule-engine evaluator exactly.

    Per rotation event: A-side adds k to LATENT; predicate firing moves ONE
    LATENT to ACTIVE; w>0 KEEP events pay min(ACTIVE, w). Masses are integers
    (w = y - C*a integral); pools are fungible counts. Returns verdict + worst
    residual. Independent implementation: no rule engine, no shared code.
    """
    injected = 0
    paid = 0
    max_res = 0
    first = None
    seqs = corpus["sequences"] if isinstance(corpus, dict) else corpus
    for seq in seqs:
        # Pools reset per sequence: each paired execution starts synchronized
        # empty (E_0 = 0). Leaking pools across sequences over-pays (false
        # feasible); the engine resets, so the checker must too.
        latent = 0
        active = 0
        for ev in seq["rotations"]:
            if ev["side"] == "A":
                latent += k
                injected += k
            if _fires(predicate, ev):
                if latent > 0:
                    latent -= 1
                    active += 1
            w = 0
            if ev["mode"] == "KEEP" and ev.get("y_edge", 0) > 0:
                w = ev["y_edge"] - c_const * ev["a_edge"]
            if ev["mode"] == "KEEP" and w > 0:
                pay = min(active, w)
                active -= pay
                paid += pay
                res = w - pay
                if res > max_res:
                    max_res = res
                    first = {"seq": seq["id"], "key": ev.get("x"),
                             "w": w, "res": res}
    return {"feasible": max_res == 0, "max_residual": [max_res, 1],
            "first_violation": first, "paid": [paid, 1],
            "injected": [injected, 1]}


def _fires(predicate: str, ev: dict) -> bool:
    """Predicate menu (finite, preregistered; mirrors the rule-engine reading)."""
    mode, case = ev.get("mode"), ev.get("splay_case")
    if predicate == "P_all":
        return True
    if predicate == "P_keep":
        return mode == "KEEP"
    if predicate == "P_zigzig":
        return mode == "KEEP" and case in ("LL", "RR")
    if predicate == "P_zigzag":
        return mode == "KEEP" and case in ("LR", "RL", "ZIG")
    if predicate == "P_zigonly":
        return mode == "KEEP" and case == "ZIG"
    if predicate == "P_never":
        return False
    raise ValueError("unknown predicate %r" % (predicate,))


# WP4-STEP-02: agreement between CEGIS verdict and exhaustive verdict.
def check_agreement(cegis_feasible: bool, brute_feasible: bool, label: str) -> list[str]:
    """Fail-closed agreement gate (any disagreement blocks the verdict)."""
    if cegis_feasible != brute_feasible:
        return ["CERT-01 disagreement on %s: cegis=%s brute=%s"
                % (label, cegis_feasible, brute_feasible)]
    print("[WP4-STEP-02] cert agreement on %s: %s" % (label, cegis_feasible), flush=True)
    return []
