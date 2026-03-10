import random
import pandas as pd
import os
from collections import defaultdict

maxPapers = 5
popSize = 1000
numGen = 2500
mutRate = 0.2

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

    return totalWeightedScore / totalPapers

def CreateIndividual(academics, papers):
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
            solution[chosen].append(paper)
    return solution

def Mutate(solution, academics, papers):
    if random.random() < mutRate:
        academic1, academic2 = random.sample(list(academics.keys()), 2)

        if solution[academic1]:
            paper = random.choice(solution[academic1])
            solution[academic1].remove(paper)
            solution[academic2].append(paper)

    return solution

def Crossover(parent1, parent2):
    child = defaultdict(list)

    for academic in parent1:
        if random.random() < 0.5:
            child[academic] = parent1[academic][:]
        else:
            child[academic] = parent2[academic][:]

    return child

def GeneticAlgorithm(data):
    academics, papers = LoadData(data)

    population = [
        CreateIndividual(academics, papers)
        for _ in range(popSize)
    ]

    for generation in range(numGen):
        population = sorted(
            population,
            key=lambda ind: Fitness(ind, academics, papers),
            reverse=True
        )

        nextGeneration = population[:10]  

        while len(nextGeneration) < popSize:
            parent1, parent2 = random.sample(population[:50], 2)
            child = Crossover(parent1, parent2)
            child = Mutate(child, academics, papers)
            nextGeneration.append(child)

        population = nextGeneration

        bestFit = Fitness(population[0], academics, papers)

        os.system('cls')
        print(nextGeneration[-1])

        print(f"Generation {generation}: Best Fitness = {bestFit}")

    return population[0]
