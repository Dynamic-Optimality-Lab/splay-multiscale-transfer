# THEOREM_STATUS_REPORT.md — SPLAY-AM-MST-v0.3 obligation ledger at seal

Lifecycle: `UNPROVED → PROVED → REVIEWED`; `BLOCKED` forbids consumption;
`NOT_APPLICABLE` only with preserved justification. Machine derivation:
`python/audit/status.py` → `artifacts/v03/proofs/obligation_status.json`;
final audit: `artifacts/v03/proofs/lifecycle_audit.json` (0 jumps, every status
has a pointer). Frozen WP-0 snapshot `math/proof_status.json` intentionally
unmodified (normative freeze, STOP-05).

| Obligation | Status | Evidence pointer |
|---|---|---|
| MST0-01 parent transport | REVIEWED | MST0-01.review.json:ACCEPT |
| MST0-02 rotation refinement | REVIEWED | MST0-02.review.json:ACCEPT |
| MST0-03 L6 translation | REVIEWED | MST0-03.review.json:ACCEPT |
| MST0-04 snapshot legitimacy | REVIEWED | MST0-04.review.json:ACCEPT |
| MST0-05 heavy path | REVIEWED | MST0-05.review.json:ACCEPT |
| MST0-06 zig-zig pairing | REVIEWED | MST0-06.review.json:ACCEPT |
| MST0-07 zig-zag bends | REVIEWED | MST0-07.review.json:ACCEPT |
| MST0-08 reference locality | REVIEWED | MST0-08.review.json:ACCEPT (scoped finite; universal blocked) |
| MST0-09 raw boundary law | UNPROVED | conjecture record + WP-5/WP-6 outcome addendum |
| MST0-10 ledger determinism | REVIEWED | MST0-10.review.json:ACCEPT |
| MST0-11 transfer preservation | UNPROVED | SETUP document (no universal proof) |
| MST0-12 signed lower bound | NOT_APPLICABLE | MST0-12.not_applicable.json (Branch B never activated) |
| MST0-13 DELETE injection | PROVED | theorem doc + review package (human review requested) |
| MST0-14 KEEP repayment | UNPROVED | status record (sibling fresh kills; survivor finite only) |
| MST0-15 integrability | UNPROVED | status record (prerequisites unproved) |
| MST0-16 block partition | REVIEWED | MST0-16.review.json:ACCEPT |
| MST0-17 Pair Access | BLOCKED | MST0-17.BLOCKED (13 pending review; 14/15 unproved) |
| MST0-18 telescoping | BLOCKED | MST0-18.BLOCKED (17 blocked) |
| MST0-19 bridge | BLOCKED | MST0-19.BLOCKED (18 blocked; L2/L3 bytes pending) |
| MST0-20 fixed-b guard | NOT_APPLICABLE | MST0-20.not_applicable.json (no such inference attempted) |
| MST0-21 negative family | NOT_APPLICABLE | MST0-21.not_applicable.json (family never activated) |
| MST0-22 constant independence | UNPROVED | WP-5 setup record |
| MST0-23 finite-integrability guard | PROVED | guard-held record + package (human review requested) |
| MST0-24 branch scope | PROVED | scope record + package (human review requested) |
| MST0-25 holdout scope | UNPROVED | WP-5 setup record |
| MST0-26 literature scope | PROVED | scope record + package (human review requested) |

Counts: REVIEWED 10, PROVED 4, NOT_APPLICABLE 3, BLOCKED 3, UNPROVED 6 (26/26).

## Ladder gates MST-GATE-0…21

Gates 0–15 reached per WP records (definitions → large-n falsification). Gate
16 (arbitrary-n injection proof): author-claim PROVED, review pending — not
consumed. Gates 17–21: NOT_REACHED (blocked/unproved prerequisites). First
decisive failure froze each failed candidate at its gate; later evidence is
supplementary only.

## Human actions required (none pre-counted)

1. Theorem review (ACCEPT/REJECT/BLOCKED) on packages MST0-13/23/24/26 per
   `math/reviews/REVIEW_TEMPLATE.md` + `schemas/theorem_review.schema.json`.
2. On MST0-13 ACCEPT: WP-6 may be re-sealed at `BOUNDED_DELETE_INJECTION_PROVED`
   by versioned amendment (new seal, never an edit of this one).
3. WP-6 universal-proof program (MST0-14/15/08-universal) is open research, not
   a pending run: no proof attempt is queued and none is claimed.
