# Theorem MST16 — block partition covers every paired execution exactly once

**Status:** PROVED (author claim; human review pending — see `math/reviews/MST0-16.REVIEW-PACKAGE.md`).
**Domain:** every finite paired-execution history `[(mode, key)]`.

## Statement
`rotations.blocks.partition` maps each history to an alternating sequence of maximal
`DELETE_BLOCK` / `KEEP_BLOCK` spans that tile `[0, len(history))` contiguously with no
gaps and no overlaps, deterministically from the history alone.

## Proof
By construction: the scanner advances `i → j` over the maximal run of equal block-kind
starting at `i`, emitting `[i, j)`, and repeats. Spans are contiguous by induction on
the scan position (`check_coverage` asserts `span[0] == pos` chaining to `len`); runs
are maximal by the inner while condition, so adjacent blocks always differ in kind;
determinism holds because the output is a pure function of the input list (tested by
re-partitioning a copy: `BLOCK-02`). Edge cases covered: empty history (zero blocks),
single access, leading/trailing runs of either kind (tested histories in `run_phase03`,
WP1-STEP-04, plus property checks in `tests/rotations`).

## Scope limits
This is the partition *preamble* (WP-1). That block inequalities telescope over this
partition into Pair Access is MST0-17 (WP-6), which additionally requires the transfer
theorems — not claimed here.
