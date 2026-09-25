"""Holdout-firewall test suite (HLD mechanics). Fixture states only — never the real bank."""
import json
import os
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

from python.holdout import firewall as firewall_mod  # noqa: E402

FAILS: list[str] = []


def check(name: str, cond: bool) -> None:
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        FAILS.append(name)


def fixture(state: dict) -> str:
    """Disposable firewall state file (real bank never touched)."""
    fd, path = tempfile.mkstemp(prefix="hld_", suffix=".json")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(state, f)
    return path


def test_firewall() -> None:
    p = fixture({"state": "BANK_COMMITTED", "unlock_count": 0})
    try:
        firewall_mod.guard_read(p, False, "discovery-probe")
        check("HLD-02 early read blocked", False)
    except PermissionError:
        check("HLD-02 early read blocked", True)
    try:
        firewall_mod.guard_read(p, True, "post-freeze-evaluate")
        check("HLD-02 frozen-context read allowed", True)
    except PermissionError:
        check("HLD-02 frozen-context read allowed", False)
    p2 = fixture({"state": "UNLOCKED_ONCE", "unlock_count": 1})
    try:
        firewall_mod.guard_read(p2, True, "second-unlock")
        check("HLD-06 second unlock blocked", False)
    except PermissionError:
        check("HLD-06 second unlock blocked", True)
    for p_ in (p, p2):
        os.remove(p_)


def test_real_bank_state() -> None:
    # NOTE (WP-5 lifecycle update): Phase 15 consumed the bank once, so the live
    # firewall is UNLOCKED_ONCE/1 with a matching reveal record. The pre-freeze
    # BANK_COMMITTED behavior remains covered by fixture tests above and by the
    # WP-5 HLD suite (HLD-07 commitment exact, HLD-08 freeze-predates-reveal,
    # HLD-09 unlock-at-most-once); git history preserves the prior PASS.
    st = firewall_mod.load_state(os.path.join(ROOT, "artifacts", "v03", "holdouts", "h3t_state.json"))
    reveal = json.load(open(os.path.join(ROOT, "artifacts", "v03", "holdouts",
                                         "h3t_reveal.json"), encoding="utf-8"))
    import hashlib as _hashlib
    digest = _hashlib.sha256(json.dumps(reveal, sort_keys=True).encode("utf-8")).hexdigest().upper()
    check("HLD-07 H3T UNLOCKED_ONCE/1 with matching reveal (post WP-5)",
          st.get("state") == "UNLOCKED_ONCE" and st.get("unlock_count") == 1
          and st.get("reveal_sha256") == digest)
    # NOTE (WP-5 lifecycle update): post-reveal, replay reads against the recorded
    # reveal are legitimate; what must stay blocked is a SECOND unlock (STOP-30).
    # That is covered by the HLD-06 fixture above and by re-running the Phase-15
    # entry gate (refuses UNLOCKED_ONCE); here assert the live record is complete.
    check("HLD-08 real bank reveal record complete (replay reads auditable)",
          st.get("reveal_record") == "h3t_reveal.json"
          and bool(st.get("candidate_set_hash")))


if __name__ == "__main__":
    test_firewall()
    test_real_bank_state()
    print("FAILURES:", FAILS if FAILS else "none")
    sys.exit(1 if FAILS else 0)
