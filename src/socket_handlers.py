from flask_socketio import emit, join_room, leave_room
from extensions import socketio
from flask import session
from manager import lobby_manager as lm

@socketio.on("join_lobby")
def join_lobby():
    if not (lobbyCode := session.get("LobbyCode")):
        return
    join_room(session["LobbyCode"])
    lobby = lm.getLobbyByCode(lobbyCode)
    players = list(lobby.getPlayers().keys())
    emit("update_player", {"players": players}, room = lobbyCode) 