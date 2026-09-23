"""Deterministic maximal-block partitioner for paired executions (MST0-16 preamble).

Every real paired execution is covered exactly once: maximal runs of DELETE
(A-only restructuring blocks) alternate with maximal runs of one-or-more KEEP
(synchronous blocks). Partition is a pure function of the (mode, key) history.
Console tag [WP1-STEP-04] on verification paths.
"""
from __future__ import annotations


def partition(history: list[dict]) -> list[dict]:
    """Partition a [(mode, key)] history into maximal DELETE/KEEP blocks.

    Each history item: {"mode": "KEEP"|"DELETE", "x": key}. Returns blocks
    [{"kind": "DELETE_BLOCK"|"KEEP_BLOCK", "span": (lo, hi), "keys": [...]}]
    with spans contiguous, non-overlapping, covering [0, len(history)).
    """
    blocks: list[dict] = []
    i = 0
    n = len(history)
    while i < n:
        kind = "DELETE_BLOCK" if history[i]["mode"] == "DELETE" else "KEEP_BLOCK"
        j = i
        while j < n and ((history[j]["mode"] == "DELETE") == (kind == "DELETE_BLOCK")):
            j += 1
        blocks.append({"kind": kind, "span": [i, j],
                       "keys": [h["x"] for h in history[i:j]]})
        i = j
    return blocks


def check_coverage(history: list[dict], blocks: list[dict]) -> bool:
    """Exact-once coverage: spans tile [0, len(history)) with no gaps/overlaps."""
    pos = 0
    for b in blocks:
        if b["span"][0] != pos:
            return False
        pos = b["span"][1]
    return pos == len(history)
