import GreedyAlgo, Tools, copy

academics, papers = Tools.LoadData(Tools.data)

def HillClimb(): 
    solution = GreedyAlgo.CreateIndWeighted(academics, papers)

    fitOverTime = []

    fitOverTime.append([0, Tools.Fitness(solution, academics, papers)])


    unassignedPapers = Tools.CalculateUnassigned(solution, papers)

    count = 0

    while True: 
        improvements = []
        for academic in solution:
            for paper1 in solution[academic]:
                for paper2 in unassignedPapers:
                    solutionCopy = copy.deepcopy(solution)
                    solutionCopy[academic].remove(paper1)
                    solutionCopy[academic].append(paper2)
                    if Tools.Fitness(solutionCopy, academics, papers) > Tools.Fitness(solution, academics, papers):
                        improvements.append([academic, paper1, paper2, Tools.Fitness(solutionCopy, academics, papers) - Tools.Fitness(solution, academics, papers)])
        if len(improvements) > 0:
            improvements = sorted(improvements, key=lambda ind: ind[3])
            bestImprove = improvements[0]
            solution[bestImprove[0]].remove(bestImprove[1])
            unassignedPapers.append(bestImprove[1])
            solution[bestImprove[0]].append(bestImprove[2])
            unassignedPapers.remove(bestImprove[2])
            count += 1
            print("improvements made: " + str(count) + ' ' + str(Tools.Fitness(solution, academics, papers)))
        else:
            return [fitOverTime, fitOverTime[0]]
        fitOverTime.append([count, Tools.Fitness(solution, academics, papers)])
