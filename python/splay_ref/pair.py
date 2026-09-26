"""Frozen Pair-Access contract (inherited from v0.1/v0.2, never redefined).

KEEP:   K_x(A,B) = (S_x A, S_x B),  a = c(A,x), y = c(B,x)
DELETE: D_x(A,B) = (S_x A, B),      a = c(A,x), y = 0
w_b(e) = y - b*a ;  l_b(e) = b*a - y   (exact Fractions at use sites)
"""
from __future__ import annotations

from fractions import Fraction

from .splay import Node, cost, splay


def keep(A: Node, B: Node, x: int) -> tuple[Node, Node, dict]:
    a = cost(A, x)
    y = cost(B, x)
    A2, ev_a = splay(A, x)
    B2, ev_b = splay(B, x)
    return A2, B2, {"mode": "KEEP", "x": x, "a": a, "y": y,
                    "events_A": ev_a, "events_B": ev_b}


def delete(A: Node, B: Node, x: int) -> tuple[Node, Node, dict]:
    a = cost(A, x)
    A2, ev_a = splay(A, x)
    return A2, B, {"mode": "DELETE", "x": x, "a": a, "y": 0,
                   "events_A": ev_a, "events_B": []}


def w_b(a: int, y: int, b: int) -> Fraction:
    return Fraction(y - b * a, 1)


def l_b(a: int, y: int, b: int) -> Fraction:
    return Fraction(b * a - y, 1)


def pair_id(A: Node | None, B: Node | None) -> str:
    """Canonical pair-state ID: SHA-256 over "serialize(A)|serialize(B)".

    Frozen convention (WorkPlan WP-1): hashed, deterministic, 64-hex.
    """
    import hashlib as _hl
    from .splay import serialize
    return _hl.sha256((serialize(A) + "|" + serialize(B)).encode("utf-8")).hexdigest()
