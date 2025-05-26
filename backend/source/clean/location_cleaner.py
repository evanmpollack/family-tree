import re
import pandas as pd
import numpy as np

COLS_PATTERN = r'CITY-*|DOD|CEMETERY'
NA_PATTERN = r'\?+|(?!\w|\w )-(?!\w| \w)|N */ *A|\d' + r'|' + COLS_PATTERN
KNOWN_ABBREVIATIONS = {'mt', 'st', 'ft'}

def _trim_column_labels(df):
    mapper = {}
    for col in df.columns:
        mapper[col] = col.strip()
    return df.rename(mapper, axis=1)

def _remove_living_prefix(df):
    df['DOD'] = df['DOD'].dropna() \
        .str.split('-') \
        .apply(lambda row: row[-1])
    return df

def _remove_cemetery_name(df):
    df['CEMETERY'] = df['CEMETERY'].dropna() \
        .str.split(',') \
        .apply(lambda row: ','.join(row[-2:]))
    return df

def _merge_locations(df):
    df['Locations'] = pd.concat([df[col] for col in df.columns], ignore_index=True)
    return df

# This function implicitly trims strings
def _extract_words(s):
    return s.dropna() \
        .apply(lambda row: [s for s in re.split(r'\b', row) if re.search(r'[a-zA-Z]', s)])

def _fix_known_abbreviations(s):
    def fix(row):
        for i,p in enumerate(row):
            if p.lower() in KNOWN_ABBREVIATIONS:
                row[i] = p.capitalize() + '.'
        return row
    return s.dropna().apply(fix)

def _join_location_parts(s):
    def join(row):
        # Russia
        if len(row) == 1:
            return row[0]
        # Miami, Fl
        if len(row[-1]) == 2:
            row[-1] = row[-1].upper()
        return f'{' '.join(row[:-1])}, {row[-1]}'
    return s.dropna().apply(join)

def clean_locations(df):
    return df.astype('string') \
        .filter(regex=COLS_PATTERN) \
        .pipe(_trim_column_labels) \
        .replace(NA_PATTERN, np.nan, regex=True) \
        .pipe(_remove_living_prefix) \
        .pipe(_remove_cemetery_name) \
        .apply(_extract_words) \
        .apply(_fix_known_abbreviations) \
        .apply(_join_location_parts) \
        .pipe(_merge_locations) \
        .loc[:, 'Locations'] \
        .drop_duplicates() \
        .dropna() \
        .sort_values()
