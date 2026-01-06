import csv
from pathlib import Path

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