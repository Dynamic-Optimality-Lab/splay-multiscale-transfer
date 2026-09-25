"""Hill-climb driver (spec Phase-13 engine): maximize an exact objective.

Objective is either a candidate's max residual (representation stress) or the
actual Splay ratio (negative-branch triage). Deterministic seeds; mutation =
single-access resample/perturbation. Console tag [WP4-STEP-06].
"""
from __future__ import annotations

import random


# WP4-STEP-06: hill climb over histories (deterministic, seeded).
def hillclimb(n: int, kind: str, length: int, steps: int, seed: int, objective_fn) -> dict:
    """Climb by single-access mutations; return trajectory + best (exact scores)."""
    from python.adversary import generators as gen_mod
    rng = random.Random(seed)
    cur = gen_mod.build_history(rng, n, kind, length)
    cur_score = objective_fn(cur)
    best, best_score = list(cur), cur_score
    traj = [cur_score]
    for _ in range(steps):
        nxt = [list(e) for e in cur]
        j = rng.randrange(len(nxt))
        if rng.random() < 0.5:
            nxt[j][0] = "KEEP" if nxt[j][0] == "DELETE" else "DELETE"
        else:
            nxt[j][1] = rng.randint(1, n)
        nxt = [tuple(e) for e in nxt]
        score = objective_fn(nxt)
        traj.append(score)
        if score > best_score:
            best, best_score = nxt, score
    print("[WP4-STEP-06] hillclimb n=%d kind=%s: start=%s best=%s"
          % (n, kind, traj[0], best_score), flush=True)
    return {"best": best, "best_score": best_score, "start": traj[0], "steps": steps}
