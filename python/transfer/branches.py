"""Branch permissions + activation discipline (spec S11.4, preregistered).

Branch A (RAW_BOUNDARY): T1-T8, T10; unsigned only. Branch B (SIGNED_MULTISCALE):
all templates incl. T9; requires a global lower-bound theorem route.
Branch B activates ONLY on exact Branch-A rejection with the WP-3-frozen grammar;
activate_branch_B returns BLOCKED otherwise (WP-3 state: no Branch-A result exists,
so activation is unconditionally BLOCKED here). Console tag [WP3-STEP-03].
"""
from __future__ import annotations

A_TEMPLATES = {"T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T10"}
B_TEMPLATES = {"T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10"}


def branch_allows(branch: str, template_short: str, signed: bool) -> bool:
    """Permission check for (branch, template, signed) triples."""
    if branch == "RAW_BOUNDARY":
        return template_short in A_TEMPLATES and not signed
    if branch == "SIGNED_MULTISCALE":
        return template_short in B_TEMPLATES
    raise ValueError("unknown branch %r" % (branch,))


def activate_branch_B(branch_a_rejection_record: dict | None) -> str:
    """Activation gate: BLOCKED unless an exact Branch-A rejection record exists.

    WP-3 verdict: no Branch-A result exists yet, so activation is BLOCKED by
    construction. WP-4/WP-5 callers pass the preserved obstruction record.
    """
    if not isinstance(branch_a_rejection_record, dict):
        print("[WP3-STEP-03] Branch B activation: BLOCKED (no rejection record)", flush=True)
        return "BLOCKED"
    required = ("grammar_version", "rule_types", "witness", "interpretation")
    if not all(k in branch_a_rejection_record for k in required):
        print("[WP3-STEP-03] Branch B activation: BLOCKED (incomplete record)", flush=True)
        return "BLOCKED"
    print("[WP3-STEP-03] Branch B activation: requirements met (record present)", flush=True)
    return "ACTIVATED"
