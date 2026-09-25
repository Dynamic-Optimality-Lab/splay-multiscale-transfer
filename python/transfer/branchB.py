"""Branch-B signed-multiscale search (spec PHASE 11): implemented, NOT activated.

Activation requires an exact Branch-A rejection record (grammar version, rule
types, witness, interpretation) AND the WP-3-frozen grammar. At WP-4 close Branch A
survives development, so this module's search entry point is never invoked in anger;
it is exercised on fixtures in tests. If Branch A dies on fresh evidence, a future
turn calls search_signed() with the preserved obstruction record (new calculus IDs).
Signed semantics here: borrowing (active pool may go negative covering regret) with
an energy floor F that must hold at all times (lower-bound discovery = floor search).
Scope: probe, not full multiscale redistribution (documented; see MST12 record).
Console tag [WP4-STEP-04].
"""
from __future__ import annotations

from fractions import Fraction

from python.transfer import branches as branches_mod


# WP4-STEP-04: signed-relaxation probe (borrowing with floor; exact simulation).
def search_signed(k: int, c_const: int, floor: int, corpus: dict,
                  rejection: dict) -> dict:
    """Joint search over signed rules + energy floor on the development corpus.

    Requires a valid Branch-A rejection record (else BLOCKED without searching).
    Returns feasibility + floor breaches + worst residual (exact Fractions).
    """
    if branches_mod.activate_branch_B(rejection) != "ACTIVATED":
        return {"status": "SIGNED_TRANSFER_NOT_ACTIVATED",
                "reason": "no exact Branch-A rejection record"}
    active = Fraction(0)
    floor_f = Fraction(floor)
    breaches = 0
    first = None
    for seq in corpus["sequences"]:
        latent = Fraction(0)
        for ev in seq["rotations"]:
            if ev["side"] == "A":
                latent += k
            w = Fraction(0)
            if ev["mode"] == "KEEP" and ev.get("y_edge", 0) > 0:
                w = Fraction(ev["y_edge"] - c_const * ev["a_edge"], 1)
            if w > 0:
                active += latent
                latent = Fraction(0)
                active -= w
                if active < floor_f:
                    breaches += 1
                    if first is None:
                        first = {"seq": seq["id"], "floor": floor,
                                 "active": [active.numerator, active.denominator]}
    feasible = breaches == 0
    print("[WP4-STEP-04] signed probe k=%d C=%d floor=%d: feasible=%s breaches=%d"
          % (k, c_const, floor, feasible, breaches), flush=True)
    return {"status": "SIGNED_TRANSFER_SURVIVES_DEV" if feasible else "SIGNED_TRANSFER_REJECTED",
            "floor": floor, "breaches": breaches, "first": first}
