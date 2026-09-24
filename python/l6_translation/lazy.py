"""PA lazy intervals (L6MAP-v0.3.1): consecutive heap-children groups + shift records.

Source (L6 v1, p.10): consecutive heap-children of each heavy path (consecutive in
symmetric order, corresponding to OPT subtrees) are grouped into lazy intervals;
the interval gap records the whole-interval shift, point gaps the unshifted values;
every rotation is handled by creating O(1) new lazy intervals.
Verdict: SAME for construction/shift bookkeeping. Growing/shrinking/broken are
structural predicates over before/after member sets (defined below); their update
RULES under rotations are WP-3 dynamics, not claimed here.
Console tag [WP2A-STEP-02].
"""
from __future__ import annotations


def initial_intervals(view: dict) -> dict[int, dict]:
    """One interval per heavy-path component covering all its heap-children.

    Interval record: {"owner": bottom-key, "members": sorted keys, "shift": 0,
    "state": "STABLE"}. Contiguity (consecutive in symmetric order) is verified
    by check_contiguity; non-consecutive groups would split (never observed on
    BST heap views — asserted by test, not assumed).
    """
    out = {}
    for b, rec in view.items():
        out[b] = {"owner": b, "members": sorted(rec["heap_children"]), "shift": 0,
                  "state": "STABLE"}
    return out


def check_contiguity(members: list[int], universe: list[int]) -> bool:
    """True iff members form a consecutive run in symmetric (key) order."""
    if not members:
        return True
    idx = sorted(universe.index(k) for k in members)
    return idx == list(range(idx[0], idx[0] + len(idx)))


def transition_state(before: list[int], after: list[int]) -> str:
    """Structural interval-state predicate over member sets across one event."""
    sb, sa = set(before), set(after)
    if sa == sb:
        return "STABLE"
    if not sa:
        return "BROKEN"
    if sa.issubset(sb) and len(sa) < len(sb):
        return "SHRINKING"
    if sb.issubset(sa) and len(sa) > len(sb):
        return "GROWING"
    if min(sa) < min(sb) or max(sa) > max(sb):
        return "BROKEN"
    return "SHRINKING"


def point_gap(raw_gap: int, shift: int) -> int:
    """Point gap = raw gap minus interval shift (exact integer arithmetic)."""
    return raw_gap - shift
