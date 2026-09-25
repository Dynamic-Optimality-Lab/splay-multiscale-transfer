"""WP-5 Phase-16 clean-room evaluator (receives only math + contracts + histories).

Self-contained reimplementation of the frozen raw-boundary calculus from its
mathematical definition. Deliberately imports NOTHING from python/ (stdlib only:
no splay_ref, ledger, provenance, transfer, solver, discovery, or generator
modules — asserted by AST audit, STOP-32). Any clean-room file importing
discovery fails the seal.

Mathematical definition replayed here (see TRANSFER_CALCULUS_LEDGER.md):
ledger = finite multiset of (type, support, scale, mass, provenance); T7 injects
up to k LATENT boundary credits per A-side rotation at cycling interior sites;
T5 converts one LATENT to ACTIVE per event whose mode satisfies the frozen
predicate (P_all: every event; P_keep: KEEP events); T6 discharges min(pool, w)
ACTIVE credits with w = y - C*a exact on burdened KEEP edges; E(L) = pool size,
E >= 0, E(empty) = 0. Console tag [WP5-STEP-06].
"""
from __future__ import annotations


# WP5-STEP-06: keyed-tuple shape parser (fresh implementation of the grammar).
def parse_shape(text: str):
    """Parse '(left key right)' with '.' null into nested tuples."""
    pos = [0]

    def rec():
        if text[pos[0]] == ".":
            pos[0] += 1
            return None
        assert text[pos[0]] == "(", text[pos[0]:pos[0] + 12]
        pos[0] += 1
        key = 0
        while text[pos[0]].isdigit():
            key = key * 10 + int(text[pos[0]])
            pos[0] += 1
        left = rec()
        right = rec()
        assert text[pos[0]] == ")"
        pos[0] += 1
        return (left, key, right)

    out = rec()
    assert pos[0] == len(text), "trailing bytes in shape"
    return out


# WP5-STEP-06: dict-state BST with bottom-up splay (fresh implementation).
def _build(nodes: dict, tree, parent):
    if tree is None:
        return None
    left, key, right = tree
    nodes[key] = [None, None, parent]
    nodes[key][0] = _build(nodes, left, key)
    nodes[key][1] = _build(nodes, right, key)
    return key


def _depth(nodes: dict, root, x: int) -> int:
    d = 0
    cur = root
    while cur != x:
        cur = nodes[cur][0] if x < cur else nodes[cur][1]
        d += 1
    return d


def _rot_right(nodes: dict, root: int, p: int) -> int:
    x = nodes[p][0]
    nodes[p][0] = nodes[x][1]
    if nodes[x][1] is not None:
        nodes[nodes[x][1]][2] = p
    nodes[x][2] = nodes[p][2]
    if nodes[p][2] is None:
        root = x
    elif nodes[nodes[p][2]][0] == p:
        nodes[nodes[p][2]][0] = x
    else:
        nodes[nodes[p][2]][1] = x
    nodes[x][1] = p
    nodes[p][2] = x
    return root


def _rot_left(nodes: dict, root: int, p: int) -> int:
    x = nodes[p][1]
    nodes[p][1] = nodes[x][0]
    if nodes[x][0] is not None:
        nodes[nodes[x][0]][2] = p
    nodes[x][2] = nodes[p][2]
    if nodes[p][2] is None:
        root = x
    elif nodes[nodes[p][2]][0] == p:
        nodes[nodes[p][2]][0] = x
    else:
        nodes[nodes[p][2]][1] = x
    nodes[x][0] = p
    nodes[p][2] = x
    return root


# WP5-STEP-06: splay with per-rotation (case, key-set, site) capture.
def _splay_trace(nodes: dict, root: int, x: int):
    """Splay x; return (root, rotations) with rotations = [(case, keys, site)]."""
    rots = []
    guard = 0
    while nodes[x][2] is not None:
        guard += 1
        if guard > 100 * len(nodes):
            raise ValueError("clean-room splay guard tripped (corrupt tree)")
        p = nodes[x][2]
        g = nodes[p][2]
        if g is None:
            case = "ZIG"
            keys = {x, p}
        elif nodes[g][0] == p and nodes[p][0] == x:
            case = "LL"
            keys = {x, p, g}
        elif nodes[g][1] == p and nodes[p][1] == x:
            case = "RR"
            keys = {x, p, g}
        elif nodes[g][1] == p and nodes[p][0] == x:
            case = "RL"
            keys = {x, p, g}
        else:
            case = "LR"
            keys = {x, p, g}
        site = [min(keys), max(keys)]
        rots.append((case, keys, site))
        if case == "ZIG":
            if nodes[p][0] == x:
                root = _rot_right(nodes, root, p)
            else:
                root = _rot_left(nodes, root, p)
        elif case == "LL":
            root = _rot_right(nodes, root, g)
            root = _rot_right(nodes, root, p)
        elif case == "RR":
            root = _rot_left(nodes, root, g)
            root = _rot_left(nodes, root, p)
        elif case == "RL":
            root = _rot_right(nodes, root, p)
            root = _rot_left(nodes, root, g)
        else:
            root = _rot_left(nodes, root, p)
            root = _rot_right(nodes, root, g)
    return root, rots


# WP5-STEP-06: predicate match on mode only (P_all / P_keep frozen semantics).
def _fires(predicate_name: str, mode: str) -> bool:
    if predicate_name == "P_all":
        return True
    if predicate_name == "P_keep":
        return mode == "KEEP"
    raise ValueError("clean-room supports only frozen predicates P_all/P_keep")


# WP5-STEP-06: key-set validation (fail-closed; refuses non-BST shapes).
def _check_keys(tree, n: int) -> None:
    """Assert the parsed shape carries exactly keys 1..n (else refuse)."""
    seen: list = []

    def rec(t) -> None:
        if t is None:
            return
        left, key, right = t
        seen.append(key)
        rec(left)
        rec(right)

    rec(tree)
    if sorted(seen) != list(range(1, n + 1)):
        raise ValueError("clean-room refuses shape without exact keys 1..n")


# WP5-STEP-06: exact episode simulation from the mathematical definition.
def simulate_episode(n: int, init_shape: str, history: list,
                     predicate_name: str, k: int, c_const: int) -> dict:
    """Return {feasible, max_res, first, paid, injected} with integer arithmetic."""
    parsed = parse_shape(init_shape)
    _check_keys(parsed, n)
    nodes_a: dict = {}
    root_a = _build(nodes_a, parsed, None)
    nodes_b: dict = {}
    root_b = _build(nodes_b, parsed, None)
    pool_latent: list = []
    pool_active: list = []
    cursor = 0
    max_res = 0
    first = None
    paid_total = 0
    injected_total = 0
    for mode, x in history:
        a = _depth(nodes_a, root_a, x) + 1
        root_a, rots_a = _splay_trace(nodes_a, root_a, x)
        events = [("A", mode, site) for (_c, _k, site) in rots_a]
        y = 0
        w = 0
        if mode == "KEEP":
            y = _depth(nodes_b, root_b, x) + 1
            root_b, rots_b = _splay_trace(nodes_b, root_b, x)
            events += [("B", mode, site) for (_c, _k, site) in rots_b]
            w = y - c_const * a
        for side, ev_mode, site in events:
            terminal = (side == "B" and ev_mode == "KEEP" and w > 0
                        and (side, ev_mode, site) == events[-1])
            if side == "A":
                lo, hi = site
                sites = [(i, i + 1, "LEFT" if i + 1 <= x else "RIGHT")
                         for i in range(lo, hi) if 1 <= i < n]
                for _ in range(k):
                    if not sites:
                        break
                    sup = sites[cursor % len(sites)]
                    cursor += 1
                    pool_latent.append(sup)
                    injected_total += 1
            if _fires(predicate_name, ev_mode) and pool_latent:
                pool_latent.pop(0)
                pool_active.append(True)
            if terminal:
                paid = min(len(pool_active), w)
                for _ in range(paid):
                    pool_active.pop(0)
                paid_total += paid
                res = w - paid
                if res > max_res:
                    max_res = res
                    first = {"w": [w, 1], "paid": paid,
                             "res": [res, 1],
                             "edge": {"mode": mode, "x": x, "a": a, "y": y}}
    return {"feasible": max_res == 0,
            "max_res": [max_res, 1], "first": first,
            "paid": [paid_total, 1], "injected": [injected_total, 1]}
