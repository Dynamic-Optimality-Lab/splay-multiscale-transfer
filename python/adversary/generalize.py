"""Counterexample generalization (spec Phase-12 triage): N1-N5 checklist.

generalize() evaluates the five activation criteria for an inflated family built
from a decisive counterexample: legal reachable executions, explicit parameterized
construction, actual-cost-ratio growth (real Splay costs, never residuals),
independent replay, and diagonal-rooted embedding plausibility. All five must hold
to activate the negative branch; otherwise NEGATIVE_FAMILY_NOT_ACTIVATED.
Console tag [WP4-STEP-07].
"""
from __future__ import annotations


# WP4-STEP-07: counterexample generalization + N1-N5 checklist.
def generalize(counterexample: dict, actual_ratios: dict) -> dict:
    """Evaluate N1-N5 for an inflated family (all must hold to activate)."""
    checks = {
        "N1_legal_reachable": bool(counterexample.get("histories")),
        "N2_explicit_construction": bool(counterexample.get("construction")),
        "N3_actual_ratio_grows": bool(actual_ratios.get("grows", False)),
        "N4_independent_replay": bool(actual_ratios.get("replayed", False)),
        "N5_diagonal_rooted": bool(counterexample.get("diagonal", False)),
    }
    active = all(checks.values())
    print("[WP4-STEP-07] triage N1-N5: %s -> %s"
          % (checks, "NEGATIVE_CYCLE_FAMILY_CANDIDATE" if active else "NEGATIVE_FAMILY_NOT_ACTIVATED"),
          flush=True)
    return {"checks": checks,
            "status": "NEGATIVE_CYCLE_FAMILY_CANDIDATE" if active else "NEGATIVE_FAMILY_NOT_ACTIVATED"}
