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


def splay2(st: dict, x: int) -> list[dict]:
    nodes = st["nodes"]
    if x not in nodes:
        raise KeyError(x)
    evs: list[dict] = []
    idx = 0
    while nodes[x][2] is not None:
        p = nodes[x][2]
        g = nodes[p][2]
        if g is None:
            case = "ZIG"
            if nodes[p][0] is x:
                _rot_right(st, p)
            else:
                _rot_left(st, p)
            evs.append({"case": case, "index": idx,
                        "keys_local": sorted([p, x])})
        elif nodes[p][0] is x and nodes[g][0] is p:
            _rot_right(st, g)
            _rot_right(st, p)
            evs.append({"case": "LL", "index": idx,
                        "keys_local": sorted([g, p, x])})
        elif nodes[p][1] is x and nodes[g][1] is p:
            _rot_left(st, g)
            _rot_left(st, p)
            evs.append({"case": "RR", "index": idx,
                        "keys_local": sorted([g, p, x])})
        elif nodes[p][0] is x and nodes[g][1] is p:
            _rot_right(st, p)
            _rot_left(st, g)
            evs.append({"case": "RL", "index": idx,
                        "keys_local": sorted([g, p, x])})
        else:
            _rot_left(st, p)
            _rot_right(st, g)
            evs.append({"case": "LR", "index": idx,
                        "keys_local": sorted([g, p, x])})
        idx += 1
    return evs
