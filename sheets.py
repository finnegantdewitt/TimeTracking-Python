import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import argparse
import cmd
import shlex
import json
import threading
import timetrack
from prettytable import PrettyTable

class TimeSheet(cmd.Cmd):
    prompt = "(TimeTrack) "
    def preloop(self):   
        self.timesheet = timetrack.TimeTrack()
        self.sheet = self.timesheet.online_sheet
        self.localSheet = self.timesheet.local_sheet
        most_recent_timer = self.timesheet.local_sheet[len(self.timesheet.local_sheet)-1]
        if(self.timesheet.is_timer_on):
            print("Timer Running")
            print("Title: ", most_recent_timer[2])
            print("Project: ", most_recent_timer[3])
            current_time = datetime.datetime.now().timestamp()
            d = str(datetime.timedelta(seconds=(int(current_time) - most_recent_timer[0])))
            print("Current Time: ", d)
        else:
            print("No timer running")
            
    def do_start_timer(self, inp):
        ''' start_timer -t title -p project -tt tag1 
        or you could include spaces in title and project
        ex: start_timer -t the title -p project 2 -t tag1 tag2 tag3
        
        This should be revisited becuase it is cumbersome and probably susceptible to user input tom-foolery
        '''
        args = tuple(inp.split())
        parsed = {"title": "", "project": "", "tags": ""}
        indices = []
        for idx, arg in enumerate(args):
            if arg == "-t":
                indices.append(["t", idx])
            if arg == "-p":
                indices.append(["p", idx])
            if arg == "-tt":
                indices.append(["tt", idx])
        for idx, elem in enumerate(indices):
            if idx < (len(indices) - 1):
                elem.append(indices[idx + 1][1])
            else:
                elem.append(len(args))
        for elem in indices:
            if elem[0] == "t":
                for i in range(elem[1]+1, elem[2]):
                    parsed["title"] += args[i] + " "
                parsed["title"] = parsed["title"].strip()
            if elem[0] == "p":
                for i in range(elem[1]+1, elem[2]):
                    parsed["project"] += args[i] + " "
                parsed["project"] = parsed["project"].strip()
            if elem[0] == "tt":
                for i in range(elem[1]+1, elem[2]):
                    parsed["tags"] += args[i] + " "
                parsed["tags"] = parsed["tags"].strip()
        self.timesheet.start_timer(parsed["title"], parsed["project"], parsed["tags"])
    

    def do_stop_timer(self, inp):
        self.timesheet.stop_timer()

    def do_update_sheet(self, inp):
        self.timesheet.update_sheet()

    def do_refresh_sheet(self, inp):
        self.timesheet.refresh_sheet()

    def do_today(self, inp):
        todays_timers = self.timesheet.get_today()
        table = PrettyTable(["Title", "Duration", "Start Time", "End Time", "Project"])
        for timer in todays_timers:
            d = ""
            if(timer[1] == 0):
                timestamp = int(datetime.datetime.now().timestamp())
                d = str(datetime.timedelta(seconds=(timestamp - timer[0])))
                table.add_row([timer[2], d, datetime.datetime.fromtimestamp(timer[0]).time(), datetime.datetime.fromtimestamp(timestamp).time(), timer[3]])
            else:
                d = str(datetime.timedelta(seconds=(timer[1] - timer[0])))
                table.add_row([timer[2], d, datetime.datetime.fromtimestamp(timer[0]).time(), datetime.datetime.fromtimestamp(timer[1]).time(), timer[3]])
        print(table)

    def do_all(self, inp):
        itertimer = iter(self.timesheet.local_sheet)
        next(itertimer)
        table = PrettyTable(["Title", "Duration", "Start Time", "End Time", "Project"])
        for timer in itertimer:
            d = ""
            if(timer[1] == 0):
                timestamp = int(datetime.datetime.now().timestamp())
                d = str(datetime.timedelta(seconds=(timestamp - timer[0])))
                table.add_row([timer[2], d, datetime.datetime.fromtimestamp(timer[0]), datetime.datetime.fromtimestamp(timestamp), timer[3]])
            else:
                d = str(datetime.timedelta(seconds=(timer[1] - timer[0])))
                table.add_row([timer[2], d, datetime.datetime.fromtimestamp(timer[0]), datetime.datetime.fromtimestamp(timer[1]), timer[3]])
        print(table)

    def do_current_timer(self, inp):
        if(self.timesheet.is_timer_on == False):
            print("Timer isn't running")
            return
        current_timer = self.timesheet.local_sheet[len(self.timesheet.local_sheet)-1]
        current_time = int(datetime.datetime.now().timestamp())
        d = str(datetime.timedelta(seconds=(current_time - int(current_timer[0]))))
        print("Time: ", d)

    def do_print_local_sheet(self, inp):
        print(self.timesheet.local_sheet)
        
    #quit
    def do_q(self, inp):
        return True


def main():
    TimeSheet().cmdloop()
   
if __name__ == "__main__":
    main()
