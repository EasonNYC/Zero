# coding=utf-8
import time
import Queue
import sound
import spchlib
import zmsg
import requests
import os
# Zero's speech process class, which allows Zero to say things using the say() function.
# All of the things Zero want's to say are stored in a deque (Q) and then permanently stored in a
# pickle file for retrieval.
#

IPADDRESS = '192.168.1.14'
PORT = '59125'
ttswavfile = 'tts.wav'



class Speech(object):

    Q = Queue.Queue()

    def __init__(self, lite=False):
        self.name = "speech"
        self.log = zmsg.Zmsg(self.name)
        self.audio = sound.Sound()

        if lite is False:
            self.speechlib = spchlib.Speechlib()
            self.speechlib.clear()

    #return just the text for now.
    def process(self, text):
        return text

    #The workhorse. Add things to say to the speech Q.
    def say(self, text):

        #process the text
        #vec = self.process(text)
        if not (text.endswith('.') or text.endswith('?')): #TODO: put this in process()
            text += '.'

        Speech.Q.put([text])
        #print Speech.Q

    def splitup(self, text):
        #print("splitting: " + text)
        stringvect = text.split(". ")

        # add . back in
        for stringnum in range(0, len(stringvect) - 1):
            stringvect[stringnum] += '.'

        return stringvect

    # returns whether we have detected the escape key pressed are done or not
    def isdone(self):
        return self.audio.isdone()

    #run Zero's text to speech module
    def run(self):

        self.audio.run()#looks for escape keypress, etc. from pygame allowing you to exit the pygame window

        # say all the things in the speech Q
        while not Speech.Q.empty():
            x = Speech.Q.get()  # get next thing to say

            #make wav file, and add it to our speech library
            num = self.speechlib.getkey(x[0])
            if num > 0:
                self.log.msg("retreaving wav of \"" + x[0] + "\" from spchlib...")
            else:
                print " looking at " + x[0]
                var = x[0]
                var2 = var[0:6]
                print "var2 :"+var2
                if var2 is 'Warning.':
                    print "found it!"
                #save string to dict, get tts, and save wav
                num = self.speechlib.add(x[0])
                self.getWavFromText(x[0], os.path.dirname(os.path.realpath(__file__))+ '/sp_cache/' +str(num) + '.wav')

            #speak
            self.log.msg("ZERO says \"" + x[0] + "\"",'INFO')
            #print("ZERO says \"" + x[0] +"\"")

            self.audio.playFile(os.path.dirname(os.path.realpath(__file__))+ '/sp_cache/' + str(num) + '.wav')




    def getWavFromText(self, text='hello', fname='ttswavfile.wav', lang='en_GB'):

        """ Uses local maryTTS server to get a wav file of
        """
        INPUT_TEXT = text
        INPUT_TYPE = 'TEXT'
        OUTPUT_TYPE = 'AUDIO'
        AUDIO = 'WAVE_FILE'
        LOCALE = lang
        VOICE = 'dfki-prudence'

        payload = {'VOICE': VOICE,
                   'LOCALE': LOCALE,
                   'AUDIO': AUDIO,
                   'OUTPUT_TYPE': OUTPUT_TYPE,
                   'INPUT_TYPE': INPUT_TYPE,
                   'INPUT_TEXT': INPUT_TEXT
                   }

        self.log.msg("Downloading wav of \"" + text + "\" from MaryTTS server")

        # get Text to speech wav file from maryTTS server using REST api
        attempts = 10
        while attempts > 0:
            try:
                r = requests.get('http://' + IPADDRESS + ':' + PORT + '/process', params=payload)
                # r = requests.get("http://192.168.1.14:59125/process?INPUT_TEXT=Hello+world&INPUT_TYPE=TEXT&OUTPUT_TYPE=AUDIO&AUDIO=WAVE_FILE&LOCALE=en_US")
                #print r.status_code
                #print r.headers
                #print r.url

                # create the wav
                self.audio.createWav(fname, r)
                (filepath, filename) = os.path.split(fname)
                self.log.msg("file ./sp_cache/" + filename + " created " + "[%.2f MB] " % self.audio.getWavSize(r) + "(%.2f Seconds)" % self.audio.getWavLength(r))

                break
            except:
                attempts -= 1
                if attempts == 0:
                    self.log.msg("[speech] maryTTS REST request timout",'FAILURE')
                #raise