# Theorem MST10 — causal ledger update is deterministic

**Status:** PROVED (author claim; human review pending — see `math/reviews/MST0-10.REVIEW-PACKAGE.md`).
**Domain:** every finite legal ledger × every legal rotation event × every finite
WELL-FORMED frozen rule list. Malformed rules (bad matches, duplicate IDs, grammar
or complexity violations) belong to validation failure before invocation
(`grammar.check_ruleset`), not to the update operator's domain.

## Statement
For every frozen legal rule list R, update_R: L × E → L × T is a well-defined
deterministic transition operator: equal inputs always yield equal outputs and
equal applied-traces. Rules are a frozen parameter, never a provenance-dependent
input; external provenance tag lists are derived bookkeeping outside the operator.

## Proof
1. Totality on the domain: the function iterates `sorted(rules, key=rule_id)`;
uniqueness of IDs is enforced both pre-invocation (`check_ruleset`) and at
invocation (duplicate IDs raise), so the order is genuinely canonical, not merely
stable. Event-only matches are total predicates; multiset removal is
present-or-skip, both branches defined; every path returns.
2. Determinism: no IO, time reads, randomness, or hidden state; all iteration over
canonically ordered structures; ledger equality is canonical-tuple equality
(`state.canonical`, which INCLUDES credit provenance fields). Re-execution on equal
inputs yields equal outputs and traces (tested + fuzzed).
3. Provenance/merge soundness: credit provenance FIELDS are part of canonical state
(`state._key`), so equal ledgers carry equal provenance content. External merged
tag lists are never consumed by update (not parameters; verified by signature and
by test: equal ledgers with different tag histories evolve identically). Hence
merge-equivalence over L alone is sound: L_1 = L_2 implies identical future
evolution. No (L,P) pairing is needed because P-tags do not influence U_R.

## Scope limits
Determinism of the MACHINERY only. Soundness of any particular rule set (transfer
preservation, MST0-11) is a separate obligation owned by WP-3 as setup and proved in
WP-6 over instantiated rules. No claim about which credits SHOULD exist.
