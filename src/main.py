import random
import csv
from pathlib import Path

from ca import build_roads, seed_vehicles
from simulation import simulate

def write_metrics_csv(path, metrics):
    vehicles = metrics["vehicles_per_step"]
    exits = metrics["exits_per_step"]

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["t", "vehicles", "exits"])
        for t in range(len(vehicles)):
            ex = 0 if t == 0 else exits[t - 1]
            w.writerow([t, vehicles[t], ex])

def run_one(cfg, print_every=0):
    height = cfg["grid"]["height"]
    width = cfg["grid"]["width"]

    horizontal_rows = cfg["roads"]["horizontal_rows"]
    vertical_cols = cfg["roads"]["vertical_cols"]

    density = cfg["traffic"]["density"]
    steps = cfg["traffic"]["steps"]
    seed = cfg["traffic"]["seed"]

    reseed_cfg = cfg["traffic"].get("reseed", {})
    reseed_enabled = reseed_cfg.get("enabled", False)
    reseed_density = reseed_cfg.get("density", density)
    reseed_announce = reseed_cfg.get("announce", False)

    roads = build_roads(height, width, horizontal_rows, vertical_cols)

    rng0 = random.Random(seed)
    occ0 = seed_vehicles(roads, density=density, rng=rng0)

    occ_final, metrics = simulate(
        roads,
        occ0,
        steps=steps,
        seed=seed,
        print_every=print_every,
        reseed_on_empty=reseed_enabled,
        reseed_density=reseed_density,
        reseed_announce=reseed_announce,
    )
    return occ_final, metrics