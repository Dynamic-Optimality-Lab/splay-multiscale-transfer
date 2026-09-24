# L6 Pair-Access mapping (L6MAP-v0.3.1) — WP-2A populated from immutable preregistration

**Source bytes:** `external/papers/L6_chmel_et_al_2026_2607.18498.pdf` (628,208 B,
SHA-256 `60B3213D…`, 68 pp). Quoted lines below are verbatim extraction contexts;
page numbers refer to the frozen PDF. Statuses resolve the preregistered
`UNRESOLVED_PRE_PROOF` values; the yaml itself is unchanged. No source-paper theorem
is consumed — only definitional language. Fallbacks (`MST_NATIVE_*`) activate solely
on `NOT_APPLICABLE`; none activates below.

## Conventions (frozen)
- Reference tree for KEEP analysis: post-A-splay snapshot A1 (`KEEP_REF_SNAPSHOT-v1`).
- Tie semantics: every tie/uniqueness assumption proved or explicitly represented.
- Naming: `PA_*` until equivalence REVIEWED.

## PA_REFERENCE_RANK — SAME
- Source (p.3/p.6): "we define its rank to be its depth in T_OPT [static]".
- PA: rank(v) = depth of v in the reference snapshot (root 0). `rank.py`.
- Obligation MST0-03. Difference: none — the source rank IS depth-in-reference, so no
  depth substitution occurred. Implementation mapping: `rank_in_reference`/`all_ranks`.

## PA_HEAVY_EDGE — SAME
- Source (p.6): "Consider an edge (u,v) with u being the parent of v. The minimum
  rank among the nodes in the subtree of u is less than or equal to the minimum rank
  among the nodes in the subtree of v. If it is equal, we call the edge heavy,
  otherwise it is light."
- PA: identical predicate on ordinary BSTs. `heavy.heavy_edges`.
- Obligation MST0-03. Difference: none in the predicate. Uniqueness (at most one
  heavy child per node) is PROVED for ordinary BSTs by the interval-LCA argument
  (see theorem_MST03; source Lemma 4 covers the ternary setting): two minimizers
  x<y at depth d force their strictly shallower LCA into the interval — contradiction.
  Hence ties are impossible (verified: 0 ties over all 19,413 reference/subject pairs
  n≤6); the both-light tie-break in code is unreachable totality insurance.

## PA_HEAVY_PATH — SAME
- Source (p.6): heavy edges decompose the tree into heavy paths and light edges.
- PA: maximal heavy-edge chains (= connected components, which are chains by the
  uniqueness result). `heavy.components`. Obligation MST0-03. Difference: none.

## PA_LIGHT_EDGE — SAME
- Source: complement of heavy (p.6). PA: complement. Obligation MST0-03. None.

## PA_HEAP_VIEW (+PA_HEAP_PARENT/CHILD_LEFT/CHILD_RIGHT) — SAME
- Source (p.10): "contracting every heavy path into the bottom-most node and keeping
  all the children of nodes on the heavy path as children of the contracted node… the
  contracted tree is heap-ordered on the ranks… heap-children whose values precede that
  of the heap-parent in symmetric order are called left heap-children; right
  heap-children analogously."
- PA: identical construction; heap-parent VALUE read as the bottom-most node's key
  (explicit reading, recorded). `heap.heap_view`. Obligation MST0-03. Difference:
  none in construction; the heap property (child rank > parent rank) is VERIFIED on
  corpus (see `gaps.check_heap_property` measurements), not assumed.

## PA_RAW_GAP / PA_INTERVAL_GAP / PA_POINT_GAP — SAME
- Source (p.8/p.10): "we define the gap of a heavy path P as the difference between
  the rank of P and the rank of the heavy path to which it is connected by a light
  edge. The gap of the root heavy path… is 0." / "The amount by which the whole
  interval is shifted is called an interval gap and the gaps without this shift are
  called point gaps."
- PA: identical rank differences; root component gap 0. `gaps.raw_gaps`. Obligation
  MST0-03. Difference: none. Source-paper gap THEOREMS remain quarantined.

## PA_LAZY_INTERVAL / PA_GROWING_INTERVAL / PA_SHRINKING_INTERVAL / PA_BROKEN_INTERVAL — SAME
- Source (p.10): "we can group consecutive heap-children of each heavy path into
  so-called lazy intervals. Instead of updating the gaps, we simply record the amount
  by which all gaps in an interval are shifted."
- PA: per-component member list + shift; growing/shrinking/broken as structural
  predicates over before/after member sets (`lazy.transition_state`). Obligation
  MST0-03. Difference: none in construction/shift bookkeeping; update RULES under
  rotations are WP-3 dynamics, not claimed here.

## PA_INTERNAL_PAIRING / PA_BOUNDARY_PAIRING — SAME
- Source (p.11): "a zig-zig takes three consecutive heap-children… We decompose this
  event into two pairings, in each of which one heap-child is hung below another
  heap-child with lower rank… boundary pairings, where the two heavy paths are not
  from the same lazy interval."
- PA: identical decomposition (`pairing.decompose_zigzig`); boundary = different
  intervals. Obligation MST0-03. Difference: none.

## PA_GOOD_PAIRING / PA_BAD_PAIRING — SAME (operationalized magnitude noted)
- Source (p.11-12): "The internal pairings where the point gaps are of the same
  magnitude, which we call good… The other internal pairings are called bad."
  Fig.8 uses ceiling-log values; the contracted function is ⌈1+log(1+x)⌉ binary.
- PA: same-magnitude read as equal contracted values (`contracted.contracted`, exact
  integer identity proved on 0..4999). `pairing.classify_pairing`. Obligation MST0-03.
  Difference: operationalization recorded (source "magnitude" → equal contracted
  values, justified by the Fig.8 ceiling-log discussion); the GOOD→decrease claim is a
  theorem to re-prove in PA (WP-6), not cited.

## PA_IMPORTANT_BOUNDARY_PAIRING / PA_UNIMPORTANT_BOUNDARY_PAIRING — SAME
- Source (p.11-12): "Some occur at the boundaries of very large lazy intervals, and
  their effects can be subsumed by internal pairings. We call these pairings
  unimportant… important pairings cannot happen too often within any one lazy interval."
- PA: unimportant iff max interval size ≥ preregistered `LARGE_INTERVAL_THRESHOLD=64`;
  otherwise important. Obligation MST0-03. Difference: threshold made explicit (source
  "very large" is asymptotic); frequency claims NOT transplanted (WP-6 business).

## PA_BEND — SAME (object only)
- Source (p.13): "A bend is an internal node where the heavy path 'turns' — it is a
  left child, but the heavy path continues to the right, or vice versa."
- PA: identical turn rule + explicit ambiguity clause (exactly one heavy child edge on
  the opposite side required). `bends.bends`. Obligation MST0-03. Difference: none in
  the OBJECT. The ribless assumption and all bend-COUNT lemmas (O(1) per rotation,
  zig-zag destroys one bend) do NOT transplant — PA reference trees are
  splay-generated, not ribless; counts are WP-2B measurements (MST0-07).

## PA_CONTRACTED_POINT_GAP_L6 — SAME (baseline only)
- Source (p.12): "we use ⌈1 + log(1 +x)⌉ for the contracted gap… binary."
- PA: exact integer form (bit-length identity, verified). `contracted.contracted`.
  Obligation MST0-03. Difference: none. Role: baseline reproduction only.

## PAIR_UP / DELETE_INTERVAL_MEMBER / INSERT_INTERVAL_MEMBER / SPLIT_INTERVAL / CONVERT_INTERVAL / TRANSFER_INTERVAL / HEAP_CHILD_EXCHANGE — SAME (vocabulary only)
- Source: structural lazy-interval operations (pp.10-12). PA: frozen event records
  (`ops.make_op`); paid/free status `UNDETERMINED_PRE_WP6` — explicitly NOT
  transplanted (prereg paid_free_rule). Obligation MST0-03. Difference: paid/free
  validity withheld for WP-6 re-derivation.

## Resolution summary
27/27 objects resolved (SAME ×27 with noted operationalizations; MODIFIED: none as
standalone verdicts — the heavy-edge tie-break question was settled by proof toward
SAME; NOT_APPLICABLE: none — no fallback activates). All resolutions refer to
definition language only; no source theorem consumed.
