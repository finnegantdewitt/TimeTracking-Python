import json
import datetime

class TimeTrack():
    def __init__(self, json_filename="timers.json"):
        self.json_filename = json_filename
        self.timers = self.get_timers_from_json()

    def get_timers_from_json(self):
        with open(self.json_filename, 'r') as file:
            return json.load(file)

    def save_to_json(self):
        with open(self.json_filename, "w") as file:
            json.dump(self.timers, file)
        
    def is_timer_on(self):
        most_recent_timer = self.get_most_recent_timer()
        if most_recent_timer["End"] == 0:
            return True
        else:
            return False
        
    def start_timer(self, title, project, tags):
        if(self.is_timer_on()):
            print("Timer is already on")
            return
        current_time = self.current_time()
        entry = {
            "Start": current_time,
            "End": 0,
            "Title": title,
            "Project": project,
            "Tags": tags
        }
        self.timers.append(entry)
        self.save_to_json()

    def stop_timer(self):
        if(self.is_timer_on() == False):
            print("Timer is not running")
            return
        current_time = self.current_time()
        current_timer = self.get_most_recent_timer()
        current_timer["End"] = current_time
        self.save_to_json()
    
    def timers_from_day(self, day):
        if not isinstance(day, datetime.datetime):
            print("not instance of datetime")
            return
        timers = []
        itertimer = iter(self.timers)
        next(itertimer)
        for timer in itertimer:
            if(datetime.date.fromtimestamp(timer["Start"]) == day.date()):
                timers.append(timer)
        return timers

    def current_time(self):
        return int(datetime.datetime.now().timestamp())
    
    def get_most_recent_timer(self):
        return self.timers[len(self.timers) - 1]