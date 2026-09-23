"""KEEP reference-snapshot convention KEEP_REF_SNAPSHOT-v1 (spec S5.2).

Analysis convention (not a change to paired execution):
  1. observe pre-KEEP pair (A0,B0);
  2. execute the A splay of x -> A1;
  3. freeze A1 as the reference snapshot for this KEEP's B-splay analysis;
  4. execute B's splay rotation by rotation against the frozen snapshot;
  5. record final pair (A1,B1).
Any alternative convention mints a new version ID with an equivalence proof or
explicit separation (MST0-04). Console tag [WP1-STEP-04] on verification paths.
"""
from __future__ import annotations

import hashlib

from python.splay_ref.splay import Node, serialize

CONVENTION = "KEEP_REF_SNAPSHOT-v1"


def snapshot_hash(A1: Node | None) -> str:
    """Reference-snapshot identity: SHA-256 of the frozen post-A-splay tree."""
    return hashlib.sha256(serialize(A1).encode("utf-8")).hexdigest()


def describe() -> dict:
    """Machine-readable convention record for ledgers and certificates."""
    return {"convention": CONVENTION,
            "order": ["observe_(A0,B0)", "splay_A_to_A1", "freeze_A1_reference",
                      "splay_B_against_frozen_reference", "record_(A1,B1)"],
            "semantics_note": "analysis_viewpoint_only_no_paired_execution_change"}
