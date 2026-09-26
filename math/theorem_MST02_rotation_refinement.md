# Theorem MST02 — rotation trace refines each Pair-Access edge

**Status:** PROVED (author claim; human review pending — see `math/reviews/MST0-02.REVIEW-PACKAGE.md`).
**Domain:** every KEEP/DELETE edge over any `n`, any legal pair state, any key.

## Statement
(i) Concatenating the recorded primitive rotations reproduces the parent `S_x(T)`.
(ii) The frozen access-cost convention (`depth+1`) is unchanged by refinement.
(iii) Refinement does not alter the pair successor or Pair-Access edge identity.

## Proof
(i) `splay()` executes exactly the recorded rotation sequence: each loop iteration
performs one case-step — a single pointer rewiring for ZIG, two for LL/RR/LR/RL —
and appends one event (`python/splay_ref/splay.py`).
The returned root is the rotated tree itself, not a reconstruction; `trace_keep` /
`trace_delete` serialize that same object. Final-tree equality between the two
independent implementations holds on all tested sequences (`ROT-01`, `ROT-10`,
foundation + stress suites), and corpus-wide replay closes every imported cycle.
(ii) `cost()` is computed from `depth()` on the pre-splay tree, independent of the
event list; rotation events are structural charging units only. No code path assigns
cost from rotation counts (`ROT-12` rationale; `test_foundation` cost checks).
(iii) Successors are computed by `keep`/`delete` (pair.py), which the trace wrappers
call without reimplementing; edge identity `(mode, pre-state, key)` is preserved in
every event's `pair_edge_id`. Cycle replay chains our successors and closes exactly.

## Scope limits
Rotation-case coverage (ROOT/ZIG/LL/RR/LR/RL) is established by construction +
corpus observation; the arbitrary-n case analysis required by later proof phases
belongs to WP-6. This theorem authorizes trace *use*, not theorem status of any
transfer law built atop traces.
