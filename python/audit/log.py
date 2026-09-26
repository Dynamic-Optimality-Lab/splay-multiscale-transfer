"""Append-only run logger (§27): every execution record carries the full field set."""
from __future__ import annotations

import datetime
import hashlib
import json
import os


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def write_log(path: str, rec: dict) -> dict:
    required = ["experiment_id", "phase", "branch", "command", "scientific_status"]
    for k in required:
        if k not in rec:
            raise ValueError(f"log missing {k}")
    rec = dict(rec)
    rec.setdefault("utc", datetime.datetime.now(datetime.timezone.utc).isoformat())
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    lines = []
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, sort_keys=True) + "\n")
    return rec


# WP-1 REPAIR STEP L1: static §27 provenance fields shared by phase runners.
def static_fields(root: str) -> dict:
    """Collect commit/pin/contract/firewall/dependency hashes (read-only).

    Unavailable values are recorded as explicit null-with-reason, never
    omitted silently and never fabricated.
    """
    import subprocess as _sp
    fields: dict = {
        "experiment_id": "SPLAY-AM-MST-v0.3",
        "parent_commits": {
            "v02": "38c1be6afd2ab2420aa094c68ce45ee6a26b3628",
            "v01": "6de1ca2a595e8895f54794f3a211fe6ee1a95a80",
        },
        "calculus_id": None,
        "constant_C": None,
        "stdout_hash": None,
        "stderr_hash": None,
        "stream_note": "console streams not captured; outputs hash-covered instead",
    }
    try:
        r = _sp.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True,
                    cwd=root, timeout=60)
        fields["local_commit"] = r.stdout.strip() or "unavailable: empty rev-parse"
    except Exception as e:  # noqa: BLE001 - provenance must not fail the run
        fields["local_commit"] = "unavailable: %s" % type(e).__name__
    for key, rel in (("spec_sha", "IMPLEMENTATION_SPEC_v0.3.md"),
                     ("prereg_sha", "prereg/prereg_sha256.txt"),
                     ("literature_manifest_sha", "external/MANIFEST.json"),
                     ("gate_matrix_sha", "prereg/theorem_gate_matrix.yaml"),
                     ("dependency_hashes", "requirements-lock.txt")):
        p = os.path.join(root, rel)
        try:
            fields[key] = sha(open(p, "rb").read())
        except OSError:
            fields[key] = "unavailable: missing " + rel
    try:
        h1 = json.load(open(os.path.join(root, "parent", "V02_H1_FIREWALL.json"),
                            encoding="utf-8"))
        h2r = json.load(open(os.path.join(root, "parent", "V02_H2R_FIREWALL.json"),
                             encoding="utf-8"))
        fields["firewall_states"] = {
            "H1": h1.get("state"),
            "H2R": "%s/unlocks=%s" % (h2r.get("state"),
                                      h2r.get("unlocks", h2r.get("unlock_count"))),
            "n8": "PARTIALLY_REVEALED_CANARY_CONTAMINATED",
        }
    except OSError:
        fields["firewall_states"] = "unavailable: parent firewall records missing"
    return fields


# WP-1 REPAIR STEP L2: hash every file in output dirs (deterministic order).
def hash_outputs(root: str, rel_dirs: list) -> dict:
    """Map relpath -> SHA-256 for all files under the given artifact dirs."""
    out: dict = {}
    for rel in rel_dirs:
        base = os.path.join(root, rel)
        if not os.path.isdir(base):
            continue
        for dp, _, fns in os.walk(base):
            for fn in sorted(fns):
                p = os.path.join(dp, fn)
                out[os.path.relpath(p, root).replace(os.sep, "/")] = sha(
                    open(p, "rb").read())
    return out
