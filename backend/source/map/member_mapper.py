def _map_partner_of(df):
    SOURCE_ID = ('Partner_Of', 'sourceId')
    DESTINATION_ID = ('Partner_Of', 'destinationId')
    df[SOURCE_ID] = df[('Member', 'full_name')]
    df[DESTINATION_ID] = df[('Member', 'partners')].str.split(',')
    tempDf = df[[SOURCE_ID, DESTINATION_ID]] \
        .explode(DESTINATION_ID, ignore_index=True) \
        .dropna(subset=[DESTINATION_ID]) \
        .reset_index(drop=True)
    df[SOURCE_ID] = tempDf[SOURCE_ID]
    df[DESTINATION_ID] = tempDf[DESTINATION_ID]
    return df


def _map_child_of(row):
    row[('Child_Of', 'childId')] = row[('Member', 'full_name')]
    row[('Child_Of', 'motherId')] = row[('Member', 'mother')]
    row[('Child_Of', 'fatherId')] = row[('Member', 'father')]
    return row

def map_member_fields(df):
    return df.astype('string') \
        .pipe(_map_partner_of) \
        .apply(_map_child_of, axis=1)
