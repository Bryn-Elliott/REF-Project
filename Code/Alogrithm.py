import random
import pandas as pd
import numpy as np
from collections import defaultdict

minPapers = 1
maxPapers = 5
popSize = 1000
numGen = 200
mutRate = 0.01

# Subject weight mapping
highWeight = 1.6
midWeight = 1.2
lowWeight = 1.0

# Define which subjects get which weights
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

def loadData(data):
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
    total_weighted_score = 0
    total_papers = 0

    for academic, assigned_papers in solution.items():
        if not (minPapers <= len(assigned_papers) <= maxPapers):
            print('too many or too few papers per aca')
            return -1  # Invalid solution


        for paper in assigned_papers:
            paper_data = papers[paper]
            paper_score = paper_data["score"]

            # Get best matching subject weight
            weights = [
                SubjectWeight(sub)
                for sub in paper_data["subjects"]
                if sub in academics[academic]
            ]

            if not weights:
                print('paper assigned to incomp aca')
                return -1  # Paper assigned to incompatible academic)

            weight = max(weights)
            total_weighted_score += paper_score * weight
            total_papers += 1

    if total_papers == 0:
        print('total papers = 0')
        return -1


    return total_weighted_score / total_papers

def CreateIndividual(academics, papers):
    
    # Start empty
    solution = {a: [] for a in academics}

    paper_list = list(papers.keys())
    random.shuffle(paper_list)

    for paper in paper_list:

        compatible = []

        for academic in academics:
            if any(sub in academics[academic]
                   for sub in papers[paper]["subjects"]):
                compatible.append(academic)

        if compatible:
            x = False
            while x == False:
                chosen = random.choice(compatible)
                x = True
                if chosen in solution:
                    if len(solution) < len(academics):
                        x = False
            
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
    academics, papers = loadData(data)

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

        nextGeneration = population[:10]  # Elitism

        while len(nextGeneration) < popSize:
            parent1, parent2 = random.sample(population[:50], 2)
            child = Crossover(parent1, parent2)
            child = Mutate(child, academics, papers)
            nextGeneration.append(child)

        population = nextGeneration

        best_fit = Fitness(population[0], academics, papers)
        print(f"Generation {generation}: Best Fitness = {best_fit}")

    return population[0]
