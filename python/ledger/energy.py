"""Integrated ledger energy (spec S10.6): E(L) = sum of per-type energies.

Energy functions map credit-type -> Fraction and are caller-supplied (WP-4/5 freeze
them per calculus); this module provides the sum, the unit default, and exact
lower-bound checking. No floats. Console tag [WP3-STEP-02].
"""
from __future__ import annotations

from fractions import Fraction


def total(ledger: list, energy_fn: dict[str, Fraction]) -> Fraction:
    """Exact integrated energy under a per-type energy map."""
    s = Fraction(0)
    for c in ledger:
        if c["type"] not in energy_fn:
            raise KeyError("no energy for credit type %r" % (c["type"],))
        s += Fraction(energy_fn[c["type"]]) * c["mass"]
    return s


def unit_energy(types: list[str]) -> dict[str, Fraction]:
    """Unit energy map (baseline reference; calculi freeze their own)."""
    return {t: Fraction(1) for t in types}


def check_lower_bound(ledger: list, energy_fn: dict[str, Fraction],
                      bound: Fraction) -> bool:
    """Exact lower-bound check E(L) >= bound (signed-branch obligation helper)."""
    return total(ledger, energy_fn) >= bound
