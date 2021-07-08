# Create a new song, based on the providede samples, wich are given in json format
# Sound effects: https://mixkit.co/free-sound-effects/
from os import pipe
import wave
import sys
import pyaudio
from struct import pack, unpack, unpack_from, error
import os.path

dic = {
    "bpm": 61,
    "samples": ["./sounds/arcade-retro-game-over.wav", "./sounds/crickets-and-insects-in-the-wild.wav", "./sounds/dog-barking-twice.wav"],
    # , "./sounds/fast-rocket-whoosh.wav"
    "effects": {
    0: "fadein", 11: "fadeout"
},
	"music": [
		[0], [], [], [0], [1], [], [0], [], [2], [0], [], [2, 4]
	]
}

# Example of the dictionary
#   {
#       "bpm": 61,
#      "samples": ["sample1", "sample2", "sample3", "sample..n"],
#       "effects": {
#       0: "fadein", 11: "fadeout"
#   },
#       "music": [
#           [0], [], [], [0], [1], [], [0], [], [2], [0], [], [2, 4]
#       ]
#   }
    
# Para controlar o volume basta multiplicar todos os valores de amplitude por um factor
# multiplicativo. Se este factor for 0.5 o volume deverá ser diminuído em metade. Se for
# 2.0 o volume deverá ser multiplicado por 2

def readSong(filePath):
    checkFile = checkSong(filePath)
    if not checkFile[0] :
        return checkFile
    
    wf = wave.open(filePath, "rb") # rb = ler em binário

    result = wf.getparams()
    # wave_read.getparams
    # Returns a namedtuple() 
    # (nchannels, sampwidth, framerate, nframes, comptype, compname), 
    # equivalent to output of the get*() methods.
    wf.close()

    return result

def checkSong(filePath):
    if os.path.isfile(filePath) :
        return[True, "success"]
    elif os.path.isdir(filePath) :
        return[False, "The provided path is a directory"]
    else :
        return [False, "The provided path doesn't exists"]

def createSong(dictionary):
    # dictionary["samples"][i] access each sample
    for sample in dictionary["samples"] :
        status = checkSong(sample)
        # print(str(sample)) DEBUG
        # print(readSong(sample)) DEBUG
        if(not status[0]):
            return [status[0], status[1]]

    # sample files are saved in dictionary["samples"]
    outFile = "newsong.wav" # song that is created

    outputAudio = []
    for files in dictionary["samples"] :
        w = wave.open(files, 'rb')
        raw_data = w.readframes( w.getnframes() )
        w.close()
        print(w.getnframes())
        print("%dh" % w.getnframes())
        data = unpack("%dh" % w.getnframes(), raw_data) # "B" para ficheiros 8bits
        for value in enumerate(data):
            outputAudio.append(value)
        

    #print(str(len(outputAudio))) DEBUG

    wvData = b""

    for v in outputAudio :
        wvData += pack("h", int(v))

    output = wave.open(outFile, 'wb')
    output.setnchannels(1)
    output.setsampwidth(2)
    output.setframerate(44100)
    output.setnframes(len(wvData))
    output.writeframes(bytearray(wvData))
    output.close()

    return [True, "Song generated"]

createSong(dic) # DEBUG 


    