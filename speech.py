import time
import Queue
import sound
import fio
# This is Zero's speech process class, which allows him to say things using the say() function.
# All of the things Zero want's to say are stored int a deque called Q. And then permanently stored in a
# pickle file for retrieval. If zero has said something before, he wont use google tts.
#

class Speech:

    MAX_CHAR = 100

    def __init__(self):
        self.Q = Queue.Queue()
        self.audio = sound.Sound()
        self.speechlib = fio.Fio()

        self.speechlib.clear()

    # returns a vector of 100 char max strings of text to say.
    def process(self, text):


        # parse down the text if greater than 100 chars
        if len(text) > self.MAX_CHAR:

            # split the text into sentences and put it into a vector
            stringvec = self.splitup(text)

            # for each string the stringvec
            for stringnum in range(0, len(stringvec)):

                # save next string
                nex = stringnum + 1

                #print "processing: " + stringvec[stringnum]

                # if this string is greater than 100, split it into 2 strings.
                if len(stringvec[stringnum]) > self.MAX_CHAR:

                    # chop it into a vector of words
                    wordvec = self.chopup(stringvec[stringnum])

                    # count up the chars of each word until you get to 100 chars
                    curstring = ''
                    for x in wordvec:
                        wordlength = len(x) + 1
                        if (len(curstring) + wordlength) <= self.MAX_CHAR:
                            curstring += x + ' '
                    n = len(curstring) + 1

                    # split the line into two strings of less than 100chars, push both to our main vector.
                    newstrvec = [stringvec[stringnum][i:i + n] for i in range(0, len(stringvec[stringnum]), n+1)]  # start0,stop(strlen),stepN

                    print("creating new string(1)[" + str(len(newstrvec[0])) + " chars]: " + newstrvec[0])
                    print("creating new string(2)[" + str(len(newstrvec[1])) + " chars]: " + newstrvec[1])

                    # insert them in backwards order so they are dispolayed properly
                    stringvec.insert(nex, newstrvec[1])  # (where to insert,  string to insert)
                    stringvec.insert(nex, newstrvec[0])

                    # and delete the old one
                    stringvec.remove(stringvec[stringnum])

                # else if the next string is not the final string and if this string and the next together are < than 100 chars long
                else:
                    try:

                        if (stringvec[nex] != stringvec[-1]) or ((len(stringvec[stringnum]) + len(stringvec[nex])) <= self.MAX_CHAR):  # thisstring + prevstring
                            stringvec = self.combine(stringvec,stringnum,nex)

                        else:
                            print stringvec[stringnum] + " fell through"
                    except:
                        # we are done, just process the last sentence by combining it with the previous one
                        if (len(stringvec[stringnum]) + len(stringvec[stringnum-1])) <= self.MAX_CHAR:
                            stringvec = self.combine(stringvec,stringnum-1,stringnum)

                        break

            # print each string in the vector
            print("#######RESULTS############")
            print("# strings created: " + str(len(stringvec)))
            for s in stringvec:
                length = len(s)
                print (str(length) + ' ' + s)
            return stringvec

        else:
            #in case no processing needed
            #print("#######RESULTS############")
            #print("# strings created: NONE.")
            #print str(len(text)) + ' ' + text
            return [text]

    #splits up a sentences
    def splitup(self, text):
         print("splitting: " + text)
         stringvect = text.split(". ")

         # add . back in
         for stringnum in range(0, len(stringvect)-1):
            stringvect[stringnum] += '.'

         return stringvect

    #chops up sentences into a vector of words
    def chopup(self, text):
        if len(text) > self.MAX_CHAR:
            print("chopping up: " + text)
            wordvec = text.split(" ")
            return wordvec
        return text

    # takes a vector, combines 2 sentences, returns the vector
    def combine(self, stringvec, stringnum1, stringnum2):
        #print "combining: " + stringvec[stringnum1] + " [AND] " + stringvec[stringnum2]

        # combine both strings
        newstring = stringvec[stringnum1] + " " + stringvec[stringnum2]

        # insert them into the vector
        stringvec.insert(stringnum2 + 1, newstring)

        # remove the old strings
        stringvec.remove(stringvec[stringnum1])
        stringvec.remove(stringvec[stringnum1])

        #print "result: " + stringvec[stringnum1]
        return stringvec

    #workhorse function. Pass it text, it will add it to the Q.
    def say(self, text):

        #process the text
        vec = self.process(text)

        if not vec:
            print "nonetype error"
        else:
            for string in vec:
                self.Q.put([string])

    #put in zero.run() in order to process everything to say.
    def run(self):

        # say all the things we have to say
        while not self.Q.empty():
            x = self.Q.get()  # get next thing to say

            #play file immediatley, else add it to our string database
            num = self.speechlib.getkey(x[0])
            if num > 0:
                print("retreaving...")
            else:
                #save string to dict, get tts, and save mp3
                num = self.speechlib.add(x[0])
                self.audio.saveMp3(x[0],str(num)+'.mp3')

            print("Zero says: " + x[0])
            self.audio.playMp3(str(num)+'.mp3')
            time.sleep(len(x[0]) / 15)  # allows time for Zero to finish speaking
            self.speechlib.printme()
