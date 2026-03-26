import random as rnd
import pandas as pd
import sys

academicsColumns = []
papersColumns = []

academicsLen = 1000
papersLen = int(3.5 * academicsLen)

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

y = 0

for x in range(0, academicsLen):
    academic = []
    academic.append('Academic ' + str(x))
    numSub = rnd.choices(numSubjects, weights=numSubWeight, k=1)
    academic.append(rnd.choices(subjects, weights=None, k=numSub[0]))
    academicsColumns.append(academic)
    y += 1

df = pd.DataFrame(academicsColumns, columns=['Name','Subjects'])
csvFilePath = 'Data/Academics.csv'
df.to_csv(csvFilePath, index=False, header=True)
print(y)
print('Academics.csv file has been created successfully.')

numSubjects = [1, 2]
numSubWeight = [90, 10]
scores = [1, 2, 3, 4]
scoreWeight = [1, 1, 2, 2]

y = 0

for x in range(0, papersLen):
    paper = []
    paper.append('Paper ' + str(x))
    numSub = rnd.choices(numSubjects, weights=numSubWeight, k=1)
    paper.append(rnd.choices(subjects, weights=None, k=numSub[0]))
    paper.append(rnd.choices(scores, weights=scoreWeight, k=1)[0])
    papersColumns.append(paper)
    y += 1

df = pd.DataFrame(papersColumns, columns=['Paper Title','Subjects','Rating'])
csvFilePath = 'Data/Papers.csv'
df.to_csv(csvFilePath, index=False, header=True)
print(y)
print('Papers.csv file has been created successfully.')