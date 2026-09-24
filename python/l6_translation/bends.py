"""PA bends (L6MAP-v0.3.1): heavy-path turn nodes.

Source (L6 v1, p.13): a bend is an internal node where the heavy path "turns" —
a left child whose heavy path continues right, or vice versa. Every zig-zag removes
one bend; splays create O(1) bends plus one per zig-zig (under ribless OPT).
Verdict on the OBJECT: SAME (turn definition transplants literally). The ribless
assumption does NOT transplant (PA reference trees are splay-generated, not ribless);
bend-creation/destruction COUNTS are therefore PA-new claims tested in WP-2B
(MST0-07), never cited from the source. Ambiguity rule (explicit): a node with a
heavy parent edge and exactly one heavy child edge on the opposite side is a bend;
any other heavy-incidence pattern (including tie-branching) is not.
Console tag [WP2A-STEP-02].
"""
from __future__ import annotations

from python.splay_ref.splay import Node


def bends(subject_root: Node | None, heavy: set[tuple[int, int]]) -> set[int]:
    """Keys of bend nodes under the explicit turn rule."""
    if subject_root is None:
        return set()
    parent: dict[int, tuple[int | None, str | None]] = {}

    def rec(n: Node | None, p: int | None, side: str | None) -> None:
        if n is None:
            return
        parent[n.key] = (p, side)
        rec(n.left, n.key, "LEFT")
        rec(n.right, n.key, "RIGHT")

    rec(subject_root, None, None)
    heavy_children: dict[int, list] = {}
    heavy_parent_edge: dict[int, bool] = {}
    for a, b in heavy:
        heavy_children.setdefault(a, []).append(b)
        heavy_parent_edge[b] = True
    out = set()
    for k, (p, side) in parent.items():
        if p is None or not heavy_parent_edge.get(k, False):
            continue
        kids = heavy_children.get(k, [])
        if len(kids) != 1:
            continue
        # Side of the unique heavy child edge.
        node = _find(subject_root, k)
        child_side = "LEFT" if node.left is not None and node.left.key == kids[0] else "RIGHT"
        if child_side != side:
            out.add(k)
    return out


def _find(root: Node | None, key: int) -> Node:
    cur = root
    while cur is not None:
        if key == cur.key:
            return cur
        cur = cur.left if key < cur.key else cur.right
    raise KeyError(key)
