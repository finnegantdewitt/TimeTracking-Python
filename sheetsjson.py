import datetime
import cmd
import json
import time
import timetrackjson
import sys
from prettytable import PrettyTable

class TimeSheet(cmd.Cmd, timetrackjson.TimeTrack):
    prompt = "(TimeTrack) "
    def preloop(self):
        timetrackjson.TimeTrack.__init__(self)
        
    def do_start_timer(self, inp=""):        
        if(self.is_timer_on()):
            print("Timer is already on")
            return
        title = str(input("Title: "))
        project = str(input("Project: "))
        tags_entry = str(input("Tags: "))
        tags = tags_entry.split(",")
        tags = list(map(str.strip, tags))
        self.start_timer(title, project, tags)

    def do_stop_timer(self, inp=""):
        self.stop_timer()

    def do_today(self, inp=""):
        todays_timers = self.timers_from_day(datetime.datetime.now())
        table = PrettyTable(["Title", "Duration", "Start Time", "End Time", "Project"])
        for timer in todays_timers:
            if(timer["End"] == 0):
                timestamp = int(datetime.datetime.now().timestamp())
                d = str(datetime.timedelta(seconds=(timestamp - timer["Start"])))
                table.add_row([timer["Title"], d, datetime.datetime.fromtimestamp(timer["Start"]).time(), datetime.datetime.fromtimestamp(timestamp).time(), timer["Project"]])
            else:
                d = str(datetime.timedelta(seconds=(timer["End"] - timer["Start"])))
                table.add_row([timer["Title"], d, datetime.datetime.fromtimestamp(timer["Start"]).time(), datetime.datetime.fromtimestamp(timer["End"]).time(), timer["Project"]])
        print(table)

    def do_watch_timer(self, inp=""):
        i = 0
        while True:
            sys.stdout.write(str(i))
            sys.stdout.flush()
            i += 1
            time.sleep(1)
            if i == 3:
                print('\n')
                break
            sys.stdout.write('\b')

    def do_q(self, inp=""):
        return True

def main():
    TimeSheet().cmdloop()
   
if __name__ == "__main__":
    main()
