"""PA translated operation vocabulary (L6MAP-v0.3.1): structural event records.

Source (L6 v1): PAIR_UP / interval member insert-delete / split / convert /
transfer / heap-child exchange. Verdict: SAME for the event vocabulary.
Paid/free classification is explicitly NOT transplanted (prereg paid_free_rule):
whether an op is paid in Pair Access is re-derived in WP-6, never cited.
Each constructor returns a frozen record; no cost semantics attached.
Console tag [WP2A-STEP-02].
"""
from __future__ import annotations

OPS = ("PAIR_UP", "DELETE_INTERVAL_MEMBER", "INSERT_INTERVAL_MEMBER",
       "SPLIT_INTERVAL", "CONVERT_INTERVAL", "TRANSFER_INTERVAL",
       "HEAP_CHILD_EXCHANGE")


def make_op(op: str, trigger: str, inputs: list, outputs: list) -> dict:
    """Frozen structural op record (no paid/free claim, no cost claim)."""
    if op not in OPS:
        raise ValueError("unknown translated op %r" % op)
    return {"op": op, "trigger_event": trigger, "inputs": list(inputs),
            "outputs": list(outputs), "paid_free": "UNDETERMINED_PRE_WP6"}
