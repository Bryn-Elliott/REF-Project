import random, pandas as pd, os, subprocess, GreedyAlgo, Tools
from collections import defaultdict

maxPapers = 5
popSize = 100
numGen = 100
mutRate = 0.05

highWeight = 1.6
midWeight = 1.2
lowWeight = 1.0

highWeightSubjects = [
    "Clinical Medicine",
    "Public Health, Health Services and Primary Care"
]

midWeightSubjects = [
    "Business and Management Studies",
    "Psychology, Psychiatry and Neuroscience",
    "Allied Health Professions, Dentistry, Nursing and Pharmacy",
    "Law",
    "Biological Sciences",
    "Architecture, Built Environment and Planning",
    "Politics and International Studies",
    "Agriculture, Food and Veterinary Sciences",
    "Geography and Environmental Studies",
    "Economics and Econometrics",
    "Social Work and Social Policy",
    "Sociology",
    "Earth Systems and Environmental Sciences",
    "Sport and Exercise Sciences, Leisure and Tourism",
    "Anthropology and Development Studies",
    "Education",
    "Computer Science and Informatics",
]

def SortSubjects(subject):
    if subject in highWeightSubjects:
        return highWeight
    if subject in midWeightSubjects:
        return midWeight
    else:
        return lowWeight

def Mutate(solution, academics, papers):
    mutateCount = random.randrange(1, int((len(academics.keys()) * mutRate * 2) - 1))

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
                    solution[a1].remove(acaWorstPap[0][0])
                    solution[a1].append(acaBestPap[0][0])
    return solution

def Crossover(parent1, parent2, academics, papers):
    child = {a: [] for a in academics}
    used = set()

    target_total = int(2.5 * len(academics))

    # Combine both parents' assignments
    combined = []

    for academic in academics:
        for paper in parent1[academic]:
            combined.append((academic, paper))
        for paper in parent2[academic]:
            combined.append((academic, paper))

    random.shuffle(combined)

    for academic, paper in combined:
        if len(used) >= target_total:
            break

        if paper in used:
            continue

        if len(child[academic]) >= 5:
            continue

        # Check compatibility
        if any(sub in academics[academic] for sub in papers[paper]["subjects"]):
            child[academic].append(paper)
            used.add(paper)

    return child

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

    greedySolution = GreedyAlgo.CreateInd(academics, papers)

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

    for generation in range(numGen):
        population = sorted(
            population,
            key=lambda ind: Tools.Fitness(ind, academics, papers),
            reverse=True
        )

        nextGeneration = population[:10] 

        while len(nextGeneration) < popSize:
            contenders = random.sample(population, int(len(population)/10))
            parent1 = max(contenders, key=lambda x: Tools.Fitness(x, academics, papers))
            contenders.remove(parent1)
            parent2 = max(contenders, key=lambda x: Tools.Fitness(x, academics, papers))
            child = Crossover(parent1, parent2, academics, papers)
            child = Mutate(child, academics, papers)
            nextGeneration.append(child)

        population = sorted(population, key=lambda ind: Tools.Fitness(ind, academics, papers), reverse=True)
        currentBest = population[0]
        currentFit = Tools.Fitness(currentBest, academics, papers)

        bestGenFit = Tools.Fitness(population[0], academics, papers)

        print(f"Generation {generation}: Best Fitness of this Generation = {bestGenFit}, Greedy Fitness = {greedyFit}")
        totalAssignedPapers = sum(len(x) for x in population[0].values())
        totalAcademics = sum(1 for v in population[0].values())
        print(str(totalAssignedPapers) + ", " + str(totalAcademics))

    return population[0]
