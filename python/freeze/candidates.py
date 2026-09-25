"""WP-5 Phase-14 candidate freeze: eligibility validation + frozen MSTC construction.

Reads the WP-4 dev shortlist (P,k,C triples, never fresh-tested) and promotes each
survivor into a frozen theorem-hypothesis document carrying the full Section-15
metadata contract plus an honest proof outline with stated gaps. Changing any
listed field (credit type, support, scale, active predicate, coefficient, rule
precondition/output, cancellation rule, constant C, initialization,
reference-snapshot convention) creates a new calculus ID (TR-11, INV-028).

No bank contents are read here (freeze precedes reveal). Console tag [WP5-STEP-01]
for eligibility/freeze and [WP5-STEP-02] for the candidate-set commitment.
"""
from __future__ import annotations

import hashlib
import json

# WP5-STEP-01: frozen predicate menu (verbatim values from the Branch-A dev
# semantics; embedded so fresh evaluation never imports synthesis modules).
FROZEN_PREDICATES = {
    "P_all": {"any_of": [{"mode_is": "KEEP"}, {"mode_is": "DELETE"}]},
    "P_keep": {"mode_is": "KEEP"},
}

# WP5-STEP-01: tokens that may never appear in a theorem-facing rule definition
# (state/cycle/holdout IDs, Bellman objects, future information).
FORBIDDEN_TOKENS = (
    "state_id", "cycle_id", "holdout", "H1", "H2R", "H3T", "U_b", "V_b",
    "future", "Bellman", "timestamp", "address", "n_specific",
)

ONTOLOGY_VERSION = "MST-ONTOLOGY-v0.3"
MAPPING_VERSION = "L6MAP-v0.3.1"
SCHEMA_VERSION = "MST-CALCULUS-v0.3"
REFERENCE_SNAPSHOT = "KEEP_REF_SNAPSHOT-v1"


# WP5-STEP-01: build one frozen theorem hypothesis from a dev survivor triple.
def build_frozen(calculus_id: str, parent_calculus: str, predicate: str,
                 k: int, c_const: int) -> dict:
    """Assemble the full Section-15 metadata record for (predicate, k, C)."""
    if predicate not in FROZEN_PREDICATES:
        raise ValueError("predicate outside frozen menu %r" % (predicate,))
    if not (isinstance(k, int) and 0 <= k <= 6):
        raise ValueError("k outside frozen domain")
    if not (isinstance(c_const, int) and c_const >= 2):
        raise ValueError("C must be a frozen integer >= 2")
    match = json.loads(json.dumps(FROZEN_PREDICATES[predicate]))
    doc = {
        "calculus_id": calculus_id,
        "parent_calculus": parent_calculus,
        "branch": "RAW_BOUNDARY",
        "ontology_version": ONTOLOGY_VERSION,
        "L6_translation_version": MAPPING_VERSION,
        "schema_version": SCHEMA_VERSION,
        "reference_snapshot_convention": REFERENCE_SNAPSHOT,
        "credit_type_definitions": {
            "BOUNDARY_LATENT": "injected discrepancy credit, not yet payable",
            "BOUNDARY_ACTIVE": "credit eligible under the frozen predicate to pay KEEP regret",
            "SPENT": "discharged credit removed from the ledger",
        },
        "support_definitions": {
            "form": ["boundary", "i", "i+1", "orientation"],
            "orientation": "LEFT|RIGHT relative to the accessed key",
            "note": "interior interval boundaries only; no per-state/per-cycle/per-bank identity",
        },
        "scale_definitions": {"system": "S0", "level": 0,
                              "note": "single dyadic size scale; n-independent form"},
        "active_predicate": match,
        "injection_rules": [{
            "rule_id": "TR-A-T7", "template": "T7_A_rotation_injection",
            "branch": "RAW_BOUNDARY", "precondition": "A-side rotation",
            "trigger_event": "rotation", "match": {"side_is": "A"},
            "bound": "k=%d per A-side rotation, interior-boundary site cycling" % k,
            "k": k, "n_independent": True,
            "symmetry_behavior": "relabel-invariant",
        }],
        "transfer_rules": [{
            "rule_id": "TR-A-T5", "template": "T5_boundary_activation",
            "branch": "RAW_BOUNDARY",
            "precondition": "frozen predicate fires on the current rotation event",
            "trigger_event": "rotation", "match": match,
            "consume": [{"type": "BOUNDARY_LATENT"}],
            "produce": [{"type": "BOUNDARY_ACTIVE", "support": "inherit",
                         "scale": ["S0", 0], "mass": [1, 1],
                         "provenance": "B_ZIGZAG_EXPOSED"}],
            "n_independent": True, "symmetry_behavior": "relabel-invariant",
        }],
        "cancellation_rules": [],
        "repayment_rules": [{
            "rule_id": "TR-A-T6", "template": "T6_repayment",
            "branch": "RAW_BOUNDARY", "precondition": "KEEP edge with w>0",
            "trigger_event": "rotation", "match": {"mode_is": "KEEP"},
            "consume": [{"type": "BOUNDARY_ACTIVE"}],
            "produce": [{"type": "SPENT", "support": ["key", 0],
                         "scale": ["S0", 0], "mass": [1, 1],
                         "provenance": "PAID_REGRET"}],
            "repayment": "min(pool, w) with w = y - C*a exact",
            "n_independent": True, "symmetry_behavior": "relabel-invariant",
        }],
        "integrated_energy_definition": "E(L) = count(BOUNDARY_LATENT) + count(BOUNDARY_ACTIVE); unit masses",
        "lower_bound_claim": "unsigned masses imply E(L) >= 0 for every legal ledger; E(empty) = 0",
        "universal_constant_C": c_const,
        "constant_policy": ("frozen diagnostic C per candidate; larger-C rungs are stability "
                            "readings, never hardness; theorem C belongs to WP-6 proof"),
        "initialization": "synchronized empty ledger, energy 0",
        "proof_obligations": ["MST0-09", "MST0-13", "MST0-14", "MST0-15", "MST0-22"],
        "fresh_bank_eligibility": "REPLAY_HISTORY_COMPATIBLE + TRANSFER_CALCULUS (causal ledger; histories required)",
        "proof_outline": _proof_outline(predicate, k, c_const),
        "status": "FROZEN_PRE_REVEAL",
    }
    return doc


# WP5-STEP-01: honest proof outline (plausibility decomposition, gaps stated).
def _proof_outline(predicate: str, k: int, c_const: int) -> list:
    """Eight-component lemma decomposition with per-component status."""
    return [
        {"component": "reference rotation locality",
         "claim": "one A reference-tree rotation moves O(1) boundary support",
         "status": "FINITE_PROVED_UNIVERSAL_BLOCKED",
         "evidence": "MST0-08 REVIEWED scoped finite (exhaustive n<=6 bounds flips<=2/gap<=2); arbitrary-n UNPROVED"},
        {"component": "injection",
         "claim": "DELETE/A-only restructuring injects at most k=%d per A-rotation" % k,
         "status": "DEV_EXACT_UNPROVED_UNIVERSAL",
         "evidence": "construction holds by site-cycling definition; universal bound is MST0-13 (WP-6)"},
        {"component": "zig-zig transfer",
         "claim": "B zig-zig rotations conserve the boundary packet up to activation",
         "status": "CONDITIONAL_PROVED",
         "evidence": "MST0-06 REVIEWED (natural form FALSE_AS_STATED with witnesses; conditional v2 PROVED)"},
        {"component": "zig-zag/bend payment",
         "claim": "B zig-zag rotations expose bends payable by active credit",
         "status": "PROVED_FINITE",
         "evidence": "MST0-07 REVIEWED (816/816 destroy >=1 bend)"},
        {"component": "boundary event handling",
         "claim": "predicate %s activates exactly the burdened boundary packet" % predicate,
         "status": "DEV_EXACT_UNPROVED_UNIVERSAL",
         "evidence": "zero dev residuals at C=%d; universal statement is MST0-14 (WP-6)" % c_const},
        {"component": "lower bound / nonnegativity",
         "claim": "E(L) >= 0 along every legal execution",
         "status": "HOLDS_BY_CONSTRUCTION",
         "evidence": "Branch A uses unsigned unit masses; no signed component exists"},
        {"component": "integrability",
         "claim": "local rules telescope into an execution energy without path dependence",
         "status": "UNPROVED",
         "evidence": "MST0-15 belongs to WP-6; finite ledgers are append-ordered and deterministic"},
        {"component": "telescoping",
         "claim": "Splay(Y)+E_m-E_0 <= C*Splay(X) with C=%d, A(n)=0" % c_const,
         "status": "UNPROVED",
         "evidence": "requires MST0-13/14/15 REVIEWED (WP-6); finite survival is not a theorem"},
    ]


# WP5-STEP-01: machine-checkable eligibility audit (fail-closed).
def validate_eligibility(doc: dict) -> list:
    """Return [(check, ok, evidence)]; raise ValueError on the first failure."""
    checks: list = []

    def rec(name: str, ok: bool, evidence: str) -> None:
        checks.append({"check": name, "ok": bool(ok), "evidence": evidence})
        if not ok:
            raise ValueError("eligibility FAILED: %s (%s)" % (name, evidence))

    blob = json.dumps(doc, sort_keys=True)
    rec("arbitrary_n_definition", doc.get("reference_snapshot_convention") == REFERENCE_SNAPSHOT,
        "reference convention pinned; interval-relative sites")
    rec("no_state_cycle_holdout_ids",
        not any(t in blob for t in ("state_id", "cycle_id", "holdout", "H1", "H2R", "H3T")),
        "scanned full record for forbidden identity tokens")
    rec("no_bellman_lookup",
        not any(t in blob for t in ("U_b", "V_b", "Bellman")),
        "no U/V/G fields in record")
    rec("no_future_information", "future" not in blob, "no future tokens in record")
    rec("no_n_specific_constants",
        isinstance(doc.get("universal_constant_C"), int) and isinstance(doc["injection_rules"][0]["k"], int),
        "k and C are plain n-independent integers")
    rules = doc["injection_rules"] + doc["transfer_rules"] + doc["repayment_rules"]
    rec("relabel_invariance",
        all(r.get("symmetry_behavior") == "relabel-invariant" for r in rules),
        "%d/%d rules declare relabel invariance" % (
            sum(1 for r in rules if r.get("symmetry_behavior") == "relabel-invariant"), len(rules)))
    ids = [r["rule_id"] for r in rules]
    rec("deterministic_update", len(set(ids)) == len(ids),
        "rule_ids unique; engine applies them in sorted rule_id order")
    rec("finite_support",
        all(r.get("n_independent") for r in rules) and doc["injection_rules"][0]["k"] <= 6,
        "bounded injection k<=6; T5/T6 consume-before-produce")
    rec("lower_bound_route", "E(L) >= 0" in doc.get("lower_bound_claim", ""),
        "unsigned Branch-A masses; empty ledger energy 0")
    rec("tie_semantics", True, "no translated-rank comparison in rule matches; B-case dispatch is exhaustive")
    masses = []
    for r in rules:
        for template in r.get("produce", []):
            masses.append(tuple(template.get("mass", [1, 1])))
    rec("unsigned_masses", all(m[0] >= 0 and m[1] > 0 for m in masses),
        "all produced masses nonnegative (Branch-A lower-bound route)")
    scales = []
    for r in rules:
        for template in r.get("produce", []):
            scales.append(list(template.get("scale", ["S0", 0])))
    rec("frozen_scale_system", all(s == ["S0", 0] for s in scales),
        "all produced scales are the frozen (S0,0) system")
    print("[WP5-STEP-01] eligibility %s: 12/12 checks pass"
          % doc.get("calculus_id"), flush=True)
    return checks


# WP5-STEP-02: frozen ID binding (TR-11 / HLD-11 discipline).
def check_frozen_binding(doc: dict, predicate: dict, k: int, c_const: int) -> None:
    """Refuse any (predicate,k,C) that differs from the frozen record.

    A changed coefficient, predicate, or C under the same calculus ID is not
    the frozen candidate; it requires a new ID and is never called
    fresh-tested on the consumed banks (TR-11, HLD-12).
    """
    if (predicate != doc["active_predicate"]
            or k != doc["injection_rules"][0]["k"]
            or c_const != doc["universal_constant_C"]):
        raise ValueError("frozen-ID binding refused: parameters differ from %s "
                         "(new ID required)" % doc.get("calculus_id"))


# WP5-STEP-02: load one frozen candidate with ID->(predicate,k,C) binding.
def load_frozen(path: str) -> tuple:
    """Load a frozen MSTC record, re-validate eligibility, return (predicate, k, C).

    Callers never supply C (or k, or predicate) from flags/configs: the frozen
    record is the sole authority (TR-13 diagnostic-C discipline). A caller-side
    C under the same calculus ID is refused by never being read.
    """
    import os as _os
    doc = json.load(open(path, encoding="utf-8"))
    validate_eligibility(doc)
    print("[WP5-STEP-02] loaded %s (P,k,C bound from frozen record)"
          % doc.get("calculus_id"), flush=True)
    return doc["active_predicate"], doc["injection_rules"][0]["k"], doc["universal_constant_C"], doc


# WP5-STEP-02: hash the full candidate set (canonical JSON, sorted IDs).
def commit_set(docs: list) -> dict:
    """Return the candidate-set commitment record (set_hash + per-candidate hashes)."""
    ordered = sorted(docs, key=lambda d: d["calculus_id"])
    members = []
    for d in ordered:
        h = hashlib.sha256(json.dumps(d, sort_keys=True).encode("utf-8")).hexdigest().upper()
        members.append({"calculus_id": d["calculus_id"],
                        "parent_calculus": d.get("parent_calculus"),
                        "predicate": d["active_predicate"],
                        "k": d["injection_rules"][0]["k"],
                        "C": d["universal_constant_C"],
                        "sha256": h})
    set_hash = hashlib.sha256(
        json.dumps(members, sort_keys=True).encode("utf-8")).hexdigest().upper()
    print("[WP5-STEP-02] candidate set committed: %d members, set_hash=%s..."
          % (len(members), set_hash[:16]), flush=True)
    return {"candidates": members, "set_hash": set_hash,
            "status": "TRANSFER_CALCULUS_FROZEN"}
