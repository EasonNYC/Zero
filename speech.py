# coding=utf-8
import time
import Queue
import sound
import fio
import requests
import os
# Zero's speech process class, which allows Zero to say things using the say() function.
# All of the things Zero want's to say are stored in a deque (Q) and then permanently stored in a
# pickle file for retrieval.
#

IPADDRESS = '192.168.1.14'
PORT = '59125'
ttswavfile = 'tts.wav'

class Speech:

    def __init__(self):
        self.Q = Queue.Queue()
        self.audio = sound.Sound()
        self.speechlib = fio.Fio()
        #self.speechlib.clear()

    #return just the text for now.
    def process(self, text):
        return text

    #The workhorse. Add things to say to the speech Q.
    def say(self, text):

        #process the text (TODO)
        #vec = self.process(text)

        self.Q.put([text])
        print self.Q

    def splitup(self, text):
        print("splitting: " + text)
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
        while not self.Q.empty():
            x = self.Q.get()  # get next thing to say

            #make wav file, and add it to our speech library
            num = self.speechlib.getkey(x[0])
            if num > 0:
                print("retreaving...")
            else:
                #save string to dict, get tts, and save wav
                num = self.speechlib.add(x[0])
                self.getWavFromText(x[0], os.path.dirname(os.path.realpath(__file__))+ '/sp_cache/' +str(num) + '.wav')

            #speak
            print("Zero says: " + x[0])
            self.audio.playFile(os.path.dirname(os.path.realpath(__file__))+ '/sp_cache/' + str(num) + '.wav')
            # TODO: calculate length of sound file from samplerate and file size. sleep for that length.
            self.speechlib.printme()



    def getWavFromText(self, text='hello', fname='ttswavfile.wav', lang='en_US'):

        """ Uses local maryTTS server to get a wav file of
        """
        INPUT_TEXT = text
        INPUT_TYPE = 'TEXT'
        OUTPUT_TYPE = 'AUDIO'
        AUDIO = 'WAVE_FILE'
        LOCALE = lang
        VOICE = 'cmu-slt-hsmm'

        payload = {'VOICE': VOICE,
                   'LOCALE': LOCALE,
                   'AUDIO': AUDIO,
                   'OUTPUT_TYPE': OUTPUT_TYPE,
                   'INPUT_TYPE': INPUT_TYPE,
                   'INPUT_TEXT': INPUT_TEXT
                   }

        # get Text to speech wav file from maryTTS server using REST api
        attempts = 10
        while attempts > 0:
            try:
                r = requests.get('http://' + IPADDRESS + ':' + PORT + '/process', params=payload)
                # r = requests.get("http://192.168.1.14:59125/process?INPUT_TEXT=Hello+world&INPUT_TYPE=TEXT&OUTPUT_TYPE=AUDIO&AUDIO=WAVE_FILE&LOCALE=en_US")
                print r.status_code
                print r.headers
                print r.url

                # create the wav
                self.audio.createWav(fname, r)
                print "wav file created."

                # get length of time for wave file  length = numbytes / (samplerate * channels * bps/8)
                print self.audio.getWavSize(r)
                print self.audio.getWavLength(r)  # seconds TDO: make these read wav info and not header info

                break
            except:
                attempts -= 1
                if attempts == 0:
                    print "maryTTS REST timout"
                #raise