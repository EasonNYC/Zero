import datetime
import random

#names stuff
names = {1: "Mister Smith",
        2: "Sir",
        3: "Master Smith",
        4: "Mister Easson",
        5: "Sire"
        } 

#############################################
class Person:
    lastcalled = "thelastthingyoucalledme"
    lastGreeting = datetime.datetime.now()
    
    def __init__(self,ID,name):
        self.ID = ID
        self.n = name

    def getName(self):
        #returns a random name of the person
        x = random.choice(list(self.n.values()))
        
        #insures the same name wont be called twice
        while x == self.lastcalled:
            x = random.choice(list(self.n.values()))
        self.lastcalled = x 

        return x
    
    def greetMe(self):
        #check whether its been a while since the person has been greeted
        thistime = datetime.datetime.now()
        if (thistime.hour - self.lastGreeting.hour) < 2:
            return True
        else:
            return False




