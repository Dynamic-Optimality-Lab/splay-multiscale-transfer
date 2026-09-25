"""Simulated-annealing driver (spec Phase-13 engine): seeded stochastic search.

Same objective interface as hillclimb; temperature schedule geometric from T0;
deterministic via seed. Console tag [WP4-STEP-06].
"""
from __future__ import annotations

import math
import random


# WP4-STEP-06: annealing over histories (deterministic, seeded).
def anneal(n: int, kind: str, length: int, steps: int, seed: int, objective_fn,
           t0: float = 2.0, decay: float = 0.97) -> dict:
    """Geometric-cooling anneal; return trajectory + best (exact scores)."""
    from python.adversary import generators as gen_mod
    rng = random.Random(seed)
    cur = gen_mod.build_history(rng, n, kind, length)
    cur_score = objective_fn(cur)
    best, best_score = list(cur), cur_score
    start = cur_score
    temp = t0
    for _ in range(steps):
        nxt = [list(e) for e in cur]
        j = rng.randrange(len(nxt))
        if rng.random() < 0.5:
            nxt[j][0] = "KEEP" if nxt[j][0] == "DELETE" else "DELETE"
        else:
            nxt[j][1] = rng.randint(1, n)
        nxt = [tuple(e) for e in nxt]
        score = objective_fn(nxt)
        if score >= cur_score or rng.random() < math.exp((score - cur_score) / max(temp, 1e-9)):
            cur, cur_score = nxt, score
        if cur_score > best_score:
            best, best_score = list(cur), cur_score
        temp *= decay
    print("[WP4-STEP-06] anneal n=%d kind=%s: start=%s best=%s"
          % (n, kind, start, best_score), flush=True)
    return {"best": best, "best_score": best_score, "start": start, "steps": steps}
