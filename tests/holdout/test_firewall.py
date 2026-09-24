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
    st = firewall_mod.load_state(os.path.join(ROOT, "artifacts", "v03", "holdouts", "h3t_state.json"))
    check("HLD-07 H3T BANK_COMMITTED unlock 0",
          st.get("state") == "BANK_COMMITTED" and st.get("unlock_count") == 0)
    try:
        firewall_mod.guard_read(os.path.join(ROOT, "artifacts", "v03", "holdouts", "h3t_state.json"),
                                False, "discovery-probe")
        check("HLD-08 real bank early read blocked", False)
    except PermissionError:
        check("HLD-08 real bank early read blocked", True)


if __name__ == "__main__":
    test_firewall()
    test_real_bank_state()
    print("FAILURES:", FAILS if FAILS else "none")
    sys.exit(1 if FAILS else 0)
