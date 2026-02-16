from collections import defaultdict
import math

def Fitness(table):
    panelTable = [row[1:] for row in table]

    scoresById = defaultdict(list)

    for row in panelTable:
        id = row[0]
        score = float(row[1])
        scoresById[id].append(score)

    results = {}
    for id, scores in scoresById.items():
        x = len(scores)
        mean = sum(scores)/x
        standardDev = math.sqrt(sum((x - mean)**2 for x in scores)/(x-1)) if x>1 else 0
        results[id] = {'mean': mean, 'SD':standardDev}
    return results