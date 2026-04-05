import Readers, PanelFitness, Tools, Alogrithm as GA

def Run(inputVals):
    data = Tools.data
    output = GA.GeneticAlgorithm(data, inputVals)
    return output