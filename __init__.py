from mycroft import MycroftSkill, intent_file_handler
import time

class MarkTime(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    #TODO: a friendly time convert/reading for minutes and hours, perhaps so on. Perhaps influenced by some settingsmeta?
    #              https://stackoverflow.com/a/775095/537243
    #      maybe an optional chime/bell at x minutes (really just a variant of mentronome, or just identical?) 
    #      technically, the  "stop" is not stateful, and so you can just ask for a stop multiple times in a row, 
    #           and he is actually still "counting" and gives a reasonable stop reply each time. 
    #           Maybe thats a feature, not a bug?
    #      maybe a settings option for operating at overriding local time and using UTC instead? but default to local
    #      decision: leave KISS as is: just "remember" the latest tzero? Or have a separate boolean state variable for "active marking session" (i.e., whether the most recent request was a "stop" and/or an expiration has passed)
    #      optional rider clause(s)? E.g., optionally be able to say:  "begin marking time, but stop after an hour." which is implicitly setting an expiration warning at that time.
    #      a couple of other maybe/possibly/onedays:  add a little bit more "memory" by keeping a little queue of maybe 3-5 of the most recent timings; allow for inquiry on "the one before that" or something. Also optional naming/tagging for each of the entries; thus could you ask "how long was the 'mile run' time?" 

    @intent_file_handler('time.mark.intent')
    def handle_time_mark(self, message):
        self.settings["tzero"] = round(time.time())
        #data = {'beginning_time': self.settings["tzero"]}
        data = {'beginning_time': time.strftime('%Y %B %d, %H:%M, %S seconds', time.localtime(self.settings["tzero"]))}
        self.speak_dialog('time.mark',data)
        #TODO: start an independent timer/metronome thread. 
        #If settingsmeta has a metronome beep interval, set that and set the beep flag to true.
        #If settingsmeta has a metronome announce interval, set that and set the announce flag to true.

    @intent_file_handler('conclude.intent')
    def handle_conclude(self, message):
        tzero = self.settings["tzero"] 
        if tzero < 0:
            LOGGER.debug("numeric error for tzero:"+tzero)
            tzero = round(time.time())
            self.settings["tzero"] = tzero
            self.speak("My apologies, but either I lost track of time, or there was not yet a marking time task assigned. I have just reset the time zero marker.")
        self.settings["prior_duration"] = round(time.time()) - tzero
        data = {'duration': self.settings["prior_duration"], 'ending_time': time.strftime("%H:%M")} #TODO: i thought this was supposed to be localtime? or it is but mark1 localtime is UTC anyway?
        self.speak_dialog('conclude',data)
        
    @intent_file_handler('report.progress.intent')
    def handle_progress(self, message):
        if tzero < 0:
            LOGGER.debug("numeric error for tzero:"+tzero)
            self.speak("My apologies, but either I lost track of time, or there was not yet a marking time task assigned.")
        else:
            running_duration = round(time.time()) - self.settings["tzero"] 
            data = {'duration': running_duration} 
            self.speak_dialog('report.progress',data)

    #TODO: maybe an intent_reset which is perhaps just a stop followed immediately by a start
def create_skill():
    return MarkTime()

