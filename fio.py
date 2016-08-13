# this is a basic binary object / file class (using pickle)
# this is so we can store wavs's of text strings and get them later. TODO: convert wav to mp3 for storage

import os
try:
    import cPickle as pickle
except:
    print "importing cpickle failed."
    import pickle

#global functions for pickle
def save(obj, datafile= os.path.dirname(os.path.realpath(__file__))+'/sp_cache/storage.pkl'):
    with open(datafile, 'wb') as fileobject:
        pickle.dump(obj, fileobject)


def load(datafile=os.path.dirname(os.path.realpath(__file__))+'/sp_cache/storage.pkl'):
    mydata = {}
    with open(datafile, 'rb') as f:
        mydata = pickle.load(f)
    return mydata #return a copy of the object

#file io class
class Fio:

    def __init__(self):

        self.mytext = {} # dictionary which holds our strings
        self.load() # load the dictionary upon startup

    def load(self):
        #load dictionary with saved values
        try:
            self.mytext = load() #call main load function above for pickle
            print "speech library loaded"
        except:
            print "speech library failed to load or does not exist"

    def printme(self):
        print "[spchlib] Contents:" + str(self.mytext)

    def exists(self,sentence):
        return sentence in self.mytext

    def getkey(self,sentence):
        if self.exists(sentence):
            return self.mytext[sentence]
        else:
            return -1

    def save(self):
        #save wrapper calls save function for pickle
        save(self.mytext)

    def clear(self):
        #clears the dictionary and the file of all entries
        self.mytext = {}
        self.save()

    def add(self,sentence):
        #adds sentence to dictionary. returns number to assign for wavfile. returns -1 if it already exists.

        if sentence in self.mytext:
            #do not add it because its already in there
            print "sentence already exists"
            return self.getkey(sentence)

        else:
            #add the sentence

            #generate new key
            try:
                newkey = max(self.mytext.values())+1
            except:
                #no keys exist yet
                newkey = 1
                print "creating first key"

            #save sentence to the dictionary
            self.mytext[sentence] = newkey
            self.save()
            print "[spchlib] Saving: [" + sentence + "]-->" + str(self.mytext.get(sentence))
            return newkey






