"""Socket.IO event handlers for real-time communication."""
from typing import Optional

from flask import session
from flask_socketio import emit, join_room

from extensions import socketio
from manager import lobby_manager
from utils import log


@socketio.on("join_lobby")
def handle_join_lobby() -> None:
    """Handle a player joining a lobby room.
    
    Adds the player to the Socket.IO room and broadcasts
    the updated player list to all players in the lobby.
    """
    lobby_code: Optional[str] = session.get("LobbyCode")
    if not lobby_code:
        log("Attempted to join lobby without lobby code in session")
        return
    
    join_room(lobby_code)
    
    lobby = lobby_manager.get_lobby_by_code(lobby_code)
    if lobby is None:
        log(f"Lobby {lobby_code} not found")
        return
    
    players = list(lobby.get_players().keys())
    emit("update_player", {"players": players}, room=lobby_code) 