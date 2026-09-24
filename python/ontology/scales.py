"""Exact scale coordinates S0..S5 (integer buckets only; WP-2B stratification use).

S0 subtree-size dyadic: floor(log2(size)); S1 depth dyadic: floor(log2(depth+1));
S2 raw-gap integer: the gap value itself; S3 contracted baseline: contracted(g);
S4 span dyadic: floor(log2(span)); S5 rank bucket: rank value itself (eligible only
where the rank translation is exact — enforced by callers via mapping status).
No floating point anywhere. Console tag [WP2B-STEP-01].
"""
from __future__ import annotations

import math


def s0_subtree(size: int) -> int:
    """Floor log2 of subtree size (size >= 1)."""
    if size < 1:
        raise ValueError("subtree size must be >= 1")
    return size.bit_length() - 1


def s1_depth(depth: int) -> int:
    """Floor log2 of depth+1 (depth >= 0)."""
    if depth < 0:
        raise ValueError("depth must be >= 0")
    return (depth + 1).bit_length() - 1


def s2_gap(gap: int) -> int:
    """Raw-gap integer coordinate (may be negative transiently; recorded as-is)."""
    return int(gap)


def s4_span(lo: int, hi: int) -> int:
    """Floor log2 of key-interval span (hi-lo+1 >= 1)."""
    span = hi - lo + 1
    if span < 1:
        raise ValueError("span must be >= 1")
    return span.bit_length() - 1
