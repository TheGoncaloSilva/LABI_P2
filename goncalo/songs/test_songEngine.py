#!/usr/bin/python3
# -*- coding: utf-8 -*-
# run program: python3 -m pytest test_songEngine.py
import pytest
import os
import sys
import songEngine
import time

# Formato de dicionário correto para criar uma música
dic = { 
    "id" : "test_song.wav",
    "bpm": 61,
    "volume" : 5,
    "mask" : 'none',
    "samples": ["./sounds/arcade-retro-game-over.wav", "./sounds/crickets-and-insects-in-the-wild.wav", "./sounds/dog-barking-twice.wav", "./sounds/fast-rocket-whoosh_2.wav"],
    "effects": {
    0: "fadein", 11: "fadeout"
},
	"music": [
		[0, 2, 3], [], [], [0], [1], [], [0], [], [2], [0], [], [2, 3]
	]
}

# Formato de dicionário incorreto para criar uma música, path para uma sample errado
badDic = {
    "id" : "test_song.wav",
    "bpm": 61,
    "volume" : 5,
    "mask" : 'none',
    "samples": ["./sounds/going-to-fail", "./sounds/crickets-and-insects-in-the-wild.wav", "./sounds/dog-barking-twice.wav", "./sounds/fast-rocket-whoosh_2.wav"],
    "effects": {
    0: "fadein", 11: "fadeout"
},
	"music": [
		[0, 2, 3], [], [], [0], [1], [], [0], [], [2], [0], [], [2, 3]
	]
}
#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*# START OF TESTING #*#*#*#*#*#*#*#*#*#*#*#*#*#*#

# Teste de criação de uma música
def test_createSong() :
    assert songEngine.createSong(badDic)[0] == False, "Teste negativo falhou -> ficheiro criado" # Teste negativo, o ficheiro não deve ser gerado e deve devolver um erro de caminho
    assert songEngine.createSong(dic)[0] == True, "Teste Positivo falhou -> ficheiro não gerado" # Teste positivo, o ficheiro deve ser gerado com sucesso
    time.sleep(2) # Esperar que o ficheiro seje gerado
    os.remove("test_song.wav") # Remover a música criada

# Teste da função de verificar se uma música existe
def test_checkSong() :
    assert songEngine.createSong(dic)[0] == True, "Teste Positivo falhou -> ficheiro não gerado" # Criar uma música
    time.sleep(2) # Esperar que seja criada
    assert songEngine.checkSong("test_song.wav")[0] == True, "Teste Positivo falhou -> A música está desaparecida" # Verificar que a música existe
    os.remove("test_song.wav") # Remover a música criada
    assert songEngine.checkSong("test_song.wav")[0] == False , "Teste Negativo falhou -> Encontrou uma música que não devia existir" # Verificar que a música já não existe

# Teste da função de retorno da duração de uma música
def test_durationSong() : 
    assert songEngine.durationSong("./sounds/arcade-retro-game-over.wav") == 2, "Teste Positivo -> Dimensão do ficheiro não correta" # Duração devolvida em segundos, está correta,
                                                                                                                                     # tendo em conta uma duração já fornecida
    assert songEngine.durationSong("./sounds/arcade-retro-game-over.wav") != 3, "Teste Negativo -> Dimensão do ficheiro correta" # Teste negativo, a duração não deve corresponder a esta

# Teste à função de cálculo da framerate
def test_calculate_Framerate() :
    assert songEngine.calculateFramerate(61) == 44835.0, "Teste Positivo -> Framerate incorreta" # Teste Positivo, a frequência criada deve corresponder
    assert songEngine.calculateFramerate(120) != 44835.0, "Teste Negativo -> Framerate incorreta" # Teste Negativo, a frequência criada não deve corresponder

#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*# END OF TESTING #*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#

