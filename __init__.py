from mycroft import MycroftSkill, intent_file_handler
import time
import datetime

class MarkTime(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    #TODO: 
    #  A friendly time convert/reading for minutes and hours, perhaps so on. Perhaps influenced by some settingsmeta?
    #    https://stackoverflow.com/a/775095/537243
    #  Maybe an optional chime/bell at x seconds/minutes intervals (really just a variant of mentronome, or even identical?) 
    #  Technically, right now, the "stop" is not stateful, and so you can just ask for a stop multiple times in a row, 
    #    and he is actually still "counting" and gives a reasonable stop reply each time. 
    #     Maybe thats a feature, not a bug?
    #  Maybe a settings option for operating at overriding local time and using UTC instead? but default to local
    #  Decision: leave KISS as is: just "remember" the latest tzero? Or have a separate boolean state variable for "active marking session" (i.e., whether the most recent request was a "stop" and/or an expiration has passed)
    #  Optional rider clause(s)? E.g., optionally be able to say:  "begin marking time, but stop after an hour." which is implicitly setting an expiration warning at that time.
    #  A couple of other maybe/possibly/onedays:  add a little bit more "memory" by keeping a little queue of maybe 3-5 of the most recent timings; allow for inquiry on "the one before that" or something. Also optional naming/tagging for each of the entries; thus could you ask "how long was the 'mile run' time?" 

    @intent_file_handler('time.mark.intent')
    def handle_time_mark(self, message):
        self.settings["tzero"] = round(time.time())
        #data = {'beginning_time': self.settings["tzero"]}
        data = {'beginning_time': time.strftime('%Y %B %d, %H:%M, %S seconds', 
                                                time.localtime(self.settings["tzero"]))}
        self.speak_dialog('time.mark',data)
        #TODO: start an independent timer/metronome thread. Inside:
        #  If settingsmeta has a metronome beep interval:
        #    set that and set the beep flag to true.
        #  If settingsmeta has a metronome announce interval:
        #    set that and set the announce flag to true.

    @intent_file_handler('conclude.intent')
    def handle_conclude(self, message):
        # It seems like sometimes a null/blank settings.json value will be "" 
        # (i.e., a string) even if settingsmeta declares it a number.
        # If this is later determined to be a bug, or a method of setting an
        # unset number comes about, remove the int() cast here.
        tzero = int(self.settings["tzero"] or 0)
        if tzero < 0:
            self.log.error("numeric error for tzero: "+tzero)
            tzero = round(time.time())
            self.settings["tzero"] = tzero
            self.speak("My apologies, but either I lost track of time, "
                       "or there was not yet a marking time task assigned. "
                       "I have just reset the time zero marker.")
        elif tzero == 0:
            self.speak_dialog('inactive')
        else:
            self.settings["prior_duration"] = round(time.time()) - tzero
            #TODO: look into this strftime call; I thought this was supposed to be localtime by default? 
            #or it is but mark1 localtime is UTC anyway?
            data = {'duration': self.nice_time_delta(self.settings["prior_duration"]), 
                    'ending_time': time.strftime("%H:%M")} 
            self.speak_dialog('conclude',data)
        
    @intent_file_handler('report.progress.intent')
    def handle_progress(self, message):
        # It seems like sometimes a null/blank settings.json value will be "" 
        # (i.e., a string) even if settingsmeta declares it a number.
        # If this is later determined to be a bug, or a method of setting an
        # unset number comes about, remove the int() cast here.
        tzero = int(self.settings["tzero"] or 0)
        if tzero < 0:
            self.log.error("numeric error for tzero: "+tzero)
            self.speak("My apologies, but either I lost track of time, "
                       "or there was not yet a marking time task assigned.")
        elif tzero == 0:
            self.speak_dialog('inactive')
        else:
            running_duration = round(time.time()) - self.settings["tzero"] 
            data = {'duration': running_duration} 
            self.speak_dialog('report.progress',data)

    #TODO: maybe an intent_reset which is perhaps just a stop followed immediately by a start

    def nice_time_delta(self, delta_seconds):
        # is a validation step on the parameter needed? 
        #   If so, what do we return? or raise exception?
        # '6 days, 22:40:00' when greater than a day's delta
        self.log.debug("Delta Style:  " + str(datetime.timedelta(seconds=delta_seconds)))
        pronounceable = ""
        nice_delta = str(datetime.timedelta(seconds=delta_seconds)).split(",")
        if len(nice_delta) == 2: #it has a day prefix
            pronounceable = nice_delta.pop(0)
        (h,m,s) = nice_delta[0].split(":") #are we assuming too much about element count?
        if int(h) > 0:
            pronounceable += " " + str(h) + " hour" + "s" if h.lstrip("0") != "1" else ""
        if int(m) > 0:
            pronounceable += " " + str(m) + " minute" + "s" if m.lstrip("0") != "1" else ""
        if int(s) > 0:
            pronounceable += " " + str(s) + " second" + "s" if s.lstrip("0") != "1" else ""
        return pronounceable


def create_skill():
    return MarkTime()

