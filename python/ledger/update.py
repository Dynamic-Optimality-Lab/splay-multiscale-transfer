"""Deterministic ledger update (spec S10.3-S10.5, MST0-10 machinery).

update_R: L x E -> L x T for every frozen legal rule list R (rules are a frozen
parameter, not a provenance-dependent input). External provenance tag lists are
derived bookkeeping, never consumed by update: equal canonical ledgers evolve
identically regardless of merged tags (credit provenance FIELDS are part of
canonical state; see state._key). Console tag [WP3-STEP-02].
"""
from __future__ import annotations

from fractions import Fraction

from python.ledger import state as ledger_state
from python.provenance import active as active_mod


def _pattern_match(pattern: dict, credit: dict) -> bool:
    """Structural pattern match on a credit (type/support/scale/provenance)."""
    for key in ("type", "provenance"):
        if key in pattern and credit.get(key) != pattern[key]:
            return False
    if "support" in pattern and list(credit.get("support", ())) != list(pattern["support"]):
        return False
    if "scale" in pattern and list(credit.get("scale", ())) != list(pattern["scale"]):
        return False
    return True


# WP3-STEP-02: deterministic update (the MST0-10 function).
def update(ledger: list, event: dict, rules: list) -> tuple[list, list]:
    """Apply rules in rule_id order; return (new_ledger, applied_trace).

    Domain: finite legal ledgers × legal rotation events × finite WELL-FORMED
    frozen rule lists (unique rule_ids, event-only matches). Malformed rules
    are rejected by the frozen validators BEFORE invocation (grammar.validate_rule,
    complexity.audit_rule, grammar.check_ruleset) and are not in this domain;
    duplicate rule_ids raise here as a final fail-closed guard.
    External provenance tag lists are not parameters: later evolution depends
    on the ledger (whose credit provenance FIELDS are canonical state) alone.
    """
    ids = [r["rule_id"] for r in rules]
    if len(set(ids)) != len(ids):
        raise ValueError("duplicate rule_id: rule order would not be canonical")
    cur = list(ledger)
    trace = []
    for rule in sorted(rules, key=lambda r: r["rule_id"]):
        active_mod.check_event_predicate(rule["match"])
        if not active_mod.evaluate(rule["match"], {"type": "", "support": (),
                                                   "scale": ("", 0),
                                                   "mass": Fraction(0),
                                                   "provenance": ""}, event):
            trace.append({"rule": rule["rule_id"], "applied": False, "reason": "no-match"})
            continue
        consumed = []
        ok = True
        for pattern in rule.get("consume", []):
            hit = next((c for c in cur if _pattern_match(pattern, c)
                        and c not in consumed), None)
            if hit is None:
                ok = False
                break
            consumed.append(hit)
        if not ok:
            trace.append({"rule": rule["rule_id"], "applied": False, "reason": "inputs-absent"})
            continue
        for c in consumed:
            cur = ledger_state.remove(cur, c)
        for template in rule.get("produce", []):
            cur = ledger_state.add(cur, dict(template))
        trace.append({"rule": rule["rule_id"], "applied": True,
                      "consumed": len(consumed),
                      "produced": len(rule.get("produce", []))})
    return cur, trace
