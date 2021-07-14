# Create a new song, based on the providede samples, wich are given in json format
# Sound effects: https://mixkit.co/free-sound-effects/
from os import pipe
import wave
import sys
import struct
import os.path
import math
import random

# normalize e modulate nao estão a funcionar

dic = {
    "id": "final_song.wav",
    "bpm": 61,
    "volume": 5,
    "mask": 'none',
    "samples": ["./sounds/arcade-retro-game-over.wav", "./sounds/crickets-and-insects-in-the-wild.wav", "./sounds/dog-barking-twice.wav", "./sounds/fast-rocket-whoosh_2.wav"],
    "effects": {
        0: "fadein", 11: "fadeout"
    },
    "music": [
        [0], [2, 3], [], [0], [1], [], [0], [], [2], [0], [], [2, 3]
    ]
}

# Example of the dictionary
#   {
#       "id" : "final_song.wav",
#        "bpm": 61,
#        "volume" : 5,
#        "mask" : 'none',
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
    checkFile = checkSong(filePath)  # Verificar a existência do ficheiro
    if not checkFile[0]:
        return checkFile  # Devolver o dicionário de erro

    wf = wave.open(filePath, "rb")  # rb = ler em binário

    result = wf.getparams()  # quardar os parâmetros
    # wave_read.getparams
    # Returns a namedtuple()
    # (nchannels, sampwidth, framerate, nframes, comptype, compname),
    # equivalent to output of the get*() methods.
    wf.close()  # fechar o ficheiro

    return result  # devolver os parâmetros

# @argumentos -> caminho do ficheiro
# @return -> lista com pos 0 True ou False, se o ficheiro existe ou não
#         -> pos 1, informação de sucesso e erro, caso algum exista
#         -> i.e [True, "Song generated"] ou [False, "The provided path doesn't exists"]


def checkSong(filePath):
    if os.path.isfile(filePath):  # Se o caminho fornecido é um ficheiro
        return[True, "success"]
    elif os.path.isdir(filePath):  # Se o caminho fornecido é um diretório
        # retorna uma mensagem de erro
        return[False, "The provided path is a directory"]
    else:  # Se o caminho fornecido não existe
        # retorna uma mensagem de erro
        return [False, "The provided path doesn't exists"]

# @argumentos -> ficheiro
# @return -> duração música em segundos


def durationSong(filePath):
    checkFile = checkSong(filePath)  # Verificar a existência do ficheiro
    if(not checkFile[0]):
        return [checkFile[0], checkFile[1]]  # Devolver o dicionário de erro
    w = wave.open(filePath, 'rb')  # ler o ficheiro em binário
    # devolver a duração em segundos
    return round(w.getnframes() / float(w.getframerate()))

# @argumentos -> bites de Música
# @return -> duração música


# aceita bytes como parâmetros, invés de um filepath (Não está a funcionar muito corretamente)
def durationData(data, framerate):
    # devolver a duração da música em segundos
    return round(data / float(framerate))

# @argumentos -> beats per minute (bpm)
# @return -> Framerate (Frames per second)
# @formula -> 44100hz = 60 bpm


def calculateFramerate(bpm):
    # 60 bpm = 1s
    # Usei esta fórmula, pois penso que o valor default de velocidade de cada música é 44110hz
    # 1hz = 1s
    # I.E 61 * 1 / 60 =  +/- 1.1, mas este valor está errado, pois a música teria horas e horas de duração
    # Assim usei uma fórmula que me parece correta
    return bpm * 44100 / 60  # devolve a framerate para utilizar no ficheiro

# @argumentos -> música, sample_rate (framerate), duração do efeito
# @return -> música com o efeito de Fade In


def fadeInSong(song, sample_rate, duration):
    new_song = []
    duration = float(duration)
    time_start = 0
    time_stop = duration * sample_rate
    step = 1.0 / (sample_rate * duration)
    for index, value in enumerate(song):
        time = index
        if time > time_start and time < time_stop:
            # usar o int para não dar erro de conversão com os outos valores
            new_song.append(value * index * int(step))
        else:
            new_song.append(value)

    return new_song  # devolver nova música com fade-in

# @argumentos -> música, sample_rate (framerate), duração do efeito
# @return -> música com o efeito de Fade out


def fadeOutSong(song, sample_rate, duration):
    new_song = []
    sample_rate = float(sample_rate)
    duration = float(duration)
    index = 0
    time_start = index - (duration * sample_rate)
    time_stop = index
    step = 1.0 / (sample_rate * duration)

    for index2, value in enumerate(song):
        time = index2
        if(time > time_start and time < time_stop):
            new_song.append(value * (index - index2) * step)
        else:
            new_song.append(value)

    return new_song  # devolver nova música com fade-out

# @argumentos -> música
# @return -> música invertida


def reverseSong(song):
    new_song = []
    # reverse() inverte a ordem dos valores, com base no índice
    for value in reversed(song):
        new_song.append(value)
    return new_song  # devolver a música invertida

# @argumentos -> música e novo volume
# @return -> música com o volume ajustado


def volumeSong(song, new_vol):
    # Para controlar o volume basta multiplicar todos os valores de amplitude por um factor
    # multiplicativo. Se este factor for 0.5 o volume deverá ser diminuído em metade. Se for
    # 2.0 o volume deverá ser multiplicado por 2
    new_song = []
    factor = float(new_vol)

    for index, value in enumerate(song):
        # usei o int, para não existirem erros de conversão com os valores
        new_song.append(value * int(factor))

    return new_song  # volume da música alterado

# @argumentos -> música
# @return -> música com o volume normalizado


def normalizeSong(data):  # Não está a funcionar corretamente
    new_song = []
    val_max = 32767
    max = 0

    for index, value in enumerate(data):
        if(abs(value) > max):
            max = abs(value)

    new_song = volumeSong(data, val_max / max)

    return new_song  # devolve a música normalizada

# @argumentos -> Musica, sample_rate (framerate), tipo de máscara, começo, duração
# @return -> Música com a máscara aplicada


def maskSong(song, sample_rate, type, start, duration):
    new_song = []
    start = float(start) * sample_rate
    duration = float(duration) * sample_rate
    end = start + duration

    for index, value in enumerate(song):
        # antes estava index > start, mas isso nunca aconteceria e os filtros nunca eram aplicados,
        #  pois o start seria, i.e 2 * 44100 = 88200. e o index, vai de 0...11.. nunca chegaria a esse valor
        if index < start and index < end:
            if(type == 'silence'):
                new_song.append(0)
            elif(type == 'noise'):
                new_song.append(random.randint(-32768, 32767))
            elif(type == 'tone'):
                new_song.append(
                    10000*math.sin(2 * math.pi * 440 * index / sample_rate))
            else:
                new_song.append(value)
        else:
            new_song.append(value)

    return new_song

# Aplicar uma modulação (multiplicar um som por outro)
# @argumentos -> Musica, sample_rate (Framerate), frequência
# @return -> Música alterada


def modulateSong(song, sample_rate, freq):  # Não está a funcionar corretamente
    new_song = []
    freq = int(freq)
    for index, value in enumerate(song):
        # adicionei o int, pois estava a ter erros de operação com outras variáveis
        new_song.append(value * math.sin(2 * math.pi *
                                         freq * index / int(sample_rate)))

    return new_song  # devolver a música modulada

# @argumentos -> Musica, sample_rate (framerate), quantidade, tempo de delay (atraso)
# @return -> Musica com delay


def delaySong(song, sample_rate, amount, delay):
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

    return new_song  # devolve Música com um atraso (delay) aplicado

# Aplicar os efeitos na música
# @argumentos -> Música, bpm (framerate), efeito escolhido
# @return -> Música com o efeito aplicado


def effectsSong(data, bpm, effects):
    if effects == "fadein":  # efeito de Fade In
        data = fadeInSong(data, bpm, 2)
    elif effects == "reverse":  # reverter a música
        data = reverseSong(data)
    elif effects == "normalize":  # normalizar o volume da música
        data = normalizeSong(data)  # Não funciona corretamente
    # Aplicar uma modulação (multiplicar um som por outro)
    elif effects == "modulate":
        data = modulateSong(data, bpm, 441)  # Não funciona corretamente
    elif effects == "delay":  # Introduzir um delay à música
        data = delaySong(data, bpm, 5, 2)
    elif effects == "fadeout":  # efeito de Fade Out
        data = fadeOutSong(data, bpm, 2)
    else:
        print("Effect doesn't exist")

    return data

# @argumentos -> dicionário com informação da música a ser criada
# @return -> lista com pos 0 True ou False, se a música for criada ou não
#         -> pos 1, informação de sucesso e erro, caso algum exista
#         -> i.e [True, "Song generated"] ou [False, "The provided path doesn't exists"]


def createSong(dictionary):
    # dictionary["samples"][i] access each sample
    # certificar que todas as samples existem
    for sample in dictionary["samples"]:
        status = checkSong(sample)
        if(not status[0]):  # verificar que não houve um erro
            print([status[0], status[1]])
            return [status[0], status[1]]  # se houver um erro, devolver

    # verificar a lista das musicas com as samples fornecidas
    for music in dictionary["music"]:
        for pos in music:
            if pos >= len(dictionary["samples"]):
                print([False, "Music indexes and samples provided do not match"])
                return [False, "Music indexes and samples provided do not match"]

    data = []
    # Percorrer o dicionário das músicas
    for i, music in enumerate(dictionary["music"]):
        if len(music) == 1:  # se não for preciso combinar músicas, apenas se acrescenta ao dicionário
            sample = dictionary["samples"][music[0]]
            w = wave.open(sample, 'rb')
            params = w.getparams()  # Obter os parâmetros do excerto
            dataTemp = w.readframes(w.getnframes())  # Ler o excerto
            # Percorrer a lista de efeitos, para determinar se existe algum
            if i in dictionary["effects"]:
                # alterar os dados lidos para o excerto com o efeito aplicado
                dataTemp = bytes(effectsSong(dataTemp, calculateFramerate(
                    dictionary["bpm"]), dictionary["effects"][i]))
            data.append([params, dataTemp])  # guardar os dados na lista
            w.close()  # fechar o excerto
        elif len(music) > 1:  # se houver mais do que uma música no índice da lista de ficheiros, vamos sobrepô-las
            overlay = b''  # inicializar a variável
            # percorrer as músicas presentes no índice
            for l, pos in enumerate(music):
                sample = dictionary["samples"][pos]
                # overlay the samples
                w = wave.open(sample, 'rb')
                params = w.getparams()  # Obter os parâmetros do excerto
                dataTemp = w.readframes(w.getnframes())  # Ler o excerto
                # Percorrer a lista de efeitos, para determinar se existe algum
                if i in dictionary["effects"]:
                    # alterar os dados lidos para o excerto com o efeito aplicado
                    overlay += bytes(effectsSong(dataTemp, calculateFramerate(
                        dictionary["bpm"]), dictionary["effects"][i]))
                else:
                    overlay += dataTemp  # copiar o excerto normal

            data.append([params, overlay])  # guardar os dados na lista
        else:
            data.append([0, bytes(0)])  # Adicionar troço de silêncio

    # Ajustar o volume
    data = volumeSong(data, int(dictionary["volume"]) / 5)

    # Adicionar Máscara, caso seje especificado
    if dictionary["mask"] != "none":
        data[0:][1] = maskSong(data, calculateFramerate(
            dictionary["bpm"]), dictionary["mask"], 2, 5)

    # sample files are saved in dictionary["samples"]

    # Indices - Valores lista data[0][0]
    # 0 - nchannels
    # 1 - sampwidth
    # 2 - framerate (song pace)
    # 3 - nframes
    # 4 - comptype
    # 5 - compname
    # print(data[0][0]) # Mostrar a informação do ficheiro original DEBUG
    # print("Output Framerate : " + str(calculateFramerate(dictionary["bpm"]))) # Mostrar a frequência do ficheiro de saída DEBUG

    # abrir / criar o ficheiro output da música
    output = wave.open(dictionary["id"], 'wb')
    # Escrever os parâmetros do ficheiro original no ficheiro de saída
    output.setparams(data[0][0])
    # Alterar a framerate do ficheiro, tendo em conta os bpm fornecidos
    output.setframerate(calculateFramerate(dictionary["bpm"]))
    for i in range(len(data)):  # percorrer a música gerada
        output.writeframes(data[i][1])  # escrever no ficheiro de saída
    output.close()  # fechar o ficheiro de saída

    print([True, "Song generated"])
    # devolver que todas as operações correram com sucesso
    return [True, "Song generated"]


createSong(dic)  # DEBUG
