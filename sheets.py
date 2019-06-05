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
        args = tuple(inp.split())
        #[-t, title, -p, project, -tt, tag, tag2]
        parsed = dict({"Title": "", "Project": "", "Tags": ""})
        indices = dict() 
        for i in range(len(args)):
            if(args[i] == "-t"):
                indices["Title"] = i
            if(args[i] == "-p"):
                indices["Project"] = i
            if(args[i] == "-tt"):
                indices["Tags"] = i
        print(args)
        print(indices)
        #for k, v in parsed:
           # if v != -1:
                #if dict.
                #for j in range(parsed)
        
        #self.timesheet.start_timer(parsed["Title"], parsed["Project"], "tag")

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

        
    #recives a dict with {"Start": int, "End": int, "Title": string, "Project": string, "Tags": list(strings)}
    #but might not have all of those keys so need to make a remake dict with blank key entries
    def addEntry(self, entry):
        return

    def do_printAll(self, inp):
        print(self.timesheet.local_sheet)

    def do_test(self, inp):
        values = self.sheet.get_all_values()
        print(values)
        print(gspread.utils.rowcol_to_a1(len(values), len(values[0])))
        
    #quit
    def do_q(self, inp):
        return True


def main():
    TimeSheet().cmdloop()
   
if __name__ == "__main__":
    main()

# s