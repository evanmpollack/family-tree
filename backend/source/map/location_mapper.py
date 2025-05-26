from clean.location_cleaner import clean_locations

def map_location_fields(df, source):
    df[('Location', 'name')] = clean_locations(source)
    return df
