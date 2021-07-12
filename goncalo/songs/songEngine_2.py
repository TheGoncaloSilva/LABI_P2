# Create a new song, based on the providede samples, wich are given in json format
# Sound effects: https://mixkit.co/free-sound-effects/
from os import pipe
import wave
import sys
import pyaudio
import struct
import os.path
import math
import random
#from pydub import AudioSegment # sudo apt-get install python3-pydub

dic = {
    "bpm": 61,
    "samples": ["./sounds/arcade-retro-game-over.wav", "./sounds/crickets-and-insects-in-the-wild.wav", "./sounds/dog-barking-twice.wav", "./sounds/fast-rocket-whoosh_2.wav"],
    "effects": {
    0: "fadein", 11: "fadeout"
},
	"music": [
		#[0, 2, 3], [], [], [0], [1], [], [0], [], [2], [0], [], [2, 3]
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


# @argumentos -> caminho do ficheiro
# @return -> informação acerca do ficheiro
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

# @argumentos -> caminho do ficheiro
# @return -> lista com pos 0 True ou False, se o ficheiro existe ou não
#         -> pos 1, informação de sucesso e erro, caso algum exista
#         -> i.e [True, "Song generated"] ou [False, "The provided path doesn't exists"]
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

# @argumentos -> música, sample_rate (framerate), duração do efeito
# @return -> música com o efeito de Fade In
def fadeInSong(song, sample_rate, duration) : 
    new_song = []
    duration = float(duration)
    time_start = 0
    time_stop = duration * sample_rate
    step = 1.0 / (sample_rate * duration)
    for index, value in enumerate(song):
        time = index
        if time > time_start and time < time_stop :
            new_song.append(value * index * int(step)) # dava erro sem o int
        else :
            new_song.append(value)

    return new_song

# @argumentos -> música, sample_rate (framerate), duração do efeito
# @return -> música com o efeito de Fade out
def fadeOutSong(song, sample_rate, duration) :
    new_song = []
    sample_rate = float(sample_rate)
    duration = float(duration)
    index = 0
    time_start = index - (duration * sample_rate)
    time_stop = index
    step = 1.0 / (sample_rate * duration)

    for index2, value in enumerate(song) :
        time = index2
        if(time > time_start and time < time_stop) :
            new_song.append(value*(index-index2)*step)
        else :
            new_song.append(value)

    return new_song

# @argumentos -> música
# @return -> música invertida
def reverseSong(song) :
    new_song = []
    for index,value in enumerate(reversed(song)):
        new_song.append(value)
    return new_song

# @argumentos -> música e novo volume
# @return -> música com o volume ajustado
def volumeSong(song, new_vol) :
    # Para controlar o volume basta multiplicar todos os valores de amplitude por um factor
    # multiplicativo. Se este factor for 0.5 o volume deverá ser diminuído em metade. Se for
    # 2.0 o volume deverá ser multiplicado por 2    
    new_song = []
    factor = float(new_vol)

    for index, value in enumerate(song):
        new_song.append(value*factor)

    return new_song

# @argumentos -> música
# @return -> música com o volume normalizado
def normalizeSong(data):
    new_song = []
    val_max = 32767
    max = 0

    for index, value in enumerate(data):
        if(abs(value)>max):
            max = abs(value)

    new_song = volumeSong(data, val_max/max)

    return new_song

# @argumentos -> Musica, sample_rate (framerate), tipo de máscara, começo, duração
# @return -> Música com a máscara aplicada 
def maskSong(song, sample_rate, type, start, duration):
    new_song = []
    start = float(start) * sample_rate
    duration = float(duration) * sample_rate
    end = start + duration

    for index, value in enumerate(song):
        if index > start and index < end:
            if(type == 'silence'):
                new_song.append(0)
            elif(type == 'noise'):
                new_song.append(random.randint(-32768, 32767))
            elif(type == 'tone'):
                new_song.append(10000*math.sin(2 * math.pi * 440 * index / sample_rate))
            else:
                new_song.append(value)
        else:
            new_song.append(value)

    return new_song

# Aplicar uma modulação (multiplicar um som por outro)
# @argumentos -> Musica, sample_rate (Framerate), frequência
# @return -> Música alterada
def modulateSong(song, sample_rate, freq) :
    new_song = []
    freq = int(freq)
    for index, value in enumerate(song):
        new_song.append(value * math.sin(2 * math.pi * freq * index / sample_rate))

    return new_song

# @argumentos -> Musica, sample_rate (framerate), quantidade, tempo de delay (atraso)
# @return -> Musica com delay
def delaySong(song, sample_rate, amount, delay) :
    amount = float(amount)
    delay = float(delay)

    new_song = [0] * len(song)

    tdelay = delay * sample_rate

    for index, value in enumerate(song):
        if index + int(tdelay) < len(new_song):
            new_song[index] = value
            new_song[index + int(tdelay)] += value * amount
        else:
            new_song[index] = value

    return new_song

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
        
    # Aplicar os efeitos na música
    for effects in dictionary["effects"] :
        # print(dictionary["effects"][effects]) Alternative
        if effects == 0 : # efeito de Fade In
            #fadeInSong(data, calculateFramerate(dictionary["bpm"]), 2)
            print("hello")
        elif effects == 1 : # reverter a música
            reverseSong(data)
        elif effects == 2 : # ajustar o volume da música
            volumeSong(data, 2) # choose new volume !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        elif effects == 3 : # normalizar o volume da música
            normalizeSong(data)
        elif effects == 4 : # Introduzir uma máscar à música
            maskSong(data, calculateFramerate(dictionary["bpm"]), "silence", 0, 3) # choose new values !!!!!!!!!!
        elif effects == 5 : # Aplicar uma modulação (multiplicar um som por outro)
            modulateSong(data, calculateFramerate(dictionary["bpm"]), 441) # choose new FREQ !!!!!!
        elif effects == 6 : # Introduzir um delay à música
            delaySong(data, calculateFramerate(dictionary["bpm"]), 5, 2) # choose new values !!!!!!!!
        elif effects == 11 : # efeito de Fade Out
            #fadeOutSong(data, calculateFramerate(dictionary["bpm"]), 2)
            print("hello")

    
    print("In")
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


    