from pandas import isna

def _map_partner_of(row):
    if isna(row[('Member', 'partners')]):
        return row
    
    # TODO: Fix bug that only writes the last partner -- need to explode based on split
    for partner in row[('Member', 'partners')].split(','):
        row[('Partner_Of', 'sourceId')] = row[('Member', 'full_name')]
        row[('Partner_Of', 'destinationId')] = partner
    return row

def _map_child_of(row):
    row[('Child_Of', 'childId')] = row[('Member', 'full_name')]
    row[('Child_Of', 'motherId')] = row[('Member', 'mother')]
    row[('Child_Of', 'fatherId')] = row[('Member', 'father')]
    return row

def map_member_fields(df):
    return df.astype('string') \
        .apply(_map_partner_of, axis=1) \
        .apply(_map_child_of, axis=1)
