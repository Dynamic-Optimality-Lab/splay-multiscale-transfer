"""PA_HEAVY_EDGE / PA_HEAVY_PATH / PA_LIGHT_EDGE (L6MAP-v0.3.1).

Source rule, verbatim (L6 v1, p.6): edge (u,v), u parent of v, is heavy iff
min-rank(subtree(u)) == min-rank(subtree(v)); otherwise light.
Verdict: SAME. The predicate transplants literally to ordinary BSTs, and the
uniqueness property is PROVED for ordinary BSTs (interval-LCA argument, recorded in
theorem_MST03): every BST-subtree interval has a unique reference-depth minimizer,
hence both children can never jointly attain the parent minimum — ties are
impossible, not merely unlikely (verified: 0 ties over all 19,413 reference/subject
pairs n<=6). The explicit tie-break in the code (both-light) is unreachable
totality insurance, retained so the function is total by construction. Heavy edges
therefore form disjoint chains. Console tag [WP2A-STEP-02].
"""
from __future__ import annotations

from python.splay_ref.splay import Node


def subtree_min_rank(node: Node | None, rank: dict[int, int]) -> float:
    """Minimum reference-rank over a subject subtree (infinity if empty)."""
    if node is None:
        return float("inf")
    best = rank[node.key]
    left = subtree_min_rank(node.left, rank)
    right = subtree_min_rank(node.right, rank)
    return min(best, left, right)


def heavy_edges(subject_root: Node | None, rank: dict[int, int]) -> set[tuple[int, int]]:
    """Set of (parent_key, child_key) heavy edges under the verbatim rule + tie-break.

    Edge (u,v) heavy iff min_rank(subtree(u)) == min_rank(subtree(v)); on a tie
    (both children attain m(u)) both edges are light.
    """
    heavy: set[tuple[int, int]] = set()

    def rec(u: Node | None) -> float:
        if u is None:
            return float("inf")
        mu = rank[u.key]
        ml = rec(u.left) if u.left is not None else float("inf")
        mr = rec(u.right) if u.right is not None else float("inf")
        mu = min(mu, ml, mr)
        kids = []
        if u.left is not None:
            kids.append((u.left.key, ml))
        if u.right is not None:
            kids.append((u.right.key, mr))
        heavy_kids = [k for k, m in kids if m == mu]
        if len(heavy_kids) == 1:
            heavy.add((u.key, heavy_kids[0]))
        # Tie (0 or 2 attaining children): all light — explicit, deterministic.
        return mu

    rec(subject_root)
    return heavy


def components(subject_root: Node | None, heavy: set[tuple[int, int]]) -> list[frozenset]:
    """Heavy-edge-connected components (forest; paths iff no tie-branching)."""
    parent: dict[int, int] = {}

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    nodes: list[int] = []

    def collect(n: Node | None) -> None:
        if n is None:
            return
        parent[n.key] = n.key
        nodes.append(n.key)
        collect(n.left)
        collect(n.right)

    collect(subject_root)
    for a, b in heavy:
        union(a, b)
    groups: dict[int, set] = {}
    for k in nodes:
        groups.setdefault(find(k), set()).add(k)
    return [frozenset(g) for g in groups.values()]


def bottom_most(comp: frozenset, depth_in_subject: dict[int, int]) -> int:
    """Deepest key of the component in the subject tree (heap-view contraction node)."""
    return max(comp, key=lambda k: (depth_in_subject[k], k))
