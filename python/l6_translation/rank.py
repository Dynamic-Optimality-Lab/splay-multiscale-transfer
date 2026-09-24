"""PA_REFERENCE_RANK (L6MAP-v0.3.1): rank as depth in the reference snapshot.

Source (L6 v1, pp.3-6): "we define its rank to be its depth in T_OPT [static]".
PA transplant: reference tree = post-A-splay snapshot A1 (KEEP) or the appropriate
A snapshot (DELETE analysis). Verdict: SAME (the source rank IS depth-in-reference;
no depth substitution occurred — depth was the definition). Console tag [WP2A-STEP-02].
"""
from __future__ import annotations

from python.splay_ref.splay import Node


def rank_in_reference(ref_root: Node | None, key: int) -> int:
    """Depth of key in the reference tree (root depth 0). Raises KeyError if absent."""
    depth = 0
    cur = ref_root
    while cur is not None:
        if key == cur.key:
            return depth
        cur = cur.left if key < cur.key else cur.right
        depth += 1
    raise KeyError(key)


def all_ranks(ref_root: Node | None) -> dict[int, int]:
    """Rank map for every key in the reference tree."""
    out: dict[int, int] = {}

    def rec(n: Node | None, d: int) -> None:
        if n is None:
            return
        out[n.key] = d
        rec(n.left, d + 1)
        rec(n.right, d + 1)

    rec(ref_root, 0)
    return out
