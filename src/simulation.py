import random

from ca import step, seed_vehicles
from metrics import count_vehicles


def simulate(
    roads,
    occ,
    steps,
    seed=None,
    reseed_on_empty=False,
    reseed_density=None,
    reseed_announce=False,
):
    rng = random.Random(seed)

    exits_per_step = []
    vehicles_per_step = []

    inter_attempts_per_step = []
    inter_waits_per_step = []

    vehicles_per_step.append(count_vehicles(occ))

    for t in range(steps):
        occ, exits, inter_attempts, inter_waits = step(roads, occ, rng=rng)

        if reseed_on_empty and count_vehicles(occ) == 0:
            if reseed_density is None:
                raise ValueError("reseed_density mora biti zadan ako reseed_on_empty=True")

            if reseed_announce:
                print(f"*** RESEED u t={t} ***")

            occ = seed_vehicles(roads, density=reseed_density, rng=rng)

        exits_per_step.append(exits)
        vehicles_per_step.append(count_vehicles(occ))

        inter_attempts_per_step.append(inter_attempts)
        inter_waits_per_step.append(inter_waits)

    return occ, {
        "exits_per_step": exits_per_step,
        "vehicles_per_step": vehicles_per_step,
        "intersection_attempts_per_step": inter_attempts_per_step,
        "intersection_waits_per_step": inter_waits_per_step,
    }