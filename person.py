import datetime
import random

#names
realname = "Eason"
names = {1: realname,
        2: "sir",
        3: "Master Smith",
        4: "Mister Smith",
        5: "your majesty"
        } 

#############################################
class Person:
    lastcalled = "thelastthingzerocalledme"
    lastGreeting = datetime.datetime.now()
    
    def __init__(self, ID, nicks):
        self.ID = ID
        self.name = realname
        self.nicks = nicks

    def getName(self):
        return self.name

    def getNick(self):
        #returns a random name of the person
        x = random.choice(list(self.nicks.values()))
        
        #insures the same name wont be called twice
        while x == self.lastcalled:
            x = random.choice(list(self.nicks.values()))
        self.lastcalled = x 

        return x
    
    def greetMe(self):
        #check whether its been a while since the person has been greeted
        thistime = datetime.datetime.now()
        if (thistime.hour - self.lastGreeting.hour) < 2:
            return True
        else:
            return False




