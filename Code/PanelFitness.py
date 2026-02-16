from collections import defaultdict
import math

def Fitness(table):
    panelTable = [row[1:] for row in table] # Remove the Instituion ID (irrelevent)

    scoresById = defaultdict(list) # Create blank dict for grouping scores

    for row in panelTable: # Assign each score to relevant ID in dict
        id = row[0]
        score = float(row[1])
        scoresById[id].append(score)

    results = {}  # Output dictionary
    for id, scores in scoresById.items(): # Calculate a mean and standard deviation for each ID based on dict values
        x = len(scores)
        mean = sum(scores)/x  # Calculate mean
        standardDev = math.sqrt(sum((x - mean)**2 for x in scores)/(x-1)) if x>1 else 0  # Calculate standard deviation
        results[id] = {'mean': mean, 'SD':standardDev} # Populate and format output dictionary
    return results