from mycroft import MycroftSkill, intent_file_handler


class MarkTime(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('time.mark.intent')
    def handle_time_mark(self, message):
        self.speak_dialog('time.mark')


def create_skill():
    return MarkTime()

