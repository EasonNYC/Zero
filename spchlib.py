# this is a basic binary object / file class (using pickle) for the speech class
# this is so we can store wavs's of text strings and retreave them later. TODO: convert wav to mp3 for storage

import os
import zmsg

try:
    import cPickle as pickle
except:
    print "importing cpickle failed."
    import pickle



#global functions for pickle file TODO: these need to be moved to their own file
def savepkl(obj, datafile=os.path.dirname(os.path.realpath(__file__)) + '/sp_cache/storage.pkl'):
    with open(datafile, 'wb') as fileobject:
        pickle.dump(obj, fileobject)


def loadpkl(datafile=os.path.dirname(os.path.realpath(__file__)) + '/sp_cache/storage.pkl'):
    mydata = {}
    with open(datafile, 'rb') as f:
        mydata = pickle.load(f)
    return mydata #return a copy of the object

def writeToLog(msg, logfile=os.path.dirname(os.path.realpath(__file__)) + '/log.txt'):
    with open(logfile, 'a+') as logfile:
        logfile.writelines(msg+'\n')
        logfile.close()


#file io class
class Speechlib:

    def __init__(self):
        self.name = 'spchlib'
        self.log = zmsg.Zmsg(self.name)

        self.mytext = {} # dictionary which holds our strings
        self.load() # load the dictionary upon startup

    def load(self):
        #load dictionary with saved values
        try:
            self.mytext = loadpkl() #call main load function above for pickle
            self.log.msg("speech library loaded", 'INFO')
        except:
            self.log.msg("Speech library not detected.",'WARNING')

    def printme(self):
        print "[spchlib] SpchLib Contents:" + str(self.mytext)

    def exists(self,sentence):
        return sentence in self.mytext

    def getkey(self,sentence):
        if self.exists(sentence):
            return self.mytext[sentence]
        else:
            return -1

    def save(self):
        #save wrapper calls save function for pickle
        #self.log.msg("Storing speech to pickle.")
        savepkl(self.mytext)

    def clear(self):
        self.log.msg("deleting speech cache.", 'INFO')
        #clears the dictionary and the file of all entries
        self.mytext = {}
        self.save()

        #clears the cache of all files
        folder = os.getcwd() + "/sp_cache"
        filelist = [f for f in os.listdir(folder)]
        #print filelist
        for f in filelist:
            filepath = os.path.join(folder, f)
            try:
                if os.path.isfile(filepath):
                    self.log.msg("Deleting " + f, 'INFO')
                    os.unlink(filepath)

            except Exception as e:
                self.log.msg(e, 'FAILURE')



    def add(self,sentence):
        #adds sentence to dictionary. returns number to assign for wavfile. returns -1 if it already exists.

        if sentence in self.mytext:
            #do not add it because its already in there
            self.log.msg("sentence found in spchlib. fetching key.")
            return self.getkey(sentence)

        else:
            #add the sentence

            #generate new key
            try:
                newkey = max(self.mytext.values())+1
            except:
                #no keys exist yet
                newkey = 1
                self.log.msg("Creating new speech library and adding first key.", 'INFO')

            #save sentence to the dictionary
            self.mytext[sentence] = newkey
            self.save()
            self.log.msg("Stored new key \"" + sentence + "\" --> './sp_cache/" + str(self.mytext.get(sentence)) + ".wav into library.")
            return newkey






