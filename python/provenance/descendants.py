"""Bounded structural descendants (PHASE 07): source -> representable packets.

Each source yields at most five bounded descriptors: interval boundary, heavy-path
relation tag, lazy-interval membership tag, heap-parent relation tag, and a
scale/orientation packet (S0 of affected span + orientation). Counts are fixed by
construction (bounded representation); no event IDs cross into descriptors.
Console tag [WP3-STEP-01].
"""
from __future__ import annotations


def descendants(source: dict, orientation: str = "MIXED") -> list[dict]:
    """Deterministic bounded descendant packet for one source descriptor."""
    if orientation not in ("LEFT", "RIGHT", "MIXED"):
        raise ValueError("orientation must be LEFT|RIGHT|MIXED")
    ref = source.get("structural_ref", {})
    interval = ref.get("interval", [])
    keys = ref.get("keys_local", [])
    span = (max(keys) - min(keys) + 1) if keys else 1
    import math
    level = span.bit_length() - 1 if span >= 1 else 0
    lo = min(interval) if len(interval) >= 2 else (min(keys) if keys else 0)
    hi = max(interval) if len(interval) >= 2 else (max(keys) if keys else 0)
    return [
        {"kind": "INTERVAL_BOUNDARY", "support": ("boundary", lo, hi, orientation)},
        {"kind": "HEAVY_PATH_RELATION", "support": ("heavy_path", lo, hi)},
        {"kind": "LAZY_MEMBERSHIP", "support": ("lazy_interval", lo, hi)},
        {"kind": "HEAP_RELATION", "support": ("heap_relation", lo, hi)},
        {"kind": "SCALE_PACKET", "support": ("interval", lo, hi),
         "scale": ("S0", level), "orientation": orientation},
    ]
