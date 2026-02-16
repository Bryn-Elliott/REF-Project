import csv
import pandas as pd
import numpy

def CSV(dataPath):
    table = list()
    with open(dataPath, mode='r', newline='', encoding='utf-8') as file: # Read file with csvreader
        reader = csv.DictReader(file)
        
        for row in reader:
            table.append([row['institution_id'], row['uoa_id'], row['aggregate_ref_score']]) # Remove unnecessary columns
        return table

def XSLX(dataPath):
    df = pd.read_excel(dataPath, header=6) # Read file with pandas
    df = df.iloc[6:]  # Remove forst 6 rows (blank/title)
    df = df[df['Profile'] == 'Overall'] # Remove non-overall scores
    df['score'] = df['4*']*4 + df['3*']*3 + df['2*']*2 + df['1*']*1 # Calculate weighted score
    df['score'] = pd.to_numeric(df['score'], errors='coerce') # Format score to number
    df['score'] = df['score'] / 100 # Account for percentages not being of 1
    df['Unit of assessment number'] = pd.to_numeric(df['Unit of assessment number'], errors='coerce') # Convert Unit of Assessment number to a number
    df['Unit of assessment number'] = df['Unit of assessment number'].astype('Int64')# Convert Unit of Assessment number to a nullable integer
    df['Unit of assessment number'] = df['Unit of assessment number'].astype(str)# Convert Unit of Assessment number to a string (now formatted to remove any decimals)
    df.drop(columns=["Institution sort order", "Main panel", "FTE of submitted staff", "Total FTE of submitted staff for joint submission", "% of eligible staff submitted", "4*", "3*", "2*", "1*", "Unclassified"], inplace=True) # Remove unnecessary columns
    df.drop(df.index[-1], inplace=True) # Remove the last row (Null)
    return df
