# Theorem MST11 — transfer grammar preserves ledger state: SETUP (not yet provable)

**Status:** SETUP — statement and schema frozen; proof belongs to WP-6 over
instantiated transfer rules (WP-4 synthesis has not run; no fitted rule exists).
Explicitly UNPROVED. No review verdict is requested for this document in WP-3.
**Domain:** every primitive rotation under every grammar-conformant rule.

## Statement (to be proved in WP-6)
For every rule record passing `grammar.validate_rule` + `complexity.audit_rule`,
the local packet replacement preserves a globally defined ledger state: the update
is independent of arbitrary decomposition choices and conserves the declared
flow quantities (or the integrated energy telescopes as claimed by the rule's
bounds).

## Frozen setup (WP-3 deliverable)
- Rule record schema with all §10.4 fields (`transfer/templates_T1_T10.py`).
- Conformance gates: grammar validation + complexity audit + flow audit, all
machine-checked per rule (`run_phase09.py` constructs one clean rule per template
and three caught negative controls).
- Branch discipline: RAW_BOUNDARY now, SIGNED_MULTISCALE only on exact Branch-A
rejection (activation BLOCKED at WP-3 close).
- Deterministic update machinery (MST0-10, REVIEWED-track pending).

## Explicitly missing (blocks PROVED)
1. Instantiated transfer rules with fitted parameters (WP-4 synthesis on development
corpora only, exact solvers with independent replay).
2. Per-rule preservation arguments + the global integrability argument (WP-6).
3. Signed-branch lower-bound route (activates only with Branch B).

## Scope limits
This document authorizes nothing theorem-facing. WP-4 may instantiate rules within
the frozen language; any preservation claim before WP-6 proof is a seal violation.
