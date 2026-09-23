# Theorem MST04 — KEEP reference-snapshot convention is legitimate

**Status:** PROVED (author claim; human review pending — see `math/reviews/MST0-04.REVIEW-PACKAGE.md`).
**Domain:** every synchronous KEEP edge under analysis convention `KEEP_REF_SNAPSHOT-v1`.

## Statement
Freezing the post-A-splay tree `A1` as the reference snapshot for the B-side structural
analysis of a KEEP does not alter the paired execution, its costs, or its successor;
it is a deterministic viewpoint function of the legal execution.

## Proof
1. The actual execution `K_x(A,B) = (S_x A, S_x B)` is computed first, identically with
or without the viewpoint (`pair.keep`; both implementations agree).
2. The snapshot hash is a pure function of `A1` (`reference.snapshot_hash`); identical
inputs reproduce identical snapshots (determinism test in `run_phase03`, WP1-STEP-04).
3. The B-side rotation sequence analyzed against the frozen snapshot is the same
sequence the execution performs — freezing only fixes *which* tree the structural
predicates (heavy paths, gaps, intervals) are evaluated on, and predicates are always
evaluated on the explicitly recorded snapshot hash, never on an ambiguous tree.
4. The convention is versioned (`KEEP_REF_SNAPSHOT-v1`, `reference.describe()`); any
alternative (e.g. synchronized reference updates inside the B splay) mints a new
version with an equivalence proof or explicit separation — so no result can silently
depend on the choice.

## Scope limits
Legitimacy is claimed for structural *accounting* (the intended use). Whether a
particular amortized comparison remains valid under this viewpoint is the subject of
the WP-6 transfer theorems, not this theorem.
