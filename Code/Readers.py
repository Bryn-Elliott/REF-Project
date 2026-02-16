import csv
import pandas as pd
import numpy

def CSV(dataPath):
    table = list()
    with open(dataPath, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            table.append([row['institution_id'], row['uoa_id'], row['aggregate_ref_score']])
        return table

def XSLX(dataPath):
    df = pd.read_excel(dataPath, header=6)
    df = df.iloc[6:] 
    df = df[df['Profile'] == 'Overall']
    df['score'] = df['4*']*4 + df['3*']*3 + df['2*']*2 + df['1*']*1
    df['score'] = pd.to_numeric(df['score'], errors='coerce')
    df['score'] = df['score'] / 100
    df['Unit of assessment number'] = pd.to_numeric(df['Unit of assessment number'], errors='coerce')
    df['Unit of assessment number'] = df['Unit of assessment number'].astype('Int64')
    df['Unit of assessment number'] = df['Unit of assessment number'].astype(str)
    df = df.drop(columns=["Institution sort order", "Main panel", "FTE of submitted staff", "Total FTE of submitted staff for joint submission", "% of eligible staff submitted", "4*", "3*", "2*", "1*", "Unclassified"])
    df = df.drop(df.index[-1])
    return df
