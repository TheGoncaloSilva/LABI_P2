#!/usr/bin/python3
# -*- coding: utf-8 -*-
# run program: python3 -m pytest test_func_songEngine.py
import pytest
import os
import sys
import songEngine
import time
from subprocess import Popen
from subprocess import PIPE

#Popen ("killall python3", stdout = PIPE, shell=True) # Acabar com processos de python que estejam a correr

# Criar uma música
def test_createSong() : 
    cmd = Popen ("python3 songEngine.py", stdout = PIPE, shell=True)
    time.sleep(2)
    assert cmd.wait() == 0 #Check Return Code
    assert cmd.stdout.read ().decode ('utf-8') == "[True, 'Song generated']\n"