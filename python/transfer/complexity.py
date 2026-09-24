"""Rule complexity bounds enforcement (spec S11.3 + S11.5 forbidden escapes).

Checks per rule: O(1) output records per triggering event (at most MAX_OUTPUTS
unless an aggregate_proof_ref pointer is present — operationalization: a rotation
touches O(1) nodes, so packets bigger than 4 records need a proved aggregate;
rationale recorded here, not fitted); no forbidden target inputs anywhere in the
rule JSON (see FORBIDDEN_TOKENS);
no n-specific constants; match patterns use role vocabulary (no literal key integers).
Console tag [WP3-STEP-03].
"""
from __future__ import annotations

import json
import re

MAX_OUTPUTS = 4
# Long tokens match by substring (no legitimate rule vocabulary contains them);
# short tokens match whole-word only (avoid false hits inside identifiers).
LONG_TOKENS = ("regret", "critical", "bellman", "state_id", "cycle_id", "holdout",  # LEAKAGE-blocklist
               "future", "global_cancel", "n_specific", "timestamp", "time_idx",  # LEAKAGE-blocklist
               "event_id", "address")  # LEAKAGE-blocklist
SHORT_TOKENS = ("H1", "H2R", "H3T", "U_b", "V_b", "0x", "/proc")  # LEAKAGE-blocklist
FORBIDDEN_TOKENS = LONG_TOKENS + SHORT_TOKENS  # LEAKAGE-blocklist
# Frozen schema field names (spec S20.5 + ledger schema): vocabulary, never content.
SCHEMA_WORDS = {"rule_id", "template", "branch", "precondition", "trigger_event",
                "match", "consume", "produce", "energy_delta_bound",
                "regret_payment_bound", "scale_movement", "symmetry_behavior",
                "aggregate_proof_ref", "type", "support", "scale", "mass",
                "provenance", "op", "trigger", "inputs", "outputs", "paid_free"}
ROLE_VOCABULARY = {"mode", "case", "side", "scale", "support_kind", "orientation",
                   "mass", "interval", "boundary", "path", "key_role"}


def _walk_strings(obj, found: list) -> None:
    if isinstance(obj, str):
        found.append(obj)
    elif isinstance(obj, dict):
        for k, v in obj.items():
            found.append(str(k))
            _walk_strings(v, found)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            _walk_strings(v, found)


# WP3-STEP-03: complexity + escape audit for one rule record.
def audit_rule(rule: dict) -> list[str]:
    """Return violations (empty means complexity-clean under WP-3 bounds)."""
    violations: list[str] = []
    produced = rule.get("produce", [])
    if len(produced) > MAX_OUTPUTS and not rule.get("aggregate_proof_ref"):
        violations.append("outputs %d exceed O(1) bound %d without aggregate proof"
                          % (len(produced), MAX_OUTPUTS))
    strings: list[str] = []
    _walk_strings(rule, strings)
    blob = " ".join(s for s in strings if s not in SCHEMA_WORDS)
    for tok in LONG_TOKENS:
        if tok in blob.lower():
            violations.append("forbidden escape token %r" % (tok,))
            break
    else:
        for tok in SHORT_TOKENS:
            if re.search(r"(?<![A-Za-z0-9_])%s(?![A-Za-z0-9_])" % re.escape(tok), blob):
                violations.append("forbidden escape token %r" % (tok,))
                break
    match = rule.get("match", {})
    ints_in_match: list = []
    _collect_ints(match, ints_in_match)
    if ints_in_match:
        violations.append("literal integers in match patterns (use roles): %s" % ints_in_match[:3])
    return violations


def _collect_ints(obj, out: list) -> None:
    if isinstance(obj, bool):
        return
    if isinstance(obj, int):
        out.append(obj)
    elif isinstance(obj, dict):
        for v in obj.values():
            _collect_ints(v, out)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            _collect_ints(v, out)


def audit_json_bytes(raw: bytes) -> list[str]:
    """Escape scan over raw rule JSON bytes (encoding-independent tripwire)."""
    return audit_rule(json.loads(raw.decode("utf-8")))
