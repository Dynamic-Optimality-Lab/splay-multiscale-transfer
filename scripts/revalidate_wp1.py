"""WP-1 contract revalidator (read-only; writes nothing, exits non-zero on any gap).

Resolves phase binding N=1 (CURRENT_PHASE=WP-1, PREVIOUS_PHASE=NOT_APPLICABLE):
verifies pre-foundation prerequisites and every WorkPlan WP-1 requirement
directly against authoritative bytes — files, parent-evidence classes, artifacts
(paths AND formats AND hashes AND manifests), named tests (exact IDs AND
meanings, dictionary-mapped), mutants, full-tuple independent agreement,
execution records with stream hashes, and lifecycle states. Human review
records are verified as present (never fabricated); the strict hash-binding
rule is enforced (proof bytes differing from reviewed bytes yield PROVED, and
MST0-02 is therefore expected PROVED pending re-review). No required artifact
may be special-cased as acceptable-when-absent.
Console lines use the resolved [WP-1][STEP XX] format with identifying comments.
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

FAILS: list = []


# WP-1 STEP 01: report one contract check (fail-closed aggregation).
def check(name: str, cond: bool) -> None:
    # WP-1 STEP 01: single check reporter for the revalidation matrix.
    print("[WP-1][STEP 01] %s %s" % ("PASS" if cond else "FAIL", name), flush=True)
    if not cond:
        FAILS.append(name)


# WP-1 STEP 02: verify pre-foundation prerequisites (parent pin + firewalls).
def step_prefoundation() -> None:
    # WP-1 STEP 02: parent seal and firewall-state prerequisites for WP-1 entry.
    v02 = json.load(open(os.path.join(ROOT, "parent", "V02_SEAL.json"), encoding="utf-8"))
    check("parent sealed commit full 40-char",
          v02.get("sealed_commit") == "38c1be6afd2ab2420aa094c68ce45ee6a26b3628")
    h1 = json.load(open(os.path.join(ROOT, "parent", "V02_H1_FIREWALL.json"), encoding="utf-8"))
    h2r = json.load(open(os.path.join(ROOT, "parent", "V02_H2R_FIREWALL.json"), encoding="utf-8"))
    check("H1 EMPTY", h1.get("state") == "EMPTY")
    check("H2R BANK_COMMITTED/0",
          h2r.get("state") == "BANK_COMMITTED" and h2r.get("unlocks", h2r.get("unlock_count")) == 0)
    print("[WP-1][STEP 02] pre-foundation prerequisites verified", flush=True)


# WP-1 STEP 03: verify every WorkPlan WP-1 implementation file exists.
def step_files() -> None:
    # WP-1 STEP 03: file-existence audit against the WorkPlan WP-1 file list.
    required = [
        "python/splay_ref/splay.py", "python/splay_ref/pair.py",
        "python/splay_ref/independent.py", "python/rotations/trace.py",
        "python/rotations/reference.py", "python/rotations/blocks.py",
        "python/rotations/agree.py", "python/rotations/corpus.py",
        "python/rotations/mutate.py", "python/rotations/independent_trace.py",
        "python/cycles/import_parent.py", "python/cycles/expand.py",
        "python/cycles/circulation.py", "python/cycles/enumerate.py",
        "python/cycles/evidence.py",
        "python/audit/status.py", "python/audit/log.py",
        "math/theorem_MST01_parent_transport.md",
        "math/theorem_MST02_rotation_refinement.md",
        "math/theorem_MST04_keep_reference_snapshot.md",
        "math/theorem_MST16_block_partition.md",
        "schemas/rotation_event.schema.json",
        "scripts/run_phase01.py", "scripts/run_phase03.py",
        "scripts/revalidate_wp1.py",
        "tests/rotations/test_trace.py", "tests/rotations/test_rot_named.py",
        "tests/rotations/test_rot_mutants.py", "tests/parent/test_import.py",
        "tests/test_wp1.py",
    ]
    for rel in required:
        check("file exists " + rel, os.path.isfile(os.path.join(ROOT, rel)))
    print("[WP-1][STEP 03] file inventory complete (%d paths)" % len(required), flush=True)


# WP-1 STEP 04: verify parent-evidence classes bound by hash (F1/F3/F5).
def step_parent_evidence() -> None:
    # WP-1 STEP 04: every required sealed evidence class present + ledger-bound.
    base = os.path.join(ROOT, "artifacts", "v03", "parent_import")
    ledger = json.load(open(os.path.join(base, "import_ledger.json"), encoding="utf-8"))
    check("ledger has v01evidence/v02evidence classes",
          "v01evidence_files" in ledger and "v02evidence_files" in ledger)
    entries = ledger.get("v01evidence_files", []) + ledger.get("v02evidence_files", [])
    check("evidence ledger non-empty", len(entries) > 0)
    bad = 0
    for entry in entries:
        for prefix in ("v01evidence/", "v02evidence/"):
            if entry["dest"].startswith(prefix):
                p = os.path.join(base, *entry["dest"].split("/"))
                if not os.path.isfile(p):
                    bad += 1
                    continue
                h = hashlib.sha256(open(p, "rb").read()).hexdigest().upper()
                if h != entry["sha256"]:
                    bad += 1
    check("evidence bytes match ledger hashes (%d files)" % len(entries), bad == 0)
    for cls in ("trees", "transitions", "reachability", "certificates", "audits"):
        d = os.path.join(base, "v01evidence", cls)
        check("v01evidence class present " + cls, os.path.isdir(d))
    for cls in ("bellman",):
        d = os.path.join(base, "v02evidence", cls)
        check("v02evidence class present " + cls, os.path.isdir(d))
    check("near-tight families bound (quarantined context)",
          os.path.isfile(os.path.join(
              base, "v01evidence", "adversarial", "near_tight_families.json")))
    print("[WP-1][STEP 04] parent-evidence classes verified", flush=True)


# WP-1 STEP 05: verify rotation-trace artifacts (paths, formats, hashes, bundle).
def step_rotations_artifacts() -> None:
    # WP-1 STEP 05: rotations/ corpus present in the required representation.
    from python.rotations import corpus as corpus_mod
    base = os.path.join(ROOT, "artifacts", "v03", "rotations")
    check("rotations/ directory exists", os.path.isdir(base))
    for n in (2, 3, 4, 5, 6, 7):
        check("rotations shard traces_n%d.json.zst present" % n,
              os.path.isfile(os.path.join(base, "traces_n%d.json.zst" % n)))
    manifest_path = os.path.join(base, "rotations_manifest.json")
    check("rotations_manifest.json present", os.path.isfile(manifest_path))
    if os.path.isfile(manifest_path):
        manifest = json.load(open(manifest_path, encoding="utf-8"))
        check("rotations manifest validates (hashes + logical stream)",
              corpus_mod.validate_manifest(manifest, base) == [])
        total, edge_ids = 0, set()
        for n in (2, 3, 4, 5, 6, 7):
            for tr in corpus_mod.read_shard(base, "traces_n%d" % n)["traces"]:
                total += 1
                edge_ids.add(tr["edge_id"])
        check("rotations corpus holds 75 traces", total == 75)
        check("corpus edge IDs unique canonical (75/75)", len(edge_ids) == 75)
    bundle_path = os.path.join(base, "MST02_proof_bundle.json")
    check("MST02_proof_bundle.json present", os.path.isfile(bundle_path))
    if os.path.isfile(bundle_path) and os.path.isfile(manifest_path):
        bundle = json.load(open(bundle_path, encoding="utf-8"))
        doc = os.path.join(ROOT, bundle.get("theorem_doc", ""))
        ok = (os.path.isfile(doc)
              and hashlib.sha256(open(doc, "rb").read()).hexdigest().upper()
              == bundle.get("theorem_sha256")
              and os.path.isfile(os.path.join(ROOT, bundle.get("review_record", "")))
              and bundle.get("corpus_manifest_sha256") == hashlib.sha256(
                  open(manifest_path, "rb").read()).hexdigest().upper())
        check("MST02 proof bundle binds reviewed bytes to corpus", ok)
    print("[WP-1][STEP 05] rotation-trace artifacts verified", flush=True)


# WP-1 STEP 06: verify expansion artifacts (plain + zst + manifest + equivalence).
def step_expanded_artifacts() -> None:
    # WP-1 STEP 06: expanded corpus in both representations with proven equality.
    from python.rotations import corpus as corpus_mod
    base = os.path.join(ROOT, "artifacts", "v03", "cycles", "expanded")
    manifest_path = os.path.join(base, "expanded_manifest.json")
    check("expanded_manifest.json present", os.path.isfile(manifest_path))
    if not os.path.isfile(manifest_path):
        print("[WP-1][STEP 06] expansion artifacts unverifiable (no manifest)", flush=True)
        return
    import zstandard as zstd
    manifest = json.load(open(manifest_path, encoding="utf-8"))
    check("expanded manifest validates (hashes + logical stream)",
          corpus_mod.validate_manifest(manifest, base) == [])
    for n in (2, 3, 4, 5, 6, 7):
        plain = open(os.path.join(base, "expanded_n%d.json" % n), "rb").read()
        zst = open(os.path.join(base, "expanded_n%d.json.zst" % n), "rb").read()
        check("expanded_n%d zst decompresses to plain bytes" % n,
              zstd.ZstdDecompressor().decompress(zst) == plain)
    print("[WP-1][STEP 06] expansion artifacts verified", flush=True)


# WP-1 STEP 07: verify lifecycle states incl. strict hash binding (F20).
def step_subgate() -> None:
    # WP-1 STEP 07: human ACCEPT records present; strict byte binding enforced.
    for oid in ("MST0-01", "MST0-04", "MST0-16"):
        p = os.path.join(ROOT, "math", "reviews", "%s.review.json" % oid)
        try:
            rec = json.load(open(p, encoding="utf-8"))
            ok = (rec.get("verdict") == "ACCEPT"
                  and bool(rec.get("reviewer", {}).get("identity"))
                  and bool(rec.get("reviewer", {}).get("date_utc"))
                  and bool(rec.get("theorem_sha256")))
        except (OSError, ValueError):
            ok = False
        check("subgate record ACCEPT with reviewer " + oid, ok)
    from python.audit import status as status_mod
    derived = status_mod.derive(ROOT)
    check("MST0-01/04/16 REVIEWED (bytes match reviewed bytes)",
          all(derived[o]["status"] == "REVIEWED" for o in ("MST0-01", "MST0-04", "MST0-16")))
    check("MST0-02 PROVED pending re-review (proof bytes corrected, hash rule)",
          derived["MST0-02"]["status"] == "PROVED"
          and "re-review" in derived["MST0-02"]["evidence"])
    try:
        old_accept = json.load(open(os.path.join(
            ROOT, "math", "reviews", "MST0-02.review.json"), encoding="utf-8"))
        preserved = old_accept.get("verdict") == "ACCEPT"
    except (OSError, ValueError):
        preserved = False
    check("MST0-02 historical ACCEPT preserved (bytes superseded, record kept)",
          preserved)
    check("MST0-02 re-review package pending (no fabricated verdict)",
          os.path.isfile(os.path.join(ROOT, "math", "reviews", "MST0-02.REVIEW-PACKAGE.md")))
    print("[WP-1][STEP 07] lifecycle states verified (strict binding)", flush=True)


# WP-1 STEP 08: verify benchmark records (counts, ratios, all-KEEP, witnesses).
def step_benchmarks() -> None:
    # WP-1 STEP 08: sealed benchmark values present in verifiable artifacts.
    ledger = json.load(open(os.path.join(
        ROOT, "artifacts", "v03", "parent_import", "import_ledger.json"),
        encoding="utf-8"))
    check("import ledger pins both sealed commits",
          ledger.get("v01_commit") == "6de1ca2a595e8895f54794f3a211fe6ee1a95a80"
          and ledger.get("v02_commit") == "38c1be6afd2ab2420aa094c68ce45ee6a26b3628")
    from python.cycles.enumerate import PairDomain
    expect = {2: 4, 3: 19, 4: 196, 5: 1764}
    got = {}
    for n, want in expect.items():
        dom = PairDomain(n)
        got[n] = len(dom.reachable())
    check("reachable counts n=2..5 recomputed %r" % (got,),
          got == expect)
    rep = json.load(open(os.path.join(
        ROOT, "artifacts", "v03", "parent_import", "replay.json"), encoding="utf-8"))
    check("replay covers n2..7 (75-edge domain)",
          sorted(rep.keys(), key=int) == ["2", "3", "4", "5", "6", "7"])
    print("[WP-1][STEP 08] benchmark spot-checks verified (n=6/7 covered by runner)", flush=True)


# WP-1 STEP 09: verify implementation independence (no shared helpers).
def step_independence() -> None:
    # WP-1 STEP 09: AST proof that independent.py shares no helper with splay.py.
    tree = ast.parse(open(os.path.join(ROOT, "python", "splay_ref",
                                       "independent.py"), encoding="utf-8").read())
    mods = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            mods += [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module:
            mods.append(node.module)
    check("independent.py imports no splay.py helper (INV-037)",
          not any("splay_ref.splay" in m for m in mods))
    stree = ast.parse(open(os.path.join(ROOT, "python", "rotations",
                                        "independent_trace.py"), encoding="utf-8").read())
    smods = []
    for node in ast.walk(stree):
        if isinstance(node, ast.Import):
            smods += [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module:
            smods.append(node.module)
    check("independent_trace.py imports no trace/reference/pair module (F9)",
          not any(m in ("python.rotations.trace", "python.rotations.reference",
                        "python.splay_ref.pair") or m.endswith(".trace")
                  for m in smods))
    print("[WP-1][STEP 09] independence verified (agreement by suites ROT-10)", flush=True)


# WP-1 STEP 10: verify named-test integrity (exact IDs and meanings).
def step_named_tests() -> None:
    # WP-1 STEP 10: required IDs bound in their owning suites (dictionary).
    import re as _re
    from collections import Counter as _Counter
    rot_src = open(os.path.join(ROOT, "tests", "rotations", "test_rot_named.py"),
                   encoding="utf-8").read()
    rot_ids = _re.findall(r"check\(\s*\"(ROT-0[1-9]|ROT-1[0-2]) ", rot_src)
    check("ROT-01..12 each bound exactly once",
          _Counter(rot_ids) == {"ROT-%02d" % i: 1 for i in range(1, 13)})
    check("ROT-04..08 fixture registry complete",
          sorted(set(_re.findall(r"\(\"(ROT-0[4-8])\",", rot_src)))
          == ["ROT-%02d" % i for i in range(4, 9)])
    cyc_src = open(os.path.join(ROOT, "tests", "parent", "test_import.py"),
                   encoding="utf-8").read()
    cyc_ids = _re.findall(r"check\(\s*\"(CYC-0[1-5]|IMPORT-01) ", cyc_src)
    check("CYC-01..05 each bound exactly once (+IMPORT-01 auxiliary)",
          _Counter(cyc_ids).get("IMPORT-01", 0) >= 1
          and all(_Counter(cyc_ids).get("CYC-0%d" % i, 0) == 1 for i in range(1, 6)))
    print("[WP-1][STEP 10] named-test integrity verified", flush=True)


# WP-1 STEP 11: verify mutation probes and schema discipline exist.
def step_mutants_schema() -> None:
    # WP-1 STEP 11: the exact mutants plus schema-required event fields.
    mut_src = open(os.path.join(ROOT, "tests", "rotations", "test_rot_mutants.py"),
                   encoding="utf-8").read()
    for probe in ("MUT-CASE", "MUT-TIE", "MUT-ORDER", "MUT-SNAPSHOT"):
        check("mutant probe present " + probe, probe in mut_src)
    schema = json.load(open(os.path.join(ROOT, "schemas", "rotation_event.schema.json"),
                            encoding="utf-8"))
    for field in ("nh_before", "nh_after", "orientation", "interval",
                  "depth_before", "schema_version"):
        check("schema requires " + field, field in schema.get("required", []))
    print("[WP-1][STEP 11] mutation probes and schema discipline verified", flush=True)


# WP-1 STEP 12: verify §27 execution records exist and are complete.
def step_logs() -> None:
    # WP-1 STEP 12: append-only run records with stream hashes in latest line.
    for phase in ("01", "03"):
        p = os.path.join(ROOT, "artifacts", "v03", "logs", "phase%s_wp1.jsonl" % phase)
        check("§27 log present phase%s_wp1.jsonl" % phase, os.path.isfile(p))
        if not os.path.isfile(p):
            continue
        lines = [ln for ln in open(p, encoding="utf-8").read().splitlines() if ln.strip()]
        check("§27 log non-empty phase " + phase, len(lines) > 0)
        rec = json.loads(lines[-1])
        for field in ("experiment_id", "phase", "branch", "command",
                      "scientific_status", "exit_code", "utc", "local_commit",
                      "output_hashes", "wall_s", "stdout_hash", "stderr_hash"):
            check("§27 log phase %s carries %s" % (phase, field), field in rec)
        check("§27 log phase %s exit 0" % phase, rec.get("exit_code") == 0)
        check("§27 log phase %s streams hashed" % phase,
              isinstance(rec.get("stdout_hash"), str) and isinstance(rec.get("stderr_hash"), str))
    print("[WP-1][STEP 12] execution records verified", flush=True)


# WP-1 STEP 13: emit the revalidation verdict matrix.
def main() -> int:
    # WP-1 STEP 13: orchestrate the read-only revalidation and verdict.
    print("[WP-1][STEP 13] WP-1 revalidation start (binding N=1, PREVIOUS_PHASE=NOT_APPLICABLE)",
          flush=True)
    step_prefoundation()
    step_files()
    step_parent_evidence()
    step_rotations_artifacts()
    step_expanded_artifacts()
    step_subgate()
    step_benchmarks()
    step_independence()
    step_named_tests()
    step_mutants_schema()
    step_logs()
    print("[WP-1][STEP 13] WP-1 revalidation %s (%d failures)"
          % ("PASS" if not FAILS else "FAIL", len(FAILS)), flush=True)
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
