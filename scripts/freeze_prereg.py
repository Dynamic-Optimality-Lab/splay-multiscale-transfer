"""Authoritative SHA-256 freezer for the v0.3 normative stack.

Uses Python buffered reads (hashlib). Chosen because PowerShell
Get-FileHash and certutil returned the empty-string digest for one
file (parent/V02_H2R_FIREWALL.json) despite 167 content bytes visible
via buffered reads and git hash-object; see Path.md WP-0 section 14.
git (buffered reads) agrees with this script.

Console output lines prefixed [WP0-STEP-11] are the auditable execution
record (see Path.md WP-0 log table). normative_hashes() is reused by the
read-only STOP-05 integrity check (no writes there).
"""
import hashlib
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NORMATIVE = [
    "IMPLEMENTATION_SPEC_v0.3.md",
    "SPLAY_AM_MST_IMPLEMENTATION_SPEC_v0.3.1_PIN.md",
    "WorkPlan.md",
    "Path.md",
    "math/proof_status.json",
    "parent/V01_SEAL.json",
    "parent/V02_SEAL.json",
    "parent/V02_H1_FIREWALL.json",
    "parent/V02_H2R_FIREWALL.json",
    "prereg/experiment_v0.3.yaml",
    "prereg/parent_contract.yaml",
    "prereg/constant_policy.yaml",
    "prereg/solver_backends.yaml",
    "prereg/l6_translation_v0.3.yaml",
    "prereg/event_ontology_v0.3.yaml",
    "prereg/transfer_grammar_v0.3.yaml",
    "prereg/cycle_corpus_policy.yaml",
    "prereg/holdouts.yaml",
    "prereg/theorem_gate_matrix.yaml",
    "prereg/threat_control_matrix.yaml",
    "prereg/stop_control_matrix.yaml",
    "prereg/discovery_splits.yaml",
    "prereg/allowed_claims.md",
    "prereg/forbidden_claims.md",
]


def normative_hashes(root: str = ROOT) -> list[str]:
    """Recompute normative SHA-256 lines (pure; performs no writes)."""
    lines = []
    for rel in NORMATIVE:
        p = os.path.join(root, rel)
        with open(p, "rb") as f:
            raw = f.read()
        digest = hashlib.sha256(raw).hexdigest().upper()
        lines.append("%s  %s" % (digest, "./" + rel.replace(os.sep, "/")))
    return lines


# WP0-STEP-11: seal the normative hashes to prereg_sha256.txt (the only writer).
def main() -> int:
    print("[WP0-STEP-11] freezing %d normative files" % len(NORMATIVE))
    lines = normative_hashes(ROOT)
    for ln in lines:
        print("[WP0-STEP-11] " + ln)
    out = os.path.join(ROOT, "prereg", "prereg_sha256.txt")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(sorted(lines)) + "\n")
    print("[WP0-STEP-11] WROTE %s %d entries" % (out, len(lines)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
