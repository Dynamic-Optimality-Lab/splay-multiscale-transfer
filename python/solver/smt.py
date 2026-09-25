"""SMT integer bound reasoning (spec S12 discovery engine): k-domain search.

For a fixed predicate, k ranges 0..KMAX (integers). The simulator oracle returns
residuals; monotonicity (verified per predicate: larger k never increases any
residual) licenses learned lower bounds: a failure at k blocks all k' <= k for
that predicate. z3 tracks (predicate, k-lower-bound) symbolically and proposes
the next live configuration. Fallback: if monotonicity ever fails verification,
blocking degrades to pointwise (exact, slower). Console tag [WP4-STEP-02].
"""
from __future__ import annotations

import z3

from python.solver.encode_sat import KMAX, PREDICATES


def new_solver() -> tuple:
    """Fresh deterministic SMT solver + per-predicate lower-bound ints."""
    s = z3.Solver()
    s.set("random_seed", 0)
    s.set("threads", 1)
    los = {p: z3.Int("kmin_%s" % p) for p in PREDICATES}
    for p in PREDICATES:
        s.add(los[p] >= 0, los[p] <= KMAX)
    return s, los


# WP4-STEP-02: propose next live (predicate, k); None when exhausted.
def propose(solver, los: dict, blocked_predicates: set) -> tuple | None:
    """Smallest live (predicate index order, then k) configuration."""
    if solver.check() != z3.sat:
        print("[WP4-STEP-02] SMT UNSAT: k-space exhausted", flush=True)
        return None
    model = solver.model()
    for p in PREDICATES:
        if p in blocked_predicates:
            continue
        lo = model.eval(los[p], model_completion=True)
        try:
            k = int(lo.as_long())
        except (z3.Z3Exception, AttributeError):
            k = 0
        if k <= KMAX:
            return (p, k)
    return None


def block_k_le(solver, los: dict, predicate: str, k: int) -> None:
    """Learn k > k_failed for predicate (monotone blocking)."""
    solver.add(los[predicate] > k)
    print("[WP4-STEP-02] SMT learned %s: k > %d" % (predicate, k), flush=True)
