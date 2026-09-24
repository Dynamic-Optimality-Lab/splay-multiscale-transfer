"""Causal ledger state (spec S10.1): finite multiset of discrepancy credits.

A credit is an immutable record (type, support, scale, mass, provenance). Ledgers
are canonicalized tuples (sorted) so equality is structural and updates are pure.
Support content restrictions are enforced by support.py (see FORBIDDEN_SUBSTRINGS). Console tag [WP3-STEP-02].
"""
from __future__ import annotations

from fractions import Fraction


def make_credit(credit_type: str, support: tuple, scale: tuple,
                mass: Fraction, provenance: str) -> dict:
    """Construct one frozen credit record (validated by support.check_support)."""
    from python.ledger import support as support_mod
    support_mod.check_support(support)
    if not isinstance(mass, Fraction):
        raise TypeError("mass must be Fraction (exact arithmetic)")
    if not (isinstance(scale, tuple) and len(scale) == 2):
        raise ValueError("scale must be (system, level)")
    return {"type": credit_type, "support": support, "scale": scale,
            "mass": mass, "provenance": provenance}


def _key(credit: dict) -> tuple:
    return (credit["type"], credit["support"], credit["scale"],
            (credit["mass"].numerator, credit["mass"].denominator),
            credit["provenance"])


def canonical(ledger: list) -> tuple:
    """Canonical sorted tuple form (structural equality + determinism basis)."""
    return tuple(sorted((_key(c) for c in ledger)))


def empty() -> list:
    """The synchronized initial ledger (energy normalization: empty)."""
    return []


def add(ledger: list, credit: dict) -> list:
    """Return new ledger with one credit appended (functional update)."""
    return list(ledger) + [credit]


def remove(ledger: list, credit: dict) -> list:
    """Return new ledger with one matching credit removed (raises if absent)."""
    target = _key(credit)
    for i, c in enumerate(ledger):
        if _key(c) == target:
            return list(ledger[:i]) + list(ledger[i + 1:])
    raise KeyError("credit not present for removal")


def count(ledger: list) -> int:
    """Finite support size."""
    return len(ledger)
