"""Independent second Splay implementation (differently structured).

Shares no helpers with splay.py: dict-based explicit tree
{key: [left, right, parent], root} to satisfy ROT-10 / T62 independence.
"""
from __future__ import annotations


def build_balanced_dict(keys: list[int]) -> dict:
    keys = sorted(keys)
    nodes: dict[int, list] = {}

    def rec(ks: list[int], parent: int | None) -> int | None:
        if not ks:
            return None
        m = len(ks) // 2
        k = ks[m]
        nodes[k] = [None, None, parent]
        nodes[k][0] = rec(ks[:m], k)
        nodes[k][1] = rec(ks[m + 1:], k)
        return k

    root = rec(keys, None)
    return {"nodes": nodes, "root": root}


def _depth(st: dict, x: int) -> int:
    d, cur = 0, st["root"]
    nodes = st["nodes"]
    while cur is not None:
        if x == cur:
            return d
        cur = nodes[cur][0] if x < cur else nodes[cur][1]
        d += 1
    raise KeyError(x)


def cost2(st: dict, x: int) -> int:
    return _depth(st, x) + 1


def _rot_right(st: dict, p: int) -> None:
    nodes = st["nodes"]
    x = nodes[p][0]
    assert x is not None
    nodes[p][0] = nodes[x][1]
    if nodes[x][1] is not None:
        nodes[nodes[x][1]][2] = p
    par = nodes[p][2]
    nodes[x][2] = par
    if par is not None:
        if nodes[par][0] is p:
            nodes[par][0] = x
        else:
            nodes[par][1] = x
    else:
        st["root"] = x
    nodes[x][1] = p
    nodes[p][2] = x


def _rot_left(st: dict, p: int) -> None:
    nodes = st["nodes"]
    x = nodes[p][1]
    assert x is not None
    nodes[p][1] = nodes[x][0]
    if nodes[x][0] is not None:
        nodes[nodes[x][0]][2] = p
    par = nodes[p][2]
    nodes[x][2] = par
    if par is not None:
        if nodes[par][0] is p:
            nodes[par][0] = x
        else:
            nodes[par][1] = x
    else:
        st["root"] = x
    nodes[x][0] = p
    nodes[p][2] = x


def from_nodes(root) -> dict:
    """Build an equivalent dict-state from a pointer-based Node tree.

    Used only for cross-implementation agreement checks: same keys, same
    BST structure. Keyed by node key; [left, right, parent] per node.
    """
    nodes: dict[int, list] = {}

    def rec(n, parent: int | None) -> int | None:
        if n is None:
            return None
        nodes[n.key] = [None, None, parent]
        nodes[n.key][0] = rec(n.left, n.key)
        nodes[n.key][1] = rec(n.right, n.key)
        return n.key

    return {"nodes": nodes, "root": rec(root, None)}


def serialize2(st: dict) -> str:
    """Keyed serialization with the exact splay.serialize grammar (cross-check)."""
    nodes = st["nodes"]

    def rec(k: int | None) -> str:
        if k is None:
            return "."
        return "(" + str(k) + rec(nodes[k][0]) + rec(nodes[k][1]) + ")"

    return rec(st["root"])


def _subserialize(nodes: dict, k: int | None) -> str:
    """Keyed subtree serialization from an arbitrary node (serialize2 grammar)."""
    if k is None:
        return "."
    return "(" + str(k) + _subserialize(nodes, nodes[k][0]) + _subserialize(nodes, nodes[k][1]) + ")"


def _nh(nodes: dict, k: int | None) -> str:
    """Neighborhood hash with the identical grammar as splay._neighborhood_hash."""
    import hashlib as _hl
    return _hl.sha256(_subserialize(nodes, k).encode("utf-8")).hexdigest()


def _depth2(nodes: dict, x: int) -> int:
    """Depth of x by parent walk (search-path position)."""
    d = 0
    while nodes[x][2] is not None:
        x = nodes[x][2]
        d += 1
    return d


def path2(st: dict, x: int) -> list[int]:
    """Root-to-x search path in dict-state (ROT-02 cross-core comparison)."""
    nodes = st["nodes"]
    if x not in nodes:
        raise KeyError(x)
    chain = [x]
    while nodes[chain[-1]][2] is not None:
        chain.append(nodes[chain[-1]][2])
    return list(reversed(chain))


def splay2(st: dict, x: int) -> list[dict]:
    nodes = st["nodes"]
    if x not in nodes:
        raise KeyError(x)
    evs: list[dict] = []
    idx = 0
    while nodes[x][2] is not None:
        p = nodes[x][2]
        g = nodes[p][2]
        depth_before = _depth2(nodes, x)
        if g is None:
            case = "ZIG"
            orientation = "L" if nodes[p][0] is x else "R"
            nh_before = _nh(nodes, p)
            if nodes[p][0] is x:
                _rot_right(st, p)
            else:
                _rot_left(st, p)
            evs.append({"case": case, "index": idx,
                        "keys_local": sorted([p, x]),
                        "nh_before": nh_before, "nh_after": _nh(nodes, x),
                        "orientation": orientation, "depth_before": depth_before})
        elif nodes[p][0] is x and nodes[g][0] is p:
            nh_before = _nh(nodes, g)
            _rot_right(st, g)
            _rot_right(st, p)
            evs.append({"case": "LL", "index": idx,
                        "keys_local": sorted([g, p, x]),
                        "nh_before": nh_before, "nh_after": _nh(nodes, x),
                        "orientation": "L,L", "depth_before": depth_before})
        elif nodes[p][1] is x and nodes[g][1] is p:
            nh_before = _nh(nodes, g)
            _rot_left(st, g)
            _rot_left(st, p)
            evs.append({"case": "RR", "index": idx,
                        "keys_local": sorted([g, p, x]),
                        "nh_before": nh_before, "nh_after": _nh(nodes, x),
                        "orientation": "R,R", "depth_before": depth_before})
        elif nodes[p][0] is x and nodes[g][1] is p:
            nh_before = _nh(nodes, g)
            _rot_right(st, p)
            _rot_left(st, g)
            evs.append({"case": "RL", "index": idx,
                        "keys_local": sorted([g, p, x]),
                        "nh_before": nh_before, "nh_after": _nh(nodes, x),
                        "orientation": "L,R", "depth_before": depth_before})
        else:
            nh_before = _nh(nodes, g)
            _rot_left(st, p)
            _rot_right(st, g)
            evs.append({"case": "LR", "index": idx,
                        "keys_local": sorted([g, p, x]),
                        "nh_before": nh_before, "nh_after": _nh(nodes, x),
                        "orientation": "R,L", "depth_before": depth_before})
        idx += 1
    return evs
