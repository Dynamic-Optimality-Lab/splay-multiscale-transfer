"""SAT CEGIS core (spec S12 discovery engine): predicate selection with blocking.

Problem: choose (predicate one-hot over the frozen menu, integer k) with zero
residuals. The exact simulator is the oracle (proposes nothing; disposes). z3
maintains the live configuration space symbolically: each oracle rejection adds a
blocking clause; UNSAT means the finite space is exhausted (cross-checked by
independent brute force in certify.py). Deterministic (fixed seeds, single thread).
Console tag [WP4-STEP-02].
"""
from __future__ import annotations

import z3

PREDICATES = ["P_all", "P_keep", "P_zigzig", "P_zigzag", "P_zigonly", "P_never"]
KMAX = 6


def new_solver() -> tuple:
    """Fresh deterministic z3 solver + predicate variables."""
    s = z3.Solver()
    s.set("random_seed", 0)
    s.set("threads", 1)
    pvars = [z3.Bool("pred_%s" % p) for p in PREDICATES]
    s.add(z3.PbEq([(v, 1) for v in pvars], 1))
    return s, pvars


# WP4-STEP-02: solve the live SAT problem (model or UNSAT).
def solve(solver, pvars: list) -> dict | None:
    """Return {predicate} model or None on UNSAT."""
    if solver.check() != z3.sat:
        print("[WP4-STEP-02] SAT UNSAT: configuration space exhausted", flush=True)
        return None
    model = solver.model()
    for v, p in zip(pvars, PREDICATES):
        if z3.is_true(model.eval(v, model_completion=True)):
            return {"predicate": p}
    raise AssertionError("one-hot violated despite PbEq")


def block_predicate(solver, pvars: list, predicate: str) -> None:
    """Block one predicate entirely (structural rejection of that family member)."""
    idx = PREDICATES.index(predicate)
    solver.add(z3.Not(pvars[idx]))
    print("[WP4-STEP-02] SAT blocked predicate %s" % predicate, flush=True)
