# Theorem MST01 — v0.3 parent import preserves exact logical content

**Status:** PROVED (author claim; human review pending — see `math/reviews/MST0-01.REVIEW-PACKAGE.md`).
**Domain:** every v0.3 WP-1 import from `SPLAY-AM-PD-v0.1@6de1ca2` and `SPLAY-AM-BD-v0.2@38c1be6`.

## Statement
Every parent fact consumed by v0.3 (pair counts, `b_n^*` ratios, critical cycles,
forced-derivative records, failure ledgers, firewall states) is byte-identical to the
sealed parent artifact, interpreted under an audited convention match, and used only
as a comparison target for independently recomputed values — never as a logical premise.

## Proof
1. **Byte-identity.** `run_phase01.py` (WP1-STEP-01) verifies source commits by
`git rev-parse` against the pinned full SHAs, vendors files by copy, and cross-checks
every vendored v0.1 cycle file against the sealed v0.1 `MANIFEST.sha256`. Any mismatch
fails closed (`IMPORT-00/01/02`). Ledger: `artifacts/v03/parent_import/import_ledger.json`.
2. **Convention audit.** v0.1 `pid = a*C+b` with ASCII-sorted shape order
(`reference/enumerate.py`, `canonical.py: a_id, b_id = divmod(pid, c)`) is reproduced
in `python/cycles/enumerate.py` (`pid`/`unpid`, `canonical_shapes`); cost `depth+1` and
bottom-up cases match L1/parent contract. Agreement is *tested*, not assumed:
recomputed reachable counts equal parent claims exactly (4/19/196/1764/17424/184041),
and every imported critical edge replays to the identical target with identical costs
(`replay.json`, zero mismatches required).
3. **Comparison-not-premise discipline.** Imported ratios/cycles enter only equality
assertions against independently recomputed values (`COUNT-01`, `REPLAY-01`). No v0.3
theorem transitively depends on a parent value: rotation traces, circulation tables,
and later transfer calculi are functions of our own evaluator outputs.
4. **Firewall compliance.** Holdout banks (v0.1 `artifacts/holdout/`, v0.2 H1/H2R banks)
are excluded from the vendor list by construction; `import_parent.V01_FILES/V02_FILES`
enumerates every readable path (audit: no holdout substring). H3T does not exist yet.

## Scope limits
This theorem covers import fidelity only. It does not assert parent theorems are true
(they are verified where recomputable, cited as claims elsewhere), nor does it authorize
consumption — that requires the `REVIEWED` verdict on this document.
