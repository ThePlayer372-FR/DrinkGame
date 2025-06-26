from flask import Flask, render_template, session, redirect, url_for, render_template_string
from manager import lobby_manager as lm, games_manager as gm
from extensions import socketio
from config import DEBUG, WEB_SOCKET_URL
from utils import log
from api import api
import os, uuid

app = Flask(__name__)
app.register_blueprint(api)
app.secret_key = os.urandom(32)
socketio.init_app(app)

@app.before_request
def before_req():
    if not session.get("user_id"):
        session["user_id"] = str(uuid.uuid4())

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/game", methods=["GET"])
def game():
    if not (lobbyCode := session.get("LobbyCode")):
        return redirect(url_for("index"))
    lobby = lm.getLobbyByCode(lobbyCode)

    if lobby == None:
        return redirect(url_for("index"))

    if not lobby.isStarted():
       return render_template("lobby.html", lobbyCode = lobbyCode, SOCKET_URL = WEB_SOCKET_URL, isHost = (lobby.getHost() == session["playerName"]))
    
    randomGame = gm.choiceGame(lobby.getSeed())
    playerCount = randomGame.getPlayerCount()

    players = lobby.choicePlayers(playerCount)
    gameOpt = randomGame.play(lobby)
    isSelected = session["playerName"] in players

    return render_template_string(gameOpt["template"], players = players, lobbyCode = lobbyCode, SOCKET_URL = WEB_SOCKET_URL, **gameOpt["options"], isHost = (lobby.getHost() == session["playerName"]), isSelected = isSelected)

import socket_handlers

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=DEBUG, use_reloader=False)