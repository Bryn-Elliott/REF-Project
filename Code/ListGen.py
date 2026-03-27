import random as rnd, pandas as pd, random


academics = []
papers = []

academicsLen = 1000
AcaPapRatio = 6
papersLen = int(AcaPapRatio * academicsLen)

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

numSubjects = [1, 2, 3, 4]
numSubWeight = [90, 5, 3, 2]

n = 0

for x in range(0, academicsLen):
    academicName = ('Academic ' + str(x))
    numSub = rnd.choices(numSubjects, weights=numSubWeight, k=1)[0]
    acaSubjects = rnd.choices(subjects, weights=None, k=numSub)
    academics.append([academicName, acaSubjects])
    n += 1

numSubjects = [1, 2]
numSubWeight = [90, 10]
scores = [1, 2, 3, 4]
scoreWeight = [1, 2, 3, 2]

y = 0

academicCount = 0

for x in range(0, papersLen):
    paper = []
    subjects = []
    paperName = 'Paper ' + str(x)
    numSub = rnd.choices(numSubjects, weights=numSubWeight, k=1)[0]
    for z in range(0, numSub):
        academic = rnd.randint(0, int(academicsLen - 1))
        subject = rnd.choice(academics[academic][1])
        subjects.append(subject)
    paper.append(paperName)
    paper.append(subjects)
    paper.append(rnd.choices(scores, weights=scoreWeight, k=1)[0])
    papers.append(paper)
    y += 1

df = pd.DataFrame(academics, columns=['Name','Subjects'])
csvFilePath = 'Data/Academics.csv'
df.to_csv(csvFilePath, index=False, header=True)
print(n)
print('Academics.csv file has been created successfully.')

df = pd.DataFrame(papers, columns=['Paper Title','Subjects','Score'])
csvFilePath = 'Data/Papers.csv'
df.to_csv(csvFilePath, index=False, header=True)
print(y)
print('Papers.csv file has been created successfully.')