import pandas as pd
from pathlib import Path

# File/Sheet Names
FILE_NAME = 'source.xlsx'
SHEET = 'Members and Relationships'

# Path
SOURCE_PATH = (Path(__file__).parent.parent / FILE_NAME).resolve()

# Series level - apply

def map_partner_of(row):
    if pd.isna(row[('Member', 'partners')]):
        return row
    
    for partner in row[('Member', 'partners')].split(','):
        row[('Partner_Of', 'sourceId')] = row.name
        row[('Partner_Of', 'destinationId')] = partner
    return row

def map_child_of(row):
    row[('Child_Of', 'childId')] = row.name
    row[('Child_Of', 'motherId')] = row[('Member', 'mother')]
    row[('Child_Of', 'fatherId')] = row[('Member', 'father')]
    return row

def main():
    pd.read_excel(
        SOURCE_PATH,
        sheet_name=SHEET,
        header=[0,1]
    ) \
    .astype('string') \
    .set_index(('Member', 'full_name')) \
    .apply(map_partner_of, axis=1) \
    .apply(map_child_of, axis=1)

if __name__ == '__main__':
    main()
