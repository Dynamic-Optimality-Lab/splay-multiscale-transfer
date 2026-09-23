# SPLAY-AM-MST v0.3: Multiscale Synchronous Transfer, Causal Discrepancy Ledgers, and Constant-Factor Pair-Access Experiment

**Document type:** Frozen mathematical implementation specification / preregistration blueprint  
**Authoring status:** `PRE_FREEZE_PARENT_PIN_REQUIRED` — scientific design is complete, but the normative v0.3 freeze occurs only after Phase 00 pins the final sealed v0.2 commit, FINAL_RESULT, manifest, archive, and normative hashes. No Phase 01+ scientific execution is permitted before that pin.  
**Target problem:** Sleator–Tarjan Dynamic Optimality Conjecture for ordinary bottom-up Splay  
**Primary bridge:** Levy–Tarjan subsequence / approximate-monotonicity route, under an explicitly audited convention match  
**Experiment short name:** `SPLAY-AM-MST-v0.3`  
**Primary parent experiment:** `SPLAY-AM-BD-v0.2` — exact Bellman-debt / kernel / recency theorem-mining experiment  
**Primary parent sealed commit:** `TO_BE_PINNED_FROM_V0.2_WP6_FINAL_SEAL`  
**Secondary ancestor:** `SPLAY-AM-PD-v0.1`, sealed commit `6de1ca2a595e8895f54794f3a211fe6ee1a95a80`  
**Primary scientific pivot:** stop searching first for a scalar state potential; search first for the rotation-level multiscale transfer law that a valid amortization would integrate  
**Primary discovery object:** a finite-alphabet **Multiscale Synchronous Discrepancy Ledger** whose credits are injected by A-only restructuring and transferred / discharged by synchronous KEEP splays  
**Primary theorem target:** a universal constant-factor Pair-Access law obtained from bounded injection + bounded synchronous transfer, not from finite curve fitting  
**Primary current-frontier comparison:** specialize the 2026 heavy-path / lazy-interval / gap / bend analysis to the special comparator in which the reference execution is itself Splay with extra accesses, and test whether its superconstant contraction loss can be removed  
**Primary implementation languages:** Python for transparent exact instrumentation and proof mining; Rust permitted for rotation-trace / SAT / flow acceleration only behind exact-agreement gates  
**Experimental style:** deterministic, exact, theorem-led, certificate-first, counterexample-guided, two-implementation verification, strict holdout firewalls, no silent literature transplantation  
**Number of implementation phases:** 20 (`PHASE 00` through `PHASE 19`)  
**Core rule:** v0.3 may prove a constant-factor transfer law, falsify the proposed transfer ontology, expose an unbounded real Splay obstruction, or end with only finite structural results. It may never turn a successful finite transfer fit, an SAT/ILP solution, a fresh-holdout survivor, or a repeated cycle pattern into a universal theorem.

---

# 0. Executive purpose

Two exact experiments have now failed to produce the missing universal Pair-Access potential, but they failed in a highly structured way.

`SPLAY-AM-PD-v0.1` established the exact pair-state transition system, finite subsequence overheads, canonical Bellman geometry, critical cycles, forced potential derivatives, and representation-class obstructions. It found that, on the certified sizes `n=4..7`, the finite optimum is cyclic and the forced critical derivatives are carried by KEEP edges rather than DELETE edges. It also showed algebraically that the original finite feature language cannot contain a universal linear potential: the combined exact derivative system becomes inconsistent.

`SPLAY-AM-BD-v0.2` then stopped guessing `H(A,B)` directly. It proved that `V_b` is the canonical future-regret object, proved the corresponding `U_b` past-slack semantics, certified a target-independent behavioral quotient, showed finite no-compression in the exact pair dynamics, proved that pure difference-only representations lose necessary absolute-shape information, built and certified a recency-augmented state system, proved recency-blindness of canonical future value on fixed `(A,B)` fibers, mined exact creation/repayment laws, and finally froze explicit candidate debt laws. Those candidates failed from complementary directions: some are too easy to create under DELETE; others are too weak to repay expensive KEEP.

The correct v0.3 lesson is **not**:

> "Potential methods failed."

It is also **not**:

> "Pair Access is probably false."

The sharper lesson is:

> **The missing proof object is unlikely to be a single monotone amount-of-disagreement statistic. The exact obstruction lives in how discrepancy is created, transported across scales, and made chargeable by synchronous Splay dynamics.**

v0.3 therefore changes the level of attack.

v0.1 asked:

```text
Which static structural function H(A,B) can satisfy the Pair-Access inequalities?
```

v0.2 asked:

```text
What canonical debt does the pair-state dynamics already encode, and which structural/history objects create or repay it?
```

v0.3 asks:

```text
What rotation-level multiscale transfer law is conserved by synchronous KEEP dynamics,
and can A-only restructuring inject only O(1) such charge per unit cost?
```

The primary scientific object is not initially a scalar state function. It is a local transfer calculus.

Conceptually, maintain a ledger

```math
\mathcal L_t
```

of discrepancy credits indexed by exact structural objects such as:

```text
(key interval, reference heavy path, scale, lazy-interval/boundary role, orientation, provenance class).
```

A DELETE/A-only Splay may create, move, split, or relabel credits. A KEEP may move credits between scales, merge them, expose them to payment, discharge them against positive Pair-Access regret, or circulate them around a critical cycle. The theorem-facing scalar energy

```math
E(\mathcal L_t)
```

is derived only after the local calculus is explicit enough to prove bounded creation, nonnegative global accounting, and sufficient KEEP repayment.

The end-to-end positive chain is frozen as:

```math
\boxed{
\text{sealed v0.1/v0.2 evidence}
\to
\text{exact rotation-level pair traces}
\to
\text{2026 heavy/lazy ontology translated into Pair Access}
\to
\text{critical KEEP-cycle decomposition}
\to
\text{causal multiscale transfer calculus}
\to
\text{bounded DELETE injection + synchronous KEEP repayment}
\to
\text{constant-factor Pair Access}
\to
\text{approximate monotonicity}
\to
\text{dynamic optimality}
}
```

The primary negative chain is:

```math
\boxed{
\text{critical KEEP motif}
\to
\text{scale-inflatable legal paired execution}
\to
\text{required ratio grows with parameter}
\to
\text{closed-form }(T_k,X_k,Y_k)
\to
\frac{\operatorname{Splay}(Y_k,T_k)}{\operatorname{Splay}(X_k,T_k)}\to\infty
\to
\text{approximate monotonicity fails}
}
```

No weaker negative signal is enough.

The experiment is allowed to end at any of these levels:

```text
- exact literature-to-Pair-Access ontology translation only;
- exact critical KEEP-cycle structural decomposition;
- exact proof that a proposed raw-gap / boundary law is false;
- exact finite multiscale transfer calculus with obstruction witnesses;
- a fresh-holdout-surviving transfer calculus;
- a universal bounded-injection theorem;
- a universal synchronous-KEEP transfer theorem;
- a universal constant-factor Pair-Access theorem;
- approximate monotonicity;
- dynamic optimality;
- an explicit unbounded negative Splay family;
- resource-limited / representation-inconclusive result.
```

The experiment fails open to new mathematics and fails closed to theorem claims.

---

# 1. Scientific scope and central question

## 1.1 Primary scientific question

The central question is:

```math
\boxed{
\text{Can the }\widetilde O(\log\log n)\text{ heavy-path/lazy-gap analysis be specialized to}
\text{ a comparator that is itself Splay with extra accesses so that the remaining loss becomes }O(1)?
}
```

The comparator specialization is the Pair-Access setting:

- execution `A` processes the full sequence `X`;
- execution `B` processes a retained subsequence `Y\preceq X`;
- KEEP splays the same key in both;
- DELETE splays the key only in `A`.

The existing 2026 result proves a sublogarithmic competitive ratio for ordinary Splay against an almost-optimal changing reference tree. v0.3 does **not** assume that proof becomes stronger when the reference is Splay. It asks whether the special synchronous geometry supplies exactly the missing constant-factor structure.

## 1.2 Why the level changes

The previous experiments jointly rule out or weaken several tempting strategies:

```text
- simple static linear feature potentials;
- global additive disagreement counts;
- bounded local disagreement counters;
- tiny target-independent pair-state quotients;
- pure difference-only state descriptions;
- simple recency-violation accounting;
- three explicit v0.2 universal debt candidates at b_H=2.
```

The failures are two-sided:

```text
GLOBAL / MAGNITUDE-RICH:
  can be created too cheaply under DELETE;

LOCAL / BOUNDED:
  often cannot repay expensive KEEP;
```

This is the multiscale gap v0.3 attacks.

## 1.3 The critical KEEP-cycle clue

The v0.1 certified finite critical geometry is imported as evidence, not assumed universally:

```text
n >= 4 certified finite optimum: cyclic criticality;
forced critical derivatives: KEEP-only;
forced states: diagonal only;
FPATH contribution disappears in the certified n>=4 critical geometry;
cycle shapes vary with n while the bottleneck remains cyclic and KEEP-dominated.
```

The experiment therefore treats DELETE primarily as a candidate **injection** mechanism and synchronous KEEP dynamics as the candidate **transport/repayment** mechanism.

Hard rule:

```text
KEEP-dominance is a finite certified clue, not a theorem about all n.
```

## 1.4 Primary theorem form

The preferred proof form is a nonnegative energy `E_t=E(\mathcal L_t)` and a universal constant `C<\infty` satisfying blockwise inequalities.

For an A-only DELETE block `D`:

```math
E_{\rm after}-E_{\rm before}
\le
C\,\operatorname{cost}_A(D).
```

For a synchronous KEEP block `K`:

```math
\operatorname{cost}_B(K)
+
E_{\rm after}-E_{\rm before}
\le
C\,\operatorname{cost}_A(K).
```

Summing blocks yields:

```math
\operatorname{Splay}(Y,T)+E_m-E_0
\le
C\operatorname{Splay}(X,T).
```

With

```math
E_0=0,\qquad E_m\ge0,
```

this yields approximate monotonicity.

The theorem may instead be stated at single-access or single-rotation granularity if the proof is cleaner. Block-level amortization is permitted only when the block partition is deterministic and every real paired execution is covered exactly once.

## 1.5 Constant policy

`b=2` remains a diagnostic microscope because it connects directly to the exact v0.1/v0.2 Bellman and critical-cycle data.

Hard rule:

```text
b=2 is not the final theorem objective.
```

The final proof may return any universal finite constant `C`.

The preregistered diagnostic constant ladder is:

```text
2, 3, 4, 6, 8, 12, 16, 24, 32, 64
```

This ladder is used only to understand how transfer grammars fail or become feasible. A final theorem constant must come from the proof, not from selecting the smallest value that survived finite data.

## 1.6 Non-goals

v0.3 does not claim:

```text
- that the 2026 heavy-path/lazy-interval proof can be reused unchanged;
- that raw gaps admit a constant-factor bound;
- that the KEEP path is all-heavy under any unverified transplanted rank definition;
- that critical KEEP cycles remain the unique obstruction for all n;
- that a transfer grammar found by SAT/ILP is a theorem;
- that a signed transfer system is legitimate before a global lower bound is proved;
- that H1/H2R/H3T survival is a theorem;
- that a fitted constant from the diagnostic ladder is universal;
- that failure of the raw-gap branch disproves Pair Access;
- that failure of the signed-transfer branch disproves Pair Access;
- that an unbounded transfer residual implies an unbounded actual Splay ratio;
- that the 2026 result is a logical premise of Dynamic Optimality;
- that a literature-inspired object retains its source-paper theorem semantics after Pair-Access transplantation.
```

---

# 2. Parent lineage and immutable inherited evidence

## 2.1 Primary parent

The primary parent is:

```text
experiment_id: SPLAY-AM-BD-v0.2
repository: Dynamic-Optimality-Lab/splay-bellman-debt
sealed_commit: TO_BE_PINNED_AFTER_WP6
terminal_claim: TO_BE_READ_FROM_PARENT_FINAL_RESULT
```

v0.3 implementation may not begin Phase 01 scientific execution until v0.2 WP-6 has produced its deterministic final seal and the exact full parent commit is pinned.

The current pre-seal lineage expected to be present in the parent history includes:

```text
WP-1 foundation seal: b444f6a
WP-2 semantic seal:   08dc1a7
WP-3 semantic seal:   19245ab
WP-4 semantic seal:   f131b14
WP-5 gated pass:      29de3df
```

These hashes are navigation aids only. The authoritative parent is the final v0.2 seal commit recorded in parent artifacts.

## 2.2 Secondary ancestor

```text
experiment_id: SPLAY-AM-PD-v0.1
repository: Dynamic-Optimality-Lab/splay-pair-dynamics
sealed_commit: 6de1ca2a595e8895f54794f3a211fe6ee1a95a80
terminal_claim: FINITE_EXACT_BN_RESULTS
```

The v0.1 seal remains immutable and may be imported either directly by hash or through v0.2's certified parent-import chain.

## 2.3 Expected certified parent facts

The following expected facts must be independently verified against the final parent seals before receiving `CERTIFIED_PARENT_FACT` status in v0.3.

Reachable pair counts:

```text
n=2:       4
n=3:      19
n=4:     196
n=5:    1764
n=6:   17424
n=7:  184041
```

Exact finite subsequence overheads:

```math
b_2^*=1,\quad
b_3^*=1,\quad
b_4^*=\frac32,\quad
b_5^*=\frac85,\quad
b_6^*=\frac85,\quad
b_7^*=\frac{23}{14}.
```

Parent Bellman anchor summary:

```text
n                 2   3   4    5     6      7
max U_2           4  10  22   38    44     58
max V_2           0   1   2    3     5      6
forced states     2   5  14   42   132    429
```

Critical-geometry facts expected from v0.1:

```text
- n>=4 optimum classified CYCLIC on certified finite sizes;
- critical forced derivatives arise from FCYCLE on certified n>=4;
- forced critical edges on certified n>=4 are KEEP edges;
- diagonal states are the pointwise forced states;
- original FF-v0.1 linear feature language becomes algebraically inconsistent across sizes;
- expanded local/nonlinear feature families remain inconsistent on the certified witness system.
```

v0.2 facts expected for import:

```text
- BD0-02/03 Bellman future-regret / past-slack semantics REVIEWED;
- BD0-04/05 transport theorems REVIEWED;
- BD0-06/07 augmented recency semantics REVIEWED;
- BD0-13 pair-corridor scope theorem REVIEWED;
- BD0-15 same-(A,B) recency-V blindness REVIEWED;
- exact behavioral quotient: KERNEL_NO_COMPRESSION on certified development domains;
- pure-difference K0 transition-insufficiency diagonal witnesses preserved;
- augmented reachable-state counts n=2,3,4: 20,235,8764; n=5 stretch: 496264;
- zero V-spread on same-(A,B) augmented fibers where certified;
- D1-D7 recency/debt atom families inconsistent on the certified development search;
- D5 repayment screen near-miss 3318/3334 preserved with all exact failures;
- PHI-0001 rejected by DELETE blowup;
- PHI-0002 rejected by KEEP underpayment;
- PHI-0003 rejected by KEEP underpayment;
- no v0.2 candidate survived development to fresh holdout consumption;
- H1 remained EMPTY/unread through the stated parent gate;
- H2R remained BANK_COMMITTED with unlock_count=0 through the stated parent gate.
```

The v0.3 importer must use the final sealed parent artifacts rather than these prose values.

## 2.4 Parent facts are evidence, never editable inputs

v0.3 may:

```text
- verify parent hashes;
- deserialize certified state/cycle/specimen tables;
- reproduce selected parent calculations independently;
- derive new rotation-level traces from certified parent states;
- cite preserved parent counterexamples;
- import H1/H2R firewall metadata;
- create new v0.3 artifacts with explicit parent provenance.
```

v0.3 may not:

```text
- rewrite v0.1/v0.2 artifacts;
- relabel a parent failure as a v0.3 success;
- regenerate a parent holdout and call it the same bank;
- edit parent theorem status;
- repair parent output in place;
- silently substitute a recomputed object for the sealed parent object.
```

Any mismatch emits:

```text
PARENT_SEAL_MISMATCH
```

and blocks theorem-facing v0.3 execution.

## 2.5 Holdout inheritance

### n8

`n=8` remains permanently:

```text
PARTIALLY_REVEALED_CANARY_CONTAMINATED
```

and may only be used after a transfer calculus is frozen as:

```text
CONTAMINATED_EXHAUSTIVE_VALIDATION
```

### H1

H1 remains a fresh state-pair holdout only if Phase 00 verifies the final parent state:

```text
firewall_state == EMPTY
unlock_record == null
commitment matches parent seal
no v0.3 discovery read occurred
```

H1 may validate a state-only energy or transition law that can be evaluated from its stored pair state and legal transition schema. It cannot validate causal provenance requiring history absent from H1.

### H2R

H2R remains fresh only if Phase 00 verifies:

```text
firewall_state == BANK_COMMITTED
unlock_count == 0
bank commitments match parent seal
replay histories exist and are hash-bound
no v0.3 discovery namespace has read bank membership/history
```

H2R is eligible for causal/history-ledger validation because the bank contains replayable legal histories.

### New transfer holdout H3T

v0.3 additionally preregisters a new transfer-specific holdout `HOLDOUT-H3T-v0.3`, generated and committed before transfer-rule synthesis. Its exact contract is defined in Section 14 and Phase 08.

---

# 3. Frozen literature sources

v0.3 freezes exact source versions before any literature object becomes executable code.

Required source set:

```text
L0a  SPLAY-AM-PD-v0.1 sealed release
L0b  SPLAY-AM-BD-v0.2 final sealed release

L1   Sleator & Tarjan
     Self-Adjusting Binary Search Trees
     JACM 1985

L2   Levy & Tarjan
     A New Path from Splay to Dynamic Optimality
     SODA 2019
     DOI 10.1137/1.9781611975482.80

L3   Levy & Tarjan
     A Foundation for Proving Splay is Dynamically Optimal
     arXiv:1907.06310

L4   Russo
     A study on splay trees
     Theoretical Computer Science 776 (2019), 1-18
     DOI 10.1016/j.tcs.2018.12.020

L5   Chalermsook & Jiamjitrak
     New Binary Search Tree Bounds via Geometric Inversions
     ESA 2020
     DOI 10.4230/LIPIcs.ESA.2020.28

L6   Chmel, Haeupler, Hladik, Koucky, Roeyskoe, Rozhon, Sladky, Tarjan
     Splay trees are almost dynamically optimal
     arXiv:2607.18498, exact frozen version
```

For each source store:

```text
source_id
canonical citation
exact version/date
freeze_method: LOCAL_BYTES | PARENT_INHERITED_BYTES | BIBLIOGRAPHIC_IDENTITY
retrieval location
retrieval UTC timestamp
local SHA-256 where applicable
sections/definitions/lemmas actually relied upon
logical role: PREMISE | TRANSLATION_TARGET | CONTEXT | FEATURE_INSPIRATION
```

Roles:

```text
L1: PREMISE for ordinary Splay semantics/context only after convention match
L2/L3: PREMISE only for the subsequence/approximate-monotonicity bridge after audit
L4: CONTEXT / independent regular-access route
L5: FEATURE_INSPIRATION unless explicit Pair-Access equivalence is proved
L6: TRANSLATION_TARGET for heavy paths, heap view, lazy intervals, gaps, pairings, bends, and current-frontier loss accounting
```

Hard rule:

```text
A source-paper theorem never survives transplantation merely because a data structure has the same English name.
```

Every L6/L5-derived Pair-Access object receives a `PA_` or `MST_` identifier until formal equivalence is proved.

---

# 4. Frozen Pair-Access and Splay contract

This section inherits the exact parent definitions and is authoritative.

Key universe:

```math
[n]=\{1,\dots,n\}.
```

Cost:

```math
c(T,x)=\operatorname{depth}_T(x)+1,
```

root depth 0.

Ordinary bottom-up Splay is inherited exactly from the parent implementation and theorem notes.

For pair state

```math
s=(A,B)
```

and key `x`:

KEEP:

```math
K_x(A,B)=(S_xA,S_xB),
\qquad a=c(A,x),\qquad y=c(B,x).
```

DELETE:

```math
D_x(A,B)=(S_xA,B),
\qquad a=c(A,x),\qquad y=0.
```

For diagnostic constant `b`:

```math
w_b(e)=y(e)-b\,a(e),
\qquad
\ell_b(e)=b\,a(e)-y(e).
```

All path/sequence correspondence, diagonal starts, exact subsequence semantics, reachable-domain definitions, canonical state IDs, tree encodings, and exact arithmetic conventions are inherited by hash.

No v0.3 code may redefine them.

---

# 5. Rotation-level execution contract

v0.3 refines every Pair-Access edge into an exact rotation trace.

## 5.1 Primitive Splay cases

Every Splay operation is decomposed into the frozen ordinary bottom-up cases:

```text
ROOT / no rotation
ZIG
LL zig-zig
RR zig-zig
LR zig-zag
RL zig-zag
```

Each primitive rotation event records the exact local tree neighborhood before/after, affected key interval, parent/child orientation, search-path position, and cumulative access-step identity.

## 5.2 KEEP evaluation order

To compare a KEEP against a reference structure, v0.3 uses an explicit analysis order:

```text
1. observe pre-KEEP pair (A_0,B_0);
2. execute the A splay of x, obtaining A_1=S_x(A_0);
3. freeze A_1 as the reference snapshot for the B-splay analysis of this KEEP;
4. execute B's splay of x rotation by rotation against that frozen reference snapshot unless a later theorem explicitly requires synchronized reference updates inside the B splay;
5. record final pair (A_1,B_1).
```

This is an **analysis convention**, not a change to the actual paired execution.

Any alternative convention creates a new theorem version and must prove equivalence or explicitly separate results.

## 5.3 DELETE evaluation order

DELETE executes `A -> S_xA` while `B` is unchanged. Every A rotation is exposed as a candidate injection event into the discrepancy ledger.

## 5.4 Block partition

Every real paired execution can be represented as an alternating sequence of maximal blocks:

```text
A-only restructuring blocks induced by DELETE positions;
synchronous KEEP blocks consisting of one or more retained accesses.
```

A theorem may instead charge per access or per rotation. If blocks are used, the partition must be deterministic from `(X,Y)` and must neither omit nor double-count any access or rotation.

## 5.5 Rotation-trace identity

Canonical rotation event identity:

```text
(parent Pair-Access edge ID,
 execution side A|B,
 local rotation index,
 local Splay case,
 canonical involved-key tuple).
```

The trace serializer is versioned and independently reimplemented.

---

# 6. Pair-Access translation of the 2026 ontology

No object in this section is theorem-facing until its translation obligation is REVIEWED.

## 6.1 Reference-rank adapter

The exact L6 rank definition used by the 2026 proof is copied into a formal mapping note. v0.3 then defines a Pair-Access counterpart:

```text
PA_REFERENCE_RANK-v0.3
```

with the reference tree explicitly identified as the post-A-splay snapshot for KEEP analysis or the appropriate A snapshot for DELETE/reference-update analysis.

If the exact L6 rank is not literally tree depth, v0.3 must **not** replace it by depth merely because a heuristic derivation looks convenient.

## 6.2 Heavy edges and heavy paths

Define:

```text
PA_HEAVY_EDGE
PA_HEAVY_PATH
PA_LIGHT_EDGE
```

by exact translation from the frozen L6 definitions.

All tie/uniqueness assumptions are proved or represented explicitly.

## 6.3 Heap view

Define a Pair-Access heap view of the heavy paths only after the heavy-path translation is certified:

```text
PA_HEAP_PARENT
PA_HEAP_CHILD_LEFT
PA_HEAP_CHILD_RIGHT
PA_HEAP_VIEW
```

## 6.4 Gaps

Raw Pair-Access gap objects receive separate names:

```text
PA_RAW_GAP
PA_INTERVAL_GAP
PA_POINT_GAP
```

A source-paper `gap` theorem cannot be cited for these objects until equivalence is formally proved.

## 6.5 Lazy intervals

Translate:

```text
PA_LAZY_INTERVAL
PA_GROWING_INTERVAL
PA_SHRINKING_INTERVAL
PA_BROKEN_INTERVAL
```

including exact ordering, ownership, interval-contiguity, and update rules.

## 6.6 Pairings

Translate / define Pair-Access versions of:

```text
PA_INTERNAL_PAIRING
PA_BOUNDARY_PAIRING
PA_GOOD_PAIRING
PA_BAD_PAIRING
PA_IMPORTANT_BOUNDARY_PAIRING
PA_UNIMPORTANT_BOUNDARY_PAIRING
```

No `good`/`bad` label is reused until the source criterion is exactly mapped.

## 6.7 Bends

Translate the heavy-path bend object as:

```text
PA_BEND
```

and instrument creation/destruction under every B zig-zag and every A reference-tree rotation.

## 6.8 Contracted gaps

The L6 logarithmically contracted point-gap quantity is implemented as:

```text
PA_CONTRACTED_POINT_GAP_L6
```

for **baseline reproduction only**.

The primary v0.3 target is not to rediscover this contraction. The experiment asks whether the special Splay-vs-Splay reference dynamics admit a stronger raw or signed-transfer law.

## 6.9 Paid/free lazy-interval operations

Translate the exact L6 operation vocabulary into versioned Pair-Access diagnostic operations:

```text
PAIR_UP
DELETE_INTERVAL_MEMBER
INSERT_INTERVAL_MEMBER
SPLIT_INTERVAL
CONVERT_INTERVAL
TRANSFER_INTERVAL
HEAP_CHILD_EXCHANGE
```

Every operation records whether the source proof treats it as paid/free and whether that classification remains valid under the Pair-Access transplant.

## 6.10 Translation freeze

All translation definitions are frozen into:

```text
prereg/l6_translation_v0.3.yaml
math/L6_PAIR_ACCESS_MAPPING.md
```

before any critical-cycle target values are joined.

---

# 7. Crown theorem ledger

Create `math/proof_status.json` before theorem-dependent shortcuts.

Required obligations:

```text
MST0-01  v0.1/v0.2 sealed-parent import preserves exact logical content
MST0-02  rotation trace refines each Pair-Access edge without changing its cost or successor
MST0-03  Pair-Access L6 translation is definitionally correct for every imported source object used theorem-facing
MST0-04  KEEP reference-snapshot convention is legitimate for the intended amortized comparison
MST0-05  KEEP heavy-path lemma: under the certified translated rank semantics, characterize exactly which B access-path edges are heavy after the A splay
MST0-06  B zig-zig rotations admit the claimed pairing decomposition under the translated Pair-Access ontology
MST0-07  B zig-zag rotations admit the claimed bend accounting under the translated Pair-Access ontology
MST0-08  one A reference-tree rotation changes the translated heavy/lazy structure through only the claimed bounded primitive modifications
MST0-09  raw boundary-damage law, if promoted, has an arbitrary-n proof with universal constant
MST0-10  causal ledger update is a deterministic function of the legal paired execution and declared provenance state
MST0-11  transfer grammar preserves a globally defined ledger state under every primitive rotation
MST0-12  signed credits, if used, admit a universal lower bound / nonnegative integrated energy
MST0-13  bounded DELETE injection theorem
MST0-14  synchronous KEEP repayment / transfer theorem
MST0-15  local transfer calculus is integrable into a valid execution energy or directly telescopes without hidden path dependence
MST0-16  block partition covers every real paired execution exactly once
MST0-17  universal block inequalities imply constant-factor Pair Access
MST0-18  Pair Access telescopes to approximate monotonicity under the frozen cost convention
MST0-19  Levy-Tarjan bridge matches Splay variant, cost, initial-tree, subsequence, additive-term, and direction conventions
MST0-20  fixed-b / finite-cycle failure does not imply unbounded subsequence overhead
MST0-21  an unbounded critical-cycle motif implies a negative result only after a closed-form diagonal-rooted real Splay family is proved
MST0-22  theorem constant C is independent of n, sequence length, tree, holdout, and fitted finite panel
MST0-23  finite transfer-grammar feasibility does not imply universal integrability
MST0-24  raw-gap branch failure does not imply signed-transfer branch failure
MST0-25  legacy H1/H2R and new H3T are interpreted only within their declared schemas
MST0-26  current-frontier L6 theorem is context/baseline unless an explicit reduction makes a source lemma a premise
```

Status namespace:

```text
UNPROVED
PROVED
REVIEWED
BLOCKED
NOT_APPLICABLE
```

Lifecycle:

```text
UNPROVED -> PROVED -> REVIEWED
```

A theorem may be `BLOCKED` by an unmet prerequisite but never silently consumed.

No theorem-dependent implementation shortcut may consume an `UNPROVED` obligation.

---
# 8. Exact event ontology v0.3

The v0.3 ontology is **event-first**. State features are permitted only insofar as they support an exact local transfer law.

## 8.1 Primitive event families

Every rotation-level event records:

```text
Pair-Access mode: KEEP | DELETE
execution side: A | B
access key x
Splay case: ROOT | ZIG | LL | RR | LR | RL
rotation index within access
pre/post local parent-child-grandparent tuple
pre/post subtree intervals of involved nodes
pre/post subtree sizes
pre/post depths
pre/post translated reference ranks
pre/post heavy/light status of affected edges
pre/post heavy-path IDs
pre/post heap-parent relations
pre/post PA_RAW_GAP / interval gap / point gap
pre/post lazy-interval membership and owner
pre/post bend status
pre/post geometric-inversion-inspired records where defined
```

Raw records are preserved; summaries never replace them.

## 8.2 Regret attribution

For each Pair-Access KEEP edge, define exact access regret at diagnostic constant `b`:

```math
w_b=c(B,x)-b\,c(A,x).
```

The Pair-Access edge regret is not arbitrarily assigned to one B rotation.

v0.3 stores three separate attribution layers:

```text
EDGE_REGRET: authoritative Pair-Access quantity;
ROTATION_CONTEXT: exact structural events occurring during the edge;
DISCOVERY_ATTRIBUTION: optional theorem-mining allocation of edge regret to primitive events.
```

Only `EDGE_REGRET` is mathematically inherited. A discovered per-rotation allocation must be separately proved before it becomes theorem-facing.

## 8.3 Zig class decomposition

For every KEEP edge preserve:

```text
#ZIG
#LL
#RR
#LR
#RL
#zig-zig total
#zig-zag total
access-path length A
access-path length B
positive regret at each diagnostic C
```

Critical-cycle analysis must be stratified by these classes.

## 8.4 Scale coordinates

The primary exact scale coordinate is discrete and integer-valued.

Allowed initial scale systems:

```text
S0 subtree-size dyadic scale: floor(log2 size)
S1 depth dyadic scale
S2 raw-gap integer scale
S3 source-L6 contracted-gap level, baseline only
S4 interval-span dyadic scale
S5 rank-difference bucket only if rank translation is exact
```

Any logarithmic scale stored theorem-facing uses integer bucket definitions or exact symbolic expressions.

## 8.5 Causal provenance tags

Every candidate ledger credit may carry a provenance tag from a frozen finite alphabet:

```text
A_ROTATION_CREATED
A_ROTATION_MOVED
B_ZIGZIG_TRANSFERRED
B_ZIGZAG_EXPOSED
BOUNDARY_INSERT_CREATED
BOUNDARY_PAIRING_MOVED
INTERVAL_SPLIT_REDISTRIBUTED
INTERVAL_TRANSFER_MOVED
HEAP_CHILD_EXCHANGE_MOVED
CANCELLED
PAID_REGRET
```

These tags are semantic bookkeeping, not historical timestamps.

A provenance tag may name the **type** of generating event and its current structural support, but theorem-facing formulas may not depend on an unbounded event ID or raw time index.

## 8.6 Active versus latent credit

v0.3 explicitly distinguishes:

```text
LATENT credit: exists in ledger but is not eligible to pay the current KEEP regret;
ACTIVE credit: eligible under a frozen local predicate to pay the current KEEP regret;
SPENT credit: discharged and removed;
TRANSFERRED credit: conserved but changes structural support/scale/type.
```

The active predicate must be structural and local-to-declared-support. It may not query future accesses, Bellman values, or holdout labels.

## 8.7 Signed transfers

Signed intermediate ledger components are allowed in the **SIGNED_TRANSFER** branch, but only if:

```text
- every signed component has a precise support;
- cancellation rules are local and deterministic;
- the integrated execution energy has a proved universal lower bound;
- the final Pair-Access telescope cannot hide arbitrarily negative terminal energy.
```

Until MST0-12 is REVIEWED, signed-transfer results are discovery-only.

---

# 9. Critical KEEP-cycle corpus

## 9.1 Purpose

The critical cycle corpus is the highest-priority exact laboratory because potential differences cancel around a cycle, so every full-cycle accounting law must expose its true conservation structure.

## 9.2 Imported corpus

Import every certified v0.1 critical FCYCLE / zero-slack cycle for `n=4..7`, together with:

```text
source pair states
ordered KEEP keys
edge costs a,y
cycle ratio / certified b_n^*
forced edge derivatives
parent certificate hashes
```

If v0.1 contains multiple critical cycles, preserve all of them. Do not select only visually convenient representatives.

## 9.3 Near-critical corpus

In addition to exact critical cycles, define a preregistered near-critical set without adaptive thresholding.

At diagnostic `b=2`, include cycles or closed walks satisfying one of:

```text
A. top-K exact ratio per n, K preregistered before inspection;
B. scaled total slack in the preregistered finite set {0,1,2};
C. parent-labelled critical motifs from v0.1, regardless of v0.3 ontology.
```

Recommended default:

```text
K = 128 per n where available.
```

## 9.4 Rotation expansion

Expand every KEEP edge of every critical/near-critical cycle into the full A-then-B rotation trace under Section 5.

Preserve:

```text
cycle ID
edge index
A trace
reference snapshot
B trace
translated L6 event stream
ledger placeholder stream
```

## 9.5 Cycle conservation tables

For every declared primitive quantity `F`, compute exact full-cycle circulation:

```math
\sum_{e\in\Gamma}\Delta F(e).
```

For genuine state functions this must be zero. For event counters it need not be.

For every proposed ledger component, distinguish:

```text
STATE_DERIVATIVE     full-cycle net zero required;
FLOW_COUNT           nonzero circulation allowed;
SOURCE_SINK_ACCOUNT  circulation balanced only after explicit injection/payment terms.
```

## 9.6 KEEP-cycle localization questions

Every critical cycle report asks:

```text
Which Splay case carries positive regret?
Which translated pairing classes occur on those edges?
Which boundary interactions coincide with regret?
Which scales are entered/exited?
Which bends are destroyed/created?
Which raw point gaps increase/decrease?
Which A-reference rotations in the diagonal-rooted prefix originally created the relevant support?
Does the same structural packet circulate repeatedly around the cycle?
Can regret be paid by a conserved transfer with zero full-cycle net creation?
```

No narrative answer becomes a theorem without an exact predicate.

---

# 10. Causal discrepancy ledger contract

## 10.1 Ledger state

A theorem-facing ledger is a finite multiset or finitely supported integer/rational measure:

```math
\mathcal L(z)=\{(\tau_i,\sigma_i,\omega_i,m_i)\}_i
```

where:

```text
tau_i    credit type from a frozen finite alphabet
sigma_i  exact structural support descriptor
omega_i  exact scale descriptor
m_i      integer/rational multiplicity or mass
```

The representation must have an arbitrary-`n` mathematical definition.

## 10.2 Support descriptor

Permitted support primitives include:

```text
key
ordered key interval [l,r]
translated heavy path identified structurally
heap-parent/heap-child relation
lazy interval identified by owner + side + structural member interval
boundary between adjacent structural objects
bend location
orientation LEFT|RIGHT|MIXED
```

Forbidden theorem-facing support:

```text
BFS state ID
raw memory address
finite-table index
cycle ID
holdout membership
absolute event timestamp
future key
Bellman value
```

## 10.3 Causal creation

Credits may be created only by an explicitly declared source event.

Primary source candidates:

```text
A-only Splay rotation under DELETE;
A-side Splay rotation before the B side of KEEP, if the analysis convention treats the reference update itself as an injection/transfer event;
translated paid lazy-interval operations whose Pair-Access cost source is explicitly identified.
```

A theorem cannot charge an arbitrary structural difference as newly created debt without identifying the cost-bearing event that funds it.

## 10.4 Transfer

A transfer replaces a finite local packet of ledger entries by another packet with a proved relation on integrated energy.

Canonical notation:

```math
\mathsf T:
\{q_1,\ldots,q_r\}
\longrightarrow
\{q'_1,\ldots,q'_s\}.
```

Each transfer rule declares:

```text
precondition
triggering primitive event
input packet
output packet
energy change
regret paid, if any
source cost charged, if any
scale movement
symmetry/relabel behavior
```

## 10.5 Cancellation

Cancellation is explicit:

```math
q^{+}+q^{-}\to\varnothing
```

or another frozen local rule.

No global "these terms cancel" statement is permitted without a finite local cancellation lemma or a telescoping identity.

## 10.6 Integrated energy

A ledger may induce energy

```math
E(\mathcal L)=\sum_{q\in\mathcal L} e(q)
```

or a bounded nonlinear aggregate, provided:

```text
- e(q) is n-independent in form;
- total energy is well-defined for every legal ledger;
- initial synchronized ledger has known energy, preferably 0;
- global lower bound is proved;
- local transfer inequalities imply the desired block inequality.
```

A ledger may also support a direct flow proof without a scalar energy if the flow theorem itself telescopes exactly across the execution. Such a proof requires MST0-15.

---

# 11. Transfer grammar v0.3

## 11.1 Philosophy

The discovery problem is not unrestricted symbolic regression.

The grammar describes a finite alphabet of **local conservation laws** suggested jointly by:

```text
- exact critical KEEP cycles;
- the L6 heavy-path/lazy-interval machinery;
- v0.1 global/local scale mismatch;
- v0.2 DELETE-creation / KEEP-repayment failures;
- geometric-inversion-style relational accounting.
```

## 11.2 Primitive rule templates

Preregister the following rule templates before target-guided synthesis.

### T1: scale-preserving move

```text
(type, support, scale j) -> (type, support', scale j)
```

### T2: upward scale transfer

```text
(type, support, j) -> bounded packet at j+1 plus local residue
```

### T3: downward scale split

```text
(type, support, j) -> bounded packet at j-1 / j
```

### T4: orientation flip

```text
LEFT credit <-> RIGHT credit
```

under an exact local Splay event.

### T5: boundary activation

```text
LATENT boundary credit -> ACTIVE boundary credit
```

when a declared B access-path condition becomes true.

### T6: repayment

```text
ACTIVE credits -> SPENT
```

with exact lower bound on paid positive KEEP regret.

### T7: A-rotation injection

```text
A rotation -> bounded packet of new latent credits
```

with total created energy bounded by a universal constant per rotation or per A access cost.

### T8: lazy-interval structural transfer

```text
credits follow Pair-up / Split / Convert / Transfer / Heap-child-exchange
```

with a theorem-facing mapping only after MST0-03/08.

### T9: signed cancellation

```text
positive and negative scale/orientation credits cancel locally
```

SIGNED_TRANSFER branch only.

### T10: bend discharge

```text
zig-zag destroys/changes bend-supported credit and pays designated regret class
```

only after MST0-07.

## 11.3 Rule complexity bounds

Every candidate rule:

```text
- inspects O(1) primitive structural objects around the triggering rotation, OR
- inspects one declared interval/heavy-path object with an exact aggregate stored in the ledger;
- creates O(1) output credit records per triggering primitive event unless a proved aggregate operation replaces many records;
- uses constants independent of n;
- is order-relabel invariant;
- contains no state/cycle/holdout lookup.
```

## 11.4 Grammar branches

Two preregistered branches exist.

### Branch A: RAW_BOUNDARY

Attempt a nonnegative raw-gap/boundary ledger with no logarithmic gap contraction.

Scientific target:

```math
\sum \text{harmful raw boundary damage}
\le
C\cdot \operatorname{cost}_A
```

under the special Splay-reference dynamics.

### Branch B: SIGNED_MULTISCALE

Activated only after an exact Branch-A obstruction is preserved.

Allows signed transfers and bounded scale redistribution, but requires a separate global lower-bound theorem.

Branch B is preregistered now; it is not an ad hoc post-failure invention.

## 11.5 Forbidden grammar escapes

Forbidden:

```text
arbitrary per-state potential lookup
arbitrary per-cycle rule
n-specific coefficient vector
unbounded-depth decision tree keyed by finite state serialization
Bellman U/V/G as rule inputs
future access information
holdout-derived predicates
free global cancellation
unbounded number of new credits per primitive event without a proved aggregate bound
```

---

# 12. Exact rule synthesis and solver policy

## 12.1 Solver roles

Permitted discovery engines:

```text
exact SAT
SMT over integers/rationals
integer linear programming
min-cost / circulation / flow formulations
exact rational linear programming with independently checkable certificates
finite-state dynamic programming
symbolic elimination
```

Heuristic search may propose grammar instantiations but cannot certify them.

## 12.2 Target-blind ontology, target-aware rule selection

Structural/event extraction is target-blind.

After hashes freeze, rule synthesis may read:

```text
exact Pair-Access regret
critical/near-critical labels
cycle membership
creation/repayment class
```

because the purpose is explicitly theorem discovery.

A rule definition itself may still not contain target values or IDs.

## 12.3 Discovery objective hierarchy

Rank candidate transfer systems lexicographically by:

```text
1. exact satisfaction of local conservation / payment inequalities;
2. exact satisfaction on all critical KEEP cycles;
3. exact bounded A-rotation injection;
4. exact repayment of positive KEEP regret;
5. cross-n survival;
6. cross-C diagnostic stability;
7. number of rule templates used;
8. number of credit types;
9. maximum local support radius / aggregate complexity;
10. expression simplicity.
```

No statistical fit outranks exact inequality coverage.

## 12.4 Minimal inconsistent subsystem

Every failed grammar family preserves an exact inclusion-minimal or solver-minimal inconsistent subsystem where computationally feasible.

Required fields:

```text
grammar version
rule types permitted
states/events involved
exact constraints
unsat certificate or independently checkable proof
smallest n under canonical search order
scientific interpretation
```

## 12.5 Solver certificate independence

A solver result is authoritative only if:

```text
SAT/feasible -> frozen assignment replayed by independent exact checker;
UNSAT/infeasible -> proof/certificate checked independently where solver supports it,
                     or reproduced by a second exact formulation / exhaustive witness on the claimed finite domain.
```

No commercial/opaque solver status string is sufficient by itself.

---

# 13. Raw boundary-damage constantification target

## 13.1 Primary Branch-A conjecture

The primary theorem-mining conjecture is deliberately stronger than the known contracted-gap analysis:

> In the Pair-Access specialization where the reference evolution is itself generated by Splay, the total harmful raw boundary interaction needed to analyze B can be charged to A with a universal constant, without logarithmic point-gap contraction.

The exact theorem statement is not frozen until the L6 translation is certified. The preregistered shape is:

```math
\sum_{t\in\text{execution}}
\operatorname{RawBoundaryDamage}(t)
\le
C_0\,\operatorname{Splay}(X,T)+O(n)
```

or a zero-initial variant without additive overhead if the ledger normalization permits it.

## 13.2 Damage must be defined exactly

`RawBoundaryDamage` may not mean "whatever quantity makes the inequality work."

It must be defined from frozen translated primitives such as:

```text
boundary pairing loser/winner
raw point-gap increase
paid insertion triggered by a boundary event
active interval boundary credit
other exact L6-translated event named before fitting
```

## 13.3 Strongest preferred form

Preferred:

```math
\operatorname{RawBoundaryDamage}(e)
\le
C_A\cdot \#\text{A rotations causally responsible for the active boundary packet}
+
\Delta E(e),
```

with bounded injection and telescoping `E`.

## 13.4 Branch-A failure

Branch A is rejected by one exact legal counterexample to the frozen local/global law.

Preserve:

```text
smallest counterexample
maximum finite violation on development
whether violation is transient or cyclic
whether motif inflates with scale
which L6 contraction would have hidden the failure
```

Do not immediately modify the definition under the same conjecture ID.

## 13.5 Relation to the 2026 bound

Reproducing the need for logarithmic contraction is a valid finite negative result about Branch A.

It is **not** evidence against Dynamic Optimality unless the underlying real Splay ratio can be made unbounded.

---

# 14. Holdout architecture

## 14.1 Philosophy

Fresh evidence is spent only after the transfer calculus is frozen.

v0.3 inherits two untouched banks and creates one new transfer-specific bank.

## 14.2 H1 legacy state-pair holdout

Use only for candidates evaluable from pair state / next transition.

Status required at v0.3 prereg:

```text
EMPTY
```

## 14.3 H2R legacy replay-history holdout

Use for causal/history-ledger candidates whose state can be reconstructed from replay history.

Status required:

```text
BANK_COMMITTED
unlock_count: 0
```

## 14.4 HOLDOUT-H3T-v0.3

Generate before any target-guided transfer-rule synthesis.

Recommended default sizes:

```text
n = 10, 12, 16, 24, 32, 48, 64
```

Episodes per size:

```text
10,000
```

Each episode stores a legal initial tree and paired KEEP/DELETE history sufficient to independently replay the complete rotation trace.

Target total:

```text
70,000 episodes
```

No fixed transition count is assumed because episode lengths are stratified.

Preregistered strata:

```text
RANDOM_LEGAL
DELETE_BURST_THEN_KEEP
ALTERNATING_KEEP_DELETE
SPINE_VS_BALANCED
OPPOSITE_SPINE
ZIGZIG_ENRICHED
ZIGZAG_ENRICHED
BOUNDARY_PAIRING_ENRICHED under target-blind structural generator
NESTED_INTERVAL_ENRICHED
MIRROR_PAIRED
MOTIF_BLIND_RANDOM_WALK (not seeded from post-freeze counterexamples)
```

Generation may use structural predicates from the frozen ontology, but may not use transfer-candidate residuals or future candidate definitions.

## 14.5 H3T commitment

Store:

```text
seed policy
generator source hash
per-size episode hashes
logical-stream hash
manifest
replay verifier hash
stratum counts
length distribution commitment
```

The bank itself is quarantined.

State machine:

```text
EMPTY
-> BANK_COMMITTED
-> TRANSFER_CALCULUS_FROZEN
-> UNLOCKED_ONCE
```

No backward transitions.

## 14.6 Validation order

For a frozen state-only candidate:

```text
1. development
2. n8 contaminated validation if applicable
3. H1 once if schema-compatible
4. H3T once
5. independent replay / adversarial search
```

For a frozen causal/history ledger:

```text
1. development
2. H2R once if schema-compatible
3. H3T once
4. independent replay / adversarial search
```

If multiple candidates survive development, freeze the entire candidate set before unlocking any fresh bank.

## 14.7 Post-reveal mutation

Any formula/rule/constant/active predicate/credit type changed after a fresh reveal receives a new ID and status:

```text
POST_HOLDOUT
```

It may not be called fresh-tested on that consumed bank.

---

# 15. Candidate transfer-calculus contract

A frozen theorem candidate is not just a scalar `Phi`.

Required metadata:

```text
calculus_id
parent_calculus
branch: RAW_BOUNDARY | SIGNED_MULTISCALE
ontology_version
L6_translation_version
credit_type_definitions
support_definitions
scale_definitions
active_predicate
injection_rules
transfer_rules
cancellation_rules
repayment_rules
integrated_energy_definition or direct-flow theorem statement
lower_bound_claim
universal_constant_C or symbolic proof-derived constant policy
initialization
proof_obligations
fresh_holdout eligibility
```

Eligibility:

```text
- arbitrary-n mathematical definition;
- no state/cycle/holdout IDs;
- no U/V/G lookup;
- no n-specific constants;
- no future information;
- order-preserving relabel invariance;
- exact tie semantics;
- deterministic update under every legal primitive event;
- finite support after every finite execution;
- explicit lower-bound route if signed;
- explicit theorem constant independent of finite n.
```

Changing any of:

```text
credit type
support
scale system
active predicate
coefficient
rule precondition
rule output
cancellation rule
constant C
initialization
reference-snapshot convention
```

creates a new calculus ID.

---

# 16. Exact arithmetic and numerical policy

## 16.1 Authoritative arithmetic

Use arbitrary-precision integers/rationals wherever definitions permit.

All pair costs, counts, scales, interval endpoints, subtree sizes, and integer transfer masses are exact.

## 16.2 Logarithmic source quantities

If source L6 definitions use logarithms or log-log contractions, preserve them symbolically or through certified exact/sign-safe representations.

Permitted authoritative methods:

```text
symbolic identities / inequalities
integer floor-log levels where definitionally correct
certified interval arithmetic with directed rounding
exact-real / proof-assistant libraries
monotonicity reductions to integer comparisons
```

If an interval straddles zero:

```text
SIGN_UNCERTIFIED
```

not PASS.

## 16.3 Optimization output

Floating-point LP/ILP relaxations may guide discovery but cannot certify a transfer law.

Every final coefficient / rule parameter is exact.

## 16.4 Statistical diagnostics

Permitted for visualization only:

```text
frequency plots
cluster diagrams
mutual information
regression diagnostics
embedding / dimensionality reduction
```

They may never define:

```text
transfer equivalence
criticality
counterexample sign
rule pass/fail
holdout verdict
claim level
```

---

# 17. Outcome taxonomy

Every phase emits a meaningful exact status.

Core statuses:

```text
PARENT_CHAIN_VERIFIED
PARENT_SEAL_MISMATCH

L6_TRANSLATION_FROZEN
L6_TRANSLATION_FAIL
L6_BASELINE_REPRODUCED
L6_BASELINE_TRANSLATION_INCOMPLETE

ROTATION_TRACE_CERTIFIED
ROTATION_TRACE_FAIL

CRITICAL_KEEP_CORPUS_CERTIFIED
CRITICAL_KEEP_CORPUS_FAIL
KEEP_REGRET_LOCALIZED
KEEP_REGRET_DISTRIBUTED

KEEP_HEAVY_LEMMA_PROVED
KEEP_HEAVY_LEMMA_FALSE_AS_STATED

CAUSAL_PROVENANCE_CERTIFIED
CAUSAL_PROVENANCE_INSUFFICIENT

RAW_BOUNDARY_LAW_SURVIVES_DEV
RAW_BOUNDARY_LAW_REJECTED
SIGNED_TRANSFER_NOT_ACTIVATED
SIGNED_TRANSFER_SURVIVES_DEV
SIGNED_TRANSFER_REJECTED

TRANSFER_GRAMMAR_FINITE_FEASIBLE
TRANSFER_GRAMMAR_FINITE_INFEASIBLE
TRANSFER_CALCULUS_FROZEN

CONTAMINATED_N8_VALIDATION_PASS
CONTAMINATED_N8_VALIDATION_FAIL
FRESH_H1_PASS
FRESH_H1_FAIL
FRESH_H2R_PASS
FRESH_H2R_FAIL
FRESH_H3T_PASS
FRESH_H3T_FAIL

INDEPENDENT_VERIFICATION_FAIL
COUNTEREXAMPLE_FOUND
NO_COUNTEREXAMPLE_FOUND

BOUNDED_DELETE_INJECTION_PROVED
SYNCHRONOUS_KEEP_TRANSFER_PROVED
UNIVERSAL_PAIR_ACCESS_LEMMA_PROVED
APPROXIMATE_MONOTONICITY_PROVED
DYNAMIC_OPTIMALITY_PROVED

NEGATIVE_FAMILY_NOT_ACTIVATED
NEGATIVE_CYCLE_FAMILY_CANDIDATE
NEGATIVE_REAL_SPLAY_FAMILY_PROVED
DYNAMIC_OPTIMALITY_DISPROVED

RESOURCE_LIMIT_NO_CLAIM
REPRESENTATION_INCONCLUSIVE
```

No generic `PASS` may replace the sealed scientific result status.

---
# 18. Repository layout

Recommended repository root:

```text
splay-multiscale-transfer/
|-- README.md
|-- IMPLEMENTATION_SPEC_v0.3.md
|-- WorkPlan.md
|-- Path.md
|-- CHANGELOG.md
|-- CITATIONS.md
|-- LICENSE
|-- pyproject.toml
|-- requirements-lock.txt
|-- .gitignore
|-- parent/
|   |-- V01_SEAL.json
|   |-- V02_SEAL.json
|   |-- V01_FINAL_RESULT.json
|   |-- V02_FINAL_RESULT.json
|   |-- V01_MANIFEST.sha256
|   |-- V02_MANIFEST.sha256
|   |-- V01_ARCHIVE.sha256
|   |-- V02_ARCHIVE.sha256
|   |-- V02_H1_FIREWALL.json
|   |-- V02_H2R_FIREWALL.json
|   |-- import_ledger.json
|   `-- BOOTSTRAP_MANIFEST.sha256
|-- prereg/
|   |-- experiment_v0.3.yaml
|   |-- parent_contract.yaml
|   |-- constant_policy.yaml
|   |-- l6_translation_v0.3.yaml
|   |-- event_ontology_v0.3.yaml
|   |-- transfer_grammar_v0.3.yaml
|   |-- cycle_corpus_policy.yaml
|   |-- holdouts.yaml
|   |-- theorem_gate_matrix.yaml
|   |-- threat_control_matrix.yaml
|   |-- stop_control_matrix.yaml
|   |-- discovery_splits.yaml
|   |-- allowed_claims.md
|   |-- forbidden_claims.md
|   `-- prereg_sha256.txt
|-- external/
|   |-- MANIFEST.json
|   `-- papers/
|       |-- L1_sleator_tarjan.pdf_or_identity
|       |-- L2_levy_tarjan_soda2019.pdf_or_identity
|       |-- L3_levy_tarjan_foundation.pdf
|       |-- L4_russo_regular_access.pdf_or_identity
|       |-- L5_geometric_inversions.pdf
|       |-- L6_chmel_et_al_2026.pdf
|       `-- SHA256SUMS
|-- math/
|   |-- definitions_v0.3.md
|   |-- L6_PAIR_ACCESS_MAPPING.md
|   |-- theorem_MST01_parent_transport.md
|   |-- theorem_MST02_rotation_refinement.md
|   |-- theorem_MST03_l6_translation.md
|   |-- theorem_MST04_keep_reference_snapshot.md
|   |-- theorem_MST05_keep_heavy_path.md
|   |-- theorem_MST06_zigzig_pairing.md
|   |-- theorem_MST07_zigzag_bends.md
|   |-- theorem_MST08_reference_rotation_locality.md
|   |-- theorem_MST09_raw_boundary.md
|   |-- theorem_MST10_ledger_determinism.md
|   |-- theorem_MST11_transfer_preservation.md
|   |-- theorem_MST12_signed_lower_bound.md
|   |-- theorem_MST13_delete_injection.md
|   |-- theorem_MST14_keep_repayment.md
|   |-- theorem_MST15_integrability.md
|   |-- theorem_MST16_block_partition.md
|   |-- theorem_MST17_pair_access.md
|   |-- theorem_MST18_telescoping.md
|   |-- theorem_MST19_bridge.md
|   |-- theorem_MST20_negative_guard.md
|   |-- theorem_MST21_negative_family.md
|   |-- theorem_MST22_constant_independence.md
|   |-- theorem_MST23_finite_integrability_guard.md
|   |-- theorem_MST24_branch_scope.md
|   |-- theorem_MST25_holdout_scope.md
|   |-- theorem_MST26_literature_scope.md
|   |-- proof_status.json
|   `-- latex/
|-- python/
|   |-- inherited/
|   |-- splay_ref/
|   |-- rotations/
|   |-- l6_translation/
|   |-- cycles/
|   |-- ontology/
|   |-- provenance/
|   |-- ledger/
|   |-- transfer/
|   |-- solver/
|   |-- holdout/
|   |-- audit/
|   `-- adversary/
|-- rust/
|   `-- optional_exact_acceleration/
|-- schemas/
|   |-- parent_import.schema.json
|   |-- rotation_event.schema.json
|   |-- l6_object.schema.json
|   |-- cycle_trace.schema.json
|   |-- provenance_packet.schema.json
|   |-- ledger_credit.schema.json
|   |-- transfer_rule.schema.json
|   |-- transfer_calculus.schema.json
|   |-- solver_certificate.schema.json
|   |-- holdout_commitment.schema.json
|   |-- counterexample.schema.json
|   |-- theorem_review.schema.json
|   `-- final_result_v0.3.schema.json
|-- tests/
|   |-- parent/
|   |-- rotations/
|   |-- translation/
|   |-- cycles/
|   |-- provenance/
|   |-- ledger/
|   |-- transfer/
|   |-- holdout/
|   |-- mutation/
|   |-- proof/
|   `-- seal/
|-- artifacts/v03/
|   |-- parent_import/
|   |-- rotations/
|   |-- translation/
|   |-- cycles/
|   |-- provenance/
|   |-- transfer_grammar/
|   |-- solver/
|   |-- hypotheses/
|   |-- holdouts/
|   |-- adversarial/
|   |-- proofs/
|   |-- audits/
|   |-- logs/
|   `-- seal/
`-- scripts/
    |-- run_phase00.sh
    |-- ...
    |-- run_phase19.sh
    `-- reproduce_all_v0.3.sh
```

Separation rules:

```text
- parent/ becomes read-only after one audited bootstrap import;
- L6 translation code may read frozen literature definitions, never Bellman targets;
- event ontology extraction may not read criticality/regret labels;
- rule synthesis may read development targets only after ontology hashes freeze;
- holdout banks may not import discovery modules;
- clean-room evaluator receives only frozen calculus + contracts + serialized legal histories;
- adversarial code may evaluate but never mutate a frozen calculus;
- proof code may use finite artifacts as examples/tests, never as logical premises.
```

---

# 19. Preregistration files

## 19.1 experiment_v0.3.yaml

Minimum:

```yaml
experiment_id: SPLAY-AM-MST-v0.3
parent:
  experiment_id: SPLAY-AM-BD-v0.2
  sealed_commit: TO_BE_PINNED_AFTER_V02_WP6
secondary_ancestor:
  experiment_id: SPLAY-AM-PD-v0.1
  sealed_commit: 6de1ca2a595e8895f54794f3a211fe6ee1a95a80
target_problem: Sleator-Tarjan dynamic optimality conjecture
bridge: Levy-Tarjan subsequence / approximate monotonicity
primary_discovery_object: multiscale_synchronous_discrepancy_ledger
primary_branch: RAW_BOUNDARY
fallback_branch: SIGNED_MULTISCALE
diagnostic_b: {p: 2, q: 1}
final_constant_policy: any_universal_finite_C
finite_evidence_is_theorem: false
```

## 19.2 constant_policy.yaml

```yaml
diagnostic_anchor:
  - {p: 2, q: 1, role: PARENT_GEOMETRY_MICROSCOPE}
diagnostic_ladder:
  - 2
  - 3
  - 4
  - 6
  - 8
  - 12
  - 16
  - 24
  - 32
  - 64
final_theorem:
  constant_must_be_universal: true
  smallest_finite_fit_is_not_theorem_constant: true
  proof_may_return_any_finite_constant: true
```

## 19.3 cycle_corpus_policy.yaml

Freeze:

```yaml
critical_sizes: [4,5,6,7]
import_all_parent_critical_cycles: true
near_critical:
  top_k_per_n: 128
  allowed_scaled_slack: [0,1,2]
canonical_order: [n, source_state_id, cycle_length, key_word_lex]
no_adaptive_thresholds: true
```

## 19.4 transfer_grammar_v0.3.yaml

Freeze:

```text
credit type schema
support schema
scale systems S0..S5
rule templates T1..T10
branch A permissions
branch B permissions
max primitive outputs per rule before aggregate proof
forbidden target inputs
solver objectives
complexity ordering
```

## 19.5 holdouts.yaml

Minimum:

```yaml
n8:
  status: PARTIALLY_REVEALED_CANARY_CONTAMINATED
  fresh: false

H1:
  inherited: true
  required_status: EMPTY
  eligible: STATE_PAIR_COMPATIBLE

H2R:
  inherited: true
  required_status: BANK_COMMITTED
  required_unlock_count: 0
  eligible: REPLAY_HISTORY_COMPATIBLE

H3T:
  inherited: false
  status_at_prereg: TO_BE_GENERATED_AND_QUARANTINED
  sizes: [10,12,16,24,32,48,64]
  episodes_per_size: 10000
  eligible: TRANSFER_CALCULUS
```

## 19.6 theorem_gate_matrix.yaml

For every MST0-01..26:

```text
owner phase
first consumer phase
required status before consumption
proof artifact
review artifact
controls
```

Multi-owner controls use arrays.

## 19.7 discovery_splits.yaml

Development evidence is frozen by **artifact class**, not by adaptively choosing easy examples.

Suggested:

```text
critical cycles n=4..6: selection
critical cycles n=7: internal validation
noncritical exact edges n=2..5: selection
noncritical exact edges n=6..7: validation
large generated legal histories: selection/validation masks frozen before target-guided solver search
```

All masks and seeds are frozen before transfer-rule synthesis.

---

# 20. Canonical data schemas

All sealed JSON:

```text
UTF-8, no BOM
sorted keys
canonical separators
newline termination
integer strings for arbitrary precision fields
explicit schema_version
```

## 20.1 Rotation event

```json
{
  "schema_version": "ROT-EVENT-v0.3",
  "n": 7,
  "pair_edge_id": "...",
  "mode": "KEEP",
  "side": "B",
  "access_key": 4,
  "rotation_index": 2,
  "splay_case": "LL",
  "keys_local": [1,3,4],
  "tree_before_hash": "...",
  "tree_after_hash": "...",
  "affected_interval": [1,4],
  "reference_snapshot_hash": "..."
}
```

## 20.2 Translated L6 object

```json
{
  "schema_version": "PA-L6-v0.3",
  "object_type": "PA_LAZY_INTERVAL",
  "reference_tree_hash": "...",
  "subject_tree_hash": "...",
  "owner_support": "...",
  "side": "LEFT",
  "member_supports": ["..."],
  "growing": false,
  "broken": false,
  "mapping_version": "L6MAP-v0.3.1"
}
```

## 20.3 Cycle trace

```json
{
  "schema_version": "MST-CYCLE-v0.3",
  "parent_source": "SPLAY-AM-PD-v0.1",
  "n": 7,
  "cycle_id": "...",
  "critical": true,
  "edge_count": 12,
  "all_modes_keep": true,
  "sum_cost_A": "...",
  "sum_cost_B": "...",
  "ratio": {"num":"23","den":"14"},
  "rotation_trace_sha256": "..."
}
```

## 20.4 Ledger credit

```json
{
  "schema_version": "MST-CREDIT-v0.3",
  "credit_type": "BOUNDARY_LATENT",
  "support": {
    "kind": "INTERVAL_BOUNDARY",
    "left": 3,
    "right": 8,
    "orientation": "LEFT"
  },
  "scale": {"system":"S0","level":3},
  "mass": {"num":"1","den":"1"},
  "provenance_class": "A_ROTATION_CREATED"
}
```

## 20.5 Transfer rule

```json
{
  "schema_version": "MST-RULE-v0.3",
  "rule_id": "TR-0007",
  "template": "T5_BOUNDARY_ACTIVATION",
  "branch": "RAW_BOUNDARY",
  "precondition_definition": "...",
  "trigger_event": "...",
  "input_credit_pattern": "...",
  "output_credit_pattern": "...",
  "energy_delta_bound": "...",
  "regret_payment_bound": "...",
  "n_specific": false
}
```

## 20.6 Transfer calculus

```json
{
  "schema_version": "MST-CALCULUS-v0.3",
  "calculus_id": "MSTC-0001",
  "branch": "RAW_BOUNDARY",
  "ontology_version": "MST-ONTOLOGY-v0.3",
  "mapping_version": "L6MAP-v0.3.1",
  "rule_ids": ["TR-0001","TR-0003","TR-0007"],
  "energy_definition": "...",
  "constant_policy": "PROOF_DERIVED",
  "fresh_holdout_status": "UNTOUCHED",
  "status": "DEV_FALSIFICATION_PENDING"
}
```

## 20.7 Counterexample

```json
{
  "schema_version": "MST-CEX-v0.3",
  "calculus_id": "MSTC-0001",
  "n": 16,
  "history_hash": "...",
  "pair_edge_index": 37,
  "rotation_index": 4,
  "failure_type": "KEEP_REPAYMENT",
  "exact_residual": {"num":"1","den":"2"},
  "smallest_under_order": true,
  "replay_sha256": "..."
}
```

---

# 21. Deterministic implementation order within every phase

Every phase follows:

```text
VERIFY PARENT / INPUT HASHES
  -> LOAD FROZEN v0.3 CONTRACT
    -> ASSERT THEOREM GATES
      -> ASSERT HOLDOUT FIREWALL
        -> COMPUTE
          -> ASSERT LOCAL INVARIANTS
            -> SAVE RAW APPEND-ONLY OUTPUT
              -> BUILD EXACT CERTIFICATE / WITNESS
                -> INDEPENDENT VERIFY
                  -> RUN MUTATION CONTROLS
                    -> WRITE SCIENTIFIC PHASE STATUS
                      -> COMMIT / PUSH
```

No failed run is deleted to make a later gate pass.

---

# 22. Twenty-phase implementation plan

# PHASE 00 - Freeze parent seals, literature, v0.3 contract, and theorem obligations

## Goal

Create a clean immutable boundary before any v0.3 scientific output exists.

## 00.1 Require final v0.2 seal

The v0.2 final seal must exist.

Pin:

```text
full sealed commit
FINAL_RESULT hash
manifest hash
archive hash
normative spec/amendment hashes
H1 firewall state
H2R firewall state
```

If v0.2 is not finally sealed:

```text
PARENT_NOT_FINAL
```

and Phase 01 scientific work is forbidden.

## 00.2 Bootstrap parent snapshot

One authorized transaction populates `parent/`, writes `BOOTSTRAP_MANIFEST.sha256`, then sets the v0.3 parent snapshot read-only.

Source parent repositories are immutable throughout.

## 00.3 Freeze literature

Freeze L0a/L0b/L1..L6 under Section 3 policy.

L6 exact version is especially important because v0.3 translates its definitions.

## 00.4 Freeze this specification

Write:

```text
IMPLEMENTATION_SPEC_v0.3.md
```

and hash the complete normative stack into `prereg/prereg_sha256.txt`.

## 00.5 Initialize theorem ledger

MST0-01..26 begin `UNPROVED` except any obligations legitimately inherited by explicit proof transport.

No theorem receives `REVIEWED` merely because an analogous v0.2 theorem exists.

## 00.6 Verify holdouts without reading contents

Required:

```text
H1 EMPTY
H2R BANK_COMMITTED / unlock_count 0
n8 contaminated
```

## 00.7 Freeze threat, stop, split, and claim matrices

Before new result inspection freeze all control matrices.

## Phase-00 gate

PASS only if:

```text
[ ] v0.2 final seal pinned
[ ] v0.1 chain verified
[ ] parent bootstrap locked
[ ] literature exact
[ ] spec/prereg hashes exact
[ ] theorem ledger exists
[ ] H1 pristine
[ ] H2R pristine
[ ] n8 contamination preserved
[ ] no v0.3 scientific output predates prereg hash
```

Failure:

```text
FOUNDATION_NOT_FROZEN
```

---

# PHASE 01 - Reverify inherited pair dynamics, critical cycles, and v0.2 failures

## Goal

Establish that v0.3 is attacking exactly the object the previous experiments certified.

## 01.1 Read-only import

Import:

```text
pair/tree universes needed for development
single-tree transition tables
reachable pair domains n=2..7
b_n^* certificates
critical/near-critical cycle artifacts
forced derivative records
v0.2 Bellman signatures/specimens as target-only context
v0.2 candidate failure ledgers
D5 exact exceptional set
```

## 01.2 Independent reproduction

Required:

```text
n=2..6: independent Pair-Access transition/cost spot/full checks
n=7: streamed certificate verification
critical cycle replay: every imported cycle closes exactly
cycle ratios: exact match
all-KEEP flag: recomputed, not trusted from prose
```

## 01.3 Failure-mechanism table

Emit exact parent failure taxonomy:

```text
GLOBAL_TOO_EASY_TO_CREATE
LOCAL_TOO_WEAK_TO_REPAY
PURE_DIFFERENCE_LOSES_ABSOLUTE_SHAPE
RECENCY_V_BLIND
RECENCY_SCALAR_UNDERPAYS_KEEP
FEATURE_DERIVATIVE_INCONSISTENT
NO_BEHAVIORAL_COMPRESSION_FINITE
```

These labels summarize parent evidence; they do not become universal theorem claims.

## Phase-01 gate

```text
PARENT_CHAIN_VERIFIED
```

only after independent replay.

---

# PHASE 02 - Freeze and prove the Pair-Access translation of the 2026 ontology

## Goal

Turn L6 from inspiration into an exact, audited translation target.

## 02.1 Definition extraction

Extract exact source definitions for:

```text
reference ranks
heavy/light edges
heavy paths
heap view
raw gaps
interval gaps
point gaps
contracted point gaps
lazy intervals
pairings
paid/free operations
bends
```

Store source section/lemma pointers.

## 02.2 Pair-Access mapping

Write `math/L6_PAIR_ACCESS_MAPPING.md` giving, for each object:

```text
source definition
Pair-Access definition
same / modified / not-applicable status
proof obligation
implementation mapping
known semantic differences
```

## 02.3 Independent translation implementation

Implement the ontology twice.

One may mirror source notation closely; the second must be independently structured.

## 02.4 Mutation controls

Mutate:

```text
rank orientation
heavy-child choice
gap sign
lazy-interval side
pairing order
bend orientation
```

The test suite must catch each mutation.

## 02.5 Proof gate

MST0-03 must become `PROVED->REVIEWED` before source lemmas are used theorem-facing.

If exact translation is impossible for some source object, mark it `NOT_APPLICABLE` and define a new Pair-Access object rather than pretending equivalence.

## Phase-02 gate

```text
L6_TRANSLATION_FROZEN
```

---

# PHASE 03 - Build exact rotation-level Pair-Access traces

## Goal

Refine every relevant Pair-Access edge into a deterministic primitive-event stream.

## 03.1 Rotation core

Implement ordinary bottom-up Splay rotation tracing with all cases.

## 03.2 Exact refinement theorem

Prove MST0-02:

```text
concatenating the primitive rotations reproduces the parent S_x(T);
summed primitive rotation/search accounting matches the frozen access-cost convention as required by the analysis;
refinement does not alter pair successor or Pair-Access edge identity.
```

Note: the parent cost `depth+1` is not automatically equal to a literal rotation count. The proof must state exactly how rotation events are used as structural charging units without silently redefining cost.

## 03.3 Reference snapshot

Implement Section 5 KEEP analysis order.

MST0-04 must review whether this frozen-reference viewpoint is legitimate for the intended structural accounting.

## 03.4 Independent core

A second Splay implementation must agree on:

```text
final tree
search path
rotation case sequence
local neighborhoods
canonical event serialization
```

## Phase-03 gate

```text
ROTATION_TRACE_CERTIFIED
```

---

# PHASE 04 - Certify the critical KEEP-cycle corpus at rotation level

## Goal

Make the exact finite bottleneck visible at the granularity where a transfer theorem could live.

## 04.1 Expand all imported critical cycles

Every cycle edge receives full A and B rotation traces and translated L6 events.

## 04.2 Classify regret by Splay case context

For every positive-regret KEEP edge record:

```text
B zig-zig count
B zig-zag count
B terminal zig
boundary pairing classes
bend changes
raw-gap changes
paid operation count
```

## 04.3 Cycle circulation

Compute exact circulation of every state-derivative candidate and exact event counts for all flow primitives.

## 04.4 Cross-n motif canonicalization

Canonical motif definitions may use:

```text
relative order
local orientations
scale transitions
heavy/lazy roles
```

but not literal node labels or cycle IDs.

## 04.5 n=7 internal validation

Motifs discovered on critical `n=4..6` are tested on `n=7` before becoming a frozen grammar predicate.

## Phase-04 gate

```text
CRITICAL_KEEP_CORPUS_CERTIFIED
```

The phase may conclude `KEEP_REGRET_DISTRIBUTED` if no single case class dominates. That is not failure.

---

# PHASE 05 - Prove or kill the KEEP heavy-path / pairing / bend lemmas

## Goal

Test the structural crown assumptions before building a ledger on them.

## 05.1 KEEP heavy-path lemma

Formalize MST0-05 under the **actual translated rank definition**.

The theorem must state exactly:

```text
which reference snapshot is used;
which nodes/edges on the B access path are heavy;
whether the statement applies to the whole path or only a subpath;
all tie/uniqueness conditions.
```

If the natural "entire path is heavy" statement is false, preserve the smallest exact counterexample and replace it only under a new theorem ID/version.

## 05.2 Zig-zig pairing theorem

Prove/kill MST0-06.

## 05.3 Zig-zag bend theorem

Prove/kill MST0-07.

## 05.4 Reference-rotation locality

Prove/kill MST0-08: one A reference rotation modifies the translated heavy/lazy structure by only the claimed bounded primitive operations.

## Phase-05 gate

At least the exact true versions of the lemmas required by later branches must be `REVIEWED`.

If the entire L6-style Pair-Access translation loses its structural advantage:

```text
L6_BASELINE_TRANSLATION_INCOMPLETE
```

and later L6-dependent branches are blocked rather than fabricated.

---

# PHASE 06 - Reproduce the known-loss baseline inside Pair Access

## Goal

Verify that the translated machinery can reproduce the *kind* of contraction loss it was designed to study before claiming to remove it.

## 06.1 Contracted baseline

Implement `PA_CONTRACTED_POINT_GAP_L6` and translated paid-operation accounting.

## 06.2 Finite baseline identities

On exact development traces verify the source-style local claims that are actually applicable after translation.

## 06.3 No theorem overclaim

The goal is not to reprove the full 2026 Splay-vs-OPT theorem. The goal is to show that our translation and instrumentation see the same structural bottlenecks: boundary pairings, contracted point-gap increases, lazy-interval operations, bends, zig-zig/zig-zag roles.

## 06.4 Baseline report

Emit:

```text
which source lemmas transfer exactly
which require modification
where log/loglog loss appears in the translated accounting
which events are unique or simpler because the reference is Splay
```

## Phase-06 gate

```text
L6_BASELINE_REPRODUCED
```

or an exact scoped incomplete status.

---

# PHASE 07 - Trace causal provenance from A restructuring to future KEEP burden

## Goal

Replace LRU-style history with structural causal provenance.

## 07.1 Source events

Every A-side rotation is a candidate source event.

## 07.2 Structural descendants

Track only boundedly representable descendants:

```text
interval boundary
heavy-path relation
lazy-interval membership
heap-parent relation
scale/orientation packet
```

No arbitrary event ID may become theorem-facing state.

## 07.3 Causal equivalence

Two provenance histories may be merged only when the frozen current ledger state is identical under the proposed deterministic update rule.

## 07.4 Counterfactual-free policy

The causal ledger does not ask whether a future access "would have" used an event. It records deterministic current structural credit and activates it only when the current KEEP event satisfies a frozen predicate.

## 07.5 D5 exceptional-set analysis

Use the 16 exact D5 repayment failures as development specimens.

Ask whether they are separated from D5 successes by:

```text
boundary class
zig-zig/zig-zag pattern
scale transition
bend structure
lazy-interval role
provenance class
absolute geometry predicate
```

The 16 failures receive more analytical weight only as exact counterexamples, not through statistical reweighting.

## Phase-07 gate

```text
CAUSAL_PROVENANCE_CERTIFIED
```

or `CAUSAL_PROVENANCE_INSUFFICIENT` with exact witnesses.

---

# PHASE 08 - Generate and quarantine HOLDOUT-H3T-v0.3

## Goal

Create fresh transfer-level evidence before rule synthesis.

## 08.1 Generator freeze

Freeze generator code, strata, episode length distribution, seeds, and exact Splay implementations.

## 08.2 Generate 70,000 legal episodes

Sizes and counts follow Section 14.

## 08.3 Independent replay

A separate Splay core verifies every sampled episode's legality and a cryptographic sample / full streamed policy verifies rotation traces before quarantine.

## 08.4 Commit bank

Write commitments and transition:

```text
EMPTY -> BANK_COMMITTED
```

## 08.5 Firewall

Discovery modules fail closed on any attempt to read H3T content before `TRANSFER_CALCULUS_FROZEN`.

## Phase-08 gate

```text
H3T_BANK_COMMITTED
```

---

# PHASE 09 - Freeze multiscale event ontology and transfer grammar

## Goal

Freeze every primitive the solver is allowed to use before target-guided rule search.

## 09.1 Event ontology

Freeze Section 8 definitions.

## 09.2 Grammar

Freeze T1..T10 and branch permissions.

## 09.3 Scale systems

Freeze S0..S5, including exactly which are theorem-eligible.

## 09.4 Active predicate language

Allowed predicates are finite combinations of declared local/aggregate structural relations. No arbitrary program synthesis outside the grammar.

## 09.5 Target leakage audit

Static audit verifies ontology extraction cannot import:

```text
regret
criticality
Bellman values
candidate IDs
holdout membership
```

## Phase-09 gate

```text
TRANSFER_GRAMMAR_FROZEN
```

---

# PHASE 10 - Solve Branch A: raw-boundary transfer laws on development

## Goal

Attack the strongest constantification conjecture first.

## 10.1 Development inputs

Selection:

```text
critical cycles n=4..6
near-critical selection corpus
noncritical exact edges n=2..5
frozen generated-history selection mask
```

Validation:

```text
critical n=7
noncritical n=6..7
frozen generated-history validation mask
```

No fresh holdout.

## 10.2 Exact synthesis

Use SAT/SMT/ILP/flow to instantiate Branch-A rules.

## 10.3 Required constraints

At minimum:

```text
bounded A-side injection
ledger determinism
nonnegative raw-boundary energy
exact repayment of positive KEEP regret at chosen diagnostic C or symbolic budget
cycle consistency
relabel/mirror covariance
no hidden per-state lookup
```

## 10.4 Failure

If Branch A is infeasible, preserve minimal inconsistent subsystems and smallest exact legal counterexamples.

## 10.5 Success

A finite feasible rule system receives:

```text
RAW_BOUNDARY_LAW_SURVIVES_DEV
```

not theorem status.

## Phase-10 gate

Exactly one:

```text
RAW_BOUNDARY_LAW_SURVIVES_DEV
RAW_BOUNDARY_LAW_REJECTED
RESOURCE_LIMIT_NO_CLAIM
```

---

# PHASE 11 - If triggered, solve Branch B: signed multiscale transfer

## Goal

Use signed scale transfers only after Branch A has an exact preserved obstruction.

## 11.1 Activation

Branch B activates only if:

```text
Branch A rejected by exact evidence
AND branch-B grammar was frozen in Phase 09
```

## 11.2 Signed lower-bound discovery

A signed solver solution is not allowed to "pay" regret by driving total energy to minus infinity.

Search jointly for:

```text
local signed transfer rules
global nonnegative or universally lower-bounded integrated energy
bounded initialization
bounded injection
repayment
```

## 11.3 Scale circulation

Critical KEEP cycles are explicitly checked for signed credit circulation across levels.

## 11.4 Exact failure

Preserve minimal signed obstruction.

## Phase-11 gate

One of:

```text
SIGNED_TRANSFER_NOT_ACTIVATED
SIGNED_TRANSFER_SURVIVES_DEV
SIGNED_TRANSFER_REJECTED
RESOURCE_LIMIT_NO_CLAIM
```

---

# PHASE 12 - Counterexample generalization and negative-branch triage

## Goal

Determine whether transfer-law failures are representation failures or signs of growing actual Pair-Access ratios.

## 12.1 Motif inflation

For every decisive Branch-A/B counterexample, attempt a canonical parameterized motif family.

## 12.2 Actual-cost ratio tracking

Measure only real paired Splay costs:

```math
R_k=\frac{\sum c_B}{\sum c_A}
```

not transfer residual magnitude.

## 12.3 Activation criteria

Negative branch candidate requires:

```text
N1 legal reachable paired executions
N2 explicit parameterized structural construction
N3 actual cost ratio or required b grows with parameter
N4 independent replay
N5 plausible diagonal-rooted embedding
```

## 12.4 No solver-defined family

"Take the worst state at size k" is not a family.

## Phase-12 gate

Normally:

```text
NEGATIVE_FAMILY_NOT_ACTIVATED
```

or, if all criteria pass:

```text
NEGATIVE_CYCLE_FAMILY_CANDIDATE
```

---

# PHASE 13 - Attack the raw/signed loss directly at larger scale

## Goal

Stress the surviving transfer mechanism before freezing a theorem candidate.

## 13.1 Adversarial development families

Use non-fresh generated development families:

```text
left/right spines
opposite spines
balanced/spine
alternating zig-zag
zig-zig enriched
nested intervals
rank-gap extremes
boundary-pairing enriched
long DELETE bursts then KEEP
repeated synchronous KEEP cycles
mirror pairs
rotation neighborhoods
motif inflation from development failures
```

## 13.2 Search engines

At least:

```text
uniform legal histories
structured generators
hill climb
simulated annealing
genetic search
rotation-neighborhood search
cycle splicing
motif inflation
counterexample generalizer
```

Heuristics propose; exact evaluator disposes.

## 13.3 Constant ladder diagnostic

If a calculus fails at `C=2`, do not immediately kill the structural law if its exact theorem form permits a larger C.

Evaluate the frozen rule system across the diagnostic ladder without changing rule definitions.

The final candidate constant is frozen only with the candidate calculus in Phase 14.

## Phase-13 gate

A candidate calculus may proceed only with zero exact development violations at its frozen theorem constant.

---

# PHASE 14 - Freeze theorem candidate calculus and constant

## Goal

Convert the best surviving structural calculus into one explicit theorem hypothesis before fresh evidence.

## 14.1 Candidate set

At most a small preregistered number of primary candidates may be frozen.

Recommended cap:

```text
3 primary calculi total across both branches
```

If more finite survivors exist, select by the frozen complexity ordering before fresh holdout contact.

## 14.2 Freeze

For every `MSTC-*` freeze all Section-15 metadata and one universal theorem constant `C`.

`C` may be conservative.

## 14.3 Proof outline

Each candidate must already have a plausible arbitrary-n lemma decomposition:

```text
reference rotation locality
injection
zig-zig transfer
zig-zag/bend payment
boundary event handling
lower bound / nonnegativity
integrability
telescoping
```

A solver-only object with no interpretable proof outline is not promoted.

## 14.4 Candidate-set commitment

Hash the full candidate set.

Transition H3T:

```text
BANK_COMMITTED -> TRANSFER_CALCULUS_FROZEN
```

and corresponding H2R/H1 candidate-set metadata without revealing contents.

## Phase-14 gate

```text
TRANSFER_CALCULUS_FROZEN
```

or `REPRESENTATION_INCONCLUSIVE` if no candidate exists.

---

# PHASE 15 - Consume fresh holdouts exactly once

## Goal

Test frozen calculi on evidence untouched by discovery.

## 15.1 Schema routing

State-only calculus:

```text
n8 contaminated -> H1 -> H3T
```

History/causal calculus:

```text
H2R -> H3T
```

Only compatible banks are used.

## 15.2 Full exact evaluation

Evaluate every eligible state/transition/episode.

Preserve:

```text
first exact violation under canonical order
maximum exact violation
failure class
replay bundle
ledger before/after
primitive event trace
```

## 15.3 Independent replay

Every fresh counterexample is replayed by a clean-room Splay + ledger evaluator.

## 15.4 No adaptation

No candidate mutation inside Phase 15.

## Phase-15 gate

Fresh survival is:

```text
FRESH_H1_PASS / FRESH_H2R_PASS / FRESH_H3T_PASS
```

as applicable.

It is never theorem status.

---

# PHASE 16 - Clean-room implementation and large-n adversarial falsification

## Goal

Try to murder every fresh survivor before proof work.

## 16.1 Clean-room evaluator

Receives only:

```text
frozen mathematical calculus
frozen constant C
Pair-Access contract
rotation contract
translated ontology contract
state/history schemas
```

No discovery imports.

## 16.2 Independent implementation

Reimplement ledger updates and energy from the mathematical definition.

## 16.3 Large-n adversarial search

Use sizes well beyond exact exhaustive development where resources permit.

Suggested:

```text
n = 16,24,32,48,64,96,128,192,256
```

The run may use random/structured histories; all claimed violations are exact replayed witnesses.

## 16.4 Mutation controls

Mutate:

```text
one credit sign
one scale level
one activation predicate
one transfer output
one injection coefficient
one C
one L6 mapping choice
one zig-zig/zig-zag classification
```

The suite must catch known bad mutants.

## Phase-16 gate

Survival ceiling:

```text
TRANSFER_CALCULUS_SURVIVES_FINITE_TESTS
```

No theorem.

---

# PHASE 17 - Universal rotation-level proof

## Goal

Stop mining and prove the calculus for arbitrary n.

At most one primary candidate is promoted at a time.

## 17.1 Well-definedness

Prove arbitrary-n ledger state and every rule are well-defined.

## 17.2 Reference locality

Prove MST0-08 in the exact form needed.

## 17.3 Injection theorem

Prove MST0-13:

```math
E_{\rm after}-E_{\rm before}
\le
C_D\cdot \operatorname{cost}_A(D)
```

for every DELETE/A-only block or the chosen finer granularity.

## 17.4 Zig-zig transfer theorem

Prove every zig-zig / pairing case.

## 17.5 Zig-zag / bend theorem

Prove every zig-zag case.

## 17.6 Boundary interactions

Prove the raw-boundary or signed-multiscale theorem with no finite premise.

## 17.7 Lower bound

If signed, prove energy lower bounded universally.

## 17.8 Integrability

Prove MST0-15: local rules define a legitimate global energy/flow accounting independent of arbitrary decomposition choices.

## 17.9 No hidden n dependence

Every constant is universal.

## 17.10 No finite premise

The proof may not rely on:

```text
n<=7
holdout pass
observed cycle catalog completeness
solver optimality
empirical scaling
finite grammar feasibility
```

## Phase-17 gate

Possible theorem-level statuses:

```text
BOUNDED_DELETE_INJECTION_PROVED
SYNCHRONOUS_KEEP_TRANSFER_PROVED
```

Both plus required integrability/lower-bound lemmas are needed to continue positive proof.

---

# PHASE 18 - Pair Access, approximate monotonicity, bridge, or negative theorem

## Goal

Finish the mathematical route in either direction.

## 18.1 Positive: block Pair Access

Prove MST0-16/17.

For arbitrary legal paired execution:

```math
\operatorname{Splay}(Y,T)+E_m-E_0
\le
C\operatorname{Splay}(X,T)+A(n)
```

where the primary route aims for `A(n)=0`; a bounded additive `O(n)` route is allowed only if the exact Levy-Tarjan bridge theorem being used permits it and the convention audit is explicit.

Preferred zero-initial route:

```math
E_0=0,\qquad E_m\ge0.
```

Conclude constant-factor approximate monotonicity in the exact permitted form.

## 18.2 Bridge audit

Audit:

```text
Splay variant
cost convention
initial tree convention
subsequence definition
additive term
constant independence
direction of implication
exact L2/L3 theorem version
```

Only then:

```text
UNIVERSAL_PAIR_ACCESS_LEMMA_PROVED
-> APPROXIMATE_MONOTONICITY_PROVED
-> DYNAMIC_OPTIMALITY_PROVED
```

## 18.3 Negative branch

If Phase 12 activated a candidate negative family, prove explicit closed form:

```math
(T_k,X_k,Y_k),\qquad Y_k\preceq X_k
```

and symbolic bounds:

```math
\operatorname{Splay}(X_k,T_k)\le f(k),
```

```math
\operatorname{Splay}(Y_k,T_k)\ge g(k),
```

```math
\frac{g(k)}{f(k)}\to\infty.
```

No transfer residual may substitute for actual Splay cost.

Only after reverse-bridge audit may the final claim be `DYNAMIC_OPTIMALITY_DISPROVED`.

## Phase-18 gate

Exactly one theorem-facing branch may be active in FINAL_RESULT unless both independently prove logically compatible statements (which would itself require contradiction resolution before sealing).

---

# PHASE 19 - Seal, reproduce, package, and release

## Goal

Create a deterministic scientific record that cleanly distinguishes finite transfer discovery from theorem-level success.

## 19.1 FINAL_RESULT

Generate from artifacts only.

Allowed terminal claim levels:

```text
PARENT_CHAIN_ONLY
FINITE_ROTATION_TRANSLATION_RESULTS
FINITE_CRITICAL_KEEP_RESULTS
FINITE_TRANSFER_OBSTRUCTION_RESULTS
FINITE_TRANSFER_CALCULUS_RESULTS
TRANSFER_CALCULUS_SURVIVES_FINITE_TESTS
BOUNDED_DELETE_INJECTION_PROVED
SYNCHRONOUS_KEEP_TRANSFER_PROVED
UNIVERSAL_PAIR_ACCESS_LEMMA_PROVED
APPROXIMATE_MONOTONICITY_PROVED
DYNAMIC_OPTIMALITY_PROVED
NEGATIVE_REAL_SPLAY_FAMILY_PROVED
DYNAMIC_OPTIMALITY_DISPROVED
RESOURCE_LIMIT_NO_CLAIM
REPRESENTATION_INCONCLUSIVE
```

Exactly one terminal claim level.

## 19.2 Fresh-checkout reproduction

Fresh checkout must:

```text
verify v0.1/v0.2 parent seals
verify literature/source hashes
rebuild deterministic small-size rotation traces
replay critical cycles
rebuild translated L6 ontology on required small sizes
reverify H3T commitment without reveal if still pristine
reverify every frozen calculus/counterexample
rerun theorem-review gates
recompute FINAL_RESULT
```

If fresh banks were consumed, verify reveal records and counterexample replay rather than pretending freshness remains.

## 19.3 Archive

Create deterministic:

```text
SPLAY-AM-MST-v0.3.tar.zst
```

with canonical ordering, normalized metadata, SHA-256, and logical-stream hashes for sharded large artifacts.

## 19.4 Paper-facing reports

Produce:

```text
MULTISCALE_TRANSFER_REPORT.md
KEEP_CYCLE_ATLAS.md
L6_PAIR_ACCESS_TRANSLATION_REPORT.md
TRANSFER_CALCULUS_LEDGER.md
COUNTEREXAMPLE_ATLAS.md
THEOREM_STATUS_REPORT.md
REPRODUCIBILITY.md
AI_USE.md
```

## 19.5 No cleanup by deletion

Unexpected scientific artifacts are included with status or cause seal audit failure.

Never delete failed experiments/counterexamples to make the archive clean.

---
# 23. Threat model

The v0.3 seal audits at least the following threats.

```text
T01  v0.2 used before final seal
T02  parent commit accepted from prose instead of artifact
T03  v0.1/v0.2 result rewritten in v0.3
T04  parent artifact mutated during bootstrap
T05  n8 contamination forgotten
T06  H1 read before calculus freeze
T07  H2R read before calculus freeze
T08  H3T read before calculus freeze
T09  H3T regenerated after candidate inspection
T10  literature version drift
T11  L6 English term reused without exact translation
T12  L6 theorem silently treated as Pair-Access theorem
T13  reference-rank definition replaced by depth without proof
T14  heavy-child tie/uniqueness silently assumed
T15  KEEP "all-heavy" intuition used before MST0-05 review
T16  frozen-reference analysis order changes actual Pair-Access semantics
T17  parent cost depth+1 silently replaced by rotation count
T18  rotation trace fails to reproduce final Splay tree
T19  zig-zig / zig-zag case mislabeled
T20  event ontology reads regret/criticality before freeze
T21  critical cycles cherry-picked
T22  near-critical threshold chosen after inspection
T23  n7 used in selection despite prereg validation role
T24  cycle ID leaks into theorem-facing rule
T25  full-cycle circulation confused with state potential derivative
T26  event flow mistaken for state function
T27  DELETE injection inferred from static discrepancy rather than cost-bearing event
T28  causal provenance stores unbounded event timestamps/IDs
T29  future access leaks into active-credit predicate
T30  global cancellation asserted without local rule/telescope
T31  signed credit drives energy to minus infinity
T32  lower bound assumed from finite tests
T33  one primitive event creates unbounded hidden credit
T34  scale definition changes after counterexample
T35  solver grammar expanded after seeing target failure without new version
T36  Branch B invented after Branch A failure rather than preregistered
T37  SAT/ILP feasible status accepted without exact replay
T38  SAT/ILP infeasible status accepted without certificate/independent confirmation
T39  floating relaxation determines theorem parameter
T40  statistical fit outranks exact violation
T41  diagnostic C=2 treated as theorem-required constant
T42  final C chosen by holdout optimization
T43  rule system changes while retaining calculus ID
T44  raw-boundary law redefined after failure under same ID
T45  signed-transfer branch hides raw-boundary counterexample
T46  contracted-gap L6 baseline presented as new constant result
T47  raw-gap finite survival called O(1) theorem
T48  source-paper asymptotic bound used as logical premise
T49  D5 near-miss treated as almost-proof
T50  16 D5 failures downweighted or suppressed
T51  transfer residual motif mistaken for actual Splay ratio motif
T52  fixed-C positive cycle called DOC disproof
T53  negative family selected as worst solver state per k
T54  motif inflation lacks diagonal-rooted legal embedding
T55  growing residual without growing actual ratio called negative evidence
T56  fresh holdout survivor called theorem
T57  H1 used for history-dependent calculus
T58  H2R replay history used during discovery before unlock
T59  H3T target-enriched generator uses post-freeze residuals
T60  candidate set altered after any fresh reveal
T61  clean-room verifier imports discovery code
T62  independent Splay core shares hidden implementation path
T63  mutation tests fail to catch known corruptions
T64  nondeterministic parallel reduction changes witness/certificate
T65  resource exhaustion interpreted as structural impossibility
T66  proof omits one Splay rotation case
T67  proof omits one ledger rule / lazy-interval operation
T68  proof hides n-dependent credit type or constant
T69  integrability assumed because local rules fit cycles
T70  energy nonnegativity assumed because examples nonnegative
T71  block partition omits/double-counts an access
T72  additive O(n) term introduced without bridge compatibility audit
T73  Levy-Tarjan theorem direction/version mismatched
T74  regular-access / subsequence / approximate-monotonicity formulations conflated without proof
T75  Pair-Access success claimed to optimize competitive constant
T76  failed calculus overwritten rather than versioned
T77  counterexamples omitted from release
T78  manifest omits large sharded scientific artifact
T79  logical-stream hash disagrees with shard manifest
T80  archive self-reference produces stale seal
T81  AI-assisted code silently changes frozen contract
T82  literature-derived proof text copied without checking hypotheses
T83  theorem review checks keywords/status only rather than mathematical obligations
T84  theorem status jumps UNPROVED->REVIEWED without preserved lifecycle
T85  branch scope theorem not reviewed before interpreting a failure
T86  pair-state Bellman corridor misapplied to causal ledger
T87  recency-V blindness misread as ledger-history blindness
T88  behavioral no-compression misread as proof complexity lower bound
T89  finite KEEP-only criticality generalized to all n
T90  parent b_n* pattern presented as boundedness theorem
```

Every threat maps to at least one test, invariant, stop, or manual review control in `prereg/threat_control_matrix.yaml`.

At seal:

```text
set(threat_ids) == {T01,...,T90}
every threat has >=1 valid control
every referenced control exists
```

No mere count check.

---

# 24. Test matrix

Minimum named tests.

## Parent / foundation

```text
PARENT-01 v0.2 final commit exact
PARENT-02 v0.2 manifest exact
PARENT-03 v0.1 ancestor chain exact
PARENT-04 H1 required firewall state
PARENT-05 H2R required firewall state
PARENT-06 n8 contamination preserved
PARENT-07 parent theorem ledger hash
PARENT-08 no pre-prereg v0.3 scientific output
```

## Literature / translation

```text
L6-01 source version hash
L6-02 rank definition mapping
L6-03 heavy-edge mapping
L6-04 heap-view mapping
L6-05 gap decomposition mapping
L6-06 lazy-interval mapping
L6-07 pairing mapping
L6-08 bend mapping
L6-09 contracted-gap baseline mapping
L6-10 independent translation agreement
L6-11 rank mutant caught
L6-12 pairing/bend mutant caught
```

## Rotation trace

```text
ROT-01 final tree matches parent Splay
ROT-02 search path exact
ROT-03 ROOT case
ROT-04 ZIG case
ROT-05 LL case
ROT-06 RR case
ROT-07 LR case
ROT-08 RL case
ROT-09 canonical event ordering
ROT-10 independent core agreement
ROT-11 reference snapshot exact
ROT-12 cost convention not redefined
```

## Critical cycles

```text
CYC-01 every imported critical cycle closes
CYC-02 exact parent ratio matches
CYC-03 all-KEEP status recomputed
CYC-04 forced derivative record matches parent
CYC-05 rotation expansion deterministic
CYC-06 cycle state-derivative circulation zero
CYC-07 n7 validation firewall respected
CYC-08 near-critical policy nonadaptive
```

## Provenance / ledger

```text
LED-01 ledger update deterministic
LED-02 support relabel invariant
LED-03 no event-ID/timestamp theorem leakage
LED-04 bounded primitive creation schema
LED-05 active predicate future-blind
LED-06 cancellation local
LED-07 initial synchronized ledger valid
LED-08 mirror covariance
LED-09 independent ledger implementation
LED-10 signed lower-bound canary
```

## Transfer grammar / solver

```text
TR-01 grammar hash frozen before target search
TR-02 forbidden target inputs absent
TR-03 exact feasible assignment replay
TR-04 infeasible certificate / second solver verification
TR-05 critical cycles satisfy candidate calculus
TR-06 bounded injection development
TR-07 KEEP repayment development
TR-08 constant independence metadata
TR-09 smallest exact counterexample
TR-10 maximum exact counterexample
TR-11 calculus ID mutation rule
TR-12 Branch-B activation discipline
TR-13 diagnostic-C mutation caught
TR-14 no hidden state lookup
```

## Holdouts

```text
HLD-01 n8 never labeled fresh
HLD-02 H1 unread pre-freeze
HLD-03 H1 unlock at most once
HLD-04 H2R commitment exact
HLD-05 H2R unread pre-freeze
HLD-06 H2R unlock at most once
HLD-07 H3T commitment exact
HLD-08 H3T unread pre-freeze
HLD-09 H3T unlock at most once
HLD-10 H3T no-regeneration-after-reveal
HLD-11 candidate-set hash immutable after reveal
HLD-12 post-holdout edit new ID
```

## Proof

```text
PR-01 MST0-05 actual translated rank hypotheses
PR-02 MST0-06 all zig-zig cases
PR-03 MST0-07 all zig-zag cases
PR-04 MST0-08 all reference rotation cases
PR-05 bounded DELETE injection arbitrary n
PR-06 KEEP repayment arbitrary n
PR-07 signed energy lower bound if applicable
PR-08 integrability / decomposition independence
PR-09 block partition coverage
PR-10 no finite premise
PR-11 universal C independence
PR-12 telescope symbolic check
PR-13 bridge convention audit
PR-14 no source-paper theorem silently imported
```

## Negative branch

```text
NEG-01 fixed-C failure not misclassified
NEG-02 actual Splay ratio used
NEG-03 family closed form
NEG-04 diagonal-rooted legality
NEG-05 symbolic full-sequence upper bound
NEG-06 symbolic subsequence lower bound
NEG-07 ratio limit proof
NEG-08 independent family replay
```

## Seal

```text
SEAL-01 fresh checkout
SEAL-02 parent chain exact
SEAL-03 threat set exact T01..T90
SEAL-04 stop set exact
SEAL-05 theorem lifecycle audit
SEAL-06 manifest completeness
SEAL-07 shard/logical-stream consistency
SEAL-08 exact arithmetic policy
SEAL-09 result recomputation
SEAL-10 archive determinism
SEAL-11 holdout reveal-state truthfulness
SEAL-12 failed artifacts retained
```

---

# 25. Permanent invariants

At minimum:

```text
INV-001 v0.3 parent is final sealed v0.2, not pre-seal WP5 HEAD
INV-002 v0.1 ancestor commit exact
INV-003 parent snapshots read-only after bootstrap
INV-004 cost remains depth+1
INV-005 Splay remains ordinary bottom-up
INV-006 Pair-Access KEEP/DELETE match parents
INV-007 b=2 diagnostic only
INV-008 final theorem may use any universal finite C
INV-009 rotation trace does not redefine cost
INV-010 reference snapshot convention versioned
INV-011 L6 source version frozen
INV-012 PA_* names used until equivalence reviewed
INV-013 ontology extraction target-blind
INV-014 critical corpus imports all certified cycles
INV-015 near-critical threshold preregistered
INV-016 n7 critical corpus reserved internal validation if frozen that way
INV-017 ledger support has arbitrary-n mathematical semantics
INV-018 no theorem-facing event IDs/timestamps
INV-019 no future info in active predicate
INV-020 credit creation has explicit source event
INV-021 local cancellation explicit
INV-022 signed branch requires lower-bound theorem
INV-023 raw branch precedes signed branch
INV-024 Branch B grammar frozen before Branch-A result
INV-025 solver output exact-replayed
INV-026 U/V/G absent from theorem-facing rule inputs
INV-027 state/cycle IDs absent from theorem-facing rule inputs
INV-028 every calculus mutation creates new ID
INV-029 C frozen before fresh holdout
INV-030 H1 fresh only if parent says EMPTY
INV-031 H2R fresh only if parent unlock_count 0
INV-032 H3T generated before synthesis
INV-033 H3T never regenerated after reveal
INV-034 n8 never fresh
INV-035 fresh banks unlocked at most once
INV-036 post-holdout descendant not fresh-tested on consumed bank
INV-037 clean-room evaluator imports no discovery implementation
INV-038 heuristics propose; exact evaluator disposes
INV-039 one exact positive residual rejects finite candidate gate
INV-040 resource limit is not negative result
INV-041 KEEP-only finite criticality never generalized without proof
INV-042 b_n* finite pattern never called boundedness theorem
INV-043 raw-gap failure not Pair-Access failure
INV-044 transfer-grammar failure not Pair-Access failure
INV-045 transfer residual not actual Splay ratio
INV-046 negative claim needs closed-form real Splay family
INV-047 every theorem status has proof/review pointer
INV-048 REVIEWED never means external peer review
INV-049 all proof consumers fail closed on status
INV-050 literature FEATURE_INSPIRATION never silently PREMISE
INV-051 L6 baseline contraction is baseline, not final target
INV-052 final proof covers ROOT/ZIG/LL/RR/LR/RL as applicable
INV-053 block proof covers all accesses exactly once
INV-054 signed terminal energy cannot be unbounded below
INV-055 initial energy normalization explicit
INV-056 additive term explicit and bridge-compatible
INV-057 theorem C independent of n and sequence
INV-058 exact counterexamples append-only
INV-059 failed calculi append-only
INV-060 final result generated from artifacts only
INV-061 manifest covers every scientific file
INV-062 large scientific files use deterministic compression/sharding policy
INV-063 logical-stream hashes stable
INV-064 deterministic sorted reduction
INV-065 AI assistance logged
INV-066 human/reviewer ownership of theorem statements/review explicit
INV-067 current web/literature context never overrides frozen source bytes
INV-068 parent holdout contents never inferred from metadata
INV-069 all theorem translations state domain explicitly
INV-070 Dynamic Optimality claim only after bridge audit
```

---

# 26. Scaling and resource policy

## 26.1 Exact exhaustive pair domain

Primary inherited exact domain:

```text
n=2..7
```

Do not regenerate huge pair domains merely to reproduce parent artifacts unless verification requires it.

## 26.2 Critical-cycle rotation traces

All certified critical cycles `n=4..7` are mandatory and expected to be manageable because only selected cycles are expanded, not every Pair-Access edge.

## 26.3 Broader edge instrumentation

Recommended:

```text
n=2..5 full rotation ontology
n=6 selected + streamed full summaries
n=7 selected / critical / validation streamed
```

Resource limits must be reported exactly.

## 26.4 Large generated histories

Use on-demand rotation traces rather than storing every intermediate tree if deterministic replay can reconstruct them.

Preserve logical-stream hashes.

## 26.5 Large artifact hygiene

No new raw JSON file should intentionally exceed GitHub practical limits.

Use deterministic:

```text
.json.zst
shards
manifest of shard hashes
logical-stream SHA-256
```

Do not rewrite old parent history to remove existing large files.

## 26.6 Parallelism

Safe parallel tasks:

```text
state-local ontology extraction
cycle-local expansion
history-local candidate evaluation
solver instances with deterministic post-sort
independent replay
```

All reductions sorted deterministically.

## 26.7 Resource failure record

Must include:

```text
phase
track/branch
n / corpus
last valid artifact
wall time
peak memory
solver state/certificate status
attempted vs unattempted work
scientific claims still valid
```

Status:

```text
RESOURCE_LIMIT_NO_CLAIM
```

---

# 27. Logging requirements

Every execution record contains:

```text
experiment_id
phase
branch
UTC timestamp
local commit
parent v0.2 commit
ancestor v0.1 commit
spec SHA
prereg SHA
literature manifest SHA
theorem-gate matrix SHA
holdout firewall states
calculus ID/hash if applicable
constant C if applicable
runtime/dependency hashes
command
input hashes
output hashes
stdout hash
stderr hash
wall time
peak memory
exit code
scientific status
```

Logs are append-only.

---

# 28. Dependencies and environment

Freeze exact versions.

Recommended baseline:

```text
Python 3.12.x
sympy
zstandard
jsonschema
networkx convenience-only, never theorem authority
numpy/pandas analysis-only
scipy/HiGHS discovery-only unless exact certificate independently checked
z3-solver or another exact SMT backend if used
pyscipopt / OR-Tools only for discovery unless exact integer assignment replayed
mpmath/arb-style interval package for certified transcendental signs if needed
Rust stable + Cargo.lock if acceleration used
```

No platform floating point decides a sealed scientific sign.

Solver versions and parameter files are frozen.

---

# 29. AI assistance policy

AI may assist:

```text
code generation
unit tests
formalization brainstorming
counterexample triage
solver encoding
literature cross-reference
proof-outline generation
prose
audit
```

AI may not silently:

```text
alter Pair-Access/Splay semantics
alter literature mapping
change a theorem statement after a failed proof without versioning
read quarantined holdouts via discovery
invent a transfer rule after holdout reveal under the same candidate ID
suppress counterexamples
upgrade finite survival to theorem
upgrade REVIEWED to external peer review
claim a source theorem applies without hypothesis audit
change branch activation rules
```

Release includes a substantive `AI_USE.md`.

---

# 30. Stop conditions

Create `prereg/stop_control_matrix.yaml` with exact IDs and multi-phase ownership arrays.

Minimum stops:

```text
STOP-01 parent v0.2 not finally sealed
STOP-02 parent hash mismatch
STOP-03 parent snapshot mutated post-lock
STOP-04 literature version unresolved
STOP-05 prereg hash mismatch
STOP-06 H1 not pristine at foundation
STOP-07 H2R not pristine at foundation
STOP-08 n8 mislabeled fresh
STOP-09 L6 translation ambiguous but used theorem-facing
STOP-10 ontology target leakage
STOP-11 rotation core disagreement
STOP-12 reference-snapshot convention theorem blocked
STOP-13 KEEP heavy lemma consumed before REVIEWED
STOP-14 zig-zig/zig-zag mapping theorem consumed before REVIEWED
STOP-15 critical corpus omits certified parent cycle
STOP-16 near-critical threshold changed after inspection
STOP-17 theorem-facing rule uses state/cycle ID
STOP-18 theorem-facing provenance uses timestamp/event ID
STOP-19 future information detected in active predicate
STOP-20 signed branch used before Branch-A exact failure
STOP-21 signed energy lacks lower-bound route
STOP-22 solver feasible assignment fails exact replay
STOP-23 solver infeasibility unverified
STOP-24 float-dependent residual sign
STOP-25 calculus mutated under same ID
STOP-26 C changed after fresh reveal
STOP-27 H1 early read
STOP-28 H2R early read
STOP-29 H3T early read
STOP-30 fresh bank second unlock
STOP-31 H3T regenerated after reveal
STOP-32 clean-room imports discovery code
STOP-33 mutation controls fail
STOP-34 negative branch uses transfer residual instead of Splay ratio
STOP-35 negative family solver-defined rather than closed-form
STOP-36 proof uses finite premise
STOP-37 proof omits Splay case
STOP-38 proof omits ledger rule case
STOP-39 hidden n-dependent constant
STOP-40 integrability unproved
STOP-41 terminal energy lower bound unproved
STOP-42 block partition coverage unproved
STOP-43 bridge convention mismatch
STOP-44 additive term incompatible with bridge
STOP-45 theorem lifecycle invalid
STOP-46 manifest incomplete
STOP-47 logical-stream/shard mismatch
STOP-48 failed scientific artifact deleted
STOP-49 nondeterministic reproduction
STOP-50 resource limit interpreted as impossibility
```

At seal:

```text
set(stop_ids)=={STOP-01,...,STOP-50}
every stop has >=1 owning phase
every handler/test exists
```

---

# 31. Transfer-theorem ladder

A transfer calculus advances only in order.

```text
MST-GATE-0   mathematical definitions total on declared domain
MST-GATE-1   L6 / Pair-Access translation reviewed
MST-GATE-2   rotation refinement reviewed
MST-GATE-3   required KEEP heavy/pairing/bend lemmas reviewed
MST-GATE-4   development ledger deterministic
MST-GATE-5   bounded injection exact on development
MST-GATE-6   KEEP repayment exact on development
MST-GATE-7   cycle consistency exact
MST-GATE-8   integrated energy lower bound / nonnegativity development checks + proof route
MST-GATE-9   internal validation n6/n7 + generated split
MST-GATE-10  candidate calculus + C frozen
MST-GATE-11  contaminated n8 if applicable
MST-GATE-12  compatible fresh H1/H2R
MST-GATE-13  fresh H3T
MST-GATE-14  clean-room implementation
MST-GATE-15  large-n adversarial falsification
MST-GATE-16  arbitrary-n injection proof
MST-GATE-17  arbitrary-n KEEP transfer proof
MST-GATE-18  integrability/lower-bound theorem
MST-GATE-19  universal Pair Access
MST-GATE-20  approximate monotonicity
MST-GATE-21  dynamic optimality bridge
```

First decisive failure freezes the candidate at that gate.

Later evidence may be attached as supplementary but cannot erase the first failure.

---

# 32. Interpretation rules

## 32.1 A true KEEP heavy-path lemma

Means:

> Under the exact translated rank/reference convention, a specific structural restriction holds on every legal KEEP.

It does not mean the constant-factor proof is solved.

## 32.2 Critical KEEP-only finite geometry

Allowed:

> On the certified finite critical cycles, forced critical derivatives are carried by KEEP transitions.

Forbidden:

> DELETE never matters asymptotically.

## 32.3 No compression

Allowed:

> The exact target-independent behavioral quotient has no nontrivial compression on the tested domains.

Forbidden:

> Any proof of Dynamic Optimality must encode the full state.

## 32.4 Raw-boundary finite success

Allowed:

> The frozen raw-boundary calculus has no counterexample on the stated development/validation domains.

Forbidden:

> Raw boundary damage is O(cost(A)) universally.

## 32.5 Raw-boundary failure

Allowed:

> The frozen Branch-A law is false, with this exact legal counterexample.

Forbidden:

> The 2026 log/loglog loss is necessary.

## 32.6 Signed-transfer finite success

Allowed:

> A signed multiscale calculus survived finite tests and has the stated lower-bound proof obligations.

Forbidden:

> Negative credits are safe globally.

## 32.7 Fresh holdout success

Allowed:

> The frozen calculus survived evidence untouched by discovery.

Forbidden:

> The theorem is proved.

## 32.8 Universal injection theorem

Means only the DELETE/reference-update side has been proved.

Do not claim Pair Access until KEEP transfer and integrability also prove.

## 32.9 Universal KEEP transfer theorem

Means only the synchronous side has been proved.

Do not claim Pair Access until injection, lower bound, and block composition prove.

## 32.10 Transfer-law failure versus negative Splay result

A growing transfer residual is a representation obstruction.

Only a growing actual ratio of legal real Splay executions can activate the negative theorem branch.

---

# 33. Allowed and forbidden claims by result level

## 33.1 `FINITE_ROTATION_TRANSLATION_RESULTS`

Allowed:

> We exactly translated and independently verified the stated heavy/lazy/rotation objects on the reported finite domains.

Forbidden:

```text
"the L6 proof improves to constant factor"
"Pair Access follows"
```

## 33.2 `FINITE_CRITICAL_KEEP_RESULTS`

Allowed:

> Exact critical KEEP-cycle traces exhibit the reported multiscale event structure.

Forbidden:

```text
"all asymptotic obstructions are KEEP cycles"
```

## 33.3 `FINITE_TRANSFER_OBSTRUCTION_RESULTS`

Allowed:

> The preregistered transfer grammar/law is exactly inconsistent on the reported witness set.

Forbidden:

```text
"no transfer proof exists"
```

## 33.4 `TRANSFER_CALCULUS_SURVIVES_FINITE_TESTS`

Allowed:

> A frozen arbitrary-n-defined calculus satisfies all tested exact inequalities, fresh holdouts, and adversarial evaluations.

Forbidden:

```text
"the calculus works for all n"
"Dynamic Optimality is proved"
```

## 33.5 `BOUNDED_DELETE_INJECTION_PROVED`

Allowed:

> A universal theorem bounds ledger injection by A-side cost under the stated calculus.

No stronger claim.

## 33.6 `SYNCHRONOUS_KEEP_TRANSFER_PROVED`

Allowed:

> A universal theorem pays synchronous KEEP burden under the stated calculus.

No Pair-Access claim until composition/integrability prove.

## 33.7 `UNIVERSAL_PAIR_ACCESS_LEMMA_PROVED`

Allowed:

> For every legal paired execution in the theorem domain, the proved block/local inequalities imply the stated universal constant-factor Pair-Access bound.

Approximate monotonicity may be claimed only after the telescope/convention gate.

## 33.8 `DYNAMIC_OPTIMALITY_PROVED`

Allowed only after the exact Levy-Tarjan bridge audit.

State the competitive theorem precisely, including additive convention if any.

## 33.9 `DYNAMIC_OPTIMALITY_DISPROVED`

Allowed only after a closed-form unbounded real Splay subsequence-overhead family and reverse-bridge audit.

---

# 34. Final seal checklist

Before Phase 19 final seal:

```text
FOUNDATION
[ ] v0.2 final seal exact
[ ] v0.1 ancestor exact
[ ] parent snapshot locked
[ ] literature exact
[ ] normative stack hashed

TRANSLATION
[ ] L6 mapping frozen
[ ] required translation theorems reviewed
[ ] no source theorem silently transplanted

ROTATIONS
[ ] exact Splay rotation trace certified
[ ] independent core agrees
[ ] cost convention unchanged

CRITICAL CORPUS
[ ] all imported critical cycles present
[ ] cycle replay exact
[ ] no adaptive omission

LEDGER / GRAMMAR
[ ] ontology target-blind
[ ] grammar frozen pre-synthesis
[ ] Branch B preregistered before Branch-A result
[ ] failed grammars/counterexamples preserved

HOLDOUTS
[ ] n8 truthful contamination label
[ ] H1 reveal state truthful
[ ] H2R reveal state truthful
[ ] H3T commitment/reveal state truthful
[ ] no bank called fresh after reveal

CANDIDATES
[ ] every calculus ID immutable
[ ] constant C frozen correctly
[ ] exact development residuals
[ ] clean-room agreement where applicable

PROOFS
[ ] theorem ledger lifecycle valid
[ ] no finite premise in universal proof
[ ] every Splay/ledger case covered
[ ] signed lower bound proved if needed
[ ] integrability proved
[ ] block coverage proved
[ ] universal C independence proved
[ ] telescope audited
[ ] bridge audited

NEGATIVE
[ ] fixed-C failures not misclassified
[ ] only actual Splay ratio used
[ ] closed form if negative theorem claimed

REPRODUCIBILITY
[ ] threat IDs exactly T01..T90
[ ] stop IDs exactly STOP-01..STOP-50
[ ] all referenced controls exist
[ ] tests pass
[ ] mutation controls pass
[ ] logical-stream hashes verify
[ ] manifest complete
[ ] fresh checkout recomputes result
[ ] deterministic archive verifies
[ ] AI use disclosed
```

---

# 35. Success criteria

v0.3 is scientifically successful if it cleanly resolves **at least one** of the following questions with exact evidence/theorem status:

```text
S1  Is the natural KEEP heavy-path statement true under the exact L6 translation?
S2  Which zig-zig/zig-zag/boundary structures carry certified critical KEEP burden?
S3  Can raw boundary damage be bounded at constant cost under Splay-reference dynamics?
S4  If not, what exact minimal obstruction forces a multiscale/signed correction?
S5  Can a finite local transfer calculus satisfy bounded injection + KEEP repayment on exact development?
S6  Does a frozen calculus survive genuinely fresh H1/H2R/H3T evidence?
S7  Can the transfer calculus be proved for arbitrary n?
S8  Does this yield constant-factor Pair Access?
S9  Does the bridge yield Dynamic Optimality?
S10 If the transfer route fails, does failure expose an actual unbounded real Splay family?
```

The strongest desired success is `DYNAMIC_OPTIMALITY_PROVED`.

However, failure to solve the conjecture is still a valid experiment if the exact sealed result identifies a new theorem-level obstruction or falsifies the central raw-boundary hypothesis without overclaiming.

---

# 36. Purpose questions the final report must answer

The final `MULTISCALE_TRANSFER_REPORT.md` must answer all of these explicitly.

```text
Q01 What exact parent facts were imported from v0.1 and v0.2?
Q02 Was v0.2 finally sealed before v0.3 scientific execution?
Q03 Which exact L6 version was frozen?
Q04 Which L6 objects translated definitionally and which changed semantics?
Q05 What is the exact KEEP reference-snapshot convention?
Q06 Is the strongest natural KEEP heavy-path lemma true or false?
Q07 How do positive-regret critical KEEP edges decompose into zig-zig / zig-zag / terminal zig?
Q08 Which pairing classes dominate or fail to dominate critical burden?
Q09 Which bend events align with zig-zag burden?
Q10 Which raw gap / point-gap changes align with critical burden?
Q11 Can one A rotation cause only O(1) translated structural modifications?
Q12 What event types inject candidate discrepancy credit?
Q13 What event types merely transfer it?
Q14 What makes credit ACTIVE rather than LATENT?
Q15 What exact objects distinguish the D5 exceptional repayment failures?
Q16 Did Branch A survive development?
Q17 If Branch A failed, what is its smallest exact counterexample?
Q18 Does the Branch-A obstruction inflate with scale?
Q19 Was Branch B activated under the preregistered rule?
Q20 If signed credits are used, what proves the energy lower bound?
Q21 What is the smallest finite transfer grammar that survives development under the frozen complexity order?
Q22 Does it remain stable across n and diagnostic C without changing rules?
Q23 What is the frozen theorem constant C and where did it come from?
Q24 Were H1/H2R/H3T still fresh when first consumed?
Q25 What did each fresh bank say?
Q26 Did clean-room implementation agree?
Q27 What was the strongest adversarial counterexample search result?
Q28 Which arbitrary-n rotation lemmas were actually proved?
Q29 Is bounded DELETE injection proved?
Q30 Is synchronous KEEP transfer proved?
Q31 Is integrability / global energy proved?
Q32 Does the block theorem cover every legal paired execution?
Q33 What exact Pair-Access inequality is obtained?
Q34 Does it include an additive term, and is that bridge-compatible?
Q35 Did the Levy-Tarjan convention audit pass?
Q36 What is the exact final claim level?
Q37 If no positive theorem, did any actual Splay ratio family grow?
Q38 If negative branch activated, is the family closed form and diagonal-rooted?
Q39 Which failures are representation obstructions versus conjecture obstructions?
Q40 What should a subsequent paper claim, and what must it explicitly not claim?
```

---

# 37. Frozen reference notes

The final repository `CITATIONS.md` must use exact bibliographic metadata from the frozen source manifest. The specification relies on the following current roles:

```text
Sleator & Tarjan:
  ordinary Splay origin / classical context.

Levy & Tarjan, SODA 2019:
  subsequence-property / simulation-embedding route and structural guidance separating types of Splay work.

Levy & Tarjan, arXiv:1907.06310:
  approximate-monotonicity foundation / equivalence route under audited conventions.

Russo 2019:
  independent regular-access formulation: adding organizing splays should not make the original work asymptotically cheaper.

Chalermsook & Jiamjitrak 2020:
  relational potential / geometric inversion evidence that two changing BST executions can be compared directly.

Chmel et al. 2026:
  current-frontier sublogarithmic Splay analysis; reference ranks, heavy paths, heap view, lazy intervals, gaps, pairings, bends, and contracted point gaps; primary translation target, not an automatic premise.
```

Current-frontier context at the time of spec authorship:

```text
arXiv:2607.18498 v1 (submitted 2026-07-20) reports
O(log log n * (log log log n)^2)
= \tilde O(log log n)
competitiveness for Splay.
```

The v0.3 scientific target is to determine whether the special Splay-with-extra-accesses comparator permits removal of the superconstant loss in the Pair-Access setting.

---

# 38. Final frozen statement of intent

`SPLAY-AM-MST-v0.3` is not a third attempt to fit a prettier scalar potential.

It is a direct attack on the remaining structural bottleneck exposed independently by:

```text
- exact KEEP-cycle critical geometry;
- exact failure of static feature languages;
- the global-too-large / local-too-small potential scale mismatch;
- exact DELETE-creation versus KEEP-repayment failures;
- Bellman future-debt semantics;
- recency-V blindness;
- the 2026 need for heavy paths, lazy intervals, boundary pairings, and contracted gaps;
- the Levy-Tarjan subsequence/approximate-monotonicity route.
```

The experiment's core hypothesis is:

> **The missing constant-factor proof is a local multiscale conservation law of synchronous Splay, not primarily a static amount-of-disagreement statistic.**

The implementation is therefore designed to discover or refute a rotation-level causal transfer calculus, freeze it before fresh validation, and then either prove it for arbitrary `n` or preserve the exact obstruction that killed it.

The strongest positive endpoint is:

```math
\boxed{
\operatorname{Splay}(Y,T)
\le
C\operatorname{Splay}(X,T)
\quad\forall T,\;\forall X,\;\forall Y\preceq X
}
```

for one universal finite `C`, followed by the audited Levy-Tarjan bridge to Dynamic Optimality.

The strongest negative endpoint is an explicit closed-form family with unbounded real Splay subsequence overhead.

Everything in between is evidence, structure, or obstruction — and is labeled accordingly.

**End of frozen implementation specification.**
