import pygame
from gtts import gTTS
import os
# uses google text to speech and pygame to play speech files.
#
#
class Sound:

    def __init__(self):
        #path to dir which holds mp3 files (change this later)
        self.FILE_DIR = os.path.dirname(os.path.realpath(__file__))+'/'

        #this is needed in init for playback
        pygame.mixer.pre_init(16000, 16, 2, 4096)
        pygame.display.set_mode((200,100))

    #play a list of mp3 file names
    def playMp3(self, filenames):
        pygame.mixer.init()
        clock = pygame.time.Clock()

        if isinstance(filenames, list):
            for x in filenames:
                clock.tick(10)
                pygame.mixer.music.load(x)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.event.poll()
                    clock.tick(10)
        else:
            clock.tick(10)
            pygame.mixer.music.load(filenames)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.event.poll()
                clock.tick(10)

    def saveMp3(self, text='hello', fname='line1.mp3', lang='en-uk'):

        """ Sends text to Google's text to speech service, saves it in the specified location
        American Female en-us
        British Female en-uk
        """

        #limit text to 100 chars
        length = len(text)
        limit = min(100, length)#100 characters is the current limit.
        text = text[0:limit]

        # get Text to speech mp3 file from google
        gtts = gTTS(text, lang)

        #save it in our speech directory
        loc = self.FILE_DIR + fname
        gtts.save(loc)
        print "new mp3 created:", loc
