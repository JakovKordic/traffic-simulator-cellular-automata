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