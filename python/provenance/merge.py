"""Deterministic provenance merge (PHASE 07): histories merge iff ledger states match.

Two provenance histories merge exactly when the frozen current ledger states are
identical under canonical equality. Merging unions provenance tags (bounded,
deduplicated, sorted). No timestamps, no counters, no lookahead data cross the merge.
Console tag [WP3-STEP-01].
"""
from __future__ import annotations

from python.ledger import state as ledger_state


def equivalent(ledger_a: list, ledger_b: list) -> bool:
    """Canonical ledger equality (the sole merge criterion)."""
    return ledger_state.canonical(ledger_a) == ledger_state.canonical(ledger_b)


def merge(tags_a: list, tags_b: list, ledger_a: list, ledger_b: list) -> list:
    """Union provenance tags iff ledgers match; else raise (no silent merge)."""
    if not equivalent(ledger_a, ledger_b):
        raise ValueError("histories diverge: ledger states differ, merge refused")
    return sorted(set(tags_a) | set(tags_b))
