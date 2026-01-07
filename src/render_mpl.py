import numpy as np
from ca import is_intersection

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