import pandas as pd
from pathlib import Path
from map.location_mapper import map_location_fields
from map.member_mapper import map_member_fields

FILE_NAME = 'source.xlsx'
SOURCE_PATH = (Path(__file__).parent / FILE_NAME).resolve()
A_SHEET = 'A'
MEMBERS_SHEET = 'Members and Relationships'
LOCATIONS_SHEET = 'Locations and Relationships'

def main():
    with pd.ExcelFile(SOURCE_PATH) as reader:
        a_sheet = pd.read_excel(reader, A_SHEET, skiprows=2, skipfooter=14)
        members_sheet = pd.read_excel(reader, MEMBERS_SHEET, header=[0,1])
        locations_sheet = pd.read_excel(reader, LOCATIONS_SHEET, header=[0,1])
    
    locations_sheet = map_location_fields(locations_sheet, a_sheet)
    members_sheet = map_member_fields(members_sheet)

    # Index column has to be removed manually. Writing to an excel file with MultiIndex cols is not implemented
    with pd.ExcelWriter(SOURCE_PATH, mode='a', if_sheet_exists='replace') as writer:
        locations_sheet.to_excel(writer, sheet_name=LOCATIONS_SHEET)
        members_sheet.to_excel(writer, sheet_name=MEMBERS_SHEET)

if __name__ == '__main__':
    main()
