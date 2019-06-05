import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import argparse
import cmd
import shlex
import json
import threading

class TimeTrack():
    def __init__(self):
        self.online_sheet = self.authenticate()
        self.local_sheet = self.get_local_sheet()
        self.is_timer_on = False 
        current_timer = self.local_sheet[len(self.local_sheet)-1]
        print(current_timer)
        last_end = current_timer[1]
        if(int(last_end) == 0):
            self.is_timer_on = True

    def authenticate(self):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        client = gspread.authorize(creds)
        online_sheet = client.open("TimeTracking0").sheet1
        return online_sheet

    def get_local_sheet(self):
        local_sheet = self.online_sheet.get_all_values()
        for i in range(len(local_sheet)):
            for j in range(2):
                if i > 0:
                    local_sheet[i][j] = int(local_sheet[i][j])
        return local_sheet



    def start_timer(self, title, project, tags):
        if(self.is_timer_on):
            print("Timer already on")
            return 
        current_time = int(datetime.datetime.now().timestamp())
        entry = [current_time, 0, title, project, tags]
        self.local_sheet.append(entry)
        self.is_timer_on = True
        threading.Thread(target=self.update_sheet).start() #add exception handler

    def stop_timer(self):
        if(self.is_timer_on == False):
            print("Timer is not on")
            return
        current_time = int(datetime.datetime.now().timestamp())
        current_timer = self.local_sheet[len(self.local_sheet)-1]
        current_timer[1] = current_time
        self.is_timer_on = False
        threading.Thread(target=self.update_sheet()).start()

    def update_sheet(self):
        cell_range = "A1:"
        cell_range += gspread.utils.rowcol_to_a1(len(self.local_sheet), len(self.local_sheet[0]))
        cell_list = self.online_sheet.range(cell_range)
        for cell in cell_list:
            cell.value = self.local_sheet[cell.row-1][cell.col-1]
        self.online_sheet.update_cells(cell_list)

    def refresh_sheet(self):
        try:
            self.local_sheet = self.get_local_sheet()
        except:
            self.online_sheet = self.authenticate()
            self.local_sheet = self.get_local_sheet()
    
    def get_today(self):
        todays_timers = []
        itertimer = iter(self.local_sheet)
        next(itertimer)
        for timer in itertimer:
            if(datetime.date.fromtimestamp(timer[0]) == datetime.date.today()):
                todays_timers.append(timer)
        return todays_timers
