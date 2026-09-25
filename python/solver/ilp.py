"""Exact small-domain integer programming (spec S12 discovery engine).

Role: minimal feasible k per (predicate, C) by monotone scan over 0..KMAX with a
complete scan log as the certificate. This is exact integer optimization on a tiny
domain (branch-and-bound degenerates to ordered enumeration with monotone pruning);
labeled honestly: no simplex, no floating point, every claim replayable from the log.
Console tag [WP4-STEP-02].
"""
from __future__ import annotations

from python.solver.encode_sat import KMAX


# WP4-STEP-02: minimal feasible k (oracle decides feasibility); log is the certificate.
def minimize_k(predicate: str, c_const: int, feasible_fn) -> tuple:
    """Scan k ascending; return (best_k or None, scan_log)."""
    log = []
    for k in range(KMAX + 1):
        ok, evidence = feasible_fn(predicate, k, c_const)
        log.append({"predicate": predicate, "k": k, "C": c_const,
                    "feasible": bool(ok), "evidence": evidence})
        if ok:
            print("[WP4-STEP-02] ILP minimal k: %s C=%d k=%d" % (predicate, c_const, k), flush=True)
            return k, log
    print("[WP4-STEP-02] ILP infeasible: %s C=%d (k=0..%d)" % (predicate, c_const, KMAX), flush=True)
    return None, log
