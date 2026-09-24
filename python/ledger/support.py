"""Ledger support descriptors (spec S10.2): allowed vs forbidden primitives.

Allowed kinds: key, interval, heavy_path, heap_relation, lazy_interval, boundary,
bend, orientation. Every support is a tuple (kind, *fields) of ints/strings only.
Theorem-facing support hygiene is enforced by field-name and value-shape checks
against FORBIDDEN_SUBSTRINGS below.
Console tag [WP3-STEP-02].
"""
from __future__ import annotations

ALLOWED_KINDS = {"key", "interval", "heavy_path", "heap_relation", "lazy_interval",
                 "boundary", "bend", "orientation"}
ORIENTATIONS = {"LEFT", "RIGHT", "MIXED"}
FORBIDDEN_SUBSTRINGS = ("state_id", "cycle", "holdout", "H1", "H2", "H3T",  # LEAKAGE-blocklist
                        "timestamp", "time_idx", "event_id", "future", "bellman",  # LEAKAGE-blocklist
                        "address", "U_b", "V_b", "/proc", "0x")  # LEAKAGE-blocklist


def check_support(support: tuple) -> None:
    """Validate a support descriptor (raises on any violation)."""
    if not (isinstance(support, tuple) and support):
        raise ValueError("support must be a non-empty tuple")
    kind = support[0]
    if kind not in ALLOWED_KINDS:
        raise ValueError("forbidden support kind %r" % (kind,))
    for field in support[1:]:
        if isinstance(field, str):
            low = field.lower()
            if any(b.lower() in low for b in FORBIDDEN_SUBSTRINGS):
                raise ValueError("forbidden support content %r" % (field,))
        elif isinstance(field, bool) or not isinstance(field, int):
            raise ValueError("support fields must be ints/strings, got %r" % (field,))
    if kind == "orientation" and (len(support) != 2 or support[1] not in ORIENTATIONS):
        raise ValueError("orientation support must be ('orientation', LEFT|RIGHT|MIXED)")
    if kind == "interval" and len(support) != 3:
        raise ValueError("interval support must be ('interval', lo, hi)")
    if kind == "boundary":
        if len(support) != 4 or support[3] not in ORIENTATIONS:
            raise ValueError("boundary support must be ('boundary', left, right, LEFT|RIGHT|MIXED)")
    if kind in ("key", "heavy_path", "heap_relation", "lazy_interval", "bend") and len(support) < 2:
        raise ValueError("support kind %r needs at least one field" % (kind,))
