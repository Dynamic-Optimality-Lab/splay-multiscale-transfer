# Theorem MST03 — Pair-Access L6 translation is definitionally correct

**Status:** PROVED (author claim; human review pending — see `math/reviews/MST0-03.REVIEW-PACKAGE.md`).
**Domain:** all 27 preregistered translation entities (L6MAP-v0.3.1).

## Statement
For every imported source object used theorem-facing, the Pair-Access counterpart is
either literally identical (SAME, with quoted source definition), or differs only as
explicitly recorded with proof; no source theorem is consumed; no object is used
before its mapping is reviewed.

## Proof
1. **Source fidelity.** All definitions were extracted from the frozen L6 bytes
(`external/papers/L6_chmel_et_al_2026_2607.18498.pdf`, 68 pp) by
`l6_translation/extract.py` (`l6_source_sites.json`); each mapping record quotes its
source passage with page number (`math/L6_PAIR_ACCESS_MAPPING.md`).
2. **Per-object verdicts.** Rank/heap/gaps/lazy/pairings/important-unimportant/bends/
contracted/ops: SAME against quoted definitions (operationalizations — heap-parent
value reading, magnitude-as-equal-contracted, explicit LARGE threshold — recorded with
justification). Heavy edge/path/light: SAME predicate (verbatim min-rank-equality)
PLUS the ordinary-BST uniqueness theorem proved here: every BST-subtree interval has
a unique reference-depth minimizer — else two minimizers x<y at depth d force their
strictly shallower LCA into the interval, contradiction; hence both children can never
jointly attain the parent minimum, ties are impossible (0 ties over all 19,413
reference/subject pairs n≤6), and the code tie-break is unreachable insurance.
3. **Dual implementation.** Pointer-based primary and dict-based independent
implementations agree on ranks, heavy sets, components, heap records, gaps, bends
(all 7 fields) on corpus + sampled pairs (`mapping_check.check_agreement`); five
mutant controls discriminate (rank orientation, tie-absence invariant, gap sign,
bend presence, contracted exactness).
4. **No-transplant discipline.** Gap/pairing/bend COUNT and paid/free claims are
explicitly withheld (mapping doc + `ops` records say so); they are WP-2B/WP-6
measurements and theorems, never citations.
5. **Fallbacks untouched.** Zero `NOT_APPLICABLE` rulings; no `MST_NATIVE_*` fallback
activates. The activation machinery stands tested by schema, not by use.

## Scope limits
Definitional correctness only. Structural *lemmas* built on these objects
(MST0-05/06/07/08) are separate obligations with their own evidence. Consuming any
source lemma theorem-facing still requires this document's REVIEWED verdict first.
