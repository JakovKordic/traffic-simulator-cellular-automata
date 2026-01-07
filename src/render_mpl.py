import numpy as np
from ca import DIRS, is_intersection

def build_base_layer(roads):
    h = len(roads)
    w = len(roads[0])
    base = np.zeros((h, w), dtype=float)

    for y in range(h):
        for x in range(w):
            allowed = roads[y][x]
            if allowed == "":
                base[y, x] = 0.0
            else:
                base[y, x] = 0.2
                if is_intersection(roads, y, x):
                    base[y, x] = 0.35
    return base

def occ_to_overlay(occ):
    h = len(next(iter(occ.values())))
    w = len(next(iter(occ.values()))[0])

    overlay = np.zeros((h, w), dtype=float)

    dir_value = {"N": 0.65, "E": 0.75, "S": 0.85, "W": 0.95}

    for d in DIRS:
        lane = occ[d]
        val = dir_value.get(d, 0.7)
        for y in range(h):
            for x in range(w):
                if lane[y][x]:
                    overlay[y, x] = max(overlay[y, x], val)

    return overlay