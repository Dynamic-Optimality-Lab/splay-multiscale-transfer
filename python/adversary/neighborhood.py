"""Rotation-neighborhood driver (spec Phase-13 engine).

Single-key perturbations of a history (rotation neighborhoods). Deterministic
seeds. Console tag [WP4-STEP-06].
"""
from __future__ import annotations

import random


# WP4-STEP-06: rotation-neighborhood perturbations (deterministic, seeded).
def neighborhood(history: list, n: int, count: int, seed: int) -> list:
    """Single-access key perturbations of one history (neighbors list)."""
    rng = random.Random(seed)
    out = []
    for _ in range(count):
        nxt = [list(e) for e in history]
        j = rng.randrange(len(nxt))
        nxt[j][1] = rng.randint(1, n)
        out.append([tuple(e) for e in nxt])
    print("[WP4-STEP-06] neighborhood: %d neighbors" % len(out), flush=True)
    return out
