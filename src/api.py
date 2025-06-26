from flask import Blueprint, jsonify, session
from manager import lobby_manager as lm
from extensions import socketio

api = Blueprint('api', __name__, url_prefix='/api')

@api.route("/createLobby", methods=["GET"])
def createLobby():
    code = lm.createLobby()
    return jsonify({"ok": True, "code": code})

@api.route("/joinLobby/<code>/<playerName>")
def joinLobby(code, playerName):
    session["LobbyCode"] = code
    session['playerName'] = playerName

    lobby = lm.getLobbyByCode(code)
    if lobby == None:
        return jsonify({"ok": False, "error": "Lobby non trovata!"})
    lobby.addPlayer(playerName)

    socketio.emit('joinPlayer', room=code)
    return jsonify({"ok": True})

@api.route("/game/start")
def startGame():
    lobby = lm.getLobbyByCode(session["LobbyCode"])
    playerName = session['playerName']

    if lobby.getHost() != playerName:
        return {"ok": False, "error": "Non sei l'host!"}
    
    lobby.start()
    socketio.emit("gameStart", room = session["LobbyCode"])

    return jsonify({"ok": True})

@api.route("/game/next")
def nextGame():
    lobby = lm.getLobbyByCode(session["LobbyCode"])
    playerName = session['playerName']

    if lobby.getHost() != playerName:
        return {"ok": False, "error": "Non sei l'host!"}

    lobby.genNewSeed()
    lobby.resetTmpValue()

    return jsonify({"ok": True})

@api.route("/reload")
def reloadPage():
    lobbyCode = session["LobbyCode"]
    socketio.emit("reload", room=lobbyCode)
    return jsonify({"ok": True})