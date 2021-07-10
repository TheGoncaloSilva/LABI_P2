# Create a new song, based on the providede samples, wich are given in json format
# Sound effects: https://mixkit.co/free-sound-effects/
from os import pipe
import wave
import sys
import pyaudio
import struct
import os.path
#from pydub import AudioSegment # sudo apt-get install python3-pydub

dic = {
    "bpm": 61,
    "samples": ["./sounds/arcade-retro-game-over.wav", "./sounds/crickets-and-insects-in-the-wild.wav", "./sounds/dog-barking-twice.wav", "./sounds/fast-rocket-whoosh_2.wav"],
    "effects": {
    0: "fadein", 11: "fadeout"
},
	"music": [
		[0, 2, 3], [], [], [0], [1], [], [0], [], [2], [0], [], [2, 3]
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

# @argumentos -> ficheiro
# @return -> duração música 
def durationSong(filePath):
    checkFile = checkSong(filePath)
    if(not checkFile[0]):
            return [checkFile[0], checkFile[1]]
    w = wave.open(filePath, 'rb')
    return round(w.getnframes() / float(w.getframerate()))

# @argumentos -> beats per minute (bpm)
# @return -> Framerate (Frames per second)
# @formula -> 44100hz = 60 bpm
def calculateFramerate(bpm) :
    #return bpm * 12 / 1
    # return bpm * 0.0166666666666667 / 1
    return bpm * 44100 / 60

# @argumentos ->
# @return -> música com o efeito de Fade In
def fadeInSong(song, sample_rate, duration) : 
    #time_start = 0
    #time_stop = duration * sample_rate
    #step = 1.0 / (sample_rate * duration)
    #for sample in enumerate(song):
    #    ...
    return True

# @argumentos ->
# @return -> música com o efeito de Fade out
def fadeOutSong(file, sample_rate, duration) :

    return True

# @argumentos -> dicionário com informação da música a ser criada
# @return -> lista com pos 0 True ou False, se a música for criada ou não
#         -> pos 1, informação de sucesso e erro, caso algum exista
#         -> i.e [True, "Song generated"] ou [False, "The provided path doesn't exists"]
def createSong(dictionary):
    # dictionary["samples"][i] access each sample
    for sample in dictionary["samples"] : # certificar que todas as samples existem
        status = checkSong(sample)
        if(not status[0]): # verificar que não houve um erro
            return [status[0], status[1]] # se houver um erro, devolver
    
    for music in dictionary["music"] : # verificar a lista das musicas com as samples fornecidas
        for pos in music :
            if pos >= len(dictionary["samples"]) :
                return [False, "Music indexes and samples provided do not match"]

    data= []
    for music in dictionary["music"] :
        if len(music) == 1 :
            sample = dictionary["samples"][music[0]]
            w = wave.open(sample, 'rb')
            data.append( [w.getparams(), w.readframes(w.getnframes())] )
            w.close()
        elif len(music) > 1 :
            #initialize variable
            overlay = b''
            for pos in music :
                sample = dictionary["samples"][pos]
                # overlay the samples
                # or just use the overlay functions on pydub
                w = wave.open(sample, 'rb')
                params = w.getparams()
                overlay += w.readframes(w.getnframes())
            data.append([params, overlay])
        else :
            print("nothing")
            # add blank sound
        
    # efeitos
    # for smtg in efeitos
    # smtg choice
    for effects in dictionary["effects"] :
        # print(dictionary["effects"][effects]) Alternative
        if effects == 0 : # efeito de Fade In
            fadeInSong(data, 1, 2)
        elif effects == 11: # efeito de Fade Out
            fadeOutSong(data, 1, 2)
    
    
    # sample files are saved in dictionary["samples"]
    outFile = "newsong.wav" # song that is created

    # Indices - Valores lista data[0][0]
    # 0 - nchannels
    # 1 - sampwidth
    # 2 - framerate (song pace)
    # 3 - nframes
    # 4 - comptype
    # 5 - compname
    print(data[0][0])

    output = wave.open(outFile, 'wb')
    output.setparams(data[0][0])
    output.setframerate(calculateFramerate(dictionary["bpm"]))
    for i in range(len(data)):
        output.writeframes(data[i][1])
    output.close()

    return [True, "Song generated"]

createSong(dic) # DEBUG 


    