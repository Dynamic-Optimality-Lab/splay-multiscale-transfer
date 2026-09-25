"""Genetic-search driver (spec Phase-13 engine): seeded population evolution.

Fixed population, crossover (single-point splice of two histories), point mutation;
selection by exact objective (elitist). Deterministic via seed.
Console tag [WP4-STEP-06].
"""
from __future__ import annotations

import random


# WP4-STEP-06: genetic search over histories (deterministic, seeded).
def genetic(n: int, kind: str, length: int, generations: int, pop: int,
            seed: int, objective_fn) -> dict:
    """Evolve a history population; return best (exact scores)."""
    from python.adversary import generators as gen_mod
    rng = random.Random(seed)
    population = [gen_mod.build_history(rng, n, kind, length) for _ in range(pop)]
    scored = sorted(((objective_fn(h), h) for h in population), reverse=True,
                    key=lambda t: t[0])
    best_score = scored[0][0]
    for _ in range(generations):
        children = [list(scored[0][1])]
        while len(children) < pop:
            a = rng.choice(scored[: max(1, pop // 2)])[1]
            b = rng.choice(scored[: max(1, pop // 2)])[1]
            cut = rng.randrange(1, length)
            child = [tuple(e) for e in (list(a[:cut]) + list(b[cut:]))]
            if rng.random() < 0.3:
                j = rng.randrange(length)
                child[j] = ("KEEP" if child[j][0] == "DELETE" else "DELETE", child[j][1])
            children.append(child)
        scored = sorted(((objective_fn(h), h) for h in children), reverse=True,
                        key=lambda t: t[0])
        if scored[0][0] > best_score:
            best_score = scored[0][0]
    print("[WP4-STEP-06] genetic n=%d kind=%s: best=%s" % (n, kind, best_score), flush=True)
    return {"best": scored[0][1], "best_score": best_score,
            "generations": generations, "pop": pop}
