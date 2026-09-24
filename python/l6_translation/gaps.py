"""PA gaps (L6MAP-v0.3.1): raw / interval / point gaps over the heap view.

Source (L6 v1, pp.8-10): gap(P) = rank(P) − rank of the heavy path connected by a
light edge to P's top-most node; root path gap 0. Interval gap = whole-interval
shift; point gaps = gaps without the shift (behave as gaps for in-interval zig-zigs).
Verdict: SAME (rank differences transplant literally; shift bookkeeping identical).
The heap-record rank fields are consumed, never recomputed here.
Console tag [WP2A-STEP-02].
"""
from __future__ import annotations


def raw_gaps(view: dict) -> dict[int, int]:
    """gap(bottom-key) for every heap node; root component gap 0.

    Requires the heap property (child rank > parent rank); records the raw
    difference, which the caller validates as non-negative.
    """
    gaps = {}
    for b, rec in view.items():
        hp = rec["heap_parent"]
        gaps[b] = 0 if hp is None else rec["rank"] - view[hp]["rank"]
    return gaps


def check_heap_property(view: dict) -> list:
    """Return [(child, parent)] violations where child rank <= parent rank."""
    bad = []
    for b, rec in view.items():
        hp = rec["heap_parent"]
        if hp is not None and not rec["rank"] > view[hp]["rank"]:
            bad.append((b, hp))
    return bad
