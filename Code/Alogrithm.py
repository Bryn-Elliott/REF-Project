import random
import pandas as pd
import os
from collections import defaultdict

maxPapers = 5
popSize = 100
numGen = 500
mutRate = 0.5

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

def LoadData(data):
    academicsPath = data[2]
    papersPath = data[3]
    academics = {}
    papers = {}

    acad_df = pd.read_csv(academicsPath)
    for _, row in acad_df.iterrows():
        name = row.iloc[0]
        subjects = [s.strip() for s in row.iloc[1].split(";")]
        academics[name] = subjects

    paper_df = pd.read_csv(papersPath)
    for _, row in paper_df.iterrows():
        name = row.iloc[0]
        subjects = [s.strip() for s in row.iloc[1].split(";")]
        score = int(row.iloc[2])
        papers[name] = {"subjects": subjects, "score": score}

    return academics, papers

def SubjectWeight(subject):
    if subject in highWeightSubjects:
        return highWeight
    elif subject in midWeightSubjects:
        return midWeight
    else:
        return lowWeight

def Fitness(solution, academics, papers):
    totalWeightedScore = 0
    totalPapers = 0

    for academic, assignedPapers in solution.items():
        if not (len(assignedPapers) <= maxPapers):
            return -1  


        for paper in assignedPapers:
            paperData = papers[paper]
            paperScore = paperData["score"]

            weights = [
                SubjectWeight(sub)
                for sub in paperData["subjects"]
                if sub in academics[academic]
            ]

            if not weights:
                return -1 
            

            weight = max(weights)
            totalWeightedScore += paperScore * weight
            totalPapers += 1

    if totalPapers == 0:
        return -1

    counter = {p: [0] for p in papers}

    for academic in solution:
        for paper in solution[academic]:
            counter[paper][0] = counter[paper][0] + 1
    
    for paper in counter:
        x = counter[paper][0]
        if x > 1:
            return -1
    
    totalAssignedPapers = sum(len(x) for x in solution.values())
    totalAcademics = sum(1 for v in solution.values())
    if totalAssignedPapers / totalAcademics != 2.5:
        return abs(2.5 - (totalAssignedPapers / totalAcademics)) * -1
    
    return totalWeightedScore / totalPapers

def CreateIndividual(academics, papers, unassignedPapers):
    solution = {a: [] for a in academics}
    for paper in papers:
        compatible = []

        for academic in academics:
            for subject in papers[paper]['subjects']:
                if subject in academics[academic]:
                    if len(solution[academic]) < 5:
                        compatible.append(academic)
                        break

        if compatible:
            chosen = random.choice(compatible)
            assigned = False
            while assigned == False:
                if paper in unassignedPapers:
                    solution[chosen].append(paper)
                    unassignedPapers.remove(paper)
                    assigned = True

        totalAssignedPapers = sum(len(x) for x in solution.values())
        totalAcademics = sum(1 for v in solution.values())
        if totalAssignedPapers / totalAcademics == 2.5:
            return solution, unassignedPapers
    return solution, unassignedPapers

def Mutate(solution, academics, papers, unassignedPapers):

    if random.random() < mutRate:
        if random.random() < 0.5:

            academic = random.choice(list(academics.keys()))

            if solution[academic]:
                paper = random.choice(solution[academic])
                solution[academic].remove(paper)
                solution[academic].append(random.choice(unassignedPapers))

    return solution

def Crossover(parent1, parent2, unassignedPapers):
    child = defaultdict(list)

    for academic in parent1:
        if random.random() < 0.5:
            child[academic] = parent1[academic][:]
            for paper in parent2[academic][:]:
                if paper not in unassignedPapers:
                    unassignedPapers.append(paper)
        else:
            child[academic] = parent2[academic][:]
            for paper in parent1[academic][:]:
                if paper not in unassignedPapers:
                    unassignedPapers.append(paper)
    return child

def GeneticAlgorithm(data):
    academics, papers = LoadData(data)

    print("Generating Pop...")
    population = []
    unassignedPapers = []
    for x in range(popSize):
        unassignedPapers.append(list(papers))
        temp = CreateIndividual(academics, papers, unassignedPapers[x])
        population.append(temp[0])
        unassignedPapers[x] = (temp[1])
        totalAssignedPapers = sum(len(x) for x in population[-1].values())
        totalAcademics = sum(1 for v in population[-1].values())
        print("Generating Ind " + str(x) + ": " + str(totalAssignedPapers) + ", " + str(totalAcademics))
    print("Pop Generated")

    for generation in range(numGen):
        population = sorted(
            population,
            key=lambda ind: Fitness(ind, academics, papers),
            reverse=True
        )

        nextGeneration = population[:10] 

        while len(nextGeneration) < popSize:
            parent1, parent2 = random.sample(population[:50], 2)
            child = Crossover(parent1, parent2, unassignedPapers)
            child = Mutate(child, academics, papers, unassignedPapers)
            nextGeneration.append(child)

        population = nextGeneration

        unassignedPapers = list(papers)
        for induvidual in population:
            for academic in induvidual:
                for paper in induvidual[academic]:
                    unassignedPapers.remove(paper)

        bestFit = Fitness(population[0], academics, papers)

        worstFit = Fitness(population[-1], academics, papers)

        print(f"Generation {generation}: Best Fitness = {bestFit}, Worst Fitness = {worstFit}")
        totalAssignedPapers = sum(len(x) for x in population[0].values())
        totalAcademics = sum(1 for v in population[0].values())
        print(str(totalAssignedPapers) + ", " + str(totalAcademics))

    return population[0]
