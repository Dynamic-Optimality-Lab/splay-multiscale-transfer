"""WP-1 full-tuple agreement checker (single source for runner and tests).

Compares trace_keep events against independent-core splay2 events per side:
case sequence, local-key tuples, neighborhood hashes, orientation, and depth.
Any single-field divergence on any event is a mismatch (fail-closed). Console
tag [WP1-STEP-04] via callers.
"""
from __future__ import annotations


# WP-1 REPAIR STEP G1: agreement signature (the full contract tuple).
def signature(ev: dict) -> tuple:
    """Case + keys + neighborhoods + orientation + depth (both event shapes)."""
    return (ev.get("splay_case", ev.get("case")), tuple(ev["keys_local"]),
            ev["nh_before"], ev["nh_after"], ev["orientation"], ev["depth_before"])


# WP-1 REPAIR STEP G2: per-side full-tuple comparison.
def compare(trace_events: list, ev_a: list, ev_b: list, tag: str) -> list[str]:
    """Return mismatch descriptions (empty iff full agreement)."""
    fails: list[str] = []
    mine_a = [signature(ev) for ev in trace_events if ev["side"] == "A"]
    mine_b = [signature(ev) for ev in trace_events if ev["side"] == "B"]
    theirs_a = [signature(ev) for ev in ev_a]
    theirs_b = [signature(ev) for ev in ev_b]
    if len(mine_a) != len(theirs_a) or len(mine_b) != len(theirs_b):
        fails.append("%s event-count mismatch A:%d/%d B:%d/%d"
                     % (tag, len(mine_a), len(theirs_a), len(mine_b), len(theirs_b)))
        return fails
    for side, mine, theirs in (("A", mine_a, theirs_a), ("B", mine_b, theirs_b)):
        for k, (m, t) in enumerate(zip(mine, theirs)):
            if m != t:
                fails.append("%s side-%s event-%d field divergence" % (tag, side, k))
    return fails
