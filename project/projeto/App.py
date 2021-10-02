import cherrypy
import sqlite3 as sql
import os
import json
from hashlib import sha256
from datetime import date
from songEngine import durationSong, createSong

PATH = os.path.abspath(os.path.dirname(__file__))
DB_NAME = "BaseDados.db"

conf = {
    "/": {
        "tools.staticdir.root": PATH
    },
    "/html": {
        "tools.staticdir.on": True,
        "tools.staticdir.dir": os.path.join(PATH, "html")
    },
    "/css": {
        "tools.staticdir.on": True,
        "tools.staticdir.dir": os.path.join(PATH, "css")
    },
    "/js": {
        "tools.staticdir.on": True,
        "tools.staticdir.dir": os.path.join(PATH, "js")
    },
    "/songs": {
        "tools.staticdir.on": True,
        "tools.staticdir.dir": os.path.join(PATH, "songs")
    },
    "/samples": {
        "tools.staticdir.on": True,
        "tools.staticdir.dir": os.path.join(PATH, "samples")
    },
    "/webfonts": {
        "tools.staticdir.on": True,
        "tools.staticdir.dir": os.path.join(PATH, "webfonts")
    },
    "/images": {
        "tools.staticdir.on": True,
        "tools.staticdir.dir": os.path.join(PATH, "images")
    }
}

# FALTA:
# funcao put para gerar as musicas com base numa pauta
# testar a funcao put


# devolve o path de um sample(excerto) com o id dado
# id -> id do sample desejado
# return -> path do sample caso exista. None caso nao exista
def getSample(id):
    db = sql.connect(DB_NAME)

    try:
        result = db.execute(
            "SELECT id FROM Samples WHERE id = ?", (str(id),)).fetchone()[0]

        return "samples/" + str(result) + ".wav"

    except:
        return None
    finally:
        db.close()


# devolve o path de uma musica com o id dado
# id -> id da musica desejada
# return -> path da musica caso exista. None caso nao exista
def getSong(id):
    db = sql.connect(DB_NAME)
    # verificar se o id existe na db
    try:
        result = db.execute(
            "SELECT id FROM Musicas WHERE id=?", (str(id),)).fetchone()[0]  # so deve existir 1, mas por precaucao pedimos so o primeiro

        return "songs/" + str(result) + ".wav"

    except:
        return None
    finally:
        db .close()


class Root(object):

    @cherrypy.expose
    def index(self):
        cherrypy.response.headers["Content-Type"] = "text/html"
        return open("./html/index.html", "r", encoding="utf-8")

    @cherrypy.expose
    def excertos(self):
        cherrypy.response.headers["Content-Type"] = "text/html"
        return open("./html/exporter.html", "r", encoding="utf-8")

    @cherrypy.expose
    def songGen(self):
        cherrypy.response.headers["Content-Type"] = "text/html"
        return open("./html/songGen.html", "r", encoding="utf-8")

    @cherrypy.expose
    # devolve uma lista com todas as musicas ou excertos no sistema
    # type -> o tipo de conteudo pretendido (songs(musicas)/samples(excertos))
    # return -> json com a informacao toda de cada musica/excerto ou mensagem de erro caso seja um type invalido
    def list(self, type):
        cherrypy.response.headers["Content-Type"] = "text/json"
        if str(type).lower() == "songs":
            db = sql.connect(DB_NAME)
            result = db.execute(
                "SELECT * FROM Musicas").fetchall()

            db.close()
            return json.dumps(result)
        elif str(type).lower() == "samples":
            db = sql.connect(DB_NAME)
            result = db.execute("SELECT * FROM Samples").fetchall()
            db.close()
            return json.dumps(result)
            # ficheiro ja existente no sistema
            #j = json.loads(open("samples.json").read())
            # return json.dumps({"result": "sucess", "samples": j["samples"]})
        else:
            return json.dumps({"result": "failure", "erro": "type invalido"})

    @cherrypy.expose
    # procura e devolve, caso exista, o path da musica/excerto com o id dado
    # id -> id da musica/excerto
    # return -> path da musica/excerto caso exista. mensagem de erro caso nao exista
    def get(self, id):
        result = getSong(id)
        cherrypy.response.headers["Content-Type"] = "text/json"
        if result != None:
            return json.dumps({"result": "sucess", "path": result})

        # nao foi encontrada nenhuma musica com o id especificado
        # possivelmente um excerto?
        result = getSample(id)

        if result != None:
            return json.dumps({"result": "sucess", "path": result})

        return json.dumps({"result": "failure", "erro": "nao existe excerto nem musica com o id"})

    @cherrypy.expose
    # adicona uma musica ao sistema
    # pauta -> pauta com a informacao da musica a ser criada
    # nome -> nome da musica a ser criada
    # autor -> nome do autor que criou a musica
    # return -> mensagem de erro ou sucesso em json
    def put(self, pauta, nome, autor):
        h = sha256()
        h.update((str(nome) + str(autor)).encode("utf-8"))
        n_id = h.hexdigest()
        jPauta = json.loads(pauta)
        song = getSong(id)

        cherrypy.response.headers["Content-Type"] = "text/json"

        if song != None:
            return json.dumps({"result": "failure", "erro": "autor ja tem uma musica com esse nome"})

        jPauta["id"] = "songs/" + n_id + ".wav"
        created = []
        try:
            created = createSong(jPauta)
        except:
            return json.dumps({"result": "failure", "erro": "erro interno"})
        if not created[0]:
            return json.dumps({"result": "failure", "erro": "erro"})

        length = durationSong("songs/" + n_id + ".wav")
        # adicionar a db
        sqlCommand = "INSERT INTO Musicas (id,nome,autor,length,date,votos) VALUES (?,?,?,?,?,?)"
        db = sql.connect(DB_NAME)
        db.execute(sqlCommand, (n_id, nome, autor,
                                length, str(date.today()), 0))
        db.commit()
        db.close()

        return json.dumps({"result": "success"})

    @cherrypy.expose
    def uploadSample(self, sample, nome):
        cherrypy.response.headers["Content-Type"] = "text/json"
        h = sha256()
        h.update(str(nome).encode("utf-8"))
        id = h.hexdigest()

        s = getSample(id)

        if s != None:
            return json.dumps({"result": "failure", "erro": "ja existe um excerto com esse nome"})
        try:
            uploadPath = os.path.join(PATH, "samples")
            uploadFile = os.path.join(uploadPath, id + ".wav")

            open(uploadFile, "wb").write(sample)
            length = durationSong("samples/" + id + ".wav")
        except:
            return json.dumps({"result": "failure", "erro": "ocorreu um erro durante o processamento"})

        db = sql.connect(DB_NAME)
        try:
            db.execute(
                "INSERT INTO Samples(id,nome,length) VALUES(?,?,?)", (id, str(nome), length))
            db.commit()
        except:
            return json.dumps({"result": "failure", "erro": "ocorreu um erro a inserir na db"})
        finally:
            db.close()

        #res = updateSamplesFile({"nome": nome, "id": id, "length": 0})

        # if not res:
            # return json.dumps({"result": "failure", "erro": "ocorreu um erro durante o processamento"})

        return json.dumps({"result": "sucess"})

    @cherrypy.expose
    # atualiza os votos de uma musica
    # id -> id da musica a atualizar
    # points -> pontos a adicionar aos votos atuais (1,-1). mensagem de erro caso points seja invalido ou a musica nao exista
    def vote(self, id, points):
        cherrypy.response.headers["Content-Type"] = "text/json"
        db = sql.connect(DB_NAME)
        num_votes = None
        try:
            num_votes = db.execute(
                "SELECT votos FROM Musicas WHERE id = ?", (str(id),)).fetchone()[0]
        except:
            db.close()
            return json.dumps({"result": "failure", "erro": "musica nao encontrada"})

        try:
            points = int(points)
        except:
            return json.dumps({"result": "failure", "erro": "points nao e inteiro"})

        if points != -1 and points != 1:
            return json.dumps({"result": "failure", "erro": "points tem de ser 1 ou -1"})

        # atualiza o numero de votos e atualiza a tabela
        new_votes = int(num_votes) + points
        db.execute("UPDATE Musicas SET votos = ? WHERE id = ?",
                   (new_votes, str(id),))

        db.commit()  # funciona como o git commit e git push
        db.close()
        return json.dumps({"result": "success"})


cherrypy.config.update({'server.socket_port': 10014})
if __name__ == "__main__":
    cherrypy.quickstart(Root(), "/", config=conf)
