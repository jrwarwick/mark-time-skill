from mycroft import MycroftSkill, intent_file_handler
import time

class MarkTime(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('time.mark.intent')
    def handle_time_mark(self, message):
        self.settings["tzero"] = round(time.time())
        data = {'beginning_time': self.settings["tzero"]}
        self.speak_dialog('time.mark',data)
        #TODO: start an independent timer/metronome thread. 
        #If settingsmeta has a metronome beep interval, set that and set the beep flag to true.
        #If settingsmeta has a metronome announce interval, set that and set the announce flag to true.

    @intent_file_handler('conclude.intent')
    def handle_conclude(self, message):
        self.settings["prior_duration"] = round(time.time()) - self.settings["tzero"] 
        data = {'duration': self.settings["prior_duration"], 'ending_time': round(time.time())}
        self.speak_dialog('conclude',data)
        

def create_skill():
    return MarkTime()

