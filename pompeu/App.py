import cherrypy
import sqlite3 as sql
import os
import json

PATH = os.path.abspath(os.path.dirname(__file__))

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
    "/musicas": {
        "tools.staticdir.on": True,
        "tools.staticdir.dir": os.path.join(PATH, "musicas")
    },
    "/excertos": {
        "tools.staticdir.on": True,
        "tools.staticdir.dir": os.path.join(PATH, "excertos")
    }
}

# FALTA:
# gerar identificadores com base no conteudo (nome musica + nome autor); usar sha128?
# funcao put para gerar as musicas com base numa pauta
# testar as diversas funcoes


class Root(object):

    @cherrypy.expose
    def index(self):
        return ''

    @cherrypy.expose
    def list(self, type):
        if str(type).lower() == "songs":
            db = sql.connect("BaseDados.db")
            # nao funciona visto que alguns campos nao existem (length,date,id)
            result = db.execute(
                "SELECT nome,id,length,date,votes FROM Musicas")
            res = [{"inicio": "inicio"}]  # debug
            # guarda os dados num array para depois tranformar num json
            for row in result:
                res.append(row)
            res.append({"fim": "fim"})  # debug
            db.close()
            # define o conteudo a ser enviado como um ficheiro json
            cherrypy.response.headers["Content-Type"] = "text/json"
            return json.dumps(res)
        elif str(type).lower() == "samples":
            cherrypy.response.headers["Content-Type"] = "text/json"
            # ficheiro ja existente no sistema
            # para ja o ficheiro esta a ser atualizado manualmente
            # mas devera ser atualizado com a funcao put
            # caso o objeto a guardar seja um sample
            return open("excertos.json")

    @cherrypy.expose
    def get(self, id):
        db = sql.connect("BaseDados.db")
        msg = ""
        # nao funciona visto que alguns campos nao existem (id)
        result = db.execute(
            "SELECT path FROM Musicas WHERE id = ?", (id)).fetchone()
        # funciona??
        # precisa de testes
        if result != None:
            res = {"path": result}
            cherrypy.response.headers["Content-Type"] = "text/json"
            msg = json.dumps(res)
        else:
            # nao foi encontrada nenhuma musica com o id especificado
            # possivelmente um excerto?

            # le os excertos todos
            content = open("excertos.json").read()
            # transforma num dicionario
            excertos = json.loads(content)["excertos"]
            for excerto in excertos:
                if id == excerto["id"]:
                    # foi encontrado um excerto com o id especificado
                    res = {"path": "excertos/" + id}
                    cherrypy.response.headers["Content-Type"] = "text/html"
                    msg = json.dumps(res)

        db.close()
        # devolve uma string vazia
        # talvez seria melhor mandar um json indicando que nao existe musica nem excerto com o id especificado
        return msg

    @cherrypy.expose
    def put(self, pauta, nome):
        return pauta + " " + nome

    @cherrypy.expose
    def vote(self, id, points):
        db = sql.connect("BaseDados.db")
        num_votes = db.execute(
            "SELECT votos FROM Musicas WHERE ID = ?", (id)).fetchone()

        if num_votes == None:
            # nao existe nenhuma musica com o id especificado
            # talvez seria melhor mandar um json a indicar que nao existe nenhuma musica com o id especificado
            return

        # atualiza o numero de votos e atualiza a tabela
        new_votes = int(num_votes) + points
        db.execute("UPDATE Musicas SET votes = ? WHERE ID = ?", (new_votes, id))
        db.close()


cherrypy.config.update({'server.socket_port': 10014})
cherrypy.quickstart(Root(), "/", config=conf)
