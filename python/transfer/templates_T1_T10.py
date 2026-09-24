"""T1..T10 rule-template constructors (spec S11.2, frozen field language).

Each constructor builds a schema-valid rule RECORD with caller-supplied patterns;
no fitted parameters, no targets, no synthesis here (WP-4 instantiates). Every
record carries the frozen §20.5 field set. Console tag [WP3-STEP-03].
"""
from __future__ import annotations

TEMPLATES = ("T1_scale_preserving_move", "T2_upward_scale_transfer",
             "T3_downward_scale_split", "T4_orientation_flip",
             "T5_boundary_activation", "T6_repayment", "T7_A_rotation_injection",
             "T8_lazy_interval_structural_transfer", "T9_signed_cancellation",
             "T10_bend_discharge")

REQUIRED_FIELDS = ("rule_id", "template", "branch", "precondition",
                   "trigger_event", "match", "consume", "produce",
                   "energy_delta_bound", "regret_payment_bound",
                   "scale_movement", "symmetry_behavior")


def make_rule(rule_id: str, template: str, branch: str, match: dict,
              consume: list | None = None, produce: list | None = None,
              energy_delta_bound: str = "0", regret_payment_bound: str = "0",
              scale_movement: str = "none", symmetry_behavior: str = "relabel-invariant",
              trigger_event: str = "rotation", precondition: str = "declared") -> dict:
    """Construct one rule record (validated downstream by grammar.validate_rule)."""
    if template not in TEMPLATES:
        raise ValueError("unknown template %r" % (template,))
    if branch not in ("RAW_BOUNDARY", "SIGNED_MULTISCALE"):
        raise ValueError("unknown branch %r" % (branch,))
    return {"rule_id": rule_id, "template": template, "branch": branch,
            "precondition": precondition, "trigger_event": trigger_event,
            "match": match, "consume": consume or [], "produce": produce or [],
            "energy_delta_bound": energy_delta_bound,
            "regret_payment_bound": regret_payment_bound,
            "scale_movement": scale_movement, "symmetry_behavior": symmetry_behavior}


def check_record_shape(rule: dict) -> list[str]:
    """Required-field presence (deeper checks live in grammar.validate_rule)."""
    return ["missing %r" % f for f in REQUIRED_FIELDS if f not in rule]
