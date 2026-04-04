import random, GreedyAlgo, Tools, csv

maxPapers = Tools.maxPapers
popSize = Tools.popSize
numGen = Tools.numGen
mutRate = Tools.mutRate

highWeight = Tools.highWeight
midWeight = Tools.midWeight
lowWeight = Tools.lowWeight

highWeightSubjects = Tools.highWeightSubjects

midWeightSubjects = Tools.midWeightSubjects

def SortSubjects(subject):
    if subject in highWeightSubjects:
        return highWeight
    if subject in midWeightSubjects:
        return midWeight
    else:
        return lowWeight

def Mutate(solution, academics, papers):
    mutateCount = random.randrange(1, int((len(academics.keys()) * mutRate) - 1))

    for _ in range(1, mutateCount):
        unassignedPapers = CalculateUnassigned(solution, papers)
        a1 = random.choice(list(solution.keys()))
        compatPap = []
        if solution[a1]:
            for paper in unassignedPapers:
                for subject in papers[paper]['subjects']:
                    if subject in academics[a1]:
                        compatPap.append(paper)

            if len(compatPap) > 0:
                acaBestPap = []
                for paper in compatPap:
                    paperBestSub = []

                    for subject in papers[paper]['subjects']:
                        if subject in academics[a1]:
                            paperBestSub.append(subject)

                    if len(paperBestSub) > 0:
                        paperBestSub = sorted(
                            paperBestSub,
                            key=lambda ind: SortSubjects(ind),
                            reverse=True
                        )
                        acaBestPap.append(paper)

                if len(acaBestPap) > 0:
                    acaBestPap = sorted(
                        acaBestPap,
                        key=lambda ind: papers[ind]["score"],
                        reverse=True
                    )
                    for x in range(len(acaBestPap)):
                        acaBestPap[x] = [acaBestPap[x], papers[acaBestPap[x]]["score"]]
                    acaWorstPap = sorted(
                        solution[a1],
                        key=lambda ind: papers[ind]["score"],
                        reverse=False
                    )
                    for x in range(len(acaWorstPap)):
                        acaWorstPap[x] = [acaWorstPap[x], papers[acaWorstPap[x]]["score"]]
                    if len(acaWorstPap) > 0:
                        solution[a1].remove(random.choice(acaWorstPap[0:int(len(acaWorstPap) / 2) + 1])[0])
                        solution[a1].append(random.choice(acaBestPap[0:int(len(acaBestPap) / 2) + 1])[0])
    return solution

def CalculateUnassigned(solution, papers):
    unassignedPapers = []

    for paper in papers:
        unassignedPapers.append(paper)

    for academic in solution:
        for paper in solution[academic]:
            if paper in unassignedPapers:
                unassignedPapers.remove(paper)
    
    return unassignedPapers

def GeneticAlgorithm(data):

    academics, papers = Tools.LoadData(data)

    greedySolution = GreedyAlgo.CreateIndWeighted(academics, papers)

    greedyFit = Tools.Fitness(greedySolution, academics, papers)

    print("Generating Pop...")
    population = []
    for x in range(popSize):
        Induvidual = GreedyAlgo.CreateInd(academics, papers)
        if x > 0:
            population.append(Mutate(Induvidual, academics, papers))
        else:
            population.append(Induvidual)
        totalAssignedPapers = sum(len(x) for x in population[-1].values())
        totalAcademics = sum(1 for v in population[-1].values())
        print("Generating Ind " + str(x) + ": " + str(totalAssignedPapers) + ", " + str(totalAcademics))
    print("Pop Generated")

    population = sorted(
        population,
        key=lambda ind: Tools.Fitness(ind, academics, papers)
    )

    bestFit = -2

    bestPop = population[:10] 

    nextGeneration = bestPop

    for generation in range(numGen):


        while len(nextGeneration) < popSize:
            contenders = random.sample(bestPop, int(len(bestPop/4)))
            parent = max(contenders, key=lambda x: Tools.Fitness(x, academics, papers))
            child = Mutate(parent, academics, papers)
            nextGeneration.append(child)


        print(f"Generation {generation}: Best Fitness so Far = {bestFit}, Greedy Fitness = {greedyFit}")
        totalAssignedPapers = sum(len(x) for x in population[0].values())
        totalAcademics = sum(1 for v in population[0].values())
        print(str(totalAssignedPapers) + ", " + str(totalAcademics))

        population = sorted(
            nextGeneration,
            key=lambda ind: Tools.Fitness(ind, academics, papers),
            reverse = True
        )

        currentBest = population[0]

        currentFit = Tools.Fitness(currentBest, academics, papers)

        if currentFit > bestFit:
            bestFit = currentFit
            bestInd = currentBest


    print("Final Fitness: " + str(bestFit))
    

        # CSV file name
    csv_filepath = "Data/Output.csv"

    # Define the field names (headers)
    fieldnames = ["Academic", "Subject(s)", "Papers"]

    data = []
    data.append(fieldnames)

    for academic in bestInd:
        subject = str(academics[academic][0])
        papers = bestInd[academic]
        data.append([academic, subject, papers])

    # Writing to CSV
    with open(csv_filepath, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
