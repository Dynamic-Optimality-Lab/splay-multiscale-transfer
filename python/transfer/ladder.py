"""Diagnostic-C ladder sweep (spec constant ladder; gate semantics honored).

The structural family (templates T5/T6/T7 + predicate menu) is FIXED across the
sweep; per rung C the search covers (predicate, k) candidates evaluated exactly.
A residual at rung C rejects that candidate at that C only; the family dies only
on infeasibility across the whole ladder. Larger C eases the inequality (stability
check, not hardness). Console tag [WP4-STEP-03].
"""
from __future__ import annotations

LADDER = (2, 3, 4, 6, 8, 12, 16, 24, 32, 64)


# WP4-STEP-03: sweep one rung (candidates evaluated, nothing mutated).
def sweep_rung(c_const: int, predicates: list, k_domain, corpus: dict,
               evaluate_fn, replay_fn) -> dict:
    """Evaluate every (predicate, k) at rung C with independent replay agreement."""
    rows = []
    for predicate in predicates:
        for k in k_domain:
            verdict = evaluate_fn(predicate, k, c_const, corpus)
            replay = replay_fn(predicate, k, c_const, corpus)
            agree = (verdict["feasible"] == replay["feasible"] and
                     verdict["max_residual"] == replay["max_residual"])
            rows.append({"predicate": predicate, "k": k, "C": c_const,
                         "feasible": verdict["feasible"],
                         "max_residual": verdict["max_residual"],
                         "first_violation": verdict["first_violation"],
                         "independent_agreement": agree})
            if not agree:
                rows[-1]["disagreement"] = {"engine": verdict["max_residual"],
                                            "replay": replay["max_residual"]}
    feas = [r for r in rows if r["feasible"]]
    print("[WP4-STEP-03] C=%d: %d/%d feasible, agreement=%s"
          % (c_const, len(feas), len(rows),
             all(r["independent_agreement"] for r in rows)), flush=True)
    return {"C": c_const, "rows": rows, "feasible": feas}
