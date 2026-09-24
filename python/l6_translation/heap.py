"""PA_HEAP_VIEW (L6MAP-v0.3.1): contract each heavy component into its bottom-most node.

Source (L6 v1, p.10): contract every heavy path into the bottom-most node, keep all
children of path nodes as children of the contracted node; the contracted tree has
only light edges, ranks increase along every edge, hence heap-ordered; heap-children
whose values precede the heap-parent's value are left heap-children (right analog).
PA reading (explicit): the heap-parent VALUE is the bottom-most node's key.
Verdict: SAME (construction is representation-agnostic); the heap property itself
(rank increase along contracted edges) is VERIFIED on corpus, not assumed.
Console tag [WP2A-STEP-02].
"""
from __future__ import annotations

from python.splay_ref.splay import Node


def depths(root: Node | None) -> dict[int, int]:
    """Depth map of the subject tree."""
    out: dict[int, int] = {}

    def rec(n: Node | None, d: int) -> None:
        if n is None:
            return
        out[n.key] = d
        rec(n.left, d + 1)
        rec(n.right, d + 1)

    rec(root, 0)
    return out


def parent_map(root: Node | None) -> dict[int, int | None]:
    """Child key -> parent key (root maps to None)."""
    out: dict[int, int | None] = {}

    def rec(n: Node | None, p: int | None) -> None:
        if n is None:
            return
        out[n.key] = p
        rec(n.left, n.key)
        rec(n.right, n.key)

    rec(root, None)
    return out


def heap_view(subject_root: Node | None, comps: list[frozenset],
              comp_rank: dict[frozenset, int]) -> dict:
    """Contract components; return heap records keyed by bottom-most key.

    Record: {"members": sorted, "rank": comp_rank, "heap_parent": bottom-key|None,
    "heap_children": [bottom-keys], "left": [...], "right": [...] (by key order
    vs the heap-parent bottom-most key)}.
    """
    from python.l6_translation.heavy import bottom_most
    dep = depths(subject_root)
    par = parent_map(subject_root)
    owner: dict[int, frozenset] = {}
    for c in comps:
        for k in c:
            owner[k] = c
    bots = {c: bottom_most(c, dep) for c in comps}
    view: dict = {}
    for c in comps:
        b = bots[c]
        tops = [k for k in c if par[k] is None or owner[par[k]] is not c]
        top = min(tops, key=lambda k: dep[k])
        hp = None if par[top] is None else bots[owner[par[top]]]
        children: set[int] = set()
        for k in c:
            node = _find(subject_root, k)
            for ch in (node.left, node.right):
                if ch is not None and owner[ch.key] is not c:
                    children.add(bots[owner[ch.key]])
        kids = sorted(children)
        view[b] = {"members": sorted(c), "rank": comp_rank[c], "heap_parent": hp,
                   "heap_children": kids,
                   "left": [k for k in kids if k < b],
                   "right": [k for k in kids if k > b]}
    return view


def _find(root: Node | None, key: int) -> Node:
    cur = root
    while cur is not None:
        if key == cur.key:
            return cur
        cur = cur.left if key < cur.key else cur.right
    raise KeyError(key)
