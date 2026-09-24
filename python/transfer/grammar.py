"""Transfer-grammar loader + rule validator (spec S11, prereg contract binding).

Loads prereg/transfer_grammar_v0.3.yaml (records its SHA-256 for freeze
certificates), exposes templates/branches/forbidden/objectives, and validates
rule records against the frozen language. Instantiation (fitted parameters) is
WP-4 synthesis; this module only enforces the language. Console tag [WP3-STEP-03].
"""
from __future__ import annotations

import hashlib
import os

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PREREG = os.path.join(ROOT, "prereg", "transfer_grammar_v0.3.yaml")


def load() -> tuple[dict, str]:
    """Load the frozen grammar + its SHA-256 (for certificates)."""
    raw = open(PREREG, "rb").read()
    digest = hashlib.sha256(raw).hexdigest().upper()
    with open(PREREG, encoding="utf-8") as f:
        grammar = yaml.safe_load(f)
    print("[WP3-STEP-03] grammar loaded sha=%s..." % digest[:16], flush=True)
    return grammar, digest


def validate_rule(rule: dict, grammar: dict) -> list[str]:
    """Validate one rule record against the frozen grammar (violations list)."""
    violations: list[str] = []
    templates = grammar.get("rule_templates", {})
    if rule.get("template") not in templates:
        violations.append("unknown template %r" % (rule.get("template"),))
    branch = rule.get("branch")
    allowed = ((grammar.get("branch_RAW_BOUNDARY", {}) if branch == "RAW_BOUNDARY"
                else grammar.get("branch_SIGNED_MULTISCALE", {}) if branch == "SIGNED_MULTISCALE"
                else {}).get("allowed_templates", []))
    short = (rule.get("template", "").split("_")[0] if rule.get("template") else "")
    if short not in allowed:
        violations.append("template %r not allowed in branch %r" % (rule.get("template"), branch))
    for field in ("rule_id", "match", "consume", "produce"):
        if field not in rule:
            violations.append("missing field %r" % field)
    try:
        from python.provenance import active as active_mod
        active_mod.check_event_predicate(rule.get("match", {}))
    except (ValueError, TypeError, AttributeError) as e:
        violations.append("match invalid: %s" % e)
    return violations


def check_ruleset(rules: list, grammar: dict) -> list[str]:
    """Well-formedness gate for a full rule list (MST0-10 domain precondition).

    Enforces r_i != r_j => id(r_i) != id(r_j) (unique IDs make rule_id sorting
    genuinely canonical), plus per-rule grammar validation. Malformed lists are
    rejected HERE, before update() invocation, keeping update total on its domain.
    """
    violations: list[str] = []
    ids = [r.get("rule_id") for r in rules]
    if len(set(ids)) != len(ids):
        violations.append("duplicate rule_id in rule list")
    for rule in rules:
        for v in validate_rule(rule, grammar):
            violations.append("%s: %s" % (rule.get("rule_id"), v))
    if not violations:
        print("[WP3-STEP-03] ruleset well-formed: %d rules, unique IDs" % len(rules), flush=True)
    return violations
