import Readers, PanelFitness, PaperFitness
def Main():
    data = ['Data\REF 2021 Results - Avg by Panel & Institution.csv', 'Data\REF 2021 Results - All.xlsx'] # Input data paths

    avgTable = Readers.CSV(data[0]) # Read and format average data
    paperTable = Readers.XSLX(data[1]) # Read and format paper data
    panelFitnessTable = PanelFitness.Fitness(avgTable) # Calculate panel fitness scores
    paperTable = PaperFitness.Fitness(paperTable, panelFitnessTable) # Calculate paper fitness scores
    print(paperTable)





Main()