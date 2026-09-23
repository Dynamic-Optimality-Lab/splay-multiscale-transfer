"""Independent canonical pair-domain enumeration for WP-1 (no parent code imported).

Conventions (open, audited against v0.1 reference/enumerate.py + canonical.py):
  tree_id = index in ASCII-sorted BST shape strings, inorder keys 1..n;
  pair pid = a_id * C + b_id with C = Catalan(n)  (v0.1: a_id, b_id = divmod(pid, c)).
Reachability is computed by our own BFS from diagonal starts over KEEP/DELETE
edges; parent counts/ratios are comparison targets, never premises.
Console output lines prefixed [WP1-STEP-0x] are the auditable execution record.
"""
from __future__ import annotations

import sys
import time

from python.splay_ref.splay import Node, cost, splay


def canonical_shapes(n: int) -> list[str]:
    """ASCII-sorted BST shape strings; index is tree_id (v0.1-compatible order)."""
    if n == 0:
        return ["."]
    out = []
    for left_size in range(n):
        right_size = n - 1 - left_size
        for left in canonical_shapes(left_size):
            for right in canonical_shapes(right_size):
                out.append("(" + left + right + ")")
    return sorted(out)


def _parse_shape(ss: str, pos: list) -> tuple | None:
    if ss[pos[0]] == ".":
        pos[0] += 1
        return None
    assert ss[pos[0]] == "("
    pos[0] += 1
    left = _parse_shape(ss, pos)
    right = _parse_shape(ss, pos)
    assert ss[pos[0]] == ")"
    pos[0] += 1
    return (left, right)


def parse_shape(ss: str) -> tuple | None:
    """Shape string to skeleton (None = empty)."""
    node = _parse_shape(ss, [0])
    return node


def build_node_tree(shape_idx_shapes: list[str], idx: int, n: int) -> Node | None:
    """Fresh pointer-based BST for tree_id idx (inorder keys 1..n)."""
    keys = iter(range(1, n + 1))

    def rec(skel: tuple | None) -> Node | None:
        if skel is None:
            return None
        left = rec(skel[0])
        node = Node(next(keys))
        node.left = left
        if node.left is not None:
            node.left.parent = node
        node.right = rec(skel[1])
        if node.right is not None:
            node.right.parent = node
        return node

    return rec(parse_shape(shape_idx_shapes[idx]))


def node_shape_string(root: Node | None) -> str:
    """Structure-only serialization (keys fixed by inorder)."""
    if root is None:
        return "."
    return "(" + node_shape_string(root.left) + node_shape_string(root.right) + ")"


class PairDomain:
    """Canonical pair domain for fixed n with exact KEEP/DELETE edge evaluation."""

    def __init__(self, n: int):
        self.n = n
        self.shapes = canonical_shapes(n)
        self.C = len(self.shapes)
        self.shape_to_id = {s: i for i, s in enumerate(self.shapes)}

    def pid(self, a: int, b: int) -> int:
        """Canonical pair ID (v0.1-compatible: a*C+b)."""
        return a * self.C + b

    def unpid(self, pid: int) -> tuple[int, int]:
        """Inverse pair ID."""
        return divmod(pid, self.C)

    def diagonals(self) -> list[int]:
        """Diagonal starts (synchronized trees)."""
        return [self.pid(i, i) for i in range(self.C)]

    def edge(self, pid: int, x: int, mode: str) -> tuple[int, int, int]:
        """Exact edge evaluation: returns (target_pid, a, y) with y=0 for DELETE."""
        a_id, b_id = self.unpid(pid)
        A = build_node_tree(self.shapes, a_id, self.n)
        B = build_node_tree(self.shapes, b_id, self.n)
        a = cost(A, x)
        if mode == "DELETE":
            A2, _ev = splay(A, x)
            return self.pid(self.shape_to_id[node_shape_string(A2)], b_id), a, 0
        if mode == "KEEP":
            y = cost(B, x)
            A2, _ev = splay(A, x)
            B2, _ev2 = splay(B, x)
            return (self.pid(self.shape_to_id[node_shape_string(A2)],
                             self.shape_to_id[node_shape_string(B2)]), a, y)
        raise ValueError("mode must be KEEP or DELETE")

    def reachable(self, progress_every: int = 0) -> set[int]:
        """BFS reachable set from diagonal starts over all KEEP/DELETE edges."""
        seen = set(self.diagonals())
        stack = list(seen)
        done = 0
        t0 = time.time()
        while stack:
            pid = stack.pop()
            for x in range(1, self.n + 1):
                for mode in ("KEEP", "DELETE"):
                    tgt, _a, _y = self.edge(pid, x, mode)
                    if tgt not in seen:
                        seen.add(tgt)
                        stack.append(tgt)
            done += 1
            if progress_every and done % progress_every == 0:
                print("[WP1-STEP-02] n=%d bfs visited=%d reached=%d elapsed=%.1fs"
                      % (self.n, done, len(seen), time.time() - t0), flush=True)
        return seen


def main() -> int:
    print("[WP1-STEP-02] canonical enumeration check")
    for n in (2, 3, 4):
        dom = PairDomain(n)
        r = dom.reachable()
        print("[WP1-STEP-02] n=%d trees=%d reachable=%d" % (n, dom.C, len(r)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
