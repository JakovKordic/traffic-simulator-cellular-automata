import random

DIRS = ("N", "E", "S", "W")
DXY = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "W": (0, -1)}

PRIORITY = ("N", "E", "S", "W")

LEFT = {"N": "W", "W": "S", "S": "E", "E": "N"}
RIGHT = {"N": "E", "E": "S", "S": "W", "W": "N"}
OPPOSITE = {"N": "S", "S": "N", "E": "W", "W": "E"}

def build_roads(height, width, horizontal_rows, vertical_cols):
    roads = []
    for _ in range(height):
        row = [""] * width
        roads.append(row)

    for y in horizontal_rows:
        if 0 <= y < height:
            for x in range(width):
                if "E" not in roads[y][x]:
                    roads[y][x] += "E"
                if "W" not in roads[y][x]:
                    roads[y][x] += "W"

    for x in vertical_cols:
        if 0 <= x < width:
            for y in range(height):
                if "N" not in roads[y][x]:
                    roads[y][x] += "N"
                if "S" not in roads[y][x]:
                    roads[y][x] += "S"

    return roads

def is_intersection(roads, y, x):
    return (
        roads[y][x].count("N")
        and roads[y][x].count("S")
        and roads[y][x].count("E")
        and roads[y][x].count("W")
    )

def empty_state(height, width):
    occ = {}
    for d in DIRS:
        lane = []
        for _ in range(height):
            row = [False] * width
            lane.append(row)
        occ[d] = lane
    return occ

def seed_vehicles(roads, density, rng=None):
    if rng is None:
        rng = random.Random()

    h = len(roads)
    w = len(roads[0])
    occ = empty_state(h, w)

    for y in range(h):
        for x in range(w):
            allowed = roads[y][x]
            if allowed == "":
                continue
            for d in allowed:
                if rng.random() < density:
                    occ[d][y][x] = True
    return occ

def choose_turn(
    roads,
    y,
    x,
    incoming_dir,
    rng,
    p_straight=0.70,
    p_left=0.13,
    p_right=0.13,
    p_uturn=0.04,
):
    allowed = roads[y][x]

    straight = incoming_dir
    left = LEFT[incoming_dir]
    right = RIGHT[incoming_dir]
    uturn = OPPOSITE[incoming_dir]

    r = rng.random()
    if r < p_straight:
        first_choice = straight
    elif r < p_straight + p_left:
        first_choice = left
    elif r < p_straight + p_left + p_right:
        first_choice = right
    else:
        first_choice = uturn

    choices = [first_choice]
    for c in (straight, left, right, uturn):
        if c not in choices:
            choices.append(c)

    for c in choices:
        if c in allowed:
            return c

    return incoming_dir

def add_request(requests, key, item):
    if key not in requests:
        requests[key] = []
    requests[key].append(item)

def step(roads, occ, rng=None):
    if rng is None:
        rng = random.Random()

    h = len(roads)
    w = len(roads[0])
    next_occ = empty_state(h, w)

    requests = {}
    exits = 0

    for incoming_dir in DIRS:
        dy, dx = DXY[incoming_dir]
        for y in range(h):
            for x in range(w):
                if not occ[incoming_dir][y][x]:
                    continue

                ny, nx = y + dy, x + dx

                if not (0 <= ny < h and 0 <= nx < w):
                    exits += 1
                    continue

                if incoming_dir not in roads[ny][nx]:
                    add_request(requests, (y, x), (y, x, incoming_dir, incoming_dir))
                    continue

                if is_intersection(roads, ny, nx):
                    out_dir = choose_turn(roads, ny, nx, incoming_dir, rng)
                else:
                    out_dir = incoming_dir

                add_request(requests, (ny, nx), (y, x, incoming_dir, out_dir))

    inter_attempts = 0
    inter_waits = 0

    for (ty, tx), candidates in requests.items():
        is_int = is_intersection(roads, ty, tx)

        if is_int:
            inter_attempts += len(candidates)

        if len(candidates) == 1:
            fy, fx, incoming_dir, out_dir = candidates[0]
            next_occ[out_dir][ty][tx] = True
            continue

        if is_int:
            winner = None
            for p in PRIORITY:
                for c in candidates:
                    if c[2] == p:
                        winner = c
                        break
                if winner is not None:
                    break

            if winner is None:
                winner = rng.choice(candidates)

            fy, fx, incoming_dir, out_dir = winner
            next_occ[out_dir][ty][tx] = True

            inter_waits += (len(candidates) - 1)

            for fy2, fx2, incoming2, out2 in candidates:
                if (fy2, fx2, incoming2, out2) == winner:
                    continue
                next_occ[incoming2][fy2][fx2] = True

        else:
            by_lane = {}
            for c in candidates:
                lane = c[3]
                if lane not in by_lane:
                    by_lane[lane] = []
                by_lane[lane].append(c)

            for lane, lane_candidates in by_lane.items():
                if len(lane_candidates) == 1:
                    fy, fx, incoming_dir, out_dir = lane_candidates[0]
                    next_occ[out_dir][ty][tx] = True
                else:
                    winner = rng.choice(lane_candidates)
                    fy, fx, incoming_dir, out_dir = winner
                    next_occ[out_dir][ty][tx] = True

                    for fy2, fx2, incoming2, out2 in lane_candidates:
                        if (fy2, fx2, incoming2, out2) == winner:
                            continue
                        next_occ[incoming2][fy2][fx2] = True

    return next_occ, exits, inter_attempts, inter_waits