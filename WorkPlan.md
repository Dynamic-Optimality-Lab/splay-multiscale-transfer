# WorkPlan.md — SPLAY-AM-MST-v0.3 Multiscale Synchronous Transfer

**Experiment:** `SPLAY-AM-MST-v0.3` — Multiscale Synchronous Transfer, Causal Discrepancy Ledgers, Constant-Factor Pair-Access
**Implementation repo:** `Dynamic-Optimality-Lab/splay-multiscale-transfer`
**Parent repo:** `Dynamic-Optimality-Lab/splay-bellman-debt`
**Normative spec:** `IMPLEMENTATION_SPEC_v0.3.md` as issued (`PRE_FREEZE_PARENT_PIN_REQUIRED`)
ratified by `SPLAY_AM_MST_IMPLEMENTATION_SPEC_v0.3.1_PIN.md` (v0.3.1 parent-pin freeze;
the v0.3 text itself is byte-identical, never edited in place)
**Secondary ancestor:** `SPLAY-AM-PD-v0.1`, sealed commit `6de1ca2a595e8895f54794f3a211fe6ee1a95a80`
**Pinned parent seal (verified 2026-09-23, ratified in v0.3.1 PIN amendment):**
`38c1be6afd2ab2420aa094c68ce45ee6a26b3628` (short `38c1be6`), terminal claim
`FINITE_DEBT_LAW_MINING_RESULTS`, with `FINAL_RESULT`/manifest/archive/route-audit
SHA-256 hashes recorded in `prereg/parent_contract.yaml` and the PIN amendment
**Parent firewall states (verified):** H1 `EMPTY`, H2R `BANK_COMMITTED/unlocks=0`, n8 `PARTIALLY_REVEALED_CANARY_CONTAMINATED`
**Parent chain aides verified in log:** `b444f6a` (WP-1), `08dc1a7` (WP2), `19245ab` (WP3), `f131b14`/`1821865` (WP-4), `29de3df` (WP-5)
**WorkPlan text frozen:** 2026-09-23 (plan-document freeze; the experiment preregistration freeze completes only at `FOUNDATION_FROZEN`)
**Work-phase count:** 7 (`WP-0` … `WP-6`). The normative spec has 20 phases; the workload is large, so the instruction "5–6 phases or more if needed" is exercised: 7 work packages are the minimal flawless partition: every spec phase has exactly one accountable owner, while every section, gate, threat, stop, test, and invariant is covered with the multiplicity allowed by the specification, without splitting atomic firewalls. Coverage is verified by the matrices in §8 below.

---

## 0. Reading guide / non-omission guarantee

This WorkPlan is a **practical-implications partition** of the normative spec, not a replacement for it. Every normative rule still binds. The partition was verified as follows:

1. Listed all 20 spec phases (00–19) and assigned each exactly one accountable owner WP
(§8.1). A WP may produce prerequisite artifacts consumed by the owning WP (e.g. WP-1
rotation expansions feed WP-2-owned Phase 04 science); accountability is never shared.
Cross-cutting controls (threats, stops, invariants, shared test families) may have
multiple owning WPs, as the specification itself supports multi-owner controls.
2. Listed all spec sections 0–38 and assigned each to at least one WP (§8.2).
3. Listed all theorem obligations `MST0-01…26`, transfer gates `MST-GATE-0…21`, threats `T01…T90`, stops `STOP-01…50`, named tests, and invariants `INV-001…070`, and mapped each to its owning WP (§8.3–§8.6).
4. Checked that firewall transitions (`EMPTY → BANK_COMMITTED → TRANSFER_CALCULUS_FROZEN → UNLOCKED_ONCE`, at most one unlock) are never split across WPs in a way that would allow a read-before-freeze.
5. This file plus `Path.md` plus the commit history is the audit trail. `Path.md` records, per WP, what was actually implemented and whether it follows this WorkPlan verbatim, with deviations versioned (never silent).

**Models / learning policy (applies to all WPs).** v0.3 trains **no statistical/ML models** (no neural nets, no regressors, no embeddings as authority). The "models" in the user's sense are **transfer calculi**: finite-alphabet local conservation laws (rule templates `T1…T10`, §11) instantiated by **exact** SAT/SMT/ILP/flow solvers. "Training benchmarks" = frozen development corpora only. "Brutally tested by benchmarks ENTIRELY different from the training benchmarks" is implemented as: (a) disjoint internal-validation split (n=7 critical, n=6–7 noncritical, generated-history validation mask — different states, cycles, histories, never used for synthesis); (b) contaminated-n8 validation (different size, contaminated label, never fresh); (c) genuinely fresh banks H1/H2R/H3T (generated/committed before synthesis, unlocked at most once, post-reveal edits get new IDs and are never called fresh-tested); (d) clean-room reimplementation + large-n adversarial search (n=16…256, all nine modes: uniform, structured, hill-climb, annealing, genetic, rotation-neighborhood, cycle-splicing, motif-inflation, counterexample-generalization — §13/§16); (e) constant-ladder stability check (same frozen rules evaluated at C ∈ {2,3,4,6,8,12,16,24,32,64} without rule mutation); (f) mutation controls (every suite must catch injected corruptions); (g) exact arithmetic throughout (integers/`Fraction`, symbolic log handling; floats visualization-only). Any single exact residual rejects that candidate at the frozen C — no statistical outranking. This anti-overfitting contract is repeated per WP where it binds, and enforced by firewalls + `STOP-10/17/18/19/22/23/24/25/26/27/28/29/30/31` + tests `TR-*`, `HLD-*`, `LED-*`.

**Stale-results policy.** The implementation repo at clone time contained only `LICENSE` (1 commit) — i.e. **zero prior scientific results**, so there was nothing stale to carry over. This WorkPlan mandates: `artifacts/v03/` contains **only** newly computed v0.3 outputs. Any unexpected pre-existing file found there during WP-0 is **quarantined outside the authoritative `v03` result namespace and hash-logged** (never silently deleted, never merged into results); if quarantine is impossible the run fails closed. This respects the seal rule that unexpected scientific artifacts are retained with status and failed experiments/counterexamples are never deleted to make the archive clean. Parent results are never copied as v0.3 results; they live read-only under `parent/` with hashes. Failed calculi/counterexamples are append-only, never deleted (§19-seal rule).

**Commit/push policy.** Every WP ends with `VERIFY → COMMIT → PUSH` per the deterministic order in §21 of the spec. No failed run is deleted to make a gate pass. Standing instruction (user): commit and push without being asked each time.

---

## WP-0 — Foundation freeze: parent pin, literature, contract, repo skeleton, theorem ledger, controls

**Covers spec:** `PHASE 00` fully; §§2, 3, 17, 18, 19 (prereg files), 21 (order), 23 (threats), 24 (foundation tests), 25 (foundation invariants), 27, 28, 29, 30 (stops). Initiates `MST0-01` (parent-transport statement setup; proof + review owned by the WP-1 pre-consumption subgate), `MST-GATE-0` (definitions-total setup), gates `FOUNDATION_NOT_FROZEN` / `PARENT_CHAIN_VERIFIED` preconditions.

### Scope (what and why)
Create the immutable boundary before any scientific output exists: pin the final v0.2 seal + v0.1 ancestor chain, bootstrap `parent/` read-only, freeze literature L0a/L0b/L1–L6 bytes/versions, freeze the normative spec + all prereg YAMLs + hashes, initialize `math/proof_status.json` (`MST0-01…26` → `UNPROVED`), freeze threat/stop/split/claim matrices, verify H1/H2R/n8 firewall states **without reading contents**, and lay the deterministic repo skeleton (§18) with logging, schemas, and foundation tests. No `PHASE 01+` scientific execution is permitted until the WP-0 gate passes (`PARENT_NOT_FINAL` otherwise).

### Files to be made (exact paths)
- `IMPLEMENTATION_SPEC_v0.3.md` (byte copy of v0.3 as issued — never edited in place) +
  `SPLAY_AM_MST_IMPLEMENTATION_SPEC_v0.3.1_PIN.md` (ratified parent-pin amendment that
  discharges `PRE_FREEZE_PARENT_PIN_REQUIRED`; included in `prereg_sha256.txt`) +
  `CITATIONS.md`, `CHANGELOG.md`, `README.md`, `LICENSE` (keep), `pyproject.toml`, `requirements-lock.txt`, `.gitignore`
- `parent/`: `V01_SEAL.json`, `V02_SEAL.json` (full 40-char commits), `V01_FINAL_RESULT.json`, `V02_FINAL_RESULT.json`, `V01_MANIFEST.sha256`, `V02_MANIFEST.sha256`, `V01_ARCHIVE.sha256`, `V02_ARCHIVE.sha256`, `V02_H1_FIREWALL.json`, `V02_H2R_FIREWALL.json`, `import_ledger.json`, `BOOTSTRAP_MANIFEST.sha256` (then read-only)
- `prereg/`: `experiment_v0.3.yaml`, `parent_contract.yaml` (full commit + `FINAL_RESULT`/
  manifest/archive/route-audit/normative-set hashes + firewall states), `constant_policy.yaml`, `solver_backends.yaml` (backend freeze record; synthesis stays blocked until populated), `l6_translation_v0.3.yaml` (fully populated translation contract: exact frozen L6 source definitions or source-section/lemma identities, Pair-Access object definitions, per-object mapping status `UNRESOLVED_PRE_PROOF` (resolvable to `SAME`/`MODIFIED`/`NOT_APPLICABLE` only by WP-2 proof with preserved justification; a refuted proposed equivalence is recorded separately with its counterexample artifact, never as a status value), exact tie and reference-snapshot semantics, proof-obligation identifiers, implementation mapping schema, known semantic-difference fields — WP-0 freezes language + proposed definitions; WP-2 determines validity but may not introduce a new definition/object without a new mapping version), `event_ontology_v0.3.yaml` (fully populated ontology contract: S8+S10 language — event fields, regret layers, zig context, S0–S5, provenance alphabet, credit lifecycle, support allowed/forbidden, target-blindness), `transfer_grammar_v0.3.yaml` (fully populated grammar contract: credit/support schemas, T1–T10 with record fields, complexity bounds, branch permissions with Branch B preregistered now per §11.4, forbidden escapes, solver objective hierarchy and certificate policy) — all three immutable after the WP-0 seal; later phases instantiate this language via freeze certificates and never extend it, `cycle_corpus_policy.yaml`, `holdouts.yaml`, `theorem_gate_matrix.yaml` (all 26 obligations with owner, FIRST consumer, required status before consumption — `REVIEWED` when applicable; `NOT_APPLICABLE` only with preserved justification; `BLOCKED` forbids consumption — proof/review artifacts, controls), `threat_control_matrix.yaml` (T01–T90 each ≥1 control), `stop_control_matrix.yaml` (STOP-01–50), `discovery_splits.yaml`, `allowed_claims.md`, `forbidden_claims.md`, `prereg_sha256.txt`
- `math/`: `definitions_v0.3.md`, `L6_PAIR_ACCESS_MAPPING.md` (skeleton), `theorem_MST*.md` stubs (26 files per §18), `proof_status.json`, `reviews/REVIEW_TEMPLATE.md` (required fields for every `REVIEWED` verdict)
- `schemas/`: all 13 schemas listed in §18 (`parent_import`, `rotation_event`, `l6_object`, `cycle_trace`, `provenance_packet`, `ledger_credit`, `transfer_rule`, `transfer_calculus`, `solver_certificate`, `holdout_commitment`, `counterexample`, `theorem_review`, `final_result_v0.3`)
- `scripts/run_phase00.py` (+ `run_phase01..19` stubs, `reproduce_all_v0.3.py`), `tests/test_foundation.py` (`PARENT-01…08`), `artifacts/v03/STALE_CLEARANCE.json`, `artifacts/v03/logs/`, `artifacts/v03/seal/`
- `WorkPlan.md` (this file), `Path.md` (tracker, created here, updated every WP)

### Code to be produced and how to code it
- `python/inherited/bootstrap_parent.py`: single authorized transaction — verifies the FULL
`38c1be6afd2ab2420aa094c68ce45ee6a26b3628` commit plus `FINAL_RESULT`/manifest/archive/
route-audit/normative-set hashes against `parent_contract.yaml` and the v0.3.1 PIN amendment,
copies sealed parent artifacts by hash, writes `BOOTSTRAP_MANIFEST.sha256`, sets read-only.
Verifies `FINAL_RESULT.terminal_claim == FINITE_DEBT_LAW_MINING_RESULTS`,
`H1.state == EMPTY`, `H2R.unlocks == 0`; any mismatch → emit `PARENT_SEAL_MISMATCH`,
exit non-zero (a short-SHA match alone never passes). No parent file is ever edited in place.
- `python/audit/verify_parent.py` + `check_prereg.py`: recompute every hash in `prereg_sha256.txt`, assert `set(threat_ids)=={T01..T90}`, `set(stop_ids)=={STOP-01..STOP-50}`, every control exists; assert no `artifacts/v03/**` scientific output predates prereg hash (mtime + git-log check).
- `python/audit/log.py`: append-only run-record writer emitting every field of §27 (experiment/phase/branch/UTC/commit/parent commits/spec+prereg+literature+gate-matrix SHAs/firewalls/calculus/C/deps/command/input+output+stdout+stderr hashes/wall/peak/exit/status).
- Coding rules: Python 3.12+ baseline (3.13.7 actually used and frozen in lock file; 3.12 was a recommended baseline, not a semantic constraint); stdlib + `zstandard`, `jsonschema`, `sympy` only for WP-0; exact integer arithmetic; deterministic sorted iteration everywhere; `ruff`/compile check.
- Verification vocabulary (used in every WP): **INDEPENDENT_COMPUTATIONAL_VERIFICATION** =
two differently-structured code paths agreeing on outputs (plus hash/seed records). This is
necessary but NEVER sufficient for a theorem `REVIEWED` verdict. **Theorem review** is a
separate human-owned act recorded in `math/reviews/MST0-XX.review.json` per
`math/reviews/REVIEW_TEMPLATE.md` and `schemas/theorem_review.schema.json`: theorem SHA,
verbatim statement + domain, hypotheses checked, proof-dependency audit, case-completeness
audit, computational evidence (supporting only), objections + resolutions, reviewer
identity/role/date, verdict `ACCEPT`/`REJECT`/`BLOCKED`. `REVIEWED` never means externally
peer reviewed. Reviews that inspect only status/keywords are rejected by seal audit.

### Benchmarks + anti-overfitting
- No synthesis in WP-0, hence no training. Solver backends are nevertheless frozen this early
by record: `prereg/solver_backends.yaml` pins the backend freeze format (exact version,
binary/package hash, seed/thread policy, parameter-file hash, certificate capability,
discovery-only vs authoritative-after-replay) and synthesis stays blocked until at least
one backend entry is frozen (existing `STOP-22/23` + `TR-01/03/04`; no new stop ID).
- Benchmarks are **verification gates**: `PARENT-01…08` (full commit/manifest/ancestor-chain/H1/H2R/n8/theorem-ledger-hash/no-pre-prereg-output), `SEAL-02/03/04/05`, `L6-01` (source-version hash). Test data is the parent seal itself — entirely different from anything v0.3 will later synthesize — plus mutation probes (corrupt one hash → suite must fail).
- Anti-overfit: nothing to overfit yet; the control is temporal — prereg hashes freeze **before** any target inspection (`STOP-05`, `TR-01`).

### Gate emitted
`FOUNDATION_FROZEN` (all Phase-00 checkboxes **plus** the ratified v0.3.1 parent pin)
or `FOUNDATION_NOT_FROZEN` / `PARENT_NOT_FINAL` / `PARENT_SEAL_MISMATCH`. Blocks WP-1+ on failure; WP-1's pre-consumption subgate then requires `MST0-01 == REVIEWED` before certified consumption.

---

## WP-1 — Exact pair dynamics + rotation traces + parent reverification (the trusted core)

**Covers spec:** `PHASE 01`, `PHASE 03`, plus prerequisite rotation-expansion artifacts
consumed by WP-2-owned `PHASE 04`; §§4 (Pair-Access contract), 5 (rotation contract),
9.4 (expansion); owns `MST0-02` (refinement), `MST0-04` (reference-snapshot legitimacy),
provides rotation-determinism prerequisites/evidence for `MST0-10` (theorem owner: WP-3),
`MST0-16` (partition preamble); `MST-GATE-2`.
**Entry:** `FOUNDATION_FROZEN`.
**Pre-consumption subgate (before any certified parent fact is consumed theorem-facing):**
inside WP-1, prove `theorem_MST01_parent_transport`, run INDEPENDENT_COMPUTATIONAL_VERIFICATION,
conduct human theorem review per `REVIEW_TEMPLATE.md`, and record `MST0-01 → REVIEWED`.
Only then may WP-1 consume certified parent facts (transitions, ratios, cycles, derivatives)
theorem-facing. This placement is semantically clean: Phase 01 is literally where the
inherited pair dynamics and parent claims are independently reverified. No certified parent fact
(parent transitions, ratios, cycles, derivatives) is consumed theorem-facing before the
parent-transport review record exists (gate matrix first-consumer rule).

### Scope
Re-derive the exact object under attack without redefining it: read-only import of parent pair/tree universes, transition tables, reachable domains n=2..7, `b_n*` certificates, critical/near-critical cycles, forced derivatives, v0.2 failure ledgers (incl. 16 D5 failures); independent reproduction (n=2..6 full, n=7 streamed); rotation-level refinement of every Pair-Access edge (ROOT/ZIG/LL/RR/LR/RL) with frozen-reference KEEP analysis order; full A-then-B expansion of all imported critical cycles; failure-mechanism table (`GLOBAL_TOO_EASY_TO_CREATE`, `LOCAL_TOO_WEAK_TO_REPAY`, etc. as evidence labels only).

### Files to be made
- `python/splay_ref/splay.py` (canonical ordinary bottom-up Splay, cost `depth+1`), `python/splay_ref/pair.py` (`K_x`/`D_x`, `w_b`/`l_b`, diagonal starts, canonical IDs), `python/splay_ref/independent.py` (second implementation, differently structured)
- `python/rotations/trace.py` (rotation serializer v0.3, event IDs per §5.5), `python/rotations/reference.py` (KEEP freeze-A1 convention + version flag), `python/rotations/blocks.py` (maximal-block partitioner)
- `python/cycles/import_parent.py`, `python/cycles/expand.py`, `python/cycles/circulation.py`
- `artifacts/v03/parent_import/` (import ledger, repro spot-checks, ratio rematches, all-KEEP recompute), `artifacts/v03/rotations/` (traces + `MST02` proof bundle), `artifacts/v03/cycles/expanded/` (per-cycle A/B traces, sharded `.json.zst` + logical-stream hashes)
- `math/theorem_MST02_rotation_refinement.md`, `math/theorem_MST04_keep_reference_snapshot.md`, `math/theorem_MST16_block_partition.md` (proof drafts + review records)
- `tests/rotations/` (`ROT-01…12`), `tests/parent/` (import + `CYC-01…05` mechanics)

### Code + how
- `splay.py`: pointer-based BST (`Node{key,left,right,parent}`), `depth+1` cost, `splay(x)` loop: while `x.parent`: case-dispatch ZIG / LL / RR / LR / RL with exact pointer rewiring; record `(case, local-key-tuple, before/after neighborhood hash)` per rotation. No path-reversal, no splay-variant drift (`INV-004/005`). Complexity O(amortized log n) per access; exhaustive n≤7 enumeration via shape grammar (Catalan) in canonical ASCII-sorted order.
- `pair.py`: `keep(A,B,x) = (splay(A,x), splay(B,x))`, `delete(A,B,x) = (splay(A,x), B)`; `w_b = y − b·a` with `Fraction`; canonical pair-state ID = `(serialize(A), serialize(B))` hashed.
- `trace.py`: wraps each access, concatenates primitive events, asserts `final_tree == parent S_x(T)` and successor equality; KEEP order = §5.2 steps 1–5 with `reference_snapshot_hash` frozen after A-splay (alternative conventions get new version IDs).
- `expand.py`: for each imported cycle edge, emits A-trace → snapshot → B-trace + placeholder ledger stream; deterministic canonical order `[n, source_state_id, cycle_length, key_word_lex]`; parallel over cycles with sorted reduce.
- Independence: `independent.py` shares **no** helper with `splay.py` (separate rotation functions); agreement gate on final tree + search path + case sequence + neighborhoods + serialization (`ROT-10`, `INV-037`, threat `T62`).
- Cost-correctness proof (`MST0-02`): states explicitly that `depth+1` ≠ rotation count; rotations are structural charging units, cost convention unchanged (`ROT-12`, `T17`).

### Benchmarks + anti-overfitting
- Training/dev: none (no synthesis). Verification benchmarks: parent `b_n*` rematch {1, 1, 3/2, 8/5, 8/5, 23/14}, reachable counts {4, 19, 196, 1764, 17424, 184041}, Bellman anchors (max U₂/V₂ table), every critical cycle closes exactly with parent ratio + recomputed all-KEEP flag. These are **entirely different** from later transfer-synthesis targets (rotation traces are target-blind: no regret/criticality/Bellman/holdout inputs — `STOP-10`, `LED-*`).
- Anti-overfit: two-implementation agreement; streamed n=7 verification (no full re-enumeration); mutation controls (flip one case label, one tie-break, snapshot order → suite must catch); n=7 reserved for validation where WP-2 needs it (`CYC-07`).

### Gates emitted
`PARENT_CHAIN_VERIFIED`, `ROTATION_TRACE_CERTIFIED` (or `ROTATION_TRACE_FAIL` / `PARENT_SEAL_MISMATCH`).
`MST0-01` reaches `REVIEWED` via the WP-1 pre-consumption subgate above (prove → independent
check → human review); `MST0-02`/`MST0-04` advance to at least `PROVED` here and must be `REVIEWED` before WP-2 consumes traces
theorem-facing (gate matrix). Required before WP-2 consumes traces theorem-facing.

---

## WP-2 — L6 translation, critical-corpus science, heavy/pairing/bend lemmas, contracted baseline

**Covers spec:** `PHASE 02`, `PHASE 04` (sole accountable owner — WP-1 supplies prerequisite
rotation-expansion artifacts), `PHASE 05`, `PHASE 06`; §§6 (translation), 8.3/8.4 (zig stratification, scales S0–S5), 9 (corpus), 13.5/§6.8 (baseline); owns `MST0-03`, `MST0-05`, `MST0-06`, `MST0-07`, `MST0-08`; `MST-GATE-1`, `MST-GATE-3`.
**Entry:** `ROTATION_TRACE_CERTIFIED` **and** `MST0-02 == REVIEWED` plus the relevant form
of `MST0-04 == REVIEWED` (gate matrix first-consumer rule for WP-2).
WP-2 executes as two strictly ordered subphases with a hard target-join barrier:

### WP-2A — Translation-only (no target data)
1. Populate `math/L6_PAIR_ACCESS_MAPPING.md` from the immutable preregistered definitions (record schema per object; the yaml itself stays `UNRESOLVED_PRE_PROOF` — resolution lives in the math doc, never as a prereg edit).
2. Resolve every mapping as `SAME` / `MODIFIED` / `NOT_APPLICABLE` (a refuted proposed equivalence is recorded separately as `proposed_equivalence_refuted: true` + counterexample artifact, never as a status value).
3. Run both translation implementations and mutation controls (`L6-10/11/12` style).
4. Prove and human-review `MST0-03` (review record per template).
5. Hash/freeze `math/L6_PAIR_ACCESS_MAPPING.md` (freeze certificate in `artifacts/v03/freeze/`, referencing the prereg yaml hash).
6. Emit `L6_TRANSLATION_FROZEN` (or scoped `L6_TRANSLATION_FAIL` / `NOT_APPLICABLE` rulings with preserved justification).
**Barrier: NO critical-cycle regret, criticality, forced-delta, Bellman, or target-valued corpus data may be joined before this gate** (`STOP-09/10`, target-leakage audit). Target-blind extraction code paths are statically barred from importing those fields.

### WP-2B — Critical-corpus science (targets allowed)
Requires `L6_TRANSLATION_FROZEN` **and** `MST0-03 == REVIEWED`. Only then: stratification, circulation, motifs, heavy-path/pairing/bend lemmas, contracted baseline.
Order: definitions → translation proof → translation freeze → target join.

### Scope
Turn L6 from inspiration into audited definitions: extract exact source definitions (ranks, heavy/light, heap view, gaps, lazy intervals, pairings, paid/free ops, bends), write `L6_PAIR_ACCESS_MAPPING.md` (same/modified/N-A per object + proof obligation), implement translation twice, prove-or-kill the KEEP heavy-path / zig-zig-pairing / zig-zag-bend / reference-rotation-locality lemmas **under the actual translated rank** (never depth-substituted), stratify critical KEEP burden by Splay-case context, compute full-cycle circulation per primitive, canonicalize cross-n motifs (order/orientation/scale/roles only), reproduce the contracted-gap baseline to see where log/loglog loss appears in Pair Access — without overclaiming it as a result.

### Files to be made
- `python/l6_translation/{rank,heavy,heap,gaps,lazy,pairing,bends,contracted,ops}.py` × 2 implementations (`primary/` + `independent/`), `python/l6_translation/mapping_check.py`
- `python/cycles/{stratify,motifs,validate_n7}.py`, `python/ontology/scales.py` (S0–S5 integer buckets), `python/provenance/d5_analysis.py` (16 D5 failures as specimens — heavier scrutiny, zero reweighting)
- `artifacts/v03/translation/` (mapping + agreement + mutant-kill logs), `artifacts/v03/cycles/{stratified,motifs,circulation}/`, `artifacts/v03/baseline/` (contracted-gap identities, loss-appearance report)
- `math/L6_PAIR_ACCESS_MAPPING.md`, `math/theorem_MST03…MST08*.md`, `KEEP_CYCLE_ATLAS.md` (draft), `L6_PAIR_ACCESS_TRANSLATION_REPORT.md` (draft)
- `tests/translation/` (`L6-02…12`), `tests/cycles/` (`CYC-06…08`)

### Code + how
- Translation: copy the frozen L6 rank definition verbatim into a mapping note; define `PA_REFERENCE_RANK` with reference tree = post-A-splay snapshot (KEEP) / appropriate A snapshot (DELETE); `PA_HEAVY_EDGE/PATH`, `PA_HEAP_*`, `PA_RAW/INTERVAL/POINT_GAP`, `PA_LAZY/GROWING/SHRINKING/BROKEN_INTERVAL`, `PA_*_PAIRING`, `PA_BEND`, `PA_CONTRACTED_POINT_GAP_L6` (baseline only) — all translation entities declared by Sections 6.1–6.9 already preregistered with proposed definitions and `UNRESOLVED_PRE_PROOF` status (resolution recorded in the math mapping doc; the yaml never changes). WP-2 proves each mapping `SAME`/`MODIFIED`/`NOT_APPLICABLE` (with preserved justification; refuted equivalences recorded separately with counterexample artifacts) and populates `math/L6_PAIR_ACCESS_MAPPING.md`; it may not introduce a new translation definition or object without a new mapping version (`T14`). `PA_`/`MST_` prefixes until equivalence `REVIEWED` (`INV-012`).
- Lemma attack: formalize `MST0-05` with exact snapshot/node/subpath/tie hypotheses; on falsification preserve smallest exact counterexample under canonical order and re-version the theorem ID (never silent repair). Same for `MST0-06/07/08` (all zig-zig / zig-zag / reference-rotation cases enumerated; `PR-01…04`).
- Stratification: per positive-regret KEEP edge store `#ZIG/#LL/#RR/#LR/#RL`, path lengths, regret per diagnostic C, pairing classes, bend deltas, gap deltas, paid-op counts; circulation `ΣΔF` per primitive with `STATE_DERIVATIVE / FLOW_COUNT / SOURCE_SINK_ACCOUNT` labels.
- Motifs: canonical predicates over relative order + orientations + scale transitions + heavy/lazy roles; n=4..6 selection → n=7 internal validation (`STOP-16/23`, `CYC-07`); top-K=128/slack∈{0,1,2} frozen, no adaptive thresholds (`CYC-08`).

### Benchmarks + anti-overfitting
- Training/dev: critical n=4..6 + near-critical selection corpus for motif predicates. Entirely-different test: critical n=7 (untouched during predicate formation), noncritical edges n=6..7, plus mutant suites (rank orientation, heavy-child choice, gap sign, lazy side, pairing order, bend orientation — suite must catch each: `L6-11/12`).
- Anti-overfit: translation code never reads Bellman targets; ontology extraction never reads regret/criticality (`STOP-10`); `MST0-03` must be `REVIEWED` before any source lemma is consumed theorem-facing (`STOP-09/13/14`); if translation loses structural advantage → `L6_BASELINE_TRANSLATION_INCOMPLETE`, dependent branches blocked, not fabricated.

### Gates emitted
WP-2A: `L6_TRANSLATION_FROZEN` (or `L6_TRANSLATION_FAIL` / scoped `NOT_APPLICABLE` rulings) — the target-join barrier. WP-2B: `CRITICAL_KEEP_CORPUS_CERTIFIED` (+ `KEEP_REGRET_LOCALIZED` / `KEEP_REGRET_DISTRIBUTED` — both non-failures), `KEEP_HEAVY_LEMMA_PROVED` or `…_FALSE_AS_STATED`, `L6_BASELINE_REPRODUCED` (or scoped incomplete).

---

## WP-3 — Causal provenance, H3T holdout, frozen ontology + transfer grammar (the pre-synthesis lock)

**Covers spec:** `PHASE 07`, `PHASE 08`, `PHASE 09`; §§8 (event ontology), 10 (ledger contract), 11 (grammar), 14 (holdouts); owns `MST0-10`, `MST0-11` (statement/setup); gates `MST-GATE-4` prep, `H3T_BANK_COMMITTED`, `TRANSFER_GRAMMAR_FROZEN`.

### Scope
Replace history with structural causal provenance (A-rotations → bounded descendants; deterministic merge; counterfactual-free; active-predicate future-blind); generate + quarantine the new 70k-episode transfer holdout H3T **before any target-guided synthesis**; freeze the multiscale event ontology (scales S0–S5, provenance alphabet, active/latent/spent/transferred, signed-transfer preconditions), the T1…T10 grammar with branch permissions (Branch A now, Branch B preregistered — not invented post-failure, `T36`), and the active-predicate language; pass a static target-leakage audit.

### Files to be made
- `python/provenance/{sources,descendants,merge,active}.py`, `python/ledger/{state,support,update,energy,flow}.py`, `python/transfer/{grammar,templates_T1_T10,branches,complexity}.py`
- `python/holdout/h3t_generate.py` (frozen generator + strata), `python/holdout/h3t_verify.py` (independent replay), `python/holdout/firewall.py` (state machine, fail-closed imports)
- `artifacts/v03/provenance/` (D5 separation analysis: boundary/zig/scale/bend/lazy/provenance/geometry predicates), `artifacts/v03/holdouts/h3t_commitment.json` (seed policy, generator hash, per-size/logical-stream hashes, manifest, replay-verifier hash, stratum counts, length distribution), quarantined bank (not in discovery path)
- `artifacts/v03/freeze/PHASE09_EVENT_ONTOLOGY_FREEZE.json`, `artifacts/v03/freeze/PHASE09_TRANSFER_GRAMMAR_FREEZE.json` — phase-freeze certificates stating preregistered ontology/grammar hashes (from WP-0 `prereg_sha256.txt`), implementation/generator hashes, freeze timestamp, and `TRANSFER_GRAMMAR_FROZEN` status; `math/theorem_MST10_ledger_determinism.md`, `math/theorem_MST11_transfer_preservation.md` (stubs + determinism proof)
- **Immutability rule (STOP-05): the WP-0 prereg files `prereg/event_ontology_v0.3.yaml`, `prereg/transfer_grammar_v0.3.yaml`, `prereg/holdouts.yaml` are NEVER edited after `prereg_sha256.txt` is sealed. WP-3 certifies/instantiates the frozen preregistration; it does not rewrite it.** `holdouts.yaml` keeps `H3T.status_at_prereg = TO_BE_GENERATED_AND_QUARANTINED` forever; the later `BANK_COMMITTED` state lives only in `artifacts/v03/holdouts/h3t_commitment.json` + the firewall artifact. Any prereg-byte change is a `STOP-05` prereg-hash-mismatch fail-closed, detectable by re-running `scripts/freeze_prereg.py`.
- `tests/provenance+ledger/` (`LED-01…10`), `tests/holdout/` (`HLD-07…10`)

### Code + how
- Provenance: every A-side rotation emits candidate source event; descendants limited to interval boundary / heavy-path relation / lazy membership / heap relation / scale-orientation packet (bounded representation); merge iff frozen ledger states identical; active predicate = finite combination of declared local/aggregate structural relations, checked against current KEEP event only (no future keys, no Bellman, no holdout labels — `STOP-19`, `LED-05`).
- Ledger: finite multiset `{τ,σ,ω,m}` with support from allowed primitives (key/interval/heavy-path/heap/lazy/boundary/bend/orientation) and arbitrary-n semantics; forbidden supports (state IDs, addresses, cycle IDs, holdout flags, timestamps, future keys, Bellman) statically rejected (`STOP-17/18`); `E(L)=Σe(q)` with n-independent `e`, known initial energy (prefer 0), proved lower bound if signed (`MST0-12` route).
- Grammar: encode T1 (move) … T10 (bend discharge) as typed rule schemas with precondition/trigger/input/output/energy-delta/regret-payment/scale-move/symmetry fields; per-rule bounds O(1) objects, O(1) outputs w/o aggregate proof, n-independent constants, relabel invariance (`TR-01/02/11/14`); signed rules quarantined to Branch B (`STOP-20/21`).
- H3T: sizes `[10,12,16,24,32,48,64]` × 10k episodes = 70k; strata `RANDOM_LEGAL, DELETE_BURST_THEN_KEEP, ALTERNATING_KEEP_DELETE, SPINE_VS_BALANCED, OPPOSITE_SPINE, ZIGZIG_ENRICHED, ZIGZAG_ENRICHED, BOUNDARY_PAIRING_ENRICHED (target-blind generator), NESTED_INTERVAL_ENRICHED, MIRROR_PAIRED, MOTIF_BLIND_RANDOM_WALK (never seeded from post-freeze counterexamples)` — 11 strata total; the 10,000 episodes per size are distributed across the 11 strata (not 10,000 per stratum); generator uses only frozen-ontology structural predicates, never candidate residuals (`T59`); bank quarantined, discovery imports fail closed (`STOP-29`).

### Benchmarks + anti-overfitting
- No synthesis yet, so no training. Entirely-different-test principle is **enforced structurally**: H3T committed before synthesis; firewall `EMPTY → BANK_COMMITTED`; independent Splay core replays legality + rotation traces (sample/full-streamed); static audit proves ontology extraction cannot import regret/criticality/Bellman/candidate/holdout fields.
- Anti-overfit: grammar frozen before target search (`TR-01`); Branch B exists already so later activation is discipline, not invention (`STOP-20`); D5-16 analysis is specimen-driven, unweighted.

### Gates emitted
`CAUSAL_PROVENANCE_CERTIFIED` (or `…_INSUFFICIENT` + witnesses), `H3T_BANK_COMMITTED`, `TRANSFER_GRAMMAR_FROZEN`. All three required before WP-4 reads any development target.

---

## WP-4 — Transfer synthesis: Branch A attack, Branch B fallback, negative triage, adversarial stress (where "training" happens — and is brutally tested)

**Covers spec:** `PHASE 10`, `PHASE 11`, `PHASE 12`, `PHASE 13`; §§12 (solver policy), 13 (raw-damage target); owns `MST0-09` (raw-boundary statement), `MST0-12` (signed-bound setup); gates `MST-GATE-5/6/7/8/9`.

### Scope
**Train** (synthesize) raw-boundary transfer laws on development only, then signed-multiscale only if Branch A is exactly refuted; generalize every decisive counterexample toward parameterized motifs and triage the negative branch on actual Splay ratios (never residuals); stress survivors across the diagnostic constant ladder and a broad adversarial development battery. One exact residual at the frozen C rejects that candidate at that C (see gate semantics below) — no fit outranks a violation.

### Files to be made
- `python/solver/{encode_sat,smt,ilp,flow,certify}.py` (exact back ends; floats guide-only), `python/transfer/{branchA,branchB,ladder}.py`, `python/adversary/{generators,hillclimb,anneal,genetic,neighborhood,splice,inflate,generalize}.py`
- `artifacts/v03/transfer_grammar/` (frozen inputs), `artifacts/v03/solver/` (assignments + replay logs + unsat certificates / second-solver confirmations), `artifacts/v03/hypotheses/MSTC-*.json` (dev-status calculi, never fresh-tested), `artifacts/v03/adversarial/` (families, `R_k` tracks, smallest/maximum violations, minimal inconsistent subsystems)
- `math/theorem_MST09_raw_boundary.md`, `math/theorem_MST12_signed_lower_bound.md` (conjecture records + obstruction witnesses), `COUNTEREXAMPLE_ATLAS.md` (draft, append-only)
- `tests/transfer/` (`TR-03…14`), `tests/proof/` (dev-side `PR-05/06` checks)

### Code + how
- Synthesis inputs (frozen selection): critical n=4..6, near-critical selection, noncritical n=2..5, generated-history selection mask. **Held-out validation (never synthesized on)**: critical n=7, noncritical n=6..7, generated-history validation mask. Objective hierarchy is lexicographic (§12.3): exact local-conservation/payment coverage → critical-cycle satisfaction → bounded injection → repayment → cross-n survival → cross-C stability → simplicity (fewest templates/types/radius). No statistical fit outranks exact coverage (`T40`).
- Constraints per candidate: bounded A-injection, determinism, nonnegative raw energy (Branch A), exact repayment at frozen diagnostic C or symbolic budget, cycle consistency, relabel/mirror covariance, no hidden state lookup. Solver outputs replayed by independent exact checker (`TR-03`); UNSAT confirmed by certificate or second formulation/exhaustive witness (`TR-04`); every failure preserves minimal inconsistent subsystem + smallest counterexample under canonical order (`TR-09/10`).
- Branch B activation: **only** if Branch A rejected by exact evidence **and** Branch-B grammar was frozen in WP-3; joint search for signed rules + global lower-bounded energy + bounded init/injection/repayment; scale-circulation checks on critical cycles.
- Negative triage: motif inflation per decisive counterexample → parameterized family; track only real `R_k = Σc_B/Σc_A`; activation needs N1–N5 (legal, explicit construction, growing actual ratio/b, independent replay, diagonal-rooted plausibility); "worst solver state per k" rejected (`T53/NEG-*`).
- Ladder/stress: frozen rules evaluated across C ∈ ladder **without rule edits**; adversarial battery (spines, opposite spines, balanced/spine, zig-zag runs, zig-zig enrichment, nested intervals, rank-gap extremes, boundary enrichment, DELETE-bursts-then-KEEP, repeated KEEP cycles, mirrors, rotation neighborhoods, dev-failure motif inflation) via **all nine spec-required search modes, each with a distinct run record** — (1) uniform legal histories, (2) structured generators, (3) hill climb, (4) simulated annealing, (5) genetic search, (6) rotation-neighborhood search, (7) cycle splicing, (8) motif inflation, (9) counterexample generalization; additional engines permitted, and two modes may share one code module only if both still emit distinct run records; heuristics propose, exact evaluator disposes (`INV-038`); zero exact violations at frozen C required to advance.

### Benchmarks (training vs ENTIRELY different testing) + anti-overfitting
- **Training benchmarks:** selection corpora above + solver-dev splits from `discovery_splits.yaml`.
- **Entirely different test benchmarks:** (i) internal validation split (different n/cycles/histories); (ii) cross-C stability/feasibility (same frozen rules evaluated across the diagnostic ladder — note larger C eases the competitive inequality, so this checks stability, not "hardness"); (iii) cross-branch check (raw failure ≠ signed failure, `MST0-24`); (iv) motif-inflation scale growth (different sizes); (v) later WPs' fresh banks + large-n + clean-room (WP-5, never touched here). Gate semantics: one exact residual at the frozen C **rejects that candidate at that C** — it does not by itself kill the underlying structural rule family, which the preregistered ladder explicitly permits re-testing at a larger C **without changing any rule** (a rule change creates a new calculus ID). Overfitting controls: target-blind ontology + frozen grammar + ID-immutable calculi + append-only counterexamples + minimal-unsat preservation + exact-replay discipline + `STOP-22/23/24/34/35` + `TR-*`/`NEG-*` suites. Diagnostic C=2 never mistaken for theorem constant (`T41`, `INV-007`).

### Gates emitted
Exactly one of `RAW_BOUNDARY_LAW_SURVIVES_DEV` / `RAW_BOUNDARY_LAW_REJECTED` / `RESOURCE_LIMIT_NO_CLAIM` … similarly `SIGNED_TRANSFER_{NOT_ACTIVATED,SURVIVES_DEV,REJECTED}` … normally `NEGATIVE_FAMILY_NOT_ACTIVATED` (or `NEGATIVE_CYCLE_FAMILY_CANDIDATE` if N1–N5 pass). Survivors capped at ≤3 primary calculi for WP-5 (frozen complexity order).

---

## WP-5 — Freeze candidates, consume fresh holdouts once, clean-room + large-n falsification

**Covers spec:** `PHASE 14`, `PHASE 15`, `PHASE 16`; §§14.6/14.7 (validation order, post-reveal mutation), 15 (calculus contract); owns `MST0-22` (constant independence), `MST0-25` (holdout scope); gates `MST-GATE-10/11/12/13/14/15`.

### Scope
Convert ≤3 dev survivors into frozen theorem hypotheses (full §15 metadata + one universal proof-derived C, conservative allowed; proof-outline with reference-locality/injection/zig-zig/zig-zag/boundary/lower-bound/integrability/telescope decomposition — solver-only objects without outlines are not promoted); hash the candidate set (H3T `BANK_COMMITTED → TRANSFER_CALCULUS_FROZEN`); consume each compatible fresh bank **exactly once** in schema order (state-only: n8-contaminated → H1 → H3T; causal: H2R → H3T) with full exact evaluation + independent replay; then try to murder survivors via clean-room reimplementation and large-n adversarial search. No candidate mutation inside evaluation; any post-reveal change → new ID + `POST_HOLDOUT`.

### Files to be made
- `artifacts/v03/hypotheses/MSTC-*.json` (frozen: calculus_id, parent, branch, ontology/mapping versions, credit/support/scale defs, active predicate, injection/transfer/cancellation/repayment rules, energy/flow statement, lower-bound claim, C, init, obligations, eligibility) + `candidate_set_commit.json`
- `artifacts/v03/holdouts/{h1,h2r,h3t}_reveal.json` (first/maximum violations, failure classes, replay bundles, ledger before/after, event traces) — truthful reveal-state labels, never "fresh" after reveal
- `python/holdout/{h1,h2r,h3t}_evaluate.py` (frozen-calculus-only imports), `python/audit/cleanroom.py` (receives only math + contracts + histories; zero discovery imports), `python/adversary/large_n.py`
- `tests/holdout/` (`HLD-01…12`), `tests/proof/` (holdout-scope `PR-*`)
- `TRANSFER_CALCULUS_LEDGER.md` (draft)

### Code + how
- Freeze: validate eligibility (arbitrary-n definition, no state/cycle/holdout IDs, no U/V/G, no n-constants, no future info, relabel invariance, tie semantics, determinism, finite support, lower-bound route, n-independent C); changing any listed field → new calculus ID (`TR-11`, `INV-028`).
- Evaluate: every eligible state/transition/episode exactly (`Fraction` residuals); canonical-order first violation + maximum violation + class + replay bundle; clean-room evaluator replays each violation from math alone; large-n sweep n ∈ {16,24,32,48,64,96,128,192,256} (resources permitting) with exact-replay of claimed violations only.
- Mutation: flip one credit sign / scale level / activation predicate / transfer output / injection coefficient / C / mapping choice / zig classification → suite must catch (`LED-10`, `TR-13`).
- Firewalls: candidate-set hash immutable after reveal (`HLD-11`); second-unlock attempts fail closed (`STOP-30`); H3T regeneration after reveal forbidden (`STOP-31`); clean-room importing discovery fails the seal (`STOP-32`).

### Benchmarks + anti-overfitting
- **Training:** nothing new (candidates frozen). **Entirely different tests:** fresh banks (H1 state-pair, H2R replay-history, H3T 70k transfer episodes across 7 sizes × 11 strata) + large-n families + clean-room agreement. These distributions, sizes, histories, and implementations are disjoint from synthesis. Anti-overfit is the firewall itself: one unlock, no adaptation, new-ID-on-edit, independent replay, mutation-caught suites.

### Gates emitted
`TRANSFER_CALCULUS_FROZEN` (or `REPRESENTATION_INCONCLUSIVE`), `FRESH_H1_{PASS,FAIL}` / `FRESH_H2R_{PASS,FAIL}` / `FRESH_H3T_{PASS,FAIL}` (survival ≠ theorem), ceiling `TRANSFER_CALCULUS_SURVIVES_FINITE_TESTS`.

---

## WP-6 — Universal proof, bridge/negative theorem, seal + release

**Covers spec:** `PHASE 17`, `PHASE 18`, `PHASE 19`; §§7 (ledger MST0-01…26 closure), 16 (arithmetic), 26 (scaling), 31 (ladder MST-GATE-16…21), 32–35 (interpretation, claims, seal checklist, success criteria), 36 (Q01–Q40), 37–38; owns `MST0-13/14/15/17/18/19/20/21`.

### Scope
Stop mining, prove for arbitrary n (at most one primary candidate at a time): well-definedness, reference locality, injection, zig-zig transfer, zig-zag/bend payment, boundary theorem, signed lower bound, integrability, n-independence, no-finite-premise; then block Pair Access → approximate monotonicity → audited Levy–Tarjan bridge to dynamic optimality, **or** the closed-form unbounded real-Splay negative family + reverse-bridge audit; then seal (`FINAL_RESULT` from artifacts only, fresh-checkout reproduction, deterministic archive, paper-facing reports).

### Files to be made
- `math/theorem_MST13_delete_injection.md` … `math/theorem_MST26_literature_scope.md` (proofs + `PROVED → REVIEWED` records; `BLOCKED` where prerequisites fail — never silently consumed)
- `math/proof_status.json` (final lifecycle audit: no `UNPROVED → REVIEWED` jumps, every status has proof/review pointer)
- `artifacts/v03/proofs/` (per-lemma bundles), `artifacts/v03/audits/` (threat/stop/test/invariant audits), `artifacts/v03/seal/{FINAL_RESULT.json,MANIFEST.sha256}` + `SPLAY-AM-MST-v0.3.tar.zst` (+ `.sha256`, shard manifests + logical-stream hashes)
- Reports: `MULTISCALE_TRANSFER_REPORT.md` (answers Q01–Q40), `KEEP_CYCLE_ATLAS.md`, `L6_PAIR_ACCESS_TRANSLATION_REPORT.md`, `TRANSFER_CALCULUS_LEDGER.md`, `COUNTEREXAMPLE_ATLAS.md`, `THEOREM_STATUS_REPORT.md`, `REPRODUCIBILITY.md`, `AI_USE.md`
- `scripts/reproduce_all_v0.3.py` (fresh-checkout reverification), `tests/seal/` (`SEAL-01…12`), `tests/proof/` (`PR-01…14`), `tests/mutation/`

### Code + how
- Proofs: arbitrary-n, case-complete (ROOT/ZIG/LL/RR/LR/RL + every ledger/lazy op), exact arithmetic/symbolic logs (`SIGN_UNCERTIFIED` on straddling intervals, never PASS), block partition covering every execution exactly once (`MST0-16`), telescope `Splay(Y)+E_m−E_0 ≤ C·Splay(X)+A(n)` with `A(n)=0` preferred (bounded `O(n)` only if bridge-compatible and audited), universal C independent of n/length/tree/holdout/panel (`MST0-22`, `PR-11`).
- Bridge audit (`MST0-19`): Splay variant, cost/initial-tree/subsequence/additive-term/constant-independence/direction/version — only then `UNIVERSAL_PAIR_ACCESS_LEMMA_PROVED → APPROXIMATE_MONOTONICITY_PROVED → DYNAMIC_OPTIMALITY_PROVED`.
- Negative path (`MST0-20/21`): closed-form `(T_k,X_k,Y_k)`, `Y_k ⪯ X_k`, symbolic `Splay(X_k)≤f(k)`, `Splay(Y_k)≥g(k)`, `g/f→∞`, diagonal-rooted legality, independent replay; transfer residuals never substitute for Splay costs (`STOP-34/35`).
- Seal: `FINAL_RESULT` generated from artifacts (exactly one terminal claim level); fresh checkout re-verifies parent/literature/traces/cycles/ontology/commitments/counterexamples/gates and recomputes the result; deterministic archive (canonical order, normalized metadata, `.json.zst` sharding >GitHub limits); failed artifacts retained (deletion = seal failure, `STOP-48`).

### Benchmarks + anti-overfitting
- **Training:** none. **Tests:** the proof itself (infinite domain) + fresh-checkout reproduction + `SEAL-*`/`PR-*`/`NEG-*` suites + threat/stop lifecycle audits. Anti-overfit at the theorem level: no finite premise in universal proofs (`STOP-36`), full case coverage (`STOP-37/38`), no hidden n-dependence (`STOP-39`), proved integrability/lower-bound/partition (`STOP-40/41/42`), audited bridge (`STOP-43/44/45`).

### Gates emitted (terminal)
One of: `BOUNDED_DELETE_INJECTION_PROVED`, `SYNCHRONOUS_KEEP_TRANSFER_PROVED`, `UNIVERSAL_PAIR_ACCESS_LEMMA_PROVED`, `APPROXIMATE_MONOTONICITY_PROVED`, `DYNAMIC_OPTIMALITY_PROVED`, `NEGATIVE_REAL_SPLAY_FAMILY_PROVED` / `DYNAMIC_OPTIMALITY_DISPROVED`, or finite/inconclusive levels (`…_RESULTS`, `TRANSFER_CALCULUS_SURVIVES_FINITE_TESTS`, `RESOURCE_LIMIT_NO_CLAIM`, `REPRESENTATION_INCONCLUSIVE`). Exactly one theorem-facing branch active in `FINAL_RESULT`.

---

## 8. Verification matrices (nothing omitted)

### 8.1 Spec PHASE → WP (each spec phase owned exactly once)
| Spec phase | Owner | Gate |
|---|---|---|
| 00 Freeze parent/literature/contract/obligations | WP-0 | FOUNDATION_FROZEN (incl. v0.3.1 pin; MST0-01 still must reach REVIEWED before WP-1 consumption) |
| 01 Reverify pair dynamics + failures | WP-1 (entry: FOUNDATION_FROZEN; pre-consumption subgate: MST0-01 REVIEWED) | PARENT_CHAIN_VERIFIED |
| 02 L6 translation freeze+proof | WP-2 (entry: MST0-02 + relevant MST0-04 REVIEWED; WP-2A translation-only before any target join, then WP-2B) | L6_TRANSLATION_FROZEN (WP-2A gate) |
| 03 Rotation traces | WP-1 | ROTATION_TRACE_CERTIFIED |
| 04 Critical corpus at rotation level | WP-2 (sole owner; WP-1 supplies prerequisite expansion artifacts) | CRITICAL_KEEP_CORPUS_CERTIFIED |
| 05 Heavy/pairing/bend lemmas | WP-2 | lemma REVIEWED set |
| 06 Known-loss baseline | WP-2 | L6_BASELINE_REPRODUCED |
| 07 Causal provenance | WP-3 | CAUSAL_PROVENANCE_CERTIFIED |
| 08 H3T generation+quarantine | WP-3 | H3T_BANK_COMMITTED |
| 09 Ontology+grammar freeze | WP-3 | TRANSFER_GRAMMAR_FROZEN |
| 10 Branch A solve (dev) | WP-4 | RAW_BOUNDARY_* |
| 11 Branch B solve (if triggered) | WP-4 | SIGNED_TRANSFER_* |
| 12 Counterexample generalization/triage | WP-4 | NEGATIVE_* |
| 13 Larger-scale loss attack | WP-4 | dev-zero-violations @ frozen C |
| 14 Freeze candidate+constant | WP-5 | TRANSFER_CALCULUS_FROZEN |
| 15 Fresh holdouts once | WP-5 | FRESH_H*_PASS/FAIL |
| 16 Clean-room + large-n falsification | WP-5 | SURVIVES_FINITE_TESTS (ceiling) |
| 17 Universal rotation-level proof | WP-6 | INJECTION/TRANSFER_PROVED |
| 18 Pair Access / bridge / negative theorem | WP-6 | PA/APPROX/DO PROVED or NEGATIVE PROVED |
| 19 Seal/reproduce/package/release | WP-6 | FINAL_RESULT sealed |

### 8.2 Spec section → WP
0 purpose → WP-0/6 (reports); 1 scope/question → WP-0/2/4/6; 2 lineage → WP-0/1; 3 literature → WP-0/2/6; 4 contract → WP-1; 5 rotations → WP-1; 6 L6 translation → WP-2; 7 crown ledger → WP-0/6; 8 ontology → WP-2/3; 9 corpus → WP-1/2; 10 ledger → WP-3; 11 grammar → WP-3/4; 12 solvers → WP-4; 13 raw-damage → WP-4; 14 holdouts → WP-3/5; 15 calculus contract → WP-5; 16 arithmetic → all (WP-0 freezes, WP-6 audits); 17 taxonomy → WP-0/6; 18 layout → WP-0; 19 prereg → WP-0; 20 schemas → WP-0/3/5; 21 order → WP-0 (all WPs follow); 22 phases → this plan; 23 threats → WP-0 (matrix) + owners per threat; 24 tests → per-WP suites; 25 invariants → WP-0 + continuous; 26 scaling → WP-1/4/5/6; 27 logging → WP-0 (all runs); 28 deps → WP-0; 29 AI use → WP-0/6; 30 stops → WP-0 + owners; 31 ladder → WP-4/5/6; 32 interpretation → WP-6; 33 claims → WP-5/6; 34 seal checklist → WP-6; 35 success S1–S10 → WP-6 report; 36 Q01–Q40 → WP-6 report; 37 refs → WP-0/6; 38 intent → WP-6.

### 8.3 Obligations MST0-01…26 → WP
01 parent transport → WP-0/1; 02 refinement → WP-1; 03 translation → WP-2; 04 snapshot → WP-1; 05 heavy → WP-2; 06 pairing → WP-2; 07 bends → WP-2; 08 ref-locality → WP-2 (+WP-6 proof); 09 raw boundary → WP-4/6; 10 determinism → WP-3; 11 preservation → WP-3/6; 12 signed bound → WP-4/6; 13 injection → WP-6 (dev checks WP-4); 14 repayment → WP-6 (dev WP-4); 15 integrability → WP-6; 16 partition → WP-1/6; 17 PA composition → WP-6; 18 telescoping → WP-6; 19 bridge → WP-6; 20 fixed-b guard → WP-4/6; 21 negative family → WP-4/6; 22 constant independence → WP-5/6; 23 finite-integrability guard → WP-4/6; 24 branch scope → WP-4/6; 25 holdout scope → WP-5; 26 literature scope → WP-2/6. Lifecycle `UNPROVED → PROVED → REVIEWED` enforced; `BLOCKED` never silently consumed. Required status before consumption is `REVIEWED` when applicable; `NOT_APPLICABLE` only with preserved justification (e.g. untranslatable L6 objects under MST0-03, unactivated signed/negative obligations under MST0-12/20/21); `BLOCKED` prevents consumption.

### 8.4 Gates MST-GATE-0…21 → WP
0 definitions → WP-0; 1 translation → WP-2; 2 refinement → WP-1; 3 lemmas → WP-2; 4 determinism → WP-3; 5 injection-dev → WP-4; 6 repayment-dev → WP-4; 7 cycle consistency → WP-4; 8 lower-bound → WP-4/6; 9 internal validation → WP-4; 10 freeze → WP-5; 11 n8 → WP-5; 12 H1/H2R → WP-5; 13 H3T → WP-5; 14 clean-room → WP-5; 15 adversarial → WP-5; 16 injection proof → WP-6; 17 KEEP proof → WP-6; 18 integrability → WP-6; 19 Pair Access → WP-6; 20 monotonicity → WP-6; 21 optimality → WP-6. First decisive failure freezes the candidate at that gate.

### 8.5 Threats T01…T90 / Stops STOP-01…50 / Tests / Invariants
Full enumerations live in `prereg/threat_control_matrix.yaml` / `stop_control_matrix.yaml` (frozen WP-0, audited WP-6: `set(threat_ids)=={T01..T90}`, `set(stop_ids)=={STOP-01..STOP-50}`, every item ≥1 control, every control exists). Named-test families map: Parent → WP-0/1; L6 → WP-2; ROT → WP-1; CYC → WP-1/2; LED → WP-3; TR → WP-3/4/5; HLD → WP-3/5; PR → WP-2/6; NEG → WP-4/6; SEAL → WP-6. Invariants INV-001…070 are asserted in the WP that first binds them and re-checked at seal.

---

## 9. Execution order (this turn and onward)

1. ✅ Clone verification (done): impl repo held only `LICENSE` → working tree = fresh; `STALE_CLEARANCE.json` records zero deletions-needed + policy.
2. ✅ This WorkPlan (WP-0 deliverable) + `Path.md` skeleton with adherence log.
3. Next (same WP-0): scaffold files listed in WP-0, run `run_phase00.py`, pass `PARENT-01…08`, commit + push.
4. Then WP-1 … WP-6 strictly in order; no WP starts until the prior WP's gate passes **and**
the gate-matrix conditions hold (WP-1 pre-consumption subgate: `MST0-01` REVIEWED before certified
consumption; `MST0-02` + relevant `MST0-04` REVIEWED before WP-2 theorem-facing use),
except WP-1 expansion mechanics may parallelize internally with sorted reductions. `Path.md` is updated **as implementation moves forward**, per-WP, with WorkPlan-adherence verdicts — never batched at the end.

---

## 10. Risk register (top risks → control)
- Parent not finally sealed → `STOP-01`, gate `PARENT_NOT_FINAL`; mitigated: ratified v0.3.1 pin (full `38c1be6afd2ab…` + all seal hashes + terminal claim) before any science.
- L6 transplant smuggling theorems → `STOP-09`, `T11/12/13/15`; mitigated: `PA_*/MST_*` naming + `MST0-03 REVIEWED` gate + dual implementation + mutants.
- Cost-convention drift (depth+1 → rotations) → `STOP-11`, `T17`; mitigated: `ROT-12` + explicit `MST0-02` statement.
- Target leakage into ontology/grammar → `STOP-10/17/18/19`; mitigated: static audit + target-blind extraction + firewall.
- Solver overclaim (feasible ⇒ theorem) → `STOP-22/23`, core rule §12.5; mitigated: independent replay + certificates + ladder + fresh banks + clean-room.
- Holdout contamination/second-unlock → `STOP-27…31`; mitigated: state machine + fail-closed imports + hash-committed candidate set.
- Finite-survival ⇒ theorem upgrade → interpretation §32 + `STOP-36`; mitigated: proof gates `MST-GATE-16…21` + claim-level discipline (§33).
- Resource exhaustion misread as impossibility → `STOP-50`; mitigated: `RESOURCE_LIMIT_NO_CLAIM` + exact resource record (§26.7).
