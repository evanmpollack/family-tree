from pandas import isna

MOTHER = ('Member', 'mother')
FATHER = ('Member', 'father')
FULL_NAME = ('Member', 'full_name')
PARTNERS = ('Member', 'partners')

def _map_partner_of(df):
    SOURCE_ID = ('Partner_Of', 'sourceId')
    DESTINATION_ID = ('Partner_Of', 'destinationId')
    df[SOURCE_ID] = df[FULL_NAME]
    df[DESTINATION_ID] = df[PARTNERS].str.split(',')
    members_with_partners_long_format = df[[SOURCE_ID, DESTINATION_ID]] \
        .explode(DESTINATION_ID, ignore_index=True) \
        .dropna(subset=[DESTINATION_ID]) \
        .reset_index(drop=True)
    df[SOURCE_ID] = members_with_partners_long_format[SOURCE_ID]
    df[DESTINATION_ID] = members_with_partners_long_format[DESTINATION_ID]
    return df


def _map_child_of(df):
    CHILD_ID = ('Child_Of', 'childId')
    MOTHER_ID = ('Child_Of', 'motherId')
    FATHER_ID = ('Child_Of', 'fatherId')
    members_with_parents = df[~(isna(df[MOTHER]) & isna(df[FATHER]))] \
        .reset_index(drop=True)
    df[CHILD_ID] = members_with_parents[FULL_NAME]
    df[MOTHER_ID] = members_with_parents[MOTHER]
    df[FATHER_ID] = members_with_parents[FATHER]
    return df

def map_member_fields(df):
    return df.astype('string') \
        .pipe(_map_partner_of) \
        .pipe(_map_child_of)
