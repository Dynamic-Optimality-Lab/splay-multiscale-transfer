"""WP-6 seal suite (SEAL-01..12). Reads sealed outputs only; rebuilds nothing."""
import hashlib
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

from python.audit import lifecycle as lifecycle_mod  # noqa: E402
from python.audit import status as status_mod  # noqa: E402
from python.seal import finalize as seal_mod  # noqa: E402

FAILS: list = []


def check(name: str, cond: bool) -> None:
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        FAILS.append(name)


def _load(rel: str):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return json.load(f)


def _sha(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def test_seal() -> None:
    final = _load("artifacts/v03/seal/FINAL_RESULT.json")
    head = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True,
                          text=True, cwd=ROOT).stdout.strip()
    anc = subprocess.run(["git", "merge-base", "--is-ancestor", final["repo_head"], head],
                         capture_output=True, text=True, cwd=ROOT)
    # NOTE: pre-commit the seal records HEAD itself; post-commit it records the
    # direct seal parent. Ancestry (never rewriting) is the invariant.
    check("SEAL-01 head coherence (recorded head is ancestor-or-self, history kept)",
          final["repo_head"] == head or anc.returncode == 0)
    v02 = _load("parent/V02_SEAL.json")
    check("SEAL-02 parent chain exact",
          v02["sealed_commit"] == "38c1be6afd2ab2420aa094c68ce45ee6a26b3628"
          and v02["terminal_claim"] == "FINITE_DEBT_LAW_MINING_RESULTS"
          and v02["h1_firewall_state"] == "EMPTY"
          and v02["h2r_firewall_state"] == "BANK_COMMITTED")
    import yaml as _yaml
    tids = set(_yaml.safe_load(
        open(os.path.join(ROOT, "prereg", "threat_control_matrix.yaml"),
             encoding="utf-8")))
    sids = set(_yaml.safe_load(
        open(os.path.join(ROOT, "prereg", "stop_control_matrix.yaml"),
             encoding="utf-8")))
    check("SEAL-03 threat set exact T01..T90",
          tids == {"T%02d" % i for i in range(1, 91)})
    check("SEAL-04 stop set exact STOP-01..STOP-50",
          sids == {"STOP-%02d" % i for i in range(1, 51)})
    try:
        record = lifecycle_mod.audit(ROOT)
        check("SEAL-05 lifecycle audit clean (0 jumps, all pointers)",
              not record["jumps"] and not record["pointerless"])
    except ValueError:
        check("SEAL-05 lifecycle audit clean (0 jumps, all pointers)", False)
    manifest_lines = open(os.path.join(ROOT, "artifacts", "v03", "seal",
                                       "MANIFEST.sha256"), encoding="utf-8").read().splitlines()
    manifest = dict((ln.split("  ./")[1], ln.split("  ./")[0]) for ln in manifest_lines if "  ./" in ln)
    tracked = seal_mod.tracked_files(ROOT)
    missing = [f for f in tracked if f not in manifest]
    stale = [f for f in manifest if not os.path.isfile(os.path.join(ROOT, f))]
    drift = [f for f in tracked if f in manifest
             and _sha(os.path.join(ROOT, f)) != manifest[f]]
    members = set(seal_mod.archive_members(ROOT))
    check("SEAL-06 manifest complete (no missing/stale/drift; archive members covered)",
          not missing and not stale and not drift
          and members == (set(manifest) | {"artifacts/v03/seal/FINAL_RESULT.json",
                                           "artifacts/v03/seal/MANIFEST.sha256"}))
    import zstandard as zstd
    commitment = _load("artifacts/v03/holdouts/h3t_commitment.json")
    bankdir = os.path.join(ROOT, "artifacts", "v03", "holdouts", "h3t_bank")
    streams = {}
    ok = True
    for n, spec in sorted(commitment["sizes"].items()):
        with open(os.path.join(bankdir, "n%s.json.zst" % n), "rb") as f:
            eps = json.loads(zstd.ZstdDecompressor().decompress(f.read()).decode("utf-8"))
        if len(eps) != spec["count"]:
            ok = False
        streams[n] = hashlib.sha256(
            "".join(sorted(e["episode_hash"] for e in eps)).encode("utf-8")).hexdigest().upper()
        if streams[n] != spec["stream"]:
            ok = False
    logical = hashlib.sha256("".join(sorted(streams.values())).encode("utf-8")).hexdigest().upper()
    check("SEAL-07 shard/logical-stream consistency", ok and logical == commitment["logical_stream"]
          and logical == final["hashes"]["h3t_logical_stream"])
    try:
        arith = seal_mod.audit_arithmetic(ROOT)
        check("SEAL-08 exact arithmetic policy (decision modules float-free)",
              not arith["decision_module_hits"])
    except ValueError:
        check("SEAL-08 exact arithmetic policy (decision modules float-free)", False)
    regen = seal_mod.build_final_result(ROOT)
    sealed_bytes = open(os.path.join(ROOT, "artifacts", "v03", "seal",
                                     "FINAL_RESULT.json"), "rb").read()
    check("SEAL-09 result recomputation (byte-identical regeneration)",
          (json.dumps(regen, sort_keys=True, indent=2) + "\n").encode("utf-8") == sealed_bytes)
    arch = os.path.join(ROOT, "artifacts", "v03", "seal", seal_mod.ARCHIVE_NAME)
    sidecar = open(os.path.join(ROOT, "artifacts", "v03", "seal",
                                "ARCHIVE.sha256"), encoding="utf-8").read()
    check("SEAL-10 archive determinism (file matches sidecar)",
          sidecar.strip() == "%s  ./%s" % (_sha(arch), seal_mod.ARCHIVE_NAME))
    h1 = _load("parent/V02_H1_FIREWALL.json")
    h2r = _load("parent/V02_H2R_FIREWALL.json")
    h3t = _load("artifacts/v03/holdouts/h3t_state.json")
    h1r = _load("artifacts/v03/holdouts/h1_reveal.json")
    h2rr = _load("artifacts/v03/holdouts/h2r_reveal.json")
    check("SEAL-11 reveal-state truthfulness (EMPTY/COMMITTED/UNLOCKED_ONCE + labels)",
          h1["state"] == "EMPTY" and h1r["verdict"] == "FRESH_H1_NOT_APPLICABLE"
          and h2r["state"] == "BANK_COMMITTED" and h2rr["verdict"] == "FRESH_H2R_NOT_APPLICABLE"
          and h3t["state"] == "UNLOCKED_ONCE" and h3t["unlock_count"] == 1
          and h1r["fresh_claim"] is False and h2rr["fresh_claim"] is False)
    devs = all(os.path.isfile(os.path.join(ROOT, "artifacts", "v03", "hypotheses",
                                           "MSTC-DEV-000%d.json" % i)) for i in (1, 2, 3))
    kills = sum(1 for r in _load("artifacts/v03/holdouts/h3t_reveal.json")["results"]
                if r["first_violation"] is not None)
    check("SEAL-12 failed artifacts retained (dev hypotheses + kill witnesses)",
          devs and kills == 2
          and os.path.isfile(os.path.join(ROOT, "artifacts", "v03", "adversarial",
                                           "triage.json")))


if __name__ == "__main__":
    test_seal()
    print("FAILURES:", FAILS if FAILS else "none")
    sys.exit(1 if FAILS else 0)
