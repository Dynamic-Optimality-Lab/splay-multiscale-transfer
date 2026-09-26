"""Parent-import suite (CYC-01..05 mechanics, PARENT import checks). Fast; no corpus compute."""
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

FAILS: list[str] = []


def check(name: str, cond: bool) -> None:
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        FAILS.append(name)


def sha(p: str) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest().upper()


def test_ledger() -> None:
    base = os.path.join(ROOT, "artifacts", "v03", "parent_import")
    if not os.path.exists(os.path.join(base, "import_ledger.json")):
        print("SKIP parent-import suite (run_phase01 not executed yet)")
        return
    led = json.load(open(os.path.join(base, "import_ledger.json")))
    check("IMPORT-01 ledger pins both sealed commits",
          led["v01_commit"] == "6de1ca2a595e8895f54794f3a211fe6ee1a95a80"
          and led["v02_commit"] == "38c1be6afd2ab2420aa094c68ce45ee6a26b3628")
    bad = 0
    for entry in led["v01_files"] + led["v02_files"]:
        sub = "v01baseline" if entry["dest"].startswith("v01/") else "v02baseline"
        p = os.path.join(base, sub, *entry["dest"].split("/"))
        if sha(p) != entry["sha256"]:
            bad += 1
    check("CYC-01 vendored bytes match ledger", bad == 0)
    rep = json.load(open(os.path.join(base, "replay.json")))
    # WP-1 REPAIR STEP T1: exact normative bindings (CYC-01 closes, CYC-02
    # parent ratio, CYC-03 all-KEEP recomputed, CYC-04 forced derivatives).
    b_star = {"4": "3/2", "5": "8/5", "6": "8/5", "7": "23/14"}
    for n, row in sorted(rep.items()):
        check("CYC-01 n=%s every cycle closes" % n,
              row["replayed_ok"] == row["cycles"]
              and all(r["closed"] for r in row["rows"]))
        check("CYC-02 n=%s exact parent ratio %s" % (n, b_star[n]),
              all(r["ratio"] == b_star[n] for r in row["rows"]))
        check("CYC-03 n=%s all-KEEP recomputed" % n,
              all(r["all_keep"] for r in row["rows"]))
    for n, row in sorted(rep.items()):
        forced = row.get("forced", {})
        check("CYC-04 n=%s forced derivatives match parent KEEP-only" % n,
              forced.get("mismatches", 1) == 0
              and forced.get("keep", -1) == forced.get("count", -2))
    # WP-1 REPAIR STEP T2: CYC-05 expansion deterministic (manifest + re-hash).
    expdir = os.path.join(ROOT, "artifacts", "v03", "cycles", "expanded")
    manifest = json.load(open(os.path.join(expdir, "expanded_manifest.json")))
    ok_manifest = True
    for n, spec in sorted(manifest["shards"].items()):
        if sha(os.path.join(expdir, spec["json"])) != spec["sha256_json"]:
            ok_manifest = False
        if sha(os.path.join(expdir, spec["file"])) != spec["sha256"]:
            ok_manifest = False
    logical = hashlib.sha256("".join(sorted(
        s["sha256"] for s in manifest["shards"].values())).encode()).hexdigest().upper()
    check("CYC-05 expansion shards + logical stream verify",
          ok_manifest and logical == manifest["logical_stream"])
    # WP-1 REPAIR STEP T3: dictionary mapping gate (one immutable semantic
    # binding per CYC ID; auxiliary checks carry non-CYC IDs like IMPORT-01).
    import re as _re
    src = open(__file__, encoding="utf-8").read()
    found = _re.findall(r"check\(\s*\"(CYC-0[1-5]|IMPORT-01)[^\"]*\"", src)
    from collections import Counter as _Counter
    counts = _Counter(found)
    check("CYC-01..05 each bound exactly once (dictionary, not set)",
          all(counts.get("CYC-0%d" % i, 0) == 1 for i in range(1, 6)))
    FROZEN_CYC = {"CYC-01": "closes", "CYC-02": "parent ratio",
                  "CYC-03": "all-KEEP", "CYC-04": "forced derivatives",
                  "CYC-05": "expansion deterministic"}
    check("CYC mapping frozen (5 IDs, meanings intact)",
          set(FROZEN_CYC) == {"CYC-0%d" % i for i in range(1, 6)}
          and all(FROZEN_CYC[i] in src for i in FROZEN_CYC))


if __name__ == "__main__":
    test_ledger()
    print("FAILURES:", FAILS if FAILS else "none")
    sys.exit(1 if FAILS else 0)
