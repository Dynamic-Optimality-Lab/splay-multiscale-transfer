"""PA pairings (L6MAP-v0.3.1): zig-zig decomposition into winner/loser pairings.

Source (L6 v1, pp.10-12): a zig-zig takes three consecutive heap-children and hangs
two below lower-rank ones — decomposed into two pairings, each hanging one heap-child
below a lower-rank heap-child. Boundary pairings join heavy paths from different lazy
intervals; internal pairings stay inside one interval. Good internal pairings join
point gaps of the same magnitude (contracted gap decreases); bad ones do not.
Important boundary pairings are those NOT at very-large-interval boundaries subsumed
by internal pairings (operationalized below as: boundary pairing whose interval sizes
are both below the large-interval threshold L; L is preregistered, not fitted).
Verdict: SAME for the decomposition vocabulary; the magnitude predicate uses the
contracted function (MODIFIED operationalization recorded: source "same magnitude"
read as equal contracted values, justified by Fig.8 ceiling-log discussion).
Console tag [WP2A-STEP-02].
"""
from __future__ import annotations

LARGE_INTERVAL_THRESHOLD = 64


def decompose_zigzig(triple: list[int], rank_of: dict[int, int]) -> list[dict]:
    """Decompose three consecutive heap-children into two pairing records.

    Each pairing: {"hung": key, "below": key} with rank(hung) > rank(below)
    (ordering by rank; ties broken by key, recorded explicitly).
    """
    if len(triple) != 3:
        raise ValueError("zig-zig takes exactly three consecutive heap-children")
    ordered = sorted(triple, key=lambda k: (rank_of[k], k))
    return [{"hung": ordered[2], "below": ordered[1]},
            {"hung": ordered[1], "below": ordered[0]}]


def classify_pairing(pairing: dict, same_interval: bool, contracted_of: dict[int, int],
                     interval_sizes: tuple[int, int]) -> str:
    """GOOD/BAD internal or IMPORTANT/UNIMPORTANT boundary pairing class."""
    if same_interval:
        g_hung = contracted_of[pairing["hung"]]
        g_below = contracted_of[pairing["below"]]
        return "GOOD" if g_hung == g_below else "BAD"
    if max(interval_sizes) >= LARGE_INTERVAL_THRESHOLD:
        return "UNIMPORTANT"
    return "IMPORTANT"
