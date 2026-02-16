import Readers, PanelFitness, PaperFitness
def Main():
    data = ['Data\REF 2021 Results - Avg by Panel & Institution.csv', 'Data\REF 2021 Results - All.xlsx']

    avgTable = Readers.CSV(data[0])
    paperTable = Readers.XSLX(data[1])
    panelFitnessTable = PanelFitness.Fitness(avgTable)
    paperTable = PaperFitness.Fitness(paperTable, panelFitnessTable)
    print(paperTable)





Main()