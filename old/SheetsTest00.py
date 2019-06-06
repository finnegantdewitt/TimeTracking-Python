import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import argparse
import cmd

class TimeSheet:
    def __init__(self):    
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        client = gspread.authorize(creds)
        
        self.sheet = client.open("TimeTracking0").sheet1

    def printAll(self):
        print(self.sheet.get_all_records())

    def startTimer(self):
        self.startTime = datetime.datetime.now()

    def do_entery(self, arg):
        self.





def main():
    timesheet = TimeSheet()
    timesheet.printAll()
    print(timesheet.sheet.cell(2, 1).value)
    timesheet.sheet.update_cell(3, 3, "lourm ipsum!!!")
    
if __name__ == "__main__":
    main()