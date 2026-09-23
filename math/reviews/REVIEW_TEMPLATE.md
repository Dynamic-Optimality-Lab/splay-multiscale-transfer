# Theorem review record — TEMPLATE (one `math/reviews/MST0-XX.review.json` per obligation)
#
# A theorem reaches REVIEWED only when a record with ALL fields below exists,
# is hash-pinned in proof_status.json, and its verdict is ACCEPT.
# REVIEWED means: human-owned internal review passed. It NEVER means external peer review.
# INDEPENDENT_COMPUTATIONAL_VERIFICATION (two code paths agreeing) is necessary
# but never sufficient for REVIEWED.

{
  "schema": "THEOREM-REVIEW-v0.3",
  "obligation_id": "MST0-XX",
  "theorem_sha256": "sha256 of the exact reviewed statement file (math/theorem_*.md at review time)",
  "statement": "verbatim theorem statement, including explicit domain (e.g. all n, all legal paired executions)",
  "hypotheses_checked": ["each premise listed with its own status pointer; no implicit premises"],
  "proof_dependency_audit": "every lemma/calculus/artifact the proof depends on, with status at review time",
  "case_completeness_audit": "enumeration of required cases (e.g. ROOT/ZIG/LL/RR/LR/RL + every ledger/lazy op) with pointer to where each is discharged",
  "computational_evidence": "INDEPENDENT_COMPUTATIONAL_VERIFICATION record (two implementations, seeds, hashes) — supporting only",
  "objections": ["raised objections and their resolutions, or empty with reviewer sign-off that none were found after adversarial reading"],
  "reviewer": {"identity": "name/role", "role": "human-owner | internal-reviewer", "date_utc": "YYYY-MM-DD"},
  "verdict": "ACCEPT | REJECT | BLOCKED",
  "lifecycle_note": "UNPROVED -> PROVED -> REVIEWED; BLOCKED never silently consumed"
}
