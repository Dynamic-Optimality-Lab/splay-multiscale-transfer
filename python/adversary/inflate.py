"""Motif-inflation driver (spec Phase-12 triage): parameterized scale families.

inflate_cycle repeats a KEEP cycle's key-word k times (k = scale parameter);
inflate_burst stretches DELETE bursts by a factor. Actual Splay ratios tracked per
k (never transfer residuals). Deterministic. Console tag [WP4-STEP-07].
"""
from __future__ import annotations


# WP4-STEP-07: motif inflation (parameterized scale families for triage).
def inflate_cycle(cycle: dict, times: int) -> list:
    """Repeat a KEEP cycle's key-word `times` times (scale parameter)."""
    hist = []
    for _ in range(times):
        for e in cycle["edges"]:
            hist.append(("KEEP", e["key"]))
    return hist


def inflate_burst(history: list, factor: int) -> list:
    """Stretch every DELETE burst by `factor` (scale parameter)."""
    out = []
    for mode, x in history:
        out.append((mode, x))
        if mode == "DELETE":
            out += [(mode, x)] * (factor - 1)
    return out
