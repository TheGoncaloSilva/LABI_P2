# Create a new song, based on the providede samples, wich are given in json format
import wave
import sys
import pyaudio
import os.path

dic = {
    "bpm": 61,
    "samples": ["sample1", "sample2", "sample3", "sample4"],
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

def readSong():
    return True

def checkSong(filepath):
    if os.path.isfile(filepath) :
        return[True, "success"]
    elif os.path.isdir(filepath) :
        return[False, "The provided path is a directory"]
    else :
        return [False, "The provided path doesn't exists"]

def createSong(dictionary):
    # dictionary["samples"][i] access each sample
    for sample in dictionary["samples"] :
        status = checkSong(sample)
        if(not status[0]):
            return [status[0], status[1]]
    
    return True

createSong(dic) # DEBUG 


    