"""Cycle-splicing driver (spec Phase-13 engine): critical cycles + DELETE bridges.

Concatenates critical-cycle key-words joined by DELETE-bridge accesses, yielding
longer paired histories that revisit bottlenecks. Deterministic. Console tag
[WP4-STEP-06].
"""
from __future__ import annotations


# WP4-STEP-06: cycle splicing (critical cycles joined by DELETE bridges).
def splice(cycles: list, bridges: list, n: int) -> list:
    """Concatenate cycle key-words with DELETE-bridge accesses (all KEEP cycles)."""
    hist = []
    pads = bridges + [bridges[-1]] * max(0, len(cycles) - len(bridges))
    for cyc, bridge in zip(cycles, pads):
        for e in cyc["edges"]:
            hist.append(("KEEP", e["key"]))
        hist.append(("DELETE", bridge))
    print("[WP4-STEP-06] splice: %d accesses from %d cycles" % (len(hist), len(cycles)), flush=True)
    return hist
