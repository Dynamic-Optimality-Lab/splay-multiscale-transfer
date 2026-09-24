"""Independent second L6-translation implementation (differently structured).

Dict-state trees {key: [left, right, parent], root} + rank dicts; no shared code
with the primary pointer-based modules. Agreement with the primary implementation
is asserted by mapping_check.py on corpus data (L6-10). Console tag [WP2A-STEP-03].
"""
from __future__ import annotations


def ranks_of(ref: dict) -> dict[int, int]:
    """Depth map from a dict-state reference tree."""
    nodes, root = ref["nodes"], ref["root"]
    out: dict[int, int] = {}
    stack = [(root, 0)] if root is not None else []
    while stack:
        k, d = stack.pop()
        out[k] = d
        l, r, _p = nodes[k]
        if l is not None:
            stack.append((l, d + 1))
        if r is not None:
            stack.append((r, d + 1))
    return out


def _submin(st: dict, k: int | None, rank: dict[int, int]) -> float:
    if k is None:
        return float("inf")
    nodes = st["nodes"]
    return min(rank[k], _submin(st, nodes[k][0], rank), _submin(st, nodes[k][1], rank))


def heavy_edges2(sub: dict, rank: dict[int, int]) -> set[tuple[int, int]]:
    """Same MODIFIED rule as primary: verbatim equality + both-light tie-break."""
    nodes = sub["nodes"]
    heavy: set[tuple[int, int]] = set()
    for k, (l, r, _p) in nodes.items():
        kids = []
        if l is not None:
            kids.append((l, _submin(sub, l, rank)))
        if r is not None:
            kids.append((r, _submin(sub, r, rank)))
        mu = min([rank[k]] + [m for _, m in kids])
        hit = [kk for kk, m in kids if m == mu]
        if len(hit) == 1:
            heavy.add((k, hit[0]))
    return heavy


def components2(sub: dict, heavy: set[tuple[int, int]]) -> list[frozenset]:
    """Heavy-edge-connected components."""
    nodes = sub["nodes"]
    parent = {k: k for k in nodes}
    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for a, b in heavy:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra
    groups: dict[int, set] = {}
    for k in nodes:
        groups.setdefault(find(k), set()).add(k)
    return [frozenset(g) for g in groups.values()]


def depths2(sub: dict) -> dict[int, int]:
    """Depth map of the subject dict-state tree."""
    return ranks_of(sub)


def heap_view2(sub: dict, comps: list[frozenset], comp_rank: dict[frozenset, int]) -> dict:
    """Contracted heap view mirroring the primary construction."""
    nodes = sub["nodes"]
    dep = depths2(sub)
    owner: dict[int, frozenset] = {}
    for c in comps:
        for k in c:
            owner[k] = c
    bots = {c: max(c, key=lambda k: (dep[k], k)) for c in comps}
    par = {k: nodes[k][2] for k in nodes}
    view: dict = {}
    for c in comps:
        b = bots[c]
        tops = [k for k in c if par[k] is None or owner[par[k]] is not c]
        top = min(tops, key=lambda k: dep[k])
        hp = None if par[top] is None else bots[owner[par[top]]]
        children: set[int] = set()
        for k in c:
            for ch in (nodes[k][0], nodes[k][1]):
                if ch is not None and owner[ch] is not c:
                    children.add(bots[owner[ch]])
        kids = sorted(children)
        view[b] = {"members": sorted(c), "rank": comp_rank[c], "heap_parent": hp,
                   "heap_children": kids,
                   "left": [k for k in kids if k < b],
                   "right": [k for k in kids if k > b]}
    return view


def gaps2(view: dict) -> tuple[dict[int, int], list]:
    """Raw gaps + heap-property violations."""
    gaps, bad = {}, []
    for b, rec in view.items():
        hp = rec["heap_parent"]
        if hp is None:
            gaps[b] = 0
        else:
            gaps[b] = rec["rank"] - view[hp]["rank"]
            if gaps[b] <= 0:
                bad.append((b, hp))
    return gaps, bad


def bends2(sub: dict, heavy: set[tuple[int, int]]) -> set[int]:
    """Bend nodes under the explicit turn rule."""
    nodes = sub["nodes"]
    kids: dict[int, list] = {}
    has_heavy_parent: dict[int, bool] = {}
    for a, b in heavy:
        kids.setdefault(a, []).append(b)
        has_heavy_parent[b] = True
    out = set()
    for k, (l, r, p) in nodes.items():
        if p is None or not has_heavy_parent.get(k, False):
            continue
        own = kids.get(k, [])
        if len(own) != 1:
            continue
        child_side = "LEFT" if l == own[0] else "RIGHT"
        node_side = "LEFT" if nodes[p][0] == k else "RIGHT"
        if child_side != node_side:
            out.add(k)
    return out
