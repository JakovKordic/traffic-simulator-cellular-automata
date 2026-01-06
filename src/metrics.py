from ca import DIRS

def count_vehicles(occ):
    total = 0
    for d in DIRS:
        for row in occ[d]:
            for cell in row:
                if cell:
                    total += 1
    return total