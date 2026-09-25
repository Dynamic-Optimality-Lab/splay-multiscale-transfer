"""WP-6 Phase-19 seal machinery: FINAL_RESULT, manifest, archive, audits.

FINAL_RESULT is generated from artifacts only with exactly one terminal claim
level. The claim-level validator recomputes the level from artifact state and
refuses any mismatch (fail-closed; a higher level requires REVIEWED universal
proofs plus a versioned amendment, never an edit). The archive is deterministic
(sorted names, normalized metadata, fixed zstd parameters). Console tag
[WP6-STEP-07/08/09].
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import tarfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

TERMINAL_LEVELS = [
    "PARENT_CHAIN_ONLY", "FINITE_ROTATION_TRANSLATION_RESULTS",
    "FINITE_CRITICAL_KEEP_RESULTS", "FINITE_TRANSFER_OBSTRUCTION_RESULTS",
    "FINITE_TRANSFER_CALCULUS_RESULTS", "TRANSFER_CALCULUS_SURVIVES_FINITE_TESTS",
    "BOUNDED_DELETE_INJECTION_PROVED", "SYNCHRONOUS_KEEP_TRANSFER_PROVED",
    "UNIVERSAL_PAIR_ACCESS_LEMMA_PROVED", "APPROXIMATE_MONOTONICITY_PROVED",
    "DYNAMIC_OPTIMALITY_PROVED", "NEGATIVE_REAL_SPLAY_FAMILY_PROVED",
    "DYNAMIC_OPTIMALITY_DISPROVED", "RESOURCE_LIMIT_NO_CLAIM",
    "REPRESENTATION_INCONCLUSIVE",
]

ARCHIVE_NAME = "SPLAY-AM-MST-v0.3.tar.zst"


# WP6-STEP-07: recompute the terminal claim level from artifact state.
def recompute_terminal(root: str = ROOT) -> str:
    """Return the single terminal level the artifacts support (fail-closed)."""
    ceiling = json.load(open(os.path.join(
        root, "artifacts", "v03", "freeze", "PHASE16_WP5_CEILING.json"),
        encoding="utf-8"))
    audit = json.load(open(os.path.join(
        root, "artifacts", "v03", "proofs", "lifecycle_audit.json"),
        encoding="utf-8"))
    reviewed = {o for o, s in audit["statuses"].items() if s["status"] == "REVIEWED"}
    universal_reviewed = reviewed & {"MST0-13", "MST0-14", "MST0-15",
                                    "MST0-17", "MST0-18", "MST0-19"}
    if universal_reviewed:
        raise ValueError("terminal recompute refused: universal REVIEWED %r needs "
                         "versioned amendment path" % (universal_reviewed,))
    if ceiling.get("ceiling") != "TRANSFER_CALCULUS_SURVIVES_FINITE_TESTS":
        raise ValueError("terminal recompute refused: ceiling=%r"
                         % ceiling.get("ceiling"))
    return "TRANSFER_CALCULUS_SURVIVES_FINITE_TESTS"


# WP6-STEP-07: build FINAL_RESULT from artifacts only.
def build_final_result(root: str = ROOT) -> dict:
    """Assemble the terminal record (exactly one claim level)."""
    level = recompute_terminal(root)
    h3t_commit = json.load(open(os.path.join(
        root, "artifacts", "v03", "holdouts", "h3t_commitment.json"),
        encoding="utf-8"))
    ceiling = json.load(open(os.path.join(
        root, "artifacts", "v03", "freeze", "PHASE16_WP5_CEILING.json"),
        encoding="utf-8"))
    lifecycle = json.load(open(os.path.join(
        root, "artifacts", "v03", "proofs", "lifecycle_audit.json"),
        encoding="utf-8"))
    commit = json.load(open(os.path.join(
        root, "artifacts", "v03", "holdouts", "candidate_set_commit.json"),
        encoding="utf-8"))
    reveal = json.load(open(os.path.join(
        root, "artifacts", "v03", "holdouts", "h3t_reveal.json"), encoding="utf-8"))
    h3t_state = json.load(open(os.path.join(
        root, "artifacts", "v03", "holdouts", "h3t_state.json"), encoding="utf-8"))
    head = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True,
                          text=True, cwd=root)
    result = {
        "experiment": "SPLAY-AM-MST-v0.3",
        "terminal_claim": level,
        "allowed_meaning": ("A frozen arbitrary-n-defined calculus satisfies all tested "
                            "exact inequalities, fresh holdouts, and adversarial evaluations."),
        "forbidden_readings": ["the calculus works for all n",
                               "Dynamic Optimality is proved"],
        "repo_head": head.stdout.strip(),
        "parent_sealed_commit": "38c1be6afd2ab2420aa094c68ce45ee6a26b3628",
        "ancestor_commit": "6de1ca2a595e8895f54794f3a211fe6ee1a95a80",
        "standing": ceiling.get("standing", []),
        "killed_fresh": [
            {"calculus_id": r["calculus_id"], "verdict": r["verdict"],
             "max_residual": r["max_residual"],
             "first_violation": ({k: r["first_violation"][k] for k in
                                  ("size", "idx", "episode_hash", "w", "paid", "res")}
                                 if r["first_violation"] else None)}
            for r in reveal["results"] if r["verdict"] != "FRESH_H3T_PASS"],
        "gates": {"MST-GATE-0..15": "reached per WP records",
                  "MST-GATE-16": "PROVED_PENDING_REVIEW (author claim, not consumed)",
                  "MST-GATE-17..21": "NOT_REACHED"},
        "obligations": lifecycle["counts"],
        "firewalls": {"H1": "EMPTY/NOT_APPLICABLE", "H2R": "BANK_COMMITTED/NOT_APPLICABLE",
                      "H3T": "%s/unlocks=%s" % (h3t_state.get("state"),
                                                h3t_state.get("unlock_count")),
                      "n8": "PARTIALLY_REVEALED_CANARY_CONTAMINATED"},
        "hashes": {"candidate_set": commit["set_hash"],
                   "h3t_reveal": h3t_state.get("reveal_sha256"),
                   "h3t_logical_stream": h3t_commit.get("logical_stream"),
                   "h3t_per_size_streams": {n: h3t_commit["sizes"][n]["stream"]
                                            for n in sorted(h3t_commit["sizes"])}},
        "branch_exclusivity": "finite branch only; no theorem branch active",
        "upgrade_path": ("pending human reviews MST0-13/23/24/26; MST0-13 ACCEPT "
                         "permits re-seal at BOUNDED_DELETE_INJECTION_PROVED by "
                         "versioned amendment only"),
    }
    print("[WP6-STEP-07] FINAL_RESULT terminal claim: %s (exactly one level)"
          % level, flush=True)
    return result


# WP6-STEP-08: sha-256 of a file (buffered reads).
def _sha(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()


# WP6-STEP-08: working-tree inventory (canonical pre-commit seal set).
def tracked_files(root: str = ROOT) -> list:
    """Return sorted seal paths: HEAD-tracked minus disk-deleted, plus new
    untracked files (seal runs pre-commit, so deletions/additions apply).
    Seal archive outputs excluded; bytecode caches excluded."""
    r = subprocess.run(["git", "ls-files"], capture_output=True, text=True, cwd=root)
    if r.returncode != 0:
        raise ValueError("git ls-files failed (seal needs a git inventory)")
    files = set(r.stdout.splitlines())
    st = subprocess.run(["git", "status", "--porcelain"], capture_output=True,
                        text=True, cwd=root)
    if st.returncode != 0:
        raise ValueError("git status failed")
    for ln in st.stdout.splitlines():
        if len(ln) < 4:
            continue
        code, rel = ln[:2], ln[3:].strip().strip('"')
        rel = rel.replace(os.sep, "/")
        if code in (" D", "D ", "AD"):
            files.discard(rel)
        elif code == "??":
            p = os.path.join(root, rel)
            if os.path.isfile(p) and "__pycache__" not in rel and not rel.endswith(".pyc"):
                files.add(rel)
            elif os.path.isdir(p):
                for dp, _, fns in os.walk(p):
                    for fn in fns:
                        q = os.path.relpath(os.path.join(dp, fn), root).replace(os.sep, "/")
                        if "__pycache__" not in q and not q.endswith(".pyc"):
                            files.add(q)
    # NOTE: the whole seal/ envelope dir is excluded from its own manifest
    # (FINAL_RESULT/MANIFEST ride inside the archive explicitly; the archive
    # and its sidecar live outside it). Forward slashes always (deterministic
    # across platforms).
    files = {f.replace(os.sep, "/") for f in files}
    return sorted(f for f in files if not f.startswith("artifacts/v03/seal/"))


# WP6-STEP-08: write MANIFEST.sha256 (every scientific file covered, INV-061).
def build_manifest(root: str = ROOT) -> tuple[str, list]:
    """Write the seal manifest; return (manifest_sha, lines)."""
    files = tracked_files(root)
    lines = []
    for rel in files:
        p = os.path.join(root, rel)
        if not os.path.isfile(p):
            raise ValueError("manifest: tracked file missing on disk: %s" % rel)
        lines.append("%s  ./%s" % (_sha(p), rel))
    out = os.path.join(root, "artifacts", "v03", "seal", "MANIFEST.sha256")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(sorted(lines)) + "\n")
    digest = _sha(out)
    print("[WP6-STEP-08] manifest: %d files, sha=%s..." % (len(lines), digest[:16]),
          flush=True)
    return digest, lines


# WP6-STEP-09: deterministic archive (normalized metadata, fixed parameters).
def archive_members(root: str = ROOT) -> list:
    """Single-inventory member list: manifest files + the two seal records that
    ride inside the archive (FINAL_RESULT + MANIFEST). The archive and its
    sidecar live outside it."""
    manifest_path = os.path.join(root, "artifacts", "v03", "seal", "MANIFEST.sha256")
    members = []
    for ln in open(manifest_path, encoding="utf-8").read().splitlines():
        if "  ./" in ln:
            members.append(ln.split("  ./")[1])
    members += ["artifacts/v03/seal/FINAL_RESULT.json",
                "artifacts/v03/seal/MANIFEST.sha256"]
    return sorted(set(members))


def archive_bytes(root: str, member_files: list) -> bytes:
    """Build the deterministic tar.zst bytes for the given members (pure)."""
    import io as _io
    import zstandard as zstd
    buf = _io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w", format=tarfile.PAX_FORMAT) as tf:
        for rel in member_files:
            p = os.path.join(root, rel)
            ti = tf.gettarinfo(p, arcname=rel)
            ti.uid = 0
            ti.gid = 0
            ti.uname = ""
            ti.gname = ""
            ti.mtime = 0
            with open(p, "rb") as f:
                tf.addfile(ti, f)
    return zstd.ZstdCompressor(level=3).compress(buf.getvalue())


def build_archive(root: str = ROOT) -> tuple[str, int, list]:
    """Write the archive + sidecar from the single-inventory member list."""
    members = archive_members(root)
    for rel in members:
        if not os.path.isfile(os.path.join(root, rel)):
            raise ValueError("archive member missing on disk: %s" % rel)
    blob = archive_bytes(root, members)
    seald = os.path.join(root, "artifacts", "v03", "seal")
    out = os.path.join(seald, ARCHIVE_NAME)
    with open(out, "wb") as f:
        f.write(blob)
    digest = _sha(out)
    with open(os.path.join(seald, "ARCHIVE.sha256"), "w",
              encoding="utf-8", newline="\n") as f:
        f.write("%s  ./%s\n" % (digest, ARCHIVE_NAME))
    print("[WP6-STEP-09] archive: %d files, %d bytes, sha=%s..."
          % (len(members), len(blob), digest[:16]), flush=True)
    return digest, len(blob), members


# WP6-STEP-08: threat audit (90 IDs, controls listed, control references exist).
def audit_threats(root: str = ROOT) -> dict:
    """Verify T01..T90 set-exactness and per-threat control references."""
    import yaml
    matrix = yaml.safe_load(open(os.path.join(root, "prereg",
                                              "threat_control_matrix.yaml"), encoding="utf-8"))
    want = {"T%02d" % i for i in range(1, 91)}
    got = set(matrix)
    corpus = _repo_corpus(root)
    missing_controls: list = []
    for tid in sorted(want & got):
        for ctl in matrix[tid].get("controls", []):
            if ctl not in corpus:
                missing_controls.append((tid, ctl))
    record = {"want": 90, "got": len(got), "set_exact": got == want,
              "missing_control_refs": missing_controls}
    print("[WP6-STEP-08] threat audit: set_exact=%s missing_refs=%d"
          % (record["set_exact"], len(missing_controls)), flush=True)
    if got != want:
        raise ValueError("threat set inexact")
    return record


# WP6-STEP-08: stop audit (50 IDs exact, handlers + owners present).
def audit_stops(root: str = ROOT) -> dict:
    """Verify STOP-01..STOP-50 set-exactness and handler/owner fields."""
    import yaml
    matrix = yaml.safe_load(open(os.path.join(root, "prereg",
                                              "stop_control_matrix.yaml"), encoding="utf-8"))
    want = {"STOP-%02d" % i for i in range(1, 51)}
    got = set(matrix)
    bad: list = []
    for sid in sorted(want & got):
        e = matrix[sid]
        if not (e.get("handler") and e.get("owners") and e.get("status")):
            bad.append(sid)
    record = {"want": 50, "got": len(got), "set_exact": got == want,
              "malformed": bad}
    print("[WP6-STEP-08] stop audit: set_exact=%s malformed=%r"
          % (record["set_exact"], bad), flush=True)
    if got != want or bad:
        raise ValueError("stop audit FAILED")
    return record


# WP6-STEP-08: invariant audit (70 IDs defined in spec, referenced in repo).
def audit_invariants(root: str = ROOT) -> dict:
    """Verify INV-001..070 defined in spec and re-checked (referenced) in repo."""
    spec = open(os.path.join(root, "IMPLEMENTATION_SPEC_v0.3.md"),
                encoding="utf-8").read()
    defined = sorted(set(re.findall(r"INV-(\d{3})", spec)))
    corpus = _repo_corpus(root, exclude_spec=True)
    unreferenced = ["INV-%s" % n for n in defined if ("INV-%s" % n) not in corpus]
    record = {"want": 70, "defined": len(defined),
              "defined_exact": [int(n) for n in defined] == list(range(1, 71)),
              "unreferenced_outside_spec": unreferenced}
    print("[WP6-STEP-08] invariant audit: defined=%d exact=%s unreferenced=%d"
          % (record["defined"], record["defined_exact"],
             len(unreferenced)), flush=True)
    if [int(n) for n in defined] != list(range(1, 71)):
        raise ValueError("invariant set inexact")
    return record


# WP6-STEP-08: test-family audit (inventory per WorkPlan §8.5 family).
def audit_tests(root: str = ROOT) -> dict:
    """Inventory test files per named family (pass evidence: reproduce exit 0)."""
    fams = {"Parent": [], "L6": [], "ROT": [], "CYC": [], "LED": [],
            "TR": [], "HLD": [], "PR": [], "NEG": [], "SEAL": []}
    table = [("tests/parent", "Parent"), ("tests/translation", "L6"),
             ("tests/rotations", "ROT"), ("tests/cycles", "CYC"),
             ("tests/provenance", "LED"), ("tests/ledger", "LED"),
             ("tests/transfer", "TR"), ("tests/solver", "TR"),
             ("tests/holdout", "HLD"), ("tests/proof", "PR"),
             ("tests/adversary", "NEG"), ("tests/seal", "SEAL")]
    for rel, fam in table:
        d = os.path.join(root, rel)
        if os.path.isdir(d):
            fams[fam] += sorted(rel + "/" + f for f in os.listdir(d)
                                if f.endswith(".py"))
    for fn in ("test_foundation.py", "test_wp0_stress.py", "test_wp1.py",
               "test_wp2.py", "test_wp3.py", "test_wp4.py", "test_wp5.py"):
        p = os.path.join(root, "tests", fn)
        if os.path.isfile(p):
            fams.setdefault("WP", []).append("tests/" + fn)
    record = {"families": {k: v for k, v in fams.items()},
              "n_files": sum(len(v) for v in fams.values())}
    print("[WP6-STEP-08] test audit: %d files across %d families"
          % (record["n_files"], len(fams)), flush=True)
    return record


# WP6-STEP-08: exact-arithmetic audit (§16; decision modules must be float-free).
def audit_arithmetic(root: str = ROOT) -> dict:
    """Assert zero inexact-arithmetic usage in decision modules; list benign hits."""
    decision = ["python/ledger", "python/holdout/h1_evaluate.py",
                "python/holdout/h2r_evaluate.py", "python/holdout/h3t_evaluate.py",
                "python/freeze", "python/seal", "python/audit/lifecycle.py",
                "python/audit/cleanroom.py", "python/transfer/branchA.py",
                "python/transfer/ladder.py", "python/solver/certify.py",
                "python/solver/flow.py", "python/solver/ilp.py",
                "python/solver/smt.py", "python/solver/encode_sat.py",
                "python/adversary/large_n.py"]
    hits: list = []
    for p in decision:
        full = os.path.join(root, p)
        targets = [os.path.join(dp, fn) for dp, _, fns in os.walk(full)
                   for fn in fns if fn.endswith(".py")
                   if "__pycache__" not in dp] if os.path.isdir(full) else [full]
        for q in targets:
            for i, ln in enumerate(open(q, encoding="utf-8").read().splitlines(), 1):
                if "SCAN-EXEMPT" in ln:
                    continue
                if re.search(r"float\(|numpy|statistics|gauss|math\.log", ln):  # SCAN-EXEMPT
                    hits.append("%s:%d" % (os.path.relpath(q, root), i))
    others: list = []
    for dp, _, fns in os.walk(os.path.join(root, "python")):
        if "__pycache__" in dp:
            continue
        for fn in fns:
            if not fn.endswith(".py"):
                continue
            q = os.path.join(dp, fn)
            if any(q == os.path.join(root, p) or q.startswith(os.path.join(root, p) + os.sep)
                   for p in decision if not p.endswith(".py")):
                continue
            if q in [os.path.join(root, p) for p in decision]:
                continue
            for i, ln in enumerate(open(q, encoding="utf-8").read().splitlines(), 1):
                if "SCAN-EXEMPT" in ln:
                    continue
                if re.search(r"float\(|numpy|statistics|gauss|math\.log", ln):  # SCAN-EXEMPT
                    others.append("%s:%d:%s" % (os.path.relpath(q, root), i,
                                                ln.strip()[:80]))
    record = {"decision_module_hits": hits, "non_decision_hits": others,
              "policy": "exact integers/Fraction in decisions; floats diagnostic-only"}
    print("[WP6-STEP-08] arithmetic audit: decision_hits=%d other=%d"
          % (len(hits), len(others)), flush=True)
    if hits:
        raise ValueError("float usage in decision modules: %r" % (hits,))
    return record


# WP6-STEP-08: resource record (§26.7; no failure occurred — stated, not filled).
def build_resource_record(root: str = ROOT, timings: dict | None = None) -> dict:
    """Record wall times, artifact sizes, attempted vs unattempted work."""
    big: list = []
    # NOTE: seal/audit outputs excluded from the size walk (measuring them
    # would make the record self-referential across re-runs; only inputs count).
    for dp, _, fns in os.walk(os.path.join(root, "artifacts")):
        rel_dp = os.path.relpath(dp, root).replace(os.sep, "/")
        if rel_dp.startswith("artifacts/v03/seal") or rel_dp.startswith("artifacts/v03/audits"):
            continue
        for fn in fns:
            q = os.path.join(dp, fn)
            big.append((os.path.getsize(q), os.path.relpath(q, root).replace(os.sep, "/")))
    big = sorted(big, reverse=True)[:8]
    record = {
        "failures": [],
        "status": "NO_RESOURCE_FAILURE (all WPs completed; RESOURCE_LIMIT_NO_CLAIM not needed)",
        "wp6_step_wall_s": timings or {},
        "largest_artifacts": [{"bytes": b, "path": p} for b, p in big],
        "attempted": ["H3T 70k exact evaluation", "large-n through n=256",
                      "clean-room agreement", "full seal + archive"],
        "unattempted_by_plan": ["n>256 histories (beyond §16 ladder bound)",
                                "post-seal proof program MST0-14/15 (open research)"],
        "claims_still_valid": "all finite claims; no claim depended on unattempted work",
    }
    print("[WP6-STEP-08] resource record: no failures; %d timings" % len(record["wp6_step_wall_s"]),
          flush=True)
    return record


# WP6-STEP-08: read-only repo corpus for control-reference checks.
def _repo_corpus(root: str, exclude_spec: bool = False) -> str:
    """Concatenate tracked text files.

    Derived audit outputs (audits/, seal/, proof bundles, lifecycle/evidence
    records) never count as independent references: an audit must not cite its
    own prior output (self-pollution fail-closed by exclusion).
    """
    skip_dirs = ("artifacts/v03/audits/", "artifacts/v03/seal/",
                 "artifacts/v03/proofs/bundles/")
    skip_files = {"artifacts/v03/proofs/lifecycle_audit.json",
                  "artifacts/v03/proofs/MST13_injection_bound.json",
                  "artifacts/v03/proofs/obligation_status.json"}
    parts: list = []
    for rel in tracked_files(root):
        if rel.endswith((".zst", ".tar.zst", ".sha256")):
            continue
        if rel.startswith(skip_dirs) or rel in skip_files:
            continue
        if exclude_spec and rel == "IMPLEMENTATION_SPEC_v0.3.md":
            continue
        p = os.path.join(root, rel)
        try:
            parts.append(open(p, encoding="utf-8").read())
        except (UnicodeDecodeError, OSError):
            continue
    return "\n".join(parts)
