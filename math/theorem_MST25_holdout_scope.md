# Theorem MST0-25 — holdout scope (WP-5 setup record)

**Status:** UNPROVED — finite-scope setup only, explicitly not a theorem.
No review verdict is requested in WP-5. First consumer WP-6 requires REVIEWED
before any theorem-facing use.

## Setup (what WP-5 records)

- H1 (EMPTY state-pair storage): NOT_APPLICABLE to causal history ledgers,
  which require replayable histories absent from H1 (spec S14.2).
- H2R (BANK_COMMITTED/unlocks=0, bytes in sealed parent custody): NOT_APPLICABLE
  without fabrication; firewall preserved.
- H3T (70k transfer episodes): fully evaluated once per frozen candidate;
  survival is finite-sample survival, never theorem status.
- n8 remains PARTIALLY_REVEALED_CANARY_CONTAMINATED and is never labeled fresh.

## Obligation (WP-6)

Interpret legacy H1/H2R and new H3T only within their declared schemas, and
prove no universal claim from finite holdout survival.
