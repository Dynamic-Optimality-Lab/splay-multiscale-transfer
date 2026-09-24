"""Causal provenance sources (spec S7/PHASE 07): A-side rotations emit candidates.

Every A-side rotation event emits bounded source-candidate descriptors; B-side
events emit transfer/exposure triggers (never new debt). Descriptors carry the
provenance CLASS + structural reference only — no event IDs, timestamps, or
lookahead keys (asserted). Console tag [WP3-STEP-01].
"""
from __future__ import annotations


def source_candidates(event: dict) -> list[dict]:
    """Source descriptors for one rotation event (A-side rotations only)."""
    _require_no_future(event)
    if event.get("side") != "A":
        return []
    interval = event.get("affected_interval")
    refs = {"interval": list(interval) if interval else [],
            "keys_local": list(event.get("keys_local", [])),
            "case": event.get("splay_case")}
    return [{"provenance_class": "A_ROTATION_CREATED", "structural_ref": refs},
            {"provenance_class": "A_ROTATION_MOVED", "structural_ref": refs}]


def b_transfer_triggers(event: dict) -> list[dict]:
    """Transfer/exposure triggers for B-side events (no new debt)."""
    _require_no_future(event)
    if event.get("side") != "B":
        return []
    case = event.get("splay_case")
    if case in ("LL", "RR"):
        cls = "B_ZIGZIG_TRANSFERRED"
    elif case in ("LR", "RL"):
        cls = "B_ZIGZAG_EXPOSED"
    elif case == "ZIG":
        cls = "B_ZIGZAG_EXPOSED"
    else:
        return []
    return [{"provenance_class": cls,
             "structural_ref": {"keys_local": list(event.get("keys_local", [])),
                                "case": case}}]


def _require_no_future(event: dict) -> None:
    """Counterfactual-free guard: reject lookahead-bearing event records."""
    blob = str(event)
    for banned in ("future", "upcoming", "would_have", "Bellman", "holdout", "H1", "H2R", "H3T"):
        if banned in blob:
            raise ValueError("provenance event carries forbidden content %r" % banned)
