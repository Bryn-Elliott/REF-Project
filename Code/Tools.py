import pandas as pd

data = ['Data/REF 2021 Results - Avg by Panel & Institution.csv', 'Data/REF 2021 Results - All.xlsx', 'Data/Academics.csv', 'Data/Papers.csv'] # Input data paths

academicsLen = 1590
AcaPapRatio = 6

subjects = [
"Clinical Medicine",
"Public Health, Health Services and Primary Care",
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
"Chemistry",
"Art and Design: History, Practice and Theory",
"Area Studies",
"Physics",
"Music, Drama, Dance, Performing Arts, Film and Screen Studies",
"Modern Languages and Linguistics",
"Mathematical Sciences",
"English Language and Literature",
"Computer Science and Informatics",
"History",
"Engineering",
"Classics",
"Archaeology",
"Philosophy",
"Theology and Religious Studies",
"Communication, Cultural and Media Studies, Library and Information Management"
]

numAcaSubjects = [1, 2, 3, 4]
numAcaSubWeight = [90, 5, 3, 2]

numPapSubjects = [1, 2]
numPapSubWeight = [90, 10]

maxPapers = 5
popSize = 100
numGen = 500
mutRate = 0.01

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


def Fitness(solution, academics, papers):
    total = 0
    count = 0

    for academic in solution:
        for paper in solution[academic]:
            weights = [
                SubjectWeight(sub)
                for sub in papers[paper]["subjects"]
                if sub in academics[academic]
            ]
            if weights:
                total += papers[paper]["score"] * max(weights)
                count += 1

    return total / count if count else 0

def SubjectWeight(subject):
    if subject in highWeightSubjects:
        return highWeight
    elif subject in midWeightSubjects:
        return midWeight
    else:
        return lowWeight
    
def LoadData(data):
    academicsPath = data[2]
    papersPath = data[3]
    academics = {}
    papers = {}

    acad_df = pd.read_csv(academicsPath)
    for _, row in acad_df.iterrows():
        name = row.iloc[0]
        subjects = [s.strip() for s in row.iloc[1].split(";")]
        academics[name] = list(subjects)

    paper_df = pd.read_csv(papersPath)
    for _, row in paper_df.iterrows():
        name = row.iloc[0]
        subjects = [s.strip() for s in row.iloc[1].split(";")]
        score = int(row.iloc[2])
        papers[name] = {"subjects": list(subjects), "score": score}

    return academics, papers
