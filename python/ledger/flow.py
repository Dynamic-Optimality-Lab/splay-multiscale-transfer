"""Direct-flow proof support (spec S10.6 alternative route): conservation auditing.

A rule conserves a declared quantity when total produced mass equals total consumed
mass per audited type group. audit_flow returns violations; an empty list means the
rule is flow-clean under the declaration. Direct-flow theorems (WP-6 alternative to
scalar energy) build on audited rules only. Console tag [WP3-STEP-02].
"""
from __future__ import annotations

from fractions import Fraction


def _mass(template: dict) -> Fraction:
    return Fraction(template.get("mass", 1))


# WP3-STEP-02: conservation audit for one rule record.
def audit_flow(rule: dict, groups: list[list[str]] | None = None) -> list[str]:
    """Check produced == consumed mass per type group (default: all types one group)."""
    violations: list[str] = []
    consumed: dict[str, Fraction] = {}
    produced: dict[str, Fraction] = {}
    for pattern in rule.get("consume", []):
        t = pattern.get("type")
        if t is None:
            violations.append("consume pattern without type")
            continue
        consumed[t] = consumed.get(t, Fraction(0)) + _mass(pattern)
    for template in rule.get("produce", []):
        t = template.get("type")
        if t is None:
            violations.append("produce template without type")
            continue
        produced[t] = produced.get(t, Fraction(0)) + _mass(template)
    if groups is None:
        groups = [sorted(set(consumed) | set(produced))]
    for group in groups:
        cin = sum((consumed.get(t, Fraction(0)) for t in group), Fraction(0))
        pout = sum((produced.get(t, Fraction(0)) for t in group), Fraction(0))
        if cin != pout:
            violations.append("group %s imbalance in=%s out=%s" % (group, cin, pout))
    return violations
