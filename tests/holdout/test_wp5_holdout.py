"""WP-5 holdout suite (HLD-01..12). Reads sealed WP-5 artifacts only; never the banks."""
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

from python.freeze import candidates as freeze_mod  # noqa: E402
from python.holdout import firewall as firewall_mod  # noqa: E402

FAILS: list = []


def check(name: str, cond: bool) -> None:
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        FAILS.append(name)


def _load(rel: str):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return json.load(f)


def test_hld() -> None:
    commit = _load("artifacts/v03/holdouts/candidate_set_commit.json")
    h3t_state = _load("artifacts/v03/holdouts/h3t_state.json")
    h1_reveal = _load("artifacts/v03/holdouts/h1_reveal.json")
    h2r_reveal = _load("artifacts/v03/holdouts/h2r_reveal.json")
    h3t_reveal = _load("artifacts/v03/holdouts/h3t_reveal.json")
    blobs = {fn: json.dumps(_load("artifacts/v03/holdouts/" + fn), sort_keys=True)
             for fn in ("candidate_set_commit.json", "h1_reveal.json",
                        "h2r_reveal.json", "h3t_reveal.json")}
    check("HLD-01 n8 never labeled fresh",
          not any("FRESH_N8" in b for b in blobs.values()))
    parent_h1 = firewall_mod.load_state(os.path.join(ROOT, "parent", "V02_H1_FIREWALL.json"))
    wp5_h1 = _load("artifacts/v03/holdouts/h1_firewall_wp5.json")
    check("HLD-02 H1 unread pre-freeze",
          parent_h1.get("state") == "EMPTY" and wp5_h1.get("contents_revealed") is False)
    check("HLD-03 H1 unlock at most once",
          h1_reveal.get("firewall_after") == "EMPTY" and h1_reveal.get("n_episodes") == 0)
    contract = open(os.path.join(ROOT, "prereg", "parent_contract.yaml"),
                    encoding="utf-8").read()
    check("HLD-04 H2R commitment exact",
          "BANK_COMMITTED" in contract and "unlock_count: 0" in contract
          and firewall_mod.load_state(
              os.path.join(ROOT, "parent", "V02_H2R_FIREWALL.json")).get("state")
          == "BANK_COMMITTED")
    wp5_h2r = _load("artifacts/v03/holdouts/h2r_firewall_wp5.json")
    check("HLD-05 H2R unread pre-freeze", wp5_h2r.get("contents_revealed") is False)
    check("HLD-06 H2R unlock at most once",
          h2r_reveal.get("firewall_after") == "BANK_COMMITTED"
          and "UNLOCKED" not in json.dumps(wp5_h2r))
    import zstandard as zstd
    bankdir = os.path.join(ROOT, "artifacts", "v03", "holdouts", "h3t_bank")
    commitment = _load("artifacts/v03/holdouts/h3t_commitment.json")
    streams = {}
    ok_counts = True
    for n, spec in sorted(commitment["sizes"].items()):
        with open(os.path.join(bankdir, "n%s.json.zst" % n), "rb") as f:
            eps = json.loads(zstd.ZstdDecompressor().decompress(f.read()).decode("utf-8"))
        if len(eps) != spec["count"]:
            ok_counts = False
        streams[n] = hashlib.sha256(
            "".join(sorted(e["episode_hash"] for e in eps)).encode("utf-8")).hexdigest().upper()
    logical = hashlib.sha256("".join(sorted(streams.values())).encode("utf-8")).hexdigest().upper()
    check("HLD-07 H3T commitment exact",
          ok_counts and logical == commitment["logical_stream"]
          and all(streams[n] == commitment["sizes"][n]["stream"] for n in streams))
    frozen_mtimes = [os.path.getmtime(os.path.join(
        ROOT, "artifacts", "v03", "hypotheses", m["calculus_id"] + ".json"))
        for m in commit["candidates"]]
    reveal_mtime = os.path.getmtime(os.path.join(
        ROOT, "artifacts", "v03", "holdouts", "h3t_reveal.json"))
    check("HLD-08 H3T unread pre-freeze (freeze predates reveal)",
          max(frozen_mtimes) < reveal_mtime)
    check("HLD-09 H3T unlock at most once",
          h3t_state.get("state") == "UNLOCKED_ONCE" and h3t_state.get("unlock_count") == 1)
    check("HLD-10 H3T no-regeneration-after-reveal (bytes still match commitment)",
          logical == commitment["logical_stream"])
    recomputed = freeze_mod.commit_set([
        json.load(open(os.path.join(ROOT, "artifacts", "v03", "hypotheses",
                                    m["calculus_id"] + ".json"), encoding="utf-8"))
        for m in commit["candidates"]])
    check("HLD-11 candidate-set hash immutable after reveal",
          recomputed["set_hash"] == commit["set_hash"]
          == h3t_state.get("candidate_set_hash"))
    try:
        bad = json.loads(json.dumps(json.load(open(os.path.join(
            ROOT, "artifacts", "v03", "hypotheses", "MSTC-0001.json"),
            encoding="utf-8"))))
        bad["injection_rules"][0]["k"] += 1
        freeze_mod.check_frozen_binding(
            json.load(open(os.path.join(ROOT, "artifacts", "v03", "hypotheses",
                                        "MSTC-0001.json"), encoding="utf-8")),
            bad["active_predicate"], bad["injection_rules"][0]["k"],
            bad["universal_constant_C"])
        check("HLD-12 post-holdout edit new ID", False)
    except ValueError:
        check("HLD-12 post-holdout edit new ID", True)


if __name__ == "__main__":
    test_hld()
    print("FAILURES:", FAILS if FAILS else "none")
    sys.exit(1 if FAILS else 0)
