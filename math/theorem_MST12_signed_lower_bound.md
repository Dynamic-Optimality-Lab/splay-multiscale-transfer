# Theorem MST12 — signed lower bound: NOT ACTIVATED (setup record)

**Status:** NOT_APPLICABLE — preserved justification in
`math/reviews/MST0-12.not_applicable.json` (supersedes the WP-4 UNPROVED setup
below, retained as history). Branch B was preregistered but never activated, so
no signed credits exist and no lower bound is owed. This record must never be
consumed as a positive result.

## WP-4 setup (retained history; was UNPROVED)

Branch A was not rejected by exact evidence (it survives development narrowly),
so the activation precondition fails. No review verdict was requested. If Branch A
dies on fresh evidence, a new signed search may activate under a new record (new ID).
**Domain:** none yet (no signed credits exist in any frozen calculus).

## WP-6 NOT_APPLICABLE justification (2026-09-25)

Fresh evidence killed two raw-branch siblings (MSTC-0001/0003) while MSTC-0002
stands finite; per MST0-24 (branch scope) these rejections say nothing about the
signed branch, so the activation precondition (exact Branch-A rejection of the
family form) remains absent — Branch B stays preregistered-not-activated, not
rejected. All frozen records carry `branch: RAW_BOUNDARY`, empty
`cancellation_rules`, and nonnegative masses (machine-checked by
`validate_eligibility`: unsigned_masses + frozen_scale_system). Vacuous scope:
nothing signed exists; no lower bound is claimed.

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
