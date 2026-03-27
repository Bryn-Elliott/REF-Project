import Alogrithm as GA, GreedyAlgo, random, Tools

data = ['Data/REF 2021 Results - Avg by Panel & Institution.csv', 'Data/REF 2021 Results - All.xlsx', 'Data/Academics.csv', 'Data/Papers.csv'] # Input data paths

def Main():
    academics, papers = Tools.LoadData(data)
    solution = GreedyAlgo.CreateInd(academics, papers)
    print(Tools.Fitness(solution, academics, papers))
    
Main()