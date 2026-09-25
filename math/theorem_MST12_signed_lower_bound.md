# Theorem MST12 — signed lower bound: NOT ACTIVATED (setup record)

**Status:** UNPROVED — Branch B was preregistered but never activated: Branch A was
not rejected by exact evidence (it survives development narrowly), so the activation
precondition fails. No review verdict is requested. If Branch A dies on fresh
evidence, a new signed search may activate under a new record (new ID).
**Domain:** none yet (no signed credits exist in any frozen calculus).

## Setup (frozen for potential activation)
- Signed branch permissions (T1–T10 incl. T9), lower-bound requirement, and the
energy-floor search shape are preregistered (`transfer_grammar_v0.3.yaml`) and
implemented (`transfer/branches.py` returns BLOCKED without an exact Branch-A
rejection record; `ledger/energy.check_lower_bound` is the floor primitive).
- Activation requires: exact Branch-A rejection record (grammar version, rule types,
witness, interpretation) — absent at WP-4 close.

## Scope limits
Nothing signed exists; no lower bound is claimed; no energy can go negative because
no signed ledger exists. Any future signed work starts from this record.
