import random

from ca import step, seed_vehicles
from scenes import print_state
from metrics import count_vehicles


def simulate(
    roads,
    occ,
    steps,
    seed=None,
    print_every=1,
    reseed_on_empty=False,
    reseed_density=None,
    reseed_announce=False,
):
    rng = random.Random(seed)

    exits_per_step = []
    vehicles_per_step = []

    vehicles_per_step.append(count_vehicles(occ))

    for t in range(steps):
        if print_every and (t % print_every == 0):
            print(f"\n--- t={t} ---")
            print_state(roads, occ)

        occ, exits = step(roads, occ, rng=rng)

        if reseed_on_empty and count_vehicles(occ) == 0:
            if reseed_density is None:
                raise ValueError("reseed_density mora biti zadan ako reseed_on_empty=True")

            if reseed_announce:
                print(f"*** RESEED u t={t} ***")

            occ = seed_vehicles(roads, density=reseed_density, rng=rng)

        exits_per_step.append(exits)
        vehicles_per_step.append(count_vehicles(occ))

    return occ, {
        "exits_per_step": exits_per_step,
        "vehicles_per_step": vehicles_per_step,
    }