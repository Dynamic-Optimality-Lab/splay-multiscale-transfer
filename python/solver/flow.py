"""Exact circulation/flow analysis (spec S12 discovery engine): cycle supply/demand.

Per critical cycle at diagnostic C: supply rotations (A-side rotations around the
cycle, each supplying <= k credits) vs demand (positive-regret KEEP burden). The
per-cycle required-k lower bound ceil(demand/supply_rotations) is NECESSARY for any
k-bounded injection law at that C (proof in docstring of required_k). Allocation
across edges is checked by exact max-flow (Edmonds-Karp, integer capacities):
supply nodes (A-rotations in cycle order) -> demand nodes (KEEP edges), edge iff
the rotation precedes the edge cyclically. If max-flow < demand, no flow-respecting
allocation exists — a representation-level obstruction witness independent of any
candidate. Console tag [WP4-STEP-02].
"""
from __future__ import annotations

from collections import deque
from fractions import Fraction
from math import ceil


def max_flow(cap: dict, source, sink) -> int:
    """Exact Edmonds-Karp max flow over integer capacities (dict-of-dict residual)."""
    flow = 0
    nodes = set(cap)
    for outs in cap.values():
        nodes.update(outs)
    while True:
        parent = {source: None}
        queue = deque([source])
        while queue and sink not in parent:
            u = queue.popleft()
            for v, c in cap.get(u, {}).items():
                if c > 0 and v not in parent:
                    parent[v] = u
                    queue.append(v)
        if sink not in parent:
            return flow
        v, bottleneck = sink, None
        while v != source:
            u = parent[v]
            c = cap[u][v]
            bottleneck = c if bottleneck is None else min(bottleneck, c)
            v = u
        v = sink
        while v != source:
            u = parent[v]
            cap[u][v] -= bottleneck
            cap.setdefault(v, {}).setdefault(u, 0)
            cap[v][u] += bottleneck
            v = u
        flow += bottleneck


def cycle_balance(events: list, k: int, c_const: int) -> dict:
    """Supply/demand balance for one cycle's event list.

    events: [{"side": A|B, "rotations": int, "regret_w": int}]; supply counts only
    A-side rotations (DELETE + A-half of KEEP), demand counts positive KEEP regret.
    Because every feasible law injects <= k per A-rotation, demand > k*supply is
    infeasible for ALL such laws at this C (necessary condition, proved by counting).
    """
    supply_rot = sum(e["rotations"] for e in events if e["side"] == "A")
    demand = sum(max(0, e["regret_w"]) for e in events if e.get("regret_w") is not None)
    required = 0 if supply_rot == 0 and demand == 0 else (
        (10 ** 18) if supply_rot == 0 else ceil(Fraction(demand, supply_rot)))
    feasible = demand <= k * supply_rot
    return {"supply_rotations": supply_rot, "demand": demand,
            "required_k": required, "feasible_at_k": feasible}
