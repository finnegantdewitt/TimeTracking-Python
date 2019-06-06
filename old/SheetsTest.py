import gspread
from oauth2client.service_account import ServiceAccountCredentials



def main():
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name hxere.
    sheet = client.open("TimeTracking0").sheet1

    # Extract and print all of the values
    list_of_hashes = sheet.get_all_records()
    print(list_of_hashes.count(1))
    print(len(list_of_hashes))
    print(sheet.cell(2, 1).value)
    sheet.update_cell(3, 3, "lourm ipsum")
    

main()