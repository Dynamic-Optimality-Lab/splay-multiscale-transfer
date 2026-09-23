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
    check("CYC-00 ledger pins both sealed commits",
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
    for n, row in rep.items():
        check("CYC-02 n=%s all cycles replayed" % n, row["replayed_ok"] == row["cycles"])
        check("CYC-03 n=%s ratio rows consistent" % n,
              all(r["mismatch_count"] == 0 for r in row["rows"]))


if __name__ == "__main__":
    test_ledger()
    print("FAILURES:", FAILS if FAILS else "none")
    sys.exit(1 if FAILS else 0)
