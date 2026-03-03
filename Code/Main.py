import Readers, PanelFitness, SubmissionFitness, Alogrithm as GA
def Main():
    data = ['Data\REF 2021 Results - Avg by Panel & Institution.csv', 'Data\REF 2021 Results - All.xlsx', 'Data\Academics.csv', 'Data\Papers.csv'] # Input data paths

    avgTable = Readers.CSV(data[0]) # Read and format average data
    paperTable = Readers.XSLX(data[1]) # Read and format paper data
    panelFitnessTable = PanelFitness.Fitness(avgTable) # Calculate panel fitness scores
    paperTable = SubmissionFitness.Fitness(paperTable, panelFitnessTable) # Calculate paper fitness scores
    GA.GeneticAlgorithm(data)
    





Main()