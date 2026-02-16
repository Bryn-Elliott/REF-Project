import pandas as pd

def Fitness(paperTable, panelFitnessTable):
    paperTable['uoaMean'] = paperTable['Unit of assessment number'].map(lambda x: panelFitnessTable.get(x, {}).get('mean')if not pd.isna(x) else None)
    paperTable['uoaSD'] = paperTable['Unit of assessment number'].map(lambda x: panelFitnessTable.get(x, {}).get('SD')if not pd.isna(x) else None)
    paperTable['fitness'] = (paperTable['score'] - paperTable['uoaMean']) / paperTable['uoaSD']
    return paperTable