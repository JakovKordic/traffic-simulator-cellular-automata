DIRS = ("N", "E", "S", "W")
DXY = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "W": (0, -1)}

PRIORITY = ("N", "E", "S", "W")

LEFT = {"N": "W", "W": "S", "S": "E", "E": "N"}
RIGHT = {"N": "E", "E": "S", "S": "W", "W": "N"}
OPPOSITE = {"N": "S", "S": "N", "E": "W", "W": "E"}