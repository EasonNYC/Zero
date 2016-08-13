import pygame
import os
# uses google text to speech and pygame to play speech files.
#
#
class Sound:

    def __init__(self):
        self.done = False
        #path to dir which holds wav files (change this later)
        self.FILE_DIR = os.path.dirname(os.path.realpath(__file__))+'/sp_cache/'

        #this is needed in init for playback
        pygame.mixer.pre_init(48000, 16, 1, 4096)
        pygame.display.set_mode((200,100))

    #returns exit condition
    def isdone(self):
        return self.done

    #routines which run on every loop
    def run(self):

        #check for exit pygame condition (esc key or pressing x on pygame window)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    self.done = True
                    break
            elif event.type == pygame.QUIT:
                self.done = True
                pygame.quit()
                break



    #play a list of wav's, given their filenames
    def playFile(self, filenames):
        pygame.mixer.init()
        clock = pygame.time.Clock()

        #handle a list of files
        if isinstance(filenames, list):
            for x in filenames:
                clock.tick(10)
                pygame.mixer.music.load(x)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy() == True:
                    pygame.event.poll()
                    clock.tick(10)
                    continue

        #handle a single file
        else:
            clock.tick(10)
            pygame.mixer.music.load(filenames)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
                pygame.event.poll()
                clock.tick(10)
                continue

    #create a wav file given a filename and a bunch of bytes.
    def createWav(self, fn, rn):
        with open(fn, 'wb') as f:
            size = f.__sizeof__()
            for chunk in rn.iter_content(chunk_size=1024):
                f.write(chunk)
            f.close()

    #returns size of wav file in megabytes using r header
    def getWavSize(self, rh):
        size = rh.headers["Content-Length"]
        return float(size) / 1000.0 / 1000.0

    #return length of speech file in seconds given a number of bytes
    def getWavLength(self, rh):
        size = rh.headers["Content-Length"]
        return float(size) / (48000 * 1 * (16 / 8))
        print time  # seconds




