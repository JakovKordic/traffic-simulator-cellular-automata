import numpy as np
import matplotlib.pyplot as plt

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
    any_lane = next(iter(occ.values()))
    h = len(any_lane)
    w = len(any_lane[0])

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

def init_mpl_view(roads, occ0):
    base = build_base_layer(roads)

    fig, ax = plt.subplots()
    ax.set_title("Simulacija prometa (cellular automata)")
    ax.set_xticks([])
    ax.set_yticks([])

    frame0 = np.clip(base + occ_to_overlay(occ0), 0.0, 1.0)
    im = ax.imshow(frame0, interpolation="nearest", vmin=0.0, vmax=1.0)

    text = ax.text(
        0.01,
        0.99,
        "",
        transform=ax.transAxes,
        va="top",
        ha="left",
    )

    return fig, ax, im, text, base
