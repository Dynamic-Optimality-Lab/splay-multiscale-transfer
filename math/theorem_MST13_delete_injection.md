# Theorem MST0-13 — bounded DELETE injection (universal, candidate MSTC-0002)

**Status:** PROVED — author proof claim for arbitrary n (human theorem review
requested; REVIEWED only on human ACCEPT per `math/reviews/REVIEW_TEMPLATE.md`).
First consumer WP-6 requires REVIEWED before theorem-facing consumption; until
then this record is evidence, not a consumed theorem.

**Domain:** every legal paired execution at arbitrary n, A-only DELETE blocks
(or finer per-access/per-rotation granularity), frozen calculus MSTC-0002
(`P_all`, k=6, C=2; Branch RAW_BOUNDARY, unsigned unit masses,
`KEEP_REF_SNAPSHOT-v1`, ontology `MST-ONTOLOGY-v0.3`).

## Statement

For every A-only DELETE block D:

```math
E_after - E_before <= 6 * cost_A(D)
```

with `E(L) = count(BOUNDARY_LATENT) + count(BOUNDARY_ACTIVE)`, `E(empty) = 0`.

## Proof

Work at rotation granularity. Fix an A-side rotation event e.

**Lemma 1 (rotations cost-bounded).** One ordinary bottom-up splay access of
cost `a = depth(x)+1` performs R rotations with R <= a. Each loop iteration
reduces depth(x) by at least its rotation count: ZIG does 1 rotation for 1
level (x reaches the root); LL/RR/LR/RL do 2 rotations for 2 levels. Summing
over the access, R <= initial depth(x) = a-1 < a. All six cases
(ROOT/ZIG/LL/RR/LR/RL) are covered: ROOT performs 0 rotations.

**Lemma 2 (injection bounded).** Rule TR-A-T7 adds at most k=6 LATENT credits
per A-side rotation (exactly 6 at cycling interior-boundary sites; fewer only
when the rotated interval contributes no interior boundary, in which case sites
are empty and injection is 0). Over block D with R_A total A-side rotations,
`injected(D) <= 6 * R_A`. By Lemma 1 summed over the block,
`R_A <= cost_A(D)`, so `injected(D) <= 6 * cost_A(D)`.

**Lemma 3 (T5 conserves).** Rule TR-A-T5 consumes one BOUNDARY_LATENT and
produces one BOUNDARY_ACTIVE (same unit mass): energy change 0 per firing,
regardless of predicate outcome.

**Lemma 4 (T6 inapplicable on DELETE).** Rule TR-A-T6 matches `mode_is: KEEP`
only. Every rotation event of a DELETE block carries mode DELETE, so T6 fires
0 times on D: energy change 0.

**Theorem.** `E_after - E_before = injected(D) + 0 + 0 <= 6 * cost_A(D)` by
Lemmas 2–4. The argument is k-generic (any frozen k gives `C_D = k`); it is
stated for the promoted primary MSTC-0002 with `C_D = 6` (Phase 17 promotes at
most one primary at a time).

## Case completeness

ROOT (vacuous, R=0), ZIG/LL/RR/LR/RL (Lemma 1 covers each; site selection
differs per case but only the count bound is used). Every ledger operation on
DELETE blocks is one of T7/T5/T6 (Lemmas 2–4 exhaust them). No lazy-interval
aggregate operation exists in Branch A (T8 absent by branch).

## No finite premise (STOP-36)

The proof uses no `n<=7` bound, no holdout pass, no cycle-catalog completeness,
no solver optimality, no empirical scaling, and no finite grammar feasibility.
Constants (k=6, unit masses, S0 scale) are n-independent in form (STOP-39).

## No hidden n-dependence

Support sites are interval-relative `(boundary, i, i+1, orientation)`; no
state/cycle/holdout IDs, no U/V/G lookup, no future information, exact
`Fraction` arithmetic throughout.

## Machine evidence (supporting only, never the proof)

`scripts/run_phase17.py` STEP-02 verifies `injected <= k * R_A` per episode on a
stratified fresh sample plus synthetic histories for all three frozen
candidates (bound holds with the candidates' own k). Evidence record:
`artifacts/v03/proofs/MST13_injection_bound.json`.

## Review request

Human reviewer: prove → independent check → verdict per REVIEW_TEMPLATE.md.
Record verdict as `math/reviews/MST0-13.review.json`. On ACCEPT the Phase-17
gate `BOUNDED_DELETE_INJECTION_PROVED` may be consumed theorem-facing; until
then FINAL_RESULT stays at the finite-survival level (fail-closed).
