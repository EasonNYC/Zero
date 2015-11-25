
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


class Zero:
    def __init__(self):
        self.voice = speech.Speech()  # activate speech module
        self.greet(Eason)

    #runs selected modules such as stt, tts etc.
    def run(self):
        # run modules
        self.voice.run()  # run speech

        # check Person queue for greeting?

    def greet(self, person):
        # say a greeting to the person you recognize in the camera

        if person.greetMe():
            greetings = {1: "Hello " + person.getName(),
                         2: "How are you today, " + person.getName() + "?",
                         3: "Lovely " + self.get_time_of_day() + ", " + person.getName(),
                         4: "Good " + self.get_time_of_day() + ", " + person.getName(),
                         5: "Hello",
                         6: "Good to see you, " + person.getName()
                         }
            greeting = random.choice(list(greetings.values()))
            self.voice.say(greeting)
        else:
            return

    def get_time(self):
        # return a speech string of the date and time

        now = datetime.datetime.now()

        hour = now.hour % 12
        if 0 <= now.minute < 4:
            pre = 'now'
            post = 'O clock'
        elif 4 <= now.minute < 16:
            pre = 'just after'
            post = 'O clock'
        elif 17 <= now.minute < 29:
            pre = 'almost'

            post = 'thirty'
            if now.hour < 12:
                post += ' A M'
            else:
                post += ' P M'
        elif 30 <= now.minute < 32:
            pre = ''
            post = 'thirty'
            if now.hour < 12:
                post += ' A M'
            else:
                post += ' P M'
        elif 33 <= now.minute < 44:
            pre = 'well past'
            post = 'thirty in the ' + self.get_time_of_day()
        elif 45 <= now.minute < 60:
            pre = 'almost'
            hour = (now.hour + 1) % 12
            post = 'O clock in the ' + self.get_time_of_day()

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
