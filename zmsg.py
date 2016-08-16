
import datetime
import spchlib #needed for writetolog #TODO change to its own class/file
import zero

LEVEL = {'DEBUG' : 0, 'FAILURE' : 1, 'WARNING' : 2, 'INFO' : 3 }

#basic debug and logging class
class Zmsg:

    DEBUG = 0
    FAILURE = 1
    WARNING = 2
    INFO = 3



    def __init__(self, name, debuglevel = 'DEBUG', loglevel = 'DEBUG'):

        self.debuglevel = LEVEL[debuglevel]
        self.loglevel = LEVEL[loglevel]
        self.t = datetime.datetime.now()
        self.name = name

    def msg(self, text = '', dbglvl = 'DEBUG', ):

        t = datetime.datetime.now()
        msg = str(t) + " <" + dbglvl + "> " + " [" + self.name + "] " + text

        #print to console
        if LEVEL[dbglvl] >= self.debuglevel:
            print msg

        #write to log
        if LEVEL[dbglvl] >= self.loglevel:
            spchlib.writeToLog(msg)

        if LEVEL[dbglvl] == LEVEL['WARNING']:
            print "warning:" + text
            s = zero.Say("Warning. " + text)


#z = Zmsg()
#z.msg(z.name, "this is a test")