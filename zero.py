
import zmsg
import person
import speech
import datetime
import random
# import time
# import clock
# import weather

# GLOBALS
# load people
Eason = person.Person(1, person.names)


def Say(text):
    s = speech.Speech(True)
    s.say(text)

class Zero:
    def __init__(self):
        self.name = "ZERO"
        self.log = zmsg.Zmsg(self.name)

        self.voice = speech.Speech(False)  # activate speech module
        self.voice.say("Zero has booted. All systems are functioning nominally.")
        self.greet(Eason)
        self.done = False

    #runs selected modules such as stt, tts etc.
    def run(self):
        # run modules
        self.voice.run()  # run speech

    #returns whether we are done or not
    def isdone(self):
        return self.voice.isdone()

    def greet(self, person):
        # say a greeting to the person you recognize in the camera TODO: make this into its own module

        if person.greetMe():
            self.log.msg("Greeeting " + person.getName())

            greetings = {1: "Hello " + person.getNick(),
                         2: "How are you today, " + person.getNick() + "?",
                         3: "Lovely " + self.get_time_of_day() + ", " + person.getNick(),
                         4: "Good " + self.get_time_of_day() + ", " + person.getNick(),
                         5: "Hello there",
                         6: "Good to see you, " + person.getNick()
                         }
            greeting = random.choice(list(greetings.values()))
            self.voice.say(greeting)

            self.log.msg("Getting the current time")
            self.voice.say("The time is " + self.get_time())


        else:
            self.log.msg("Skip greeeting " + person.getNick())




    def get_time(self):  #TODO: make this into its own module
        # return a speech string of the date and time
        self.log.msg("getting time of day")
        now = datetime.datetime.now()

        pre =''
        post = ''
        hour = now.hour % 12

        if hour is 0:
            hour = 12

        if 0 <= now.minute < 4:
            pre = 'now'
            post = 'oclock'

        elif 4 <= now.minute < 16:
            pre = 'just after'
            post = 'oclock'

        elif 16 <= now.minute < 29:
            pre = 'almost'
            post = 'thirty'

            if now.hour < 12:
                post += ' aay emm'
            else:
                post += ' pee emm'
        elif 30 <= now.minute < 32:
            pre = 'near'
            post = 'thirty'
            if now.hour < 12:
                post += ' aay emm'
            else:
                post += ' pee emm'
        elif 33 <= now.minute < 44:
            pre = 'just past'
            post = 'thirty in the ' + self.get_time_of_day()
        elif 45 <= now.minute < 60:
            pre = 'almost'
            post = 'oclock in the ' + self.get_time_of_day()

        x = pre + ' ' + str(hour) + ' ' + post

        return x


    def get_time_of_day(self):
        # returns a speech string with the time of day

        now = datetime.datetime.now()
        x = ""
        if now.hour < 12:
            x = "morning"
        elif 12 <= now.hour < 17:
            x = "afternoon"
        elif now.hour >= 17:
            x = "evening"

        return x
