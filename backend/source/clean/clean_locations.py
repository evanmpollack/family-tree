import re
import pandas as pd
import numpy as np
from pathlib import Path

# File/Sheet Names
FILE_NAME = 'source.xlsx'
SHEET = 'A'

# Path
SOURCE_PATH = (Path(__file__).parent.parent / FILE_NAME).resolve()

# Pattern Constants
COLS_PATTERN = r'CITY-*|DOD|CEMETERY'
NA_PATTERN = r'\?+|(?!\w|\w )-(?!\w| \w)|N */ *A|\d' + r'|' + COLS_PATTERN
KNOWN_ABBREVIATIONS = {'mt', 'st', 'ft'}

# DF Level - pipe

def trim_column_labels(df):
    mapper = {}
    for col in df.columns:
        mapper[col] = col.strip()
    return df.rename(mapper, axis=1)

def remove_living_prefix(df):
    COL = 'DOD'
    df[COL] = df[COL].dropna() \
        .str.split('-') \
        .apply(lambda row: row[-1])
    return df

def remove_cemetery_name(df):
    COL = 'CEMETERY'
    df[COL] = df[COL].dropna() \
        .str.split(',') \
        .apply(lambda row: ','.join(row[-2:]))
    return df

def merge_locations(df):
    COL = 'Locations'
    df[COL] = pd.concat([df[col] for col in df.columns], ignore_index=True)
    return df

# Row level - apply

# This function implicitly trims strings
def extract_words(s):
    return s.dropna() \
        .apply(lambda row: [s for s in re.split(r'\b', row) if re.search(r'[a-zA-Z]', s)])

def fix_known_abbreviations(s):
    def fix(row):
        for i,p in enumerate(row):
            if p.lower() in KNOWN_ABBREVIATIONS:
                row[i] = p.capitalize() + '.'
        return row
    return s.dropna().apply(fix)

def join_location_parts(s):
    def join(row):
        # Russia
        if len(row) == 1:
            return row[0]
        # Miami, Fl
        if len(row[-1]) == 2:
            row[-1] = row[-1].upper()
        return f'{' '.join(row[:-1])}, {row[-1]}'
    return s.dropna().apply(join)

def main():
    pd.read_excel(
        SOURCE_PATH, 
        sheet_name=SHEET,  
        skiprows=2, 
        skipfooter=14
    ) \
    .astype('string') \
    .filter(regex=COLS_PATTERN) \
    .pipe(trim_column_labels) \
    .replace(NA_PATTERN, np.nan, regex=True) \
    .pipe(remove_living_prefix) \
    .pipe(remove_cemetery_name) \
    .apply(extract_words) \
    .apply(fix_known_abbreviations) \
    .apply(join_location_parts) \
    .pipe(merge_locations) \
    
    # return df['Locations'].drop_duplicates().dropna().sort_values()

if __name__ == '__main__':
    main()
