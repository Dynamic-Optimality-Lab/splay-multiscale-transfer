# TRANSFER_CALCULUS_LEDGER.md — SPLAY-AM-MST-v0.3 frozen transfer calculi (WP-5 draft)

**Status:** `TRANSFER_CALCULUS_FROZEN` (finite hypotheses, explicitly not theorems).
Finite survival is never theorem status; arbitrary-n proof belongs to WP-6.

## Frozen set (Phase-14 commitment)

| ID | Parent | Branch | Predicate | k | C | H3T verdict |
|----|--------|--------|-----------|---|---|-------------|
| MSTC-0001 | MSTC-DEV-0001 | RAW_BOUNDARY | P_all | 2 | 2 | see `artifacts/v03/holdouts/h3t_reveal.json` |
| MSTC-0002 | MSTC-DEV-0002 | RAW_BOUNDARY | P_all | 6 | 2 | see `artifacts/v03/holdouts/h3t_reveal.json` |
| MSTC-0003 | MSTC-DEV-0003 | RAW_BOUNDARY | P_keep | 1 | 6 | see `artifacts/v03/holdouts/h3t_reveal.json` |

Set hash: see `artifacts/v03/holdouts/candidate_set_commit.json`.
Ontology `MST-ONTOLOGY-v0.3`; mapping `L6MAP-v0.3.1`; reference `KEEP_REF_SNAPSHOT-v1`.

## Mathematical definition (replayed independently by three code paths)

Ledger `L` = finite multiset of `(type, support, scale, mass, provenance)` with
`type ∈ {BOUNDARY_LATENT, BOUNDARY_ACTIVE, SPENT}`,
`support = (boundary, i, i+1, orientation)`, `scale = (S0, 0)`, unit masses,
unsigned (Branch A). Initial ledger empty, `E(L) = |LATENT| + |ACTIVE|`, `E0 = 0`.

- **T7 injection:** each A-side rotation injects up to `k` LATENT credits at
  cycling interior interval boundaries `(i,i+1)`, oriented LEFT iff `i+1 <= x`.
- **T5 activation:** each rotation event whose mode satisfies the frozen
  predicate converts one LATENT credit into an ACTIVE credit (same support).
- **T6 repayment:** on a burdened KEEP edge (`w = y − C·a > 0`, carried by the
  terminal B-rotation), discharge `min(pool, w)` ACTIVE credits; residual
  `res = w − paid`. One exact residual at the frozen C rejects that candidate
  at that C.
- **Lower bound:** unsigned masses imply `E(L) >= 0` on every legal ledger.

## Fresh-test scope (Phase-15/16)

H1 `NOT_APPLICABLE` (causal ledgers need histories; H1 is EMPTY state-pair
storage). H2R `NOT_APPLICABLE` (schema-compatible, bank bytes in sealed parent
custody, never vendored; no fabrication). H3T evaluated fully (70,000 episodes,
7 sizes × 11 strata), every claimed violation replayed by the clean-room
evaluator, large-n sweep `n = 16..256`, 8 mutation controls all caught.
Ceiling at most `TRANSFER_CALCULUS_SURVIVES_FINITE_TESTS`.

## Post-reveal rule

Any change to credit type, support, scale, predicate, coefficient, rule
precondition/output, cancellation rule, C, initialization, or snapshot
convention mints a new calculus ID with status `POST_HOLDOUT` and is never
called fresh-tested on the consumed banks (TR-11, HLD-12).

## WP-6 seal (FINAL)

<!-- WP6-SEAL -->
Standing finite survivor: MSTC-0002 (P_all, k=6, C=2) —
70,000/70,000 H3T episodes + 54 large-n trials, zero exact
residuals. Siblings MSTC-0001 (max_res=8) and MSTC-0003
(max_res=23) killed fresh with witnesses in
`artifacts/v03/holdouts/h3t_reveal.json`. Terminal claim:
`TRANSFER_CALCULUS_SURVIVES_FINITE_TESTS` (see
`artifacts/v03/seal/FINAL_RESULT.json`). No theorem; pending
human reviews MST0-13/23/24/26 are not consumed.
