import random as rnd, pandas as pd, numpy as np, PanelFitness, Readers, Tools

def Generate(inputVals):
    data = Tools.data[0]

    academics = []
    papers = []

    academicsLen = inputVals[0]
    AcaPapRatio = inputVals[1]
    papersLen = int(AcaPapRatio * academicsLen)

    subjects = Tools.subjects
    numAcaSubjects = Tools.numAcaSubjects
    numAcaSubWeight = Tools.numAcaSubWeight

    numPapSubjects = Tools.numPapSubjects
    numPapSubWeight = Tools.numPapSubWeight


    n = 0

    for x in range(0, academicsLen):
        academicName = ('Academic ' + str(x))
        numSub = rnd.choices(numAcaSubjects, weights=numAcaSubWeight, k=1)[0]
        acaSubjects = rnd.choices(subjects, weights=None, k=numSub)
        academics.append([academicName, acaSubjects])
        n += 1

    y = 0

    academicCount = 0

    avgTable = Readers.CSV(data) # Read and format average data
    subjectAvgs = PanelFitness.Fitness(avgTable)

    for x in range(0, papersLen):
        paper = []
        subjects = []
        paperName = 'Paper ' + str(x)
        numSub = rnd.choices(numPapSubjects, weights=numPapSubWeight, k=1)[0]
        for z in range(0, numSub):
            academic = rnd.randint(0, int(academicsLen - 1))
            subject = rnd.choice(academics[academic][1])
            subjects.append(subject)
        paper.append(paperName)
        paper.append(subjects)

        paperMean = 0
        paperSd = 0
        count = 0
        for subject in subjects:
            paperMean += subjectAvgs[subject]['mean']
            paperSd += subjectAvgs[subject]['SD']
            count += 1

        paperMean = paperMean / count
        paperSd = paperSd / count
        paper.append(int(np.random.normal(paperMean, paperSd)))
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

Generate([500, 4])