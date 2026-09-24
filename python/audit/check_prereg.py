"""Preregistration integrity checks for WP-0 (read-only; never writes).

STOP-05 enforcement lives here: check_freeze_integrity recomputes the normative
hashes and compares against the committed prereg_sha256.txt without modifying it.
Console output lines prefixed [WP0-STEP-0x] are the auditable execution record.
"""
from __future__ import annotations

import json
import os
import re
import sys

from python.audit.verify_parent import sha_file


# WP0-STEP-05: theorem ledger shape + gate-matrix first-consumer fields.
def check_theorem_gates(root: str) -> list[str]:
    fails: list[str] = []
    with open(os.path.join(root, "math", "proof_status.json"), encoding="utf-8") as f:
        ps = json.load(f)
    want = {"MST0-%02d" % (i,) for i in range(1, 27)}
    if set(ps.get("obligations", {})) != want:
        fails.append("PARENT-07 theorem ledger shape wrong")
    else:
        print("[WP0-STEP-05] ledger holds 26 obligations, all lifecycle-tracked")
    gm = open(os.path.join(root, "prereg", "theorem_gate_matrix.yaml"), encoding="utf-8").read()
    headers = set(re.findall(r"^(MST0-\d\d):", gm, re.M))
    if headers != want:
        fails.append("GATE-01 matrix obligation headers wrong (missing=%s extra=%s)"
                     % (sorted(want - headers), sorted(headers - want)))
    else:
        print("[WP0-STEP-05] gate matrix headers exact: 26 obligations")
        if gm.count("first_consumer:") != 26 or gm.count("required_status_before_consumption: REVIEWED") != 26:
            fails.append("GATE-01 matrix lacks first-consumer/REVIEWED fields")
        else:
            print("[WP0-STEP-05] gate matrix: 26 first-consumers, 26 REVIEWED requirements")
        m1 = re.search(r"MST0-01:\n(?:.*\n){1,2}.*first_consumer: (\S+)", gm)
        if not m1 or m1.group(1) != "WP-1":
            fails.append("GATE-01 MST0-01 first consumer must be WP-1")
        else:
            print("[WP0-STEP-05] MST0-01 first consumer: WP-1 (via WP-1 pre-consumption subgate)")
    return fails


# WP0-STEP-06: L6 translation contract completeness (language + proposed definitions).
def check_l6_contract(root: str) -> list[str]:
    fails: list[str] = []
    try:
        import yaml as _yaml
    except ImportError:
        print("[WP0-STEP-06] pyyaml unavailable")
        return ["L6-00 pyyaml unavailable for contract check"]
    with open(os.path.join(root, "prereg", "l6_translation_v0.3.yaml"), encoding="utf-8") as f:
        l6 = _yaml.safe_load(f)
    objs = l6.get("objects", {})
    expected = l6.get("declared_top_level_objects")
    if expected is None or len(objs) != expected:
        fails.append("L6-00 preregistered object set changed (found %s, declared %s)"
                     % (len(objs), expected))
    else:
        print("[WP0-STEP-06] %d translation objects preregistered (yaml self-declares count)" % len(objs))
    for name, rec in objs.items():
        for field in ("source_identity", "proposed_pair_access_definition",
                      "fallback_pa_native_object", "fallback_pa_native_definition",
                      "mapping_status", "obligation"):
            if field not in rec:
                fails.append("L6-00 %s missing %s" % (name, field))
                break
        if rec.get("mapping_status") != "UNRESOLVED_PRE_PROOF":
            fails.append("L6-00 %s must start UNRESOLVED_PRE_PROOF" % name)
    for rule in ("fallback_activation_rule", "no_invention_rule"):
        if rule not in l6:
            fails.append("L6-00 missing %s" % rule)
    if "UNRESOLVED_PRE_PROOF" not in l6.get("status_vocabulary", []):
        fails.append("L6-00 status vocabulary lacks UNRESOLVED_PRE_PROOF")
    if not fails:
        print("[WP0-STEP-06] all objects carry source identity + proposal + fallback + UNRESOLVED status")
    return fails


# WP0-STEP-07: threat/stop ID sets exact (spec SEAL-03/04).
def check_matrices(root: str) -> list[str]:
    fails: list[str] = []
    t = open(os.path.join(root, "prereg", "threat_control_matrix.yaml"), encoding="utf-8").read()
    tids = set(re.findall(r"^T\d\d", t, re.M))
    if tids != {"T%02d" % (i,) for i in range(1, 91)}:
        fails.append("SEAL-03 threat set wrong (%d)" % len(tids))
    else:
        print("[WP0-STEP-07] threat set exact: T01..T90")
    s = open(os.path.join(root, "prereg", "stop_control_matrix.yaml"), encoding="utf-8").read()
    sids = set(re.findall(r"STOP-\d\d", s))
    if sids != {"STOP-%02d" % (i,) for i in range(1, 51)}:
        fails.append("SEAL-04 stop set wrong (%d)" % len(sids))
    else:
        print("[WP0-STEP-07] stop set exact: STOP-01..STOP-50")
    return fails


# WP0-STEP-08: solver-freeze record exists; synthesis blocked until a backend is frozen.
def check_solver_record(root: str) -> list[str]:
    fails: list[str] = []
    sb = os.path.join(root, "prereg", "solver_backends.yaml")
    if not os.path.exists(sb):
        print("[WP0-STEP-08] solver_backends.yaml MISSING")
        return ["SOLV-01 solver_backends.yaml missing (freeze must precede synthesis)"]
    if "synthesis_authorized: false" not in open(sb, encoding="utf-8").read():
        fails.append("SOLV-01 solver freeze record malformed")
    else:
        print("[WP0-STEP-08] solver freeze record present; synthesis_authorized: false")
    return fails


# WP0-STEP-09: STOP-05 — recompute normative hashes, compare to committed file (read-only).
def check_freeze_integrity(root: str) -> list[str]:
    fails: list[str] = []
    sys.path.insert(0, os.path.join(root, "scripts"))
    try:
        import freeze_prereg
        recomputed = freeze_prereg.normative_hashes(root)
    finally:
        sys.path.pop(0)
    committed = open(os.path.join(root, "prereg", "prereg_sha256.txt"), encoding="utf-8").read()
    if "\n".join(sorted(recomputed)) + "\n" != committed.replace("\r\n", "\n"):
        fails.append("STOP-05 prereg hash mismatch: working tree differs from sealed freeze")
    else:
        print("[WP0-STEP-09] STOP-05 clear: %d normative hashes recompute exactly" % len(recomputed))
    for token in ("SPLAY_AM_MST_IMPLEMENTATION_SPEC_v0.3.1_PIN.md", "solver_backends.yaml"):
        if token not in committed:
            fails.append("PIN-03/SOLV-02 prereg_sha256 omits %s" % token)
    if not fails:
        print("[WP0-STEP-09] amendment + solver record covered by freeze")
    return fails


# WP0-STEP-10: no unauthorized science output (explicit namespace allowlist).
# Each entry names its authorizing WP turn; extending this list without a Path.md
# record + owning-phase justification is a seal violation. Anything else fails.
AUTHORIZED_NAMESPACES = {
    "STALE_CLEARANCE.json": "WP-0 stale policy",
    "logs/": "WP-0 run records (any phase may append)",
    "freeze/": "WP-0 freeze certificates (WP-2A mapping, WP-3 grammar)",
    "seal/": "WP-6 seal outputs",
    "parent_import/": "WP-1 sealed-evidence import + verification",
    "cycles/expanded/": "WP-1 rotation-expansion mechanics (WP-2 science consumes)",
    "cycles/stratified/": "WP-2B stratification tables",
    "cycles/motif_catalog.json": "WP-2B motif catalog (n4-6 selection)",
    "cycles/n7_validation.json": "WP-2B n7 validation record",
    "cycles/d5_analysis.json": "WP-2B D5 analysis record",
    "translation/": "WP-2A source sites + WP-2B lemma measurements",
    "baseline/": "WP-2B contracted baseline record",
    "proofs/obligation_status.json": "WP-1 derived obligation statuses",
}
DENIED_UNTIL_AUTHORIZED = ("hypotheses/", "solver/", "transfer_grammar/",
                           "holdouts/h3t_bank", "seal/FINAL_RESULT.json")


def check_no_early_science(root: str, artifacts_rel: str = "artifacts/v03") -> list[str]:
    fails: list[str] = []
    base = os.path.join(root, artifacts_rel)
    if not os.path.isdir(base):
        print("[WP0-STEP-10] no artifacts tree; nothing to predate freeze")
        return fails
    violations = []
    for dirpath, _dirnames, filenames in os.walk(base):
        for fn in filenames:
            rel = os.path.relpath(os.path.join(dirpath, fn), base).replace(os.sep, "/")
            if rel in AUTHORIZED_NAMESPACES or \
                    any(rel.startswith(k) for k in AUTHORIZED_NAMESPACES if k.endswith("/")):
                continue
            violations.append(rel)
    denied = [v for v in violations
              if v.startswith(DENIED_UNTIL_AUTHORIZED) or v in DENIED_UNTIL_AUTHORIZED]
    if violations:
        fails.append("EARLY-SCIENCE %d unlisted files under %s%s: %s"
                     % (len(violations), artifacts_rel,
                        " (DENIED namespace)" if denied else "",
                        ",".join(sorted(violations)[:8])))
    else:
        print("[WP0-STEP-10] no unauthorized science output (allowlist holds)", flush=True)
    return fails
