# Path.md — SPLAY-AM-MST-v0.3 execution tracker (WorkPlan adherence log)

**Rule (standing):** this file is updated **as implementation moves forward**, per work package, with the same depth as `WorkPlan.md`: scope actually executed, files actually made, code actually produced + how, benchmarks actually run (training vs entirely-different tests), anti-overfitting evidence, gates actually emitted, and an explicit **WorkPlan-adherence verdict** per WP. Deviations are versioned here, never silent. Failed runs/counterexamples are retained, never deleted.

**Repo:** `Dynamic-Optimality-Lab/splay-multiscale-transfer` · **Parent:** `splay-bellman-debt@38c1be6afd2ab2420aa094c68ce45ee6a26b3628` (ratified v0.3.1 PIN) · **Ancestor:** `6de1ca2a595e8895f54794f3a211fe6ee1a95a80` · **Start:** 2026-09-23

---

## Review-response turn (2026-09-23): 10 findings → 10 repairs, no architecture change

An external review graded the foundation `FAIL_REPAIRABLE` on freeze compliance and
theorem review/gate lifecycle while passing scientific architecture, phase mapping (after
a small ownership correction), holdout/branch discipline, and claim discipline. All ten
findings were repaired in this turn; nothing was redesigned. Per-finding log
(severity · fix · files · verification):

1. **BLOCKER — v0.3 called "frozen" while `PRE_FREEZE_PARENT_PIN_REQUIRED`.**
Fix: v0.3 text left byte-identical (SHA-256 `462676E1…` re-verified inside the
amendment); new ratified file `SPLAY_AM_MST_IMPLEMENTATION_SPEC_v0.3.1_PIN.md`
discharges the condition with the full parent identity (§2: full commit,
`FINAL_RESULT`/manifest/archive/route-audit hashes, authoritative normative set,
H1/H2R/n8 states, ancestor pin). Amendment added to `prereg_sha256.txt` (now 24
entries). Verified: `run_phase00.py` PIN-01/02/03 checks + freeze output
(`0A51BEB3… ./SPLAY_AM_MST_IMPLEMENTATION_SPEC_v0.3.1_PIN.md`).
2. **BLOCKER — short-SHA parent pin.** Fix: `prereg/parent_contract.yaml` now carries the
full 40-char commit `38c1be6afd2ab2420aa094c68ce45ee6a26b3628` plus every required
artifact hash (values read from the sealed clone at that commit, clean tree), and
`bootstrap_parent.py`'s contract (WorkPlan) requires full-SHA + artifact-hash match —
short-SHA alone never passes. `prereg/experiment_v0.3.yaml` likewise updated.
Verified: new `PARENT-01`/`PARENT-01b` checks in `run_phase00.py`, PHASE00_PASS.
3. **BLOCKER — first-consumer gates (MST0-01/02/04).** Fix: `prereg/theorem_gate_matrix.yaml`
regenerated with full fields for all 26 obligations (owner, FIRST consumer, required
status `REVIEWED` ×26, proof/review artifacts, controls). WP-1 entry now requires
`MST0-01 == REVIEWED`; WP-2 entry requires `MST0-02` + relevant `MST0-04 == REVIEWED`
(WorkPlan §§WP-1/WP-2/8.1/9). Honest consequence recorded: all 26 obligations are
currently `UNPROVED` (no human review has occurred), so WP-1 certified consumption is
BLOCKED until the MST0-01 review record exists — computational reproduction is not
theorem-facing consumption and does not bypass this. Verified: `GATE-01` checks.
4. **MAJOR — "script re-verifies itself" mislabeled as review.** Fix: WorkPlan now defines
**INDEPENDENT_COMPUTATIONAL_VERIFICATION** (two code paths agreeing — necessary, never
sufficient) separately from **theorem review**: human-owned `math/reviews/MST0-XX.review.json`
per `math/reviews/REVIEW_TEMPLATE.md` + `schemas/theorem_review.schema.json`
(theorem SHA, verbatim statement + domain, hypotheses, dependency audit,
case-completeness audit, supporting computation only, objections, reviewer
identity/role/date, verdict; `REVIEWED` never means externally peer reviewed).
Verified: template + schema exist; gate matrix points each obligation at its record.
5. **MEDIUM — Phase 04 double ownership.** Fix: WP-2 is now the sole accountable owner of
spec Phase 04; WP-1 supplies prerequisite expansion artifacts (WorkPlan §§WP-1/WP-2/8.1).
Opening language changed to "one accountable owner per spec phase; cross-cutting
controls may have multiple owning WPs" (spec-supported). Verified: §8.1 row updated.
6. **MEDIUM — "≥8 engines" weakened adversarial set.** Fix: WP-4 now mandates all nine
spec-required search modes with distinct run records — uniform histories, structured
generators, hill climb, simulated annealing, genetic search, rotation-neighborhood
search, cycle splicing, motif inflation, counterexample generalization — plus any
additional engines. Verified: text updated (code lands in WP-4).
7. **MEDIUM — solver freeze too late/vague.** Fix: new `prereg/solver_backends.yaml`
(freeze record created in WP-0: exact version, binary/package hash, seed/thread policy,
parameter-file hash, certificate capability, discovery-only vs authoritative-after-replay;
synthesis stays blocked via existing STOP-22/23 + TR-01/03/04 — no new stop ID, set
stays exactly STOP-01..50). Truthful probe recorded (scipy 1.16.3 present but UNFROZEN
for synthesis; z3/OR-Tools/pyscipopt absent); `requirements-lock.txt` corrected to
actual installed versions; Python 3.13.7 noted as frozen actual vs 3.12 recommended
baseline. Verified: `SOLV-01/02` checks + freeze entry (`B0DC97B6… solver_backends.yaml`).
8. **MEDIUM/LOW — stale policy "deleted".** Fix: policy is now quarantine-outside-`v03` +
hash-log, fail-closed if quarantine is impossible (WorkPlan §0 + `STALE_CLEARANCE.json`
with `stale_scientific_file_count: 0`). Verified: JSON updated; count is 0 in fact.
9. **MINOR — "12 schemas".** Fix: 13/13 schema files now exist (added `parent_import`,
`l6_object`, `cycle_trace`, `provenance_packet`, `holdout_commitment`,
`solver_certificate`, `theorem_review`) and WorkPlan says 13. Verified: directory listing.
10. **MINOR — WP-4 residual / "harder C" wording.** Fix: one exact residual at frozen C
rejects *that candidate at that C* (ladder re-test at larger C without rule change is
explicitly allowed; rule changes mint new IDs); "harder C" → "cross-C
stability/feasibility (larger C eases the inequality)". Verified: text updated.

Transparency note on pre-seal prereg edits: `parent_contract.yaml`,
`theorem_gate_matrix.yaml`, `experiment_v0.3.yaml`, `requirements-lock.txt`, and
`run_phase00.py` were revised in this turn *before any FOUNDATION_FROZEN seal claim*
(the turn-1 `PHASE00_PASS` was a checks-pass, not a seal claim), each revision reasoned
above, and `prereg_sha256.txt` was regenerated accordingly (22 → 24 entries). The only
immutable texts — `IMPLEMENTATION_SPEC_v0.3.md` and sealed parent artifacts — were never
edited (amendment mechanism used instead).

---

## WP-0 — Foundation freeze [IN PROGRESS → foundation commit pending]

### WorkPlan prescription (recap)
Spec `PHASE 00`: pin final v0.2 seal + v0.1 chain, bootstrap `parent/` read-only, freeze literature + spec + prereg + hashes, init `proof_status.json` (26 obligations `UNPROVED`), freeze threat/stop/split/claim matrices, verify H1/H2R/n8 **contents-unread**, scaffold §18 layout, logging/schemas/tests, gate `FOUNDATION_FROZEN`. No Phase-01+ science before gate.

### What was actually done (this turn, in order)
1. **Repo clone + stale-result clearance.** Cloned `splay-multiscale-transfer`; remote `HEAD = 3f8571d` (single `Initial commit`, only file `LICENSE`). Moved `.git`/`LICENSE` to working root (`Number2`) so the working directory **is** the repo. Verified: zero prior scientific results existed → nothing stale to delete. Wrote `artifacts/v03/STALE_CLEARANCE.json` (`impl_repo_at_clone: {commits:1, files:[LICENSE]}`, `cleared_preexisting_results: []`, policy: `artifacts/v03` holds only new v0.3 outputs; parent evidence read-only under `parent/`). **Adherence: follows WP-0 exactly** (user instruction "previous results are cleared, only new results present" satisfied vacuously + enforced by policy + logged).
2. **Deep doc study before acting.** Read the full v0.3 spec (4600 lines, normative §§0–38, PHASE 00–19) as pasted + local copy; read v0.2 spec head + v0.3 head from `Downloads`; cloned parent `splay-bellman-debt` (depth 50) to temp and verified: `HEAD 38c1be6` = WP-6 GATED_PASS, `FINAL_RESULT.terminal_claim = FINITE_DEBT_LAW_MINING_RESULTS`, H1 `EMPTY`, H2R `BANK_COMMITTED/unlocks 0`, ancestor `6de1ca2` chain with aides `b444f6a/08dc1a7/19245ab/f131b14/29de3df` all present, normative spec set (v0.2 + SA01 + SA02). Inspected parent `python/` layout to mirror conventions without importing parent code. **Adherence: follows WP-0 §00.1/00.2** (pin from artifacts, not prose).
3. **WorkPlan.md written.** 7 WPs (WP-0…WP-6) with per-WP scope/files/code-how/benchmarks/anti-overfit/gates + §8 verification matrices (PHASE→WP 20/20, section→WP 0–38, MST0-01…26, MST-GATE-0…21, T01…T90, STOP-01…50). Model policy stated: no ML models; transfer calculi = models; training = dev corpora; brutal entirely-different testing = validation splits + n8 + H1/H2R/H3T + clean-room + large-n + ladder + mutants + exact arithmetic. **Adherence: N/A (this file IS the WP-0 deliverable); workload justification "more if needed" recorded.**
4. **Spec frozen into repo.** Byte-copied `SPLAY_AM_MST_IMPLEMENTATION_SPEC_v0.3.md` → `IMPLEMENTATION_SPEC_v0.3.md` (120,420 bytes). **Adherence: follows WP-0 file list exactly.**
5. **Scaffolded §18 layout.** Created `parent/prereg/math/math/latex/python/*(13 pkgs)/rust/schemas/tests/*(10)/artifacts/v03/*(13)/scripts/external/papers`. **Adherence: follows WP-0 exactly** (superset paths all per §18; `rust/` kept as permitted-acceleration placeholder).
6. **Parent bootstrap (read-only).** Wrote `parent/V01_SEAL.json` (6de1ca2…), `V02_SEAL.json` (38c1be6…, chain aides, firewall states), `V01/V02_FINAL_RESULT.json`, `V01/V02_MANIFEST/V01/V02_ARCHIVE/BOOTSTRAP_MANIFEST` hashes, `V02_H1_FIREWALL.json` (EMPTY), `V02_H2R_FIREWALL.json` (BANK_COMMITTED/0), `import_ledger.json`. No parent source file copied as v0.3 evidence. **Adherence: follows WP-0 exactly.**
7. **Prereg frozen.** `experiment_v0.3.yaml` (parent pin 38c1be6), `parent_contract.yaml`, `constant_policy.yaml` (ladder 2…64), `cycle_corpus_policy.yaml` (K=128, slack {0,1,2}), `holdouts.yaml` (70k H3T design + state machines + validation orders), `transfer_grammar_v0.3.yaml` (T1…T10, Branch B preregistered now), `l6_translation_v0.3.yaml` (22 objects, stubs), `event_ontology_v0.3.yaml` (provenance alphabet, LATENT/ACTIVE/SPENT/TRANSFERRED, target-blind), `discovery_splits.yaml`, `allowed/forbidden_claims.md`, `theorem_gate_matrix.yaml` (26/26 generated + asserted), `threat_control_matrix.yaml` (90/90 generated + asserted), `stop_control_matrix.yaml` (50/50 generated + asserted). **Adherence: follows WP-0 exactly; ID-set completeness machine-checked.**
8. **Theorem ledger + math stubs.** Generated `math/proof_status.json` (26 obligations, all UNPROVED, lifecycle `UNPROVED→PROVED→REVIEWED`) + 26 `theorem_MST*_stub.md` placeholders + `definitions_v0.3.md` + `L6_PAIR_ACCESS_MAPPING.md` skeleton. **Adherence: follows WP-0** (proofs belong to owning WPs; stubs are scaffolding, not claims).
9. **Core code (WP-0 scope + WP-1 head-start, clearly labeled).** Implemented `python/splay_ref/splay.py` (pointer BST, depth+1 cost, ZIG/LL/RR/LR/RL with event capture, balanced/spine builders, serialize/inorder), `pair.py` (KEEP/DELETE, `w_b`/`l_b` Fractions, pair IDs), `independent.py` (dict-based second implementation, zero shared helpers), `rotations/trace.py` (KEEP_REF_SNAPSHOT-v1 frozen-reference convention), `holdout/firewall.py` (fail-closed `guard_read` + commit helper), `audit/log.py` (append-only §27 records), 13 package `__init__.py`. **Adherence: follows WP-0 code list; splay/pair/trace overlap WP-1 file list — this is declared head-start, not scope creep: WP-1 will consume them via `ROT-*` suites without redefinition.**
10. **Schemas/scripts/tests.** 6 schemas (rotation_event, ledger_credit, transfer_rule, transfer_calculus, counterexample, final_result), `scripts/run_phase00.py` (parent pin + ledger + threat/stop set checks), `scripts/reproduce_all_v0.3.py` (WP-0 scope), `tests/test_foundation.py` (PARENT-01…07, ROT-01/10, TRACE, HLD-02 fail-closed). Top-level `README/CHANGELOG/CITATIONS/pyproject/requirements-lock/.gitignore`, `external/MANIFEST.json`. **Adherence: follows WP-0 exactly.**
11. **Verification executed (evidence, not assertion).** `run_phase00.py` → `PHASE00_PASS`; `test_foundation.py` → 47/47 PASS (`PARENT-01…07`, ROT across n=3/5/7 all keys, ROT-10 agreement x∈{4,2,5,1}, keep/delete traces, HLD-02 fail-closed); `reproduce_all_v0.3.py` → PASS. Log saved to `artifacts/v03/logs/phase00_wp0.json`. **Adherence: exceeds WP-0 minimum (which requires the checks; all green).**
12. **Deviation found + fixed (versioned, not silent).** `tests/test_foundation.py` agreement loop reused a stale root variable (`splay(r,x)` called twice; second call searched from non-root → `KeyError key 4`). Fixed by capturing the new root once (`r, e1 = splay(r,x)`) and comparing against the independent core's post-splay state. Also fixed `__init__.py` escape-sequence warnings (rewrote without backslashes). Both fixes logged here + in commit message. No spec/prereg/contract file was altered to make tests pass. **Adherence: process deviation handled per WP-0 "no failed run deleted" rule — failure preserved in this log.**
13. **Commit/push (standing instruction).** Single WP-0 foundation commit + push (this turn). No Phase-01+ science executed; H1/H2R/H3T contents never read (only firewall-state JSONs); no target-guided synthesis; no fresh-bank contact.

### 14. Environment hash anomaly found + resolved (transparent record — no data touched silently)
During close-out, `prereg_sha256.txt` generation showed `parent/V02_H2R_FIREWALL.json` hashing to the **empty-string SHA-256** (`e0b0…`) under PowerShell `Get-FileHash`, `certutil`, AND Python `hashlib` — while the file's 167 bytes were verified correct by 4 independent readers (PowerShell byte read, Python `read()`, `git hash-object`, and md5/sha1/sha512/blake2b digests, all self-consistent). Bisection proved the trigger is exactly that one 167-byte input: every mutation (pad/truncate/drop-first/substring/reverse/xor/H2X) hashed correctly, as did every other repo file. Cause is therefore an environment-level SHA-256-path quirk for one exact input, NOT a data-integrity problem (JSON semantics verified field-by-field).
Resolution (semantics-preserving, logged here): rewrote ONLY that WP-0 bootstrap record in canonical pretty-printed form (177 bytes; identical `bank_id`/`state`/`unlocks`/`note` values — verified by re-parsing), which hashes consistently across all three SHA-256 readers (Python `5839cd99…` == PowerShell `5839CD99…`, plus agreeing `git hash-object`). Authoritative freezer is `scripts/freeze_prereg.py` (Python `hashlib`, 22 normative entries). No parent-issued value was altered; no test/prereg/contract logic was changed to accommodate it. One-off diagnostic `scripts/diag_parent.py` was deleted pre-commit (it is not a WorkPlan deliverable); the `mini_hash*.py` probes lived only in Temp, never in the repo. Lesson for later WPs: cross-check every seal hash with ≥2 independent readers (`STOP-22/23` spirit) — now standard procedure.

### WorkPlan-adherence verdict — WP-0 (to date)
**FOLLOWS WorkPlan.md.** Every WP-0 file/code-suite item is implemented; verification evidence is green; the one test bug was repaired transparently above. Remaining WP-0 close-out (next turn or same turn if clean): compute `prereg/prereg_sha256.txt` over the normative stack, set `parent/` read-only, re-run gates, commit + push. No `FOUNDATION_FROZEN` claim is made until that close-out passes; no WP-1 scientific execution has begun.

---

## WP-1 — Exact pair dynamics + rotation traces [PENDING — entry: FOUNDATION_FROZEN; pre-consumption subgate: MST0-01 REVIEWED before certified consumption]

Planned scope/files/code/benchmarks per WorkPlan.md §WP-1 (spec PHASE 01/03/04-expansion; MST0-02/04/16; MST-GATE-2). Head-start already in tree: `splay.py/pair.py/independent.py/trace.py` + 47 green checks. Remaining: `rotations/reference.py`, `rotations/blocks.py`, `cycles/import_parent.py`, `cycles/expand.py`, `cycles/circulation.py`, `artifacts/v03/parent_import|rotations|cycles/expanded`, `theorem_MST02/04/16` proofs, `tests/rotations + tests/parent`. Adherence verdict to be recorded when executed.

## WP-2 — L6 translation + corpus science + lemmas + baseline [PENDING — entry: ROTATION_TRACE_CERTIFIED]

Per WorkPlan.md §WP-2 (spec PHASE 02/04-science/05/06; MST0-03/05/06/07/08). Nothing implemented yet beyond prereg stubs. Adherence verdict to be recorded when executed.

## WP-3 — Provenance + H3T + ontology/grammar lock [PENDING — entry: WP-2 gates; prereg files immutable, WP-3 emits freeze certificates only]

Per WorkPlan.md §WP-3 (spec PHASE 07/08/09; MST0-10/11). `firewall.py` skeleton exists; generator/ledger/grammar code pending. No H3T bank content exists; no discovery read has occurred. Adherence verdict to be recorded when executed.

## WP-4 — Transfer synthesis (Branch A/B, triage, stress) [PENDING — entry: TRANSFER_GRAMMAR_FROZEN]

Per WorkPlan.md §WP-4 (spec PHASE 10/11/12/13; MST0-09/12). This is the "training" WP: dev-only synthesis with the brutal entirely-different-test battery defined in WorkPlan. No solver code, no hypotheses, no residuals exist yet. Adherence verdict to be recorded when executed.

## WP-5 — Freeze candidates + fresh holdouts + clean-room/large-n [PENDING — entry: dev-zero-violations @ frozen C]

Per WorkPlan.md §WP-5 (spec PHASE 14/15/16; MST0-22/25). No frozen calculi, no reveals, no clean-room exist yet. Fresh banks untouched. Adherence verdict to be recorded when executed.

## WP-6 — Universal proof + bridge/negative + seal [PENDING — entry: TRANSFER_CALCULUS_SURVIVES_FINITE_TESTS or direct proof trigger]

Per WorkPlan.md §WP-6 (spec PHASE 17/18/19; MST0-13/14/15/17/18/19/20/21). No proofs beyond stubs; no FINAL_RESULT; no archive. Adherence verdict to be recorded when executed.

---

## Review-response turn 2 (2026-09-23): freeze-conflict, MST0-01 handoff, wording

1. **Prereg-freeze vs WP-3 "finalization" conflict (fix-before-implementation).**
WP-0 prereg files (`event_ontology`, `transfer_grammar`, `holdouts` + all of
`prereg_sha256.txt`) are now permanently immutable after the WP-0 seal; the WP-3
"(finalized)" line is replaced by phase-freeze certificates in
`artifacts/v03/freeze/` (`PHASE09_*_FREEZE.json` carrying preregistered hash +
implementation/generator hashes + timestamp + status). `holdouts.yaml` keeps
`H3T.status_at_prereg = TO_BE_GENERATED_AND_QUARANTINED` forever; `BANK_COMMITTED`
lives only in the commitment/firewall artifact. Preregistered rule vs observed
execution state stay separated (STOP-05 fail-closed via `freeze_prereg.py` re-run).
Verified: WorkPlan §§WP-3/WP-0 + `artifacts/v03/freeze/README.md`; `holdouts.yaml`
bytes unchanged (hash `477D2D33…` stable across freezes).
2. **MST0-01 handoff deadlock.** Adopted the preferred option: WP-1 entry needs
`FOUNDATION_FROZEN` only; a WP-1 **pre-consumption subgate** (prove MST0-01 →
INDEPENDENT_COMPUTATIONAL_VERIFICATION → human review → `REVIEWED`) gates all
certified parent-fact consumption. Gate-matrix owner for MST0-01 moved WP-0 → WP-1
(WP-0 keeps statement setup); header notes the subgate. Current status honestly
`UNPROVED`, so consumption remains blocked — no implicit transition.
Verified: `GATE-01` checks still pass (first_consumer WP-1, 26×REVIEWED-required).
3. **Wording:** "covered exactly once" → "one accountable owner per spec phase;
multiplicity allowed by the specification for sections/gates/threats/stops/tests/
invariants" (WorkPlan §0). Gate description → "`REVIEWED` when applicable;
`NOT_APPLICABLE` only with preserved justification; `BLOCKED` prevents consumption"
(§8.3 + gate-matrix header naming MST0-03/12/20/21 as conditional).


---

## Review-response turn 3 (2026-09-23): populated prereg contracts, 11 strata, consistency

1. **BLOCKER — immutable stubs.** The three prereg files were promoted from initial stub
form to fully populated preregistered contracts *before any FOUNDATION_FROZEN seal
claim* (hashes regenerated; turn-1 "stub" mentions above are the superseded history):
`event_ontology_v0.3.yaml` (21 keys: S8+S10 language — event record fields, regret
layers, zig context, S0–S5 definitions with eligibility, 11-tag provenance alphabet,
credit lifecycle, support allowed/forbidden, target-blindness), `transfer_grammar_v0.3.yaml`
(16 keys: credit/support schemas + vocabulary rule, T1–T10 with record fields, complexity
bounds, Branch A/B permissions with B preregistered, 9 forbidden escapes, 10-step solver
objective hierarchy, certificate policy), `l6_translation_v0.3.yaml` (27 objects each with
source ref + obligation + naming/tie/rank rules; WP-2 fills records in
`math/L6_PAIR_ACCESS_MAPPING.md` without changing this language). All three parse as
valid YAML (PyYAML 6.0.2) with content assertions green (prov=11, T=10, objectives=10,
objects=27). WP-3 certificates now realize `preregistered language → implementation →
freeze certificate`. **Adherence: follows the repaired WorkPlan; no post-seal mutation
(no seal claim exists yet).**
2. **BLOCKER — H3T 10 vs 11 strata.** `prereg/holdouts.yaml` already enumerated 11
(asserted: 11); the WorkPlan's combined `ZIGZIG/ZIGZAG_ENRICHED` token is split into
`ZIGZIG_ENRICHED` + `ZIGZAG_ENRICHED`, with the 10,000-episodes-per-size distributed
across the 11 strata (not per stratum) — 70k total unchanged. WP-5's "11 strata" text
was already correct; the contradiction is closed. Verified: strata count assertion.
3. **Consistency:** WP-1 now "provides rotation-determinism prerequisites/evidence for
MST0-10 (theorem owner: WP-3)" (matrix already assigned MST0-10 → WP-3); WP-0 file-list
wording matches the conditional gate rule (`REVIEWED` when applicable;
`NOT_APPLICABLE` only with preserved justification; `BLOCKED` forbids consumption).

---

## Review-response turn 4 (2026-09-23): L6 lifecycle, engine-list and date-label polish

1. **BLOCKER — L6 "mapping vocabulary" vs "all translation definitions".**
`l6_translation_v0.3.yaml` now freezes the complete language + **proposed** definitions:
per-object L6 source identity (paper v1 + definition slot; exact sections pinned at
literature freeze), proposed PA definition from spec §6, `mapping_status:
UNRESOLVED_PRE_PROOF` ×27, obligation, mapping schema, semantic-difference slot — plus
frozen tie/reference-snapshot semantics, `wp2_rule`, and consumption rule. WP-2 may
resolve statuses (`SAME`→proved, `MODIFIED`/`NOT_APPLICABLE`/`FALSE` with preserved
justification, i.e. `SAME → FALSE/NOT_APPLICABLE` discovery allowed) and populate
`math/L6_PAIR_ACCESS_MAPPING.md`, but may not introduce a new definition/object without
a new mapping version. Honesty note: L6 source bytes are not yet in-repo
(`external/papers/` pending literature freeze), so source *identities* — the explicitly
allowed alternative — are frozen, with `external/MANIFEST.json` recording the exact L6
version identity (arXiv:2607.18498 v1). Verified: new `L6-00` gate in `run_phase00.py`
(27 objects × required fields, all `UNRESOLVED_PRE_PROOF`) passes; YAML parses.
2. **Polish:** top-level models paragraph now lists all nine adversarial modes (added
counterexample-generalization; authoritative WP-4 list unchanged); residual summary
reworded to candidate-at-frozen-C; `Date frozen` → `WorkPlan text frozen` with the
preregistration freeze completing only at `FOUNDATION_FROZEN`.
3. **Caveat answer:** the v0.3.1 PIN amendment IS in-repo and hash-covered
(`0A51BEB3…` in `prereg_sha256.txt`); its contents are re-verified by PIN-01/02/03 on
every gate run — no separate obligation remains.

---

## Cross-cutting log
- 2026-09-23: Turn 1 — clone (LICENSE-only, HEAD 3f8571d) → study (v0.3 full + v0.2/v0.1 + parent clone verify 38c1be6/H1 EMPTY/H2R COMMITTED-0/n8 contaminated) → WorkPlan.md (7 WPs, matrices 26/90/50 machine-checked) → scaffold + core + schemas + scripts + tests → 47/47 green + PHASE00_PASS → Path.md (this file) → prereg_sha256 → commit+push (`163299e`).
- 2026-09-23: Turn 2 (review-response) — 10 findings repaired per section above: v0.3.1 PIN amendment (+24-entry freeze), full-SHA parent contract, first-consumer gate matrix (REVIEWED-required when applicable, all UNPROVED → WP-1 consumption blocked pending MST0-01 subgate review), review-record template+schema, Phase-04 single ownership, nine adversarial modes, solver_backends freeze, quarantine stale policy, 13 schemas, WP-4 wording. Re-verified (freeze + PHASE00_PASS + 47/47) → commit+push.
- 2026-09-23: Turn 3 (review-response II) — prereg-immutability fix: WP-3 certifies via `artifacts/v03/freeze/` certificates, never rewrites prereg; MST0-01 via WP-1 pre-consumption subgate (owner WP-1); conditional-obligation + multiplicity wording. Re-verified → commit+push.
- 2026-09-23: Turn 4 (review-response III) — three prereg files promoted stub → fully populated contracts (YAML-validated: prov=11, T=10, objectives=10, objects=27); H3T 11 strata (WorkPlan token split; 10k/size distributed); WP-1 MST0-10 prerequisite wording; conditional gate wording in WP-0 list. Re-verified → commit+push.
- 2026-09-23: Turn 5 (review-response IV) — L6 language+proposed-definitions freeze (27×UNRESOLVED_PRE_PROOF, L6-00 gate, L6 version identity in manifest); nine-mode summary + candidate-at-C + WorkPlan-text-freeze date wording; Path.md turn order restored chronological. Re-verified → commit+push.
- Standing user instructions honored: Path/WorkPlan depth rule, stale-clearance rule, commit+push without prompting.
- Failures preserved: test-loop stale-root KeyError (fixed, see WP-0 §12); SHA-256 environment quirk (resolved §14); no scientific failures yet (no science run yet).
