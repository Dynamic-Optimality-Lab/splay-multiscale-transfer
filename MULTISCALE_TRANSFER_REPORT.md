# MULTISCALE_TRANSFER_REPORT.md — SPLAY-AM-MST-v0.3 final report (answers Q01–Q40)

**Experiment:** `SPLAY-AM-MST-v0.3` · **Terminal claim:**
`TRANSFER_CALCULUS_SURVIVES_FINITE_TESTS` (finite level; see Q36). Finite
survival is never a theorem (§32.7). All quantities below are exact
(integers/`Fraction`); floats were visualization-only.

## Q01 What exact parent facts were imported from v0.1 and v0.2?

Reachable pair counts n=2..7: 4/19/196/1764/17424/184041 (independently
recomputed, all equal). Finite subsequence overheads b*: 1, 1, 3/2, 8/5, 8/5,
23/14 (strict chained replay 19/19 cycles, all closed, all-KEEP). Bellman
anchors max U_2/V_2 per n imported as context claims. Critical geometry:
n≥4 cyclic, KEEP-only forced derivatives, diagonal forced states. v0.2: Bellman
future-regret/past-slack semantics, behavioral quotient KERNEL_NO_COMPRESSION,
D1–D7 atom inconsistency, D5 3318/3334 near-miss with 16 exact failures,
PHI-0001/2/3 REJECTED, H1 EMPTY, H2R BANK_COMMITTED/0. Evidence:
`artifacts/v03/parent_import/`, `cycles/expanded/`.

## Q02 Was v0.2 finally sealed before v0.3 scientific execution?

Yes. Full commit `38c1be6afd2ab2420aa094c68ce45ee6a26b3628`, terminal claim
`FINITE_DEBT_LAW_MINING_RESULTS`, manifest/archive/route-audit hashes pinned in
`SPLAY_AM_MST_IMPLEMENTATION_SPEC_v0.3.1_PIN.md` discharging
`PRE_FREEZE_PARENT_PIN_REQUIRED`. No Phase-01+ science predates the pin.

## Q03 Which exact L6 version was frozen?

Chmel et al., `arXiv:2607.18498 v1` (2026-07-20), 68 pages, 628,208 bytes,
SHA-256 recorded in `external/MANIFEST.json`. Identity frozen pre-proof;
source identities (paper v1 + definition slots) frozen where bytes sufficed.

## Q04 Which L6 objects translated definitionally and which changed semantics?

All 27 declared translation entities resolved SAME with recorded
operationalizations (heavy-edge uniqueness proved for ordinary BSTs via
interval-LCA; 0 ties over 19,413 pairs; tie-break unreachable insurance).
`PA_*`/`MST_*` prefixes kept until REVIEWED. Every record carries a
preregistered `MST_NATIVE_*` fallback; none activated (no NOT_APPLICABLE ruling
needed). Refuted equivalences: none (no proposed equivalence was refuted).

## Q05 What is the exact KEEP reference-snapshot convention?

`KEEP_REF_SNAPSHOT-v1`: observe pre-KEEP pair → execute A splay → freeze A_1 as
the reference snapshot → execute B splay rotation-by-rotation against it →
record final pair. Analysis convention only; alternative conventions mint new
version IDs (MST0-04 REVIEWED).

## Q06 Is the strongest natural KEEP heavy-path lemma true or false?

True in the proved form: under the translated rank, every B-path edge attains
min-rank 0 on both sides because x is the A1-root (rank-0 proof, MST0-05
REVIEWED). No stronger all-heavy claim was transplanted without proof.

## Q07 How do positive-regret critical KEEP edges decompose?

Per-edge `#ZIG/#LL/#RR/#LR/#RL`, A/B path lengths, regret per diagnostic C,
pairing classes, bend/gap/contracted deltas, interval creation counts stored
for 70/70 critical edges (`cycles/stratified/`). Analysis stratified by these
classes throughout; no narrative answer stands without its predicate.

## Q08 Which pairing classes dominate or fail critical burden?

R1: 2856 GOOD / 2301 BAD; R2: 692 / 799 at n64 (both classes real). Natural
MST0-06 FALSE_AS_STATED (degeneracy structural via MST0-05) with smallest
witnesses preserved; conditional v2 PROVED and REVIEWED.

## Q09 Which bend events align with zig-zag burden?

816/816 B zig-zag rotations destroy ≥1 bend (turn-destruction proof, MST0-07
REVIEWED). Bend-supported credit discharge (T10) therefore has proved
finite mechanics; universal payment is not claimed (MST0-14 UNPROVED).

## Q10 Which raw gap / point-gap changes align with critical burden?

Contracted deltas in [-1,6], important-boundary max +6, structural ops/rotation
≤6 (baseline shape reproduced; paid/free classification UNDETERMINED).
Raw gaps instrumented per rotation; no raw-gap theorem claimed.

## Q11 Can one A rotation cause only O(1) translated structural modifications?

Finitely yes: exhaustive n≤6 (870 rotations: flips≤2/gap≤2/created≤3) plus
hill-climb maxima 2 at n8–64. Universally open (MST0-08 SPLIT: finite PROVED,
arbitrary-n UNPROVED with explicit gap; universal consumption blocked).

## Q12 What event types inject candidate discrepancy credit?

A-side rotations only (T7, ≤k per rotation at cycling interior-boundary
sites). B-side rotations, KEEP/DELETE labels alone, and reference updates
inject nothing.

## Q13 What event types merely transfer it?

T5 activation (LATENT→ACTIVE, count-conserving) on frozen-predicate events; T6
repayment (ACTIVE→SPENT) on burdened KEEP edges. T1–T4/T8–T10 templates exist in
grammar; frozen candidates instantiate T5/T6/T7 only.

## Q14 What makes credit ACTIVE rather than LATENT?

The frozen structural predicate evaluated on the current rotation event only
(P_all: every event; P_keep: KEEP events). No future keys, Bellman values, or
holdout labels are consulted (static audit + `check_event_predicate`).

## Q15 What exact objects distinguish the D5 exceptional repayment failures?

The 16 D5 failures (counters verified 3318/3334) analyzed as specimens with
boundary/zig/scale/bend/lazy/provenance/geometry predicates; structural
separation recorded with zero reweighting (`cycles/d5_analysis` via WP-2B).

## Q16 Did Branch A survive development?

Yes, narrowly: `RAW_BOUNDARY_LAW_SURVIVES_DEV` (P_all-only survival; 30/42
feasible at C=2, 42/42 at C≥3; histories screen P_all-only; battery 84/0).

## Q17 If Branch A failed, what is its smallest exact counterexample?

Branch A as a family did not fail development; killed sub-families: all
non-P_all predicates dead ∀k≤6 (timing killer: no activation during DELETE
bursts); P_all k=1 dead at C=2..4 (rate insufficiency). Smallest witnesses in
`solver/histories_screen.json` (e.g. P_keep first violation paid=3 res=[2,1] on
gen-0 at C=2).

## Q18 Does the Branch-A obstruction inflate with scale?

No scale growth observed: 11 motif inflations ×1/2/4/8 give CONSTANT actual
ratios (= cycle ratio). The obstruction is a representation (timing/rate)
obstruction at every tested scale, not a growing one.

## Q19 Was Branch B activated under the preregistered rule?

No. Activation requires exact Branch-A rejection; Branch A kept a standing
finite survivor through WP-5. `SIGNED_TRANSFER_NOT_ACTIVATED`; probe module
tested on fixtures, unfired on corpus.

## Q20 If signed credits are used, what proves the energy lower bound?

Not applicable: zero signed components exist in any frozen calculus
(MST0-12 NOT_APPLICABLE with preserved justification).

## Q21 What is the smallest finite transfer grammar that survives development under the frozen complexity order?

(P_all, k=2, C=2) — minimal-k anchor MSTC-DEV-0001/MSTC-0001. Max-headroom
(P_all, k=6, C=2); weakest-predicate survivor (P_keep, k=1, C=6).

## Q22 Does it remain stable across n and diagnostic C without changing rules?

Rules frozen; C varied only: C=2 binding (30/42), C≥3 all 42/42 on cycles;
histories C≥12 VACUOUS (recorded inconclusive, never passes). Larger C eases
the inequality (stability reading, not hardness).

## Q23 What is the frozen theorem constant C and where did it come from?

2 / 2 / 6 per candidate, taken from the WP-4 dev shortlist (diagnostic
anchors, conservative). No theorem constant exists; WP-6 proves none (MST0-22
UNPROVED setup).

## Q24 Were H1/H2R/H3T still fresh when first consumed?

H1 EMPTY (never fresh content; routed NOT_APPLICABLE). H2R BANK_COMMITTED/0
(fresh by firewall, but bytes in sealed parent custody and never vendored;
routed NOT_APPLICABLE without fabrication). H3T BANK_COMMITTED/0 at freeze,
transitioned FROZEN then UNLOCKED_ONCE exactly once (Phase 15). n8 kept
contaminated, never fresh (HLD-01).

## Q25 What did each fresh bank say?

H1/H2R: no verdict (incompatible/absent, truthfully recorded). H3T (70,000
episodes exact): MSTC-0001 FAIL (max_res=8; first n32 idx 4406, w=11 paid 9);
MSTC-0002 PASS (max_res=0, 70k/70k); MSTC-0003 FAIL (max_res=23; first n16 idx
3610, w=8 paid 7). All violations clean-room replayed.

## Q26 Did clean-room implementation agree?

Yes: 16/16 Phase-15 replay checks, 27/27 Phase-16 battery checks, agreement on
every large-n trial (54/54). Zero disagreements anywhere.

## Q27 What was the strongest adversarial counterexample search result?

Against survivors: nothing — WP-4 battery 84 evaluations 0 kills; WP-5 large-n
54 trials 0 kills (n≤256). The strongest kill signals in the seal are the H3T
fresh falsifications of MSTC-0001/0003 (exact residuals 8 and 23 with
edge-level witnesses).

## Q28 Which arbitrary-n rotation lemmas were actually proved?

Author-claim PROVED (human review pending): MST0-13 DELETE injection
(C_D=6 for MSTC-0002; k-generic mechanics). REVIEWED finite: MST0-05,
MST0-06-conditional, MST0-07, MST0-08-finite. UNPROVED universal: MST0-08
universal, MST0-14, MST0-15.

## Q29 Is bounded DELETE injection proved?

Author proof claim PROVED for MSTC-0002 (`E_after − E_before ≤ 6·cost_A(D)`,
case-complete, no finite premise, machine-checked bound on fresh samples);
human review requested, not yet REVIEWED, hence not consumed theorem-facing.

## Q30 Is synchronous KEEP transfer proved?

No (MST0-14 UNPROVED). Sibling fresh falsifications plus survivor-only finite
evidence; no universal repayment argument exists.

## Q31 Is integrability / global energy proved?

No (MST0-15 UNPROVED). Finite ledgers are deterministic and canonical-ordered;
decomposition independence is unproved.

## Q32 Does the block theorem cover every legal paired execution?

The partition does (MST0-16 REVIEWED: maximal blocks cover every execution
exactly once). The block inequality theorem does not exist (MST0-17 BLOCKED).

## Q33 What exact Pair-Access inequality is obtained?

None universally. Finite form for MSTC-0002 on tested episodes:
`Splay(Y) + E_m − E_0 ≤ 2·Splay(X)` with `E_0 = 0 ≤ E_m` observed (not proved)
on 70,054+ episodes. This is evidence, not an inequality theorem.

## Q34 Does it include an additive term, and is that bridge-compatible?

No additive term exists because no telescope is proved (MST0-18 BLOCKED). The
preferred `A(n) = 0` route is targeted but unreached.

## Q35 Did the Levy–Tarjan convention audit pass?

The audit was not reached (MST0-19 BLOCKED). Checklist recorded with L2/L3
premise bytes PENDING (downstream-use blocks hold). No bridge conclusion drawn.

## Q36 What is the exact final claim level?

`TRANSFER_CALCULUS_SURVIVES_FINITE_TESTS`, standing calculus MSTC-0002
(P_all, k=6, C=2). Exactly one terminal level; no theorem-facing branch active.

## Q37 If no positive theorem, did any actual Splay ratio family grow?

No. Every inflation produced constant actual ratios. No unbounded real Splay
family exists in the record.

## Q38 If negative branch activated, is the family closed form and diagonal-rooted?

Not applicable: the negative branch never activated (NEGATIVE_FAMILY_
NOT_ACTIVATED 11/11). No family, no form, no claim.

## Q39 Which failures are representation obstructions versus conjecture obstructions?

All recorded failures are representation obstructions (a frozen ledger cannot
pay observed burden at frozen C — timing/rate mechanics identified). No
conjecture obstruction is established in either direction: Pair Access is
neither proved nor disproved; the 2026 log/loglog loss is neither shown
necessary nor removed.

## Q40 What should a subsequent paper claim, and what must it explicitly not claim?

May claim: exact L6→Pair-Access translation with finite lemmas; critical-cycle
rotation-level corpus and burden decomposition; dev/fresh finite survival of
(P_all,k=6,C=2) with H3T witnesses; the MST0-13 injection lemma (only after
its requested human review returns ACCEPT); the two fresh falsifications with
minimal witnesses. Must not claim: any universal Pair-Access/monotonicity/
optimality theorem; a theorem constant; signed-credit safety; necessity of
logarithmic loss; any unbounded Splay family; that finite survival implies
arbitrary-n behavior. The pending human reviews (MST0-13/23/24/26) are the
defined upgrade path and none is pre-counted.
