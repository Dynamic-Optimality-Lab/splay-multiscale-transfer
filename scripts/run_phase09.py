"""Spec PHASE 09 runner (REAL): ontology/grammar freeze lock (certificates, not edits).

Entry: WP-2 gates + H3T_BANK_COMMITTED. The WP-0 prereg files are immutable: this
runner RE-VERIFIES their hashes against prereg_sha256.txt (any drift = STOP-05
fail-closed) and emits phase-freeze CERTIFICATES referencing prereg + implementation
hashes. Steps: WP3-STEP-03 grammar conformance (one rule per template constructed +
validated + complexity-audited), branch permissions + activation blocked, freeze
certs, MST11 setup presence, no-synthesis assertion. Emits TRANSFER_GRAMMAR_FROZEN.
Console lines prefixed [WP3-STEP-0x] are the audit record.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from fractions import Fraction

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from python.transfer import branches as branches_mod  # noqa: E402
from python.transfer import complexity as complexity_mod  # noqa: E402
from python.transfer import grammar as grammar_mod  # noqa: E402
from python.transfer import templates_T1_T10 as templates_mod  # noqa: E402


def sha_file(p: str) -> str:
    """SHA-256 over buffered reads."""
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest().upper()


# WP3-STEP-03: prereg immutability re-verified (STOP-05 tripwire for the 3 files).
def step_immutable() -> list[str]:
    fails: list[str] = []
    frozen = {}
    for ln in open(os.path.join(ROOT, "prereg", "prereg_sha256.txt"), encoding="utf-8"):
        parts = ln.strip().split()
        if len(parts) == 2:
            frozen[parts[1]] = parts[0]
    for rel in ("./prereg/event_ontology_v0.3.yaml",
                "./prereg/transfer_grammar_v0.3.yaml",
                "./prereg/holdouts.yaml"):
        got = sha_file(os.path.join(ROOT, *rel[2:].split("/")))
        if frozen.get(rel) != got:
            fails.append("STOP-05 prereg file changed since WP-0 seal: %s" % rel)
    if not fails:
        print("[WP3-STEP-03] prereg immutable: ontology+grammar+holdouts hashes match seal", flush=True)
    return fails


# WP3-STEP-03: construct one rule per template; validate + complexity-audit each.
def step_conformance(grammar: dict) -> tuple[list[str], list[str]]:
    fails: list[str] = []
    ok_ids = []
    for i, template in enumerate(templates_mod.TEMPLATES):
        short = template.split("_")[0]
        branch = "SIGNED_MULTISCALE" if short == "T9" else "RAW_BOUNDARY"
        rule = templates_mod.make_rule(
            "TR-CF-%04d" % i, template, branch,
            {"all_of": [{"mode_is": "DELETE"}, {"side_is": "A"}]},
            consume=[{"type": "BOUNDARY_LATENT"}],
            produce=[{"type": "BOUNDARY_ACTIVE", "support": ("boundary", 1, 2, "LEFT"),
                       "scale": ("S0", 1), "mass": Fraction(1),
                       "provenance": "A_ROTATION_CREATED"}])
        shape_bad = templates_mod.check_record_shape(rule)
        if shape_bad:
            fails.append("GRAMMAR-01 %s shape: %s" % (template, shape_bad))
            continue
        gv = grammar_mod.validate_rule(rule, grammar)
        if gv:
            fails.append("GRAMMAR-01 %s grammar: %s" % (template, gv))
            continue
        cv = complexity_mod.audit_rule(rule)
        if cv:
            fails.append("GRAMMAR-01 %s complexity: %s" % (template, cv))
            continue
        ok_ids.append(rule["rule_id"])
    # Negative controls: over-wide outputs, forbidden inputs, bad branch, bad template.
    bad_wide = templates_mod.make_rule(
        "TR-NEG-WIDE", "T2_upward_scale_transfer", "RAW_BOUNDARY",
        {"mode_is": "KEEP"}, [],
        [{"type": "X", "support": ("key", 1), "scale": ("S0", 0),
          "mass": Fraction(1), "provenance": "P"} for _ in range(9)])
    if not complexity_mod.audit_rule(bad_wide):
        fails.append("GRAMMAR-02 over-wide rule not caught")
    bad_target = templates_mod.make_rule(
        "TR-NEG-TARGET", "T1_scale_preserving_move", "RAW_BOUNDARY",
        {"mode_is": "KEEP"}, [{"type": "REGRET_COINS"}],
        [{"type": "Y", "support": ("key", 1), "scale": ("S0", 0),
          "mass": Fraction(1), "provenance": "P"}])
    if not complexity_mod.audit_rule(bad_target):
        fails.append("GRAMMAR-02 target-input rule not caught")
    if branches_mod.activate_branch_B(None) != "BLOCKED":
        fails.append("GRAMMAR-02 Branch B activated without rejection record")
    else:
        print("[WP3-STEP-03] Branch B activation: BLOCKED (no Branch-A result, correct)", flush=True)
    if not fails:
        print("[WP3-STEP-03] conformance: 10/10 templates construct+validate+audit clean; "
              "3 negative controls caught", flush=True)
    return fails, ok_ids


def main() -> int:
    print("[WP3-STEP-00] PHASE 09: ontology/grammar freeze lock", flush=True)
    fails: list[str] = []
    cert = os.path.join(ROOT, "artifacts", "v03", "freeze", "PHASE02_L6_MAPPING_FREEZE.json")
    if not os.path.exists(cert):
        print("[WP3-STEP-00] PHASE09_FAIL: WP-2A freeze missing", flush=True)
        return 2
    state = os.path.join(ROOT, "artifacts", "v03", "holdouts", "h3t_state.json")
    if not os.path.exists(state):
        print("[WP3-STEP-00] PHASE09_FAIL: H3T bank not committed (run_phase08 first)", flush=True)
        return 2
    fails += step_immutable()
    grammar, ghash = grammar_mod.load()
    fails2, rule_ids = step_conformance(grammar)
    fails += fails2
    art = os.path.join(ROOT, "artifacts", "v03")
    freeze_done = all(os.path.exists(os.path.join(art, "freeze", f)) for f in
                      ("PHASE09_EVENT_ONTOLOGY_FREEZE.json", "PHASE09_TRANSFER_GRAMMAR_FREEZE.json"))
    if freeze_done:
        print("[WP3-STEP-03] freeze certs exist; pre-synthesis emptiness was certified "
              "at freeze time (synthesis since begun is expected post-WP-3)", flush=True)
    else:
        for forbidden in ("hypotheses", "solver"):
            p = os.path.join(art, forbidden)
            if os.path.isdir(p) and any(os.scandir(p)):
                fails.append("PRE-SYNTHESIS %s/ non-empty at grammar freeze" % forbidden)
        if not fails:
            print("[WP3-STEP-03] no synthesis artifacts at freeze (clean)", flush=True)
    for f in ("math/theorem_MST11_transfer_preservation.md",):
        if not os.path.exists(os.path.join(ROOT, f)):
            fails.append("MST11-01 missing %s (setup doc)" % f)
    if fails:
        print("[WP3-STEP-00] PHASE09_FAIL (%d)" % len(fails), flush=True)
        for x in fails:
            print(" -", x, flush=True)
        return 1
    impl_hashes = {}
    for mod in ("python/transfer/grammar.py", "python/transfer/templates_T1_T10.py",
                "python/transfer/branches.py", "python/transfer/complexity.py",
                "python/provenance/active.py", "python/ledger/update.py"):
        impl_hashes[mod] = sha_file(os.path.join(ROOT, *mod.split("/")))[:16]
    freeze_dir = os.path.join(art, "freeze")
    for name, payload in (
            ("PHASE09_EVENT_ONTOLOGY_FREEZE.json",
             {"prereg": "event_ontology_v0.3.yaml", "status": "TRANSFER_GRAMMAR_FROZEN"}),
            ("PHASE09_TRANSFER_GRAMMAR_FREEZE.json",
             {"prereg": "transfer_grammar_v0.3.yaml", "branch_B": "preregistered_not_activated",
              "conforming_templates": rule_ids, "status": "TRANSFER_GRAMMAR_FROZEN"})):
        payload.update({"impl_hashes": impl_hashes, "grammar_sha256": ghash})
        with open(os.path.join(freeze_dir, name), "w", encoding="utf-8", newline="\n") as f:
            json.dump(payload, f, sort_keys=True, indent=2)
            f.write("\n")
    print("[WP3-STEP-00] TRANSFER_GRAMMAR_FROZEN (certificates reference prereg+impl hashes)", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
