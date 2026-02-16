import pandas as pd

def Fitness(paperTable, panelFitnessTable):
    paperTable['uoaMean'] = paperTable['Unit of assessment number'].map(lambda x: panelFitnessTable.get(x, {}).get('mean')if not pd.isna(x) else None) # Map Unit of Assessment mean onto each paper
    paperTable['uoaSD'] = paperTable['Unit of assessment number'].map(lambda x: panelFitnessTable.get(x, {}).get('SD')if not pd.isna(x) else None) # Map Unit of Assessment standard deviation onto each paper
    paperTable['fitness'] = (paperTable['score'] - paperTable['uoaMean']) / paperTable['uoaSD'] # Calculate z-score for each paper as fitness
    return paperTable