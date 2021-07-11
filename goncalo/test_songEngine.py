#!/usr/bin/python3
# -*- coding: utf-8 -*-
# run program: python3 -m pytest test_songEngine.py
import pytest
import os
import sys
import songEngine

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
badDic = {
    "bpm": 61,
    "samples": ["./sounds/going-to-fail", "./sounds/crickets-and-insects-in-the-wild.wav", "./sounds/dog-barking-twice.wav", "./sounds/fast-rocket-whoosh_2.wav"],
    "effects": {
    0: "fadein", 11: "fadeout"
},
	"music": [
		[0, 2, 3], [], [], [0], [1], [], [0], [], [2], [0], [], [2, 3]
	]
}

def test_createSong():
    assert songEngine.createSong(badDic)[0] == False, "Teste negativo falhou -> ficheiro criado"
    assert songEngine.createSong(dic)[0] == True, "Teste Positivo falhou -> ficheiro não gerado"

def test_checkSong():
    assert songEngine.createSong(dic)[0] == True, "Teste Positivo falhou -> ficheiro não gerado"
    assert songEngine.checkSong(id_da_musica_criada)[0] == True, "Teste Positivo falhout -> A música está desaparecida"
    os.remove(id_da_musica_criada) # Remover a música criada
    assert songEngine.checkSong(id_da_musica_criada)[0] == False , "Teste Negativo falhou -> Encontrou uma música que não devia existir" # Verificar que a música já não existe

