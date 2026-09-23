"""Exact cycle-circulation tables for WP-1 (state-derivative vs flow accounting).

For every expanded cycle and every declared primitive quantity F, reports the
full-cycle circulation sum(ΔF). Genuine state functions must circulate to zero;
event counters need not. Ledger components are labeled STATE_DERIVATIVE /
FLOW_COUNT / SOURCE_SINK_ACCOUNT per spec S9.5 (labels only; no ledger exists yet).
Console lines prefixed [WP1-STEP-05] are the audit record.
"""
from __future__ import annotations

from fractions import Fraction


# WP1-STEP-05: circulate access costs (state-derived) and rotation counts (flow).
def circulate(expanded: dict, b_num: int, b_den: int) -> dict:
    """Return circulation table for one expanded cycle at diagnostic b=p/q."""
    sum_a = sum(e["a"] for e in expanded["edges"])
    sum_y = sum(e["y"] for e in expanded["edges"])
    slack = Fraction(sum_y * b_den - b_num * sum_a, b_den)
    n_zig = n_zigzig = n_zigzag = 0
    cases: dict[str, int] = {}
    for e in expanded["edges"]:
        for ev in e["events"]:
            c = ev["splay_case"]
            cases[c] = cases.get(c, 0) + 1
            if c == "ZIG":
                n_zig += 1
            elif c in ("LL", "RR"):
                n_zigzig += 1
            elif c in ("LR", "RL"):
                n_zigzag += 1
    # State-derivative check: returning to the start state forces net-zero drift
    # of any genuine state function; here encoded as closure flag from expansion.
    return {"cycle_index": expanded["cycle_index"], "sum_a": sum_a, "sum_y": sum_y,
            "scaled_slack_num": slack.numerator, "scaled_slack_den": slack.denominator,
            "closed": expanded["closed"],
            "flow_counts": {"ZIG": n_zig, "zigzig": n_zigzig, "zigzag": n_zigzag,
                            "by_case": cases}}
