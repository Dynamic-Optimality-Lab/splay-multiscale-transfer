"""Exact ordinary bottom-up Splay + BST core (v0.3 canonical implementation).

Contract (inherited, never redefined):
  keys [n] = {1..n}; root depth 0; cost c(T,x) = depth+1;
  ordinary bottom-up splay cases: ROOT/ZIG/LL/RR/LR/RL.
Cost convention is depth+1; rotation events are structural charging
units and never redefine cost (MST0-02 / ROT-12).
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Node:
    key: int
    left: "Node | None" = None
    right: "Node | None" = None
    parent: "Node | None" = None


def depth(root: "Node | None", x: int) -> int:
    d = 0
    cur = root
    while cur is not None:
        if x == cur.key:
            return d
        cur = cur.left if x < cur.key else cur.right
        d += 1
    raise KeyError(f"key {x} not in tree")


def cost(root: "Node | None", x: int) -> int:
    """Frozen cost: depth + 1."""
    return depth(root, x) + 1


def _rotate_right(p: Node) -> None:
    x = p.left
    assert x is not None
    p.left = x.right
    if x.right is not None:
        x.right.parent = p
    x.parent = p.parent
    if p.parent is not None:
        if p.parent.left is p:
            p.parent.left = x
        else:
            p.parent.right = x
    x.right = p
    p.parent = x


def _rotate_left(p: Node) -> None:
    x = p.right
    assert x is not None
    p.right = x.left
    if x.left is not None:
        x.left.parent = p
    x.parent = p.parent
    if p.parent is not None:
        if p.parent.left is p:
            p.parent.left = x
        else:
            p.parent.right = x
    x.left = p
    p.parent = x


def _root_of(n: Node) -> Node:
    while n.parent is not None:
        n = n.parent
    return n


def search_path(root: Node, x: int) -> list[int]:
    path: list[int] = []
    cur: Node | None = root
    while cur is not None:
        path.append(cur.key)
        if x == cur.key:
            return path
        cur = cur.left if x < cur.key else cur.right
    raise KeyError(f"key {x} not in tree")


def splay(root: Node, x: int) -> tuple[Node, list[dict]]:
    """Splay key x to root. Returns (new_root, rotation_events).

    Each event: {case, index, keys_local}. Cases: ROOT/ZIG/LL/RR/LR/RL.
    """
    # locate node
    cur: Node | None = root
    while cur is not None and cur.key != x:
        cur = cur.left if x < cur.key else cur.right
    if cur is None:
        raise KeyError(f"key {x} not in tree")
    node = cur
    events: list[dict] = []
    idx = 0
    while node.parent is not None:
        p = node.parent
        g = p.parent
        if g is None:
            case = "ZIG"
            if p.left is node:
                _rotate_right(p)
            else:
                _rotate_left(p)
            events.append({"case": case, "index": idx,
                           "keys_local": sorted([p.key, node.key])})
        elif p.left is node and g.left is p:
            case = "LL"
            _rotate_right(g)
            _rotate_right(p)
            events.append({"case": case, "index": idx,
                           "keys_local": sorted([g.key, p.key, node.key])})
        elif p.right is node and g.right is p:
            case = "RR"
            _rotate_left(g)
            _rotate_left(p)
            events.append({"case": case, "index": idx,
                           "keys_local": sorted([g.key, p.key, node.key])})
        elif p.left is node and g.right is p:
            case = "RL"
            _rotate_right(p)
            _rotate_left(g)
            events.append({"case": case, "index": idx,
                           "keys_local": sorted([g.key, p.key, node.key])})
        elif p.right is node and g.left is p:
            case = "LR"
            _rotate_left(p)
            _rotate_right(g)
            events.append({"case": case, "index": idx,
                           "keys_local": sorted([g.key, p.key, node.key])})
        else:  # pragma: no cover - unreachable under BST invariant
            raise AssertionError("splay parent/child inconsistency")
        idx += 1
    return node, events


def build_balanced(keys: list[int]) -> Node | None:
    """Deterministic balanced BST from sorted keys (median root)."""
    if not keys:
        return None
    mid = len(keys) // 2
    root = Node(keys[mid])
    root.left = build_balanced(keys[:mid])
    if root.left is not None:
        root.left.parent = root
    root.right = build_balanced(keys[mid + 1:])
    if root.right is not None:
        root.right.parent = root
    return root


def build_spine(keys: list[int], left: bool = True) -> Node | None:
    """Deterministic spine: left=True -> decreasing chain (root=max)."""
    root: Node | None = None
    seq = sorted(keys) if left else sorted(keys, reverse=True)
    for k in seq:
        n = Node(k)
        if root is None:
            root = n
        elif left:
            n.left = root
            root.parent = n
            root = n
        else:
            n.right = root
            root.parent = n
            root = n
    return root


def serialize(root: Node | None) -> str:
    if root is None:
        return "."
    return f"({root.key}{serialize(root.left)}{serialize(root.right)})"


def inorder(root: Node | None) -> list[int]:
    out: list[int] = []

    def rec(n: Node | None) -> None:
        if n is None:
            return
        rec(n.left)
        out.append(n.key)
        rec(n.right)

    rec(root)
    return out
