from ca import DIRS

def count_vehicles(occ):
    total = 0
    for d in DIRS:
        for row in occ[d]:
            for cell in row:
                if cell:
                    total += 1
    return total

def vehicles_per_direction(occ, d):
    total = 0
    for row in occ[d]:
        for cell in row:
            if cell:
                total += 1
    return total

def total_exits(exits_per_step):
    return sum(exits_per_step)