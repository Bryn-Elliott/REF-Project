import Alogrithm as GA
import random

data = ['Data/REF 2021 Results - Avg by Panel & Institution.csv', 'Data/REF 2021 Results - All.xlsx', 'Data/Academics.csv', 'Data/Papers.csv'] # Input data paths

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
def Main():
    academics, papers = GA.LoadData(data)

    scoredPapers = []

    for paper in papers:
        weights = []
        for subject in papers[paper]["subjects"]:
            weights.append(SortSubjects(subject))
        sortedWeights = sorted(weights)
        papers[paper]["score"] = papers[paper]["score"] * sortedWeights[0]

    sortedPapers = sorted(papers, key=lambda paper: papers[paper]["score"])

    solution = {a: [] for a in academics}

    for paper in sortedPapers:
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

        totalAssignedPapers = sum(len(x) for x in solution.values())
        totalAcademics = sum(1 for v in solution.values())
        if totalAssignedPapers / totalAcademics == 2.5:
            break

    print(GA.Fitness(solution, academics, papers))


def SortSubjects(subject):
    if subject in highWeightSubjects:
        return highWeight
    if subject in midWeightSubjects:
        return midWeight
    else:
        return lowWeight
    
Main()