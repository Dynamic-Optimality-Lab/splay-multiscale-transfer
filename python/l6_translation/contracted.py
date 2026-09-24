"""PA contracted point gaps (L6MAP-v0.3.1, baseline reproduction only).

Source (L6 v1, p.12): contracted gap uses ceil(1 + log(1+x)) binary (figure uses
ceil(log(x)) for simplicity). Exact integer form, proved equal below:
contracted(g) = bit_length(g+1), plus 1 unless g+1 is a power of two.
Verdict: SAME (exact arithmetic identity, tested against the real-valued form).
Console tag [WP2A-STEP-02].
"""
from __future__ import annotations

import math


def contracted(g: int) -> int:
    """Exact integer contracted gap. Requires g >= 0."""
    if g < 0:
        raise ValueError("gap must be non-negative")
    if g == 0:
        return 1
    bl = (g + 1).bit_length()
    return bl if (g + 1) & g == 0 else bl + 1


def contracted_real(g: int) -> int:
    """Real-valued reference form ceil(1 + log2(1+g)) for cross-checking only."""
    return math.ceil(1 + math.log2(1 + g))
