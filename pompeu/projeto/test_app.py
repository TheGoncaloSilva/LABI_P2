#!/usr/bin/python3
# -*- coding: utf-8 -*-
# run program: python3 -m pytest test_app.py
import pytest
import App
import json
import sqlite3 as sql

erro_list = json.dumps(
    {"result": "failure", "erro": "type invalido"})
erro_get = json.dumps(
    {"result": "failure", "erro": "nao existe excerto nem musica com o id"})

erro_vote_songNotFound = json.dumps(
    {"result": "failure", "erro": "musica nao encontrada"})

erro_vote_invalidPoints = json.dumps(
    {"result": "failure", "erro": "points nao e inteiro"})

erro_vote_invalidPoints2 = json.dumps(
    {"result": "failure", "erro": "points tem de ser 1 ou -1"})

vote_sucess = json.dumps({"result": "success"})


def test_list():
    assert App.Root().list("text") == erro_list, "Teste falhou -> nao deu erro"


def test_get():
    assert App.Root().get("t") == json.dumps(
        {"result": "sucess", "path": "songs/t.wav"}), "Teste falhou -> devolveu erro1"
    assert App.Root().get("falhar") == erro_get, "Teste falhou -> nao devolveu erro2"
    assert App.Root().get("2") == erro_get, "Teste falhou -> nao devolveu erro3"


def test_vote():
    assert App.Root().vote(
        "falhar", 1) == erro_vote_songNotFound, "Teste falhou -> musica encontrada"
    assert App.Root().vote(
        "t", "a") == erro_vote_invalidPoints, "Teste falhou -> points foi considerado inteiro"
    assert App.Root().vote(
        "t", 2) == erro_vote_invalidPoints2, "Teste falhou -> aceitou numero diferente de -1 e 1"
    assert App.Root().vote(
        "t", 1) == vote_sucess, "Teste falhou -> voto nao foi feito com sucesso"

    db = sql.connect("BaseDados.db")
    votos = db.execute(
        "select votos from Musicas where id = \"t\"").fetchone()[0]
    App.Root().vote("t", 1)
    n_votos = db.execute(
        "select votos from Musicas where id = \"t\"").fetchone()[0]

    assert int(n_votos) == int(votos) + \
        1, "Teste falhou -> votos nao estao corretos"


def test_uploadSample():
    fdata = open("./sounds/arcade-retro-game-over.wav", "rb").read()

    # cada assert so pode ser feito 1x pois caso o sample nao exista, vai ser adicionado ao sistema
    # e as tentativas de assert do mesmo ficheiro nao vao dar certo porque o resultado sera diferente
    #{"result":"failure","erro":"ja existe um excerto com esse nome"}
    assert App.Root().uploadSample(
        fdata, "antonio") == json.dumps({"result": "sucess"})
