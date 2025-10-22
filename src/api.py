"""API endpoints for the DrinkGame application."""
from typing import Dict, Any

from flask import Blueprint, jsonify, session, Response

from manager import lobby_manager
from extensions import socketio

api = Blueprint('api', __name__, url_prefix='/api')


@api.route("/createLobby", methods=["GET"])
def create_lobby() -> Response:
    """Create a new lobby.
    
    Returns:
        JSON response with lobby code
    """
    code = lobby_manager.create_lobby()
    return jsonify({"ok": True, "code": code})


@api.route("/joinLobby/<code>/<playerName>")
def join_lobby(code: str, playerName: str) -> Response:
    """Join an existing lobby.
    
    Args:
        code: The lobby code
        playerName: The player's name
        
    Returns:
        JSON response indicating success or error
    """
    if not code or not playerName:
        return jsonify({"ok": False, "error": "Invalid code or player name!"})
    
    if len(playerName) > 50:
        return jsonify({"ok": False, "error": "Player name too long!"})
    
    session["LobbyCode"] = code
    session['playerName'] = playerName

    lobby = lobby_manager.get_lobby_by_code(code)
    if lobby is None:
        return jsonify({"ok": False, "error": "Lobby not found!"})
    
    lobby.add_player(playerName)
    socketio.emit('joinPlayer', room=code)
    
    return jsonify({"ok": True})


@api.route("/game/start")
def start_game() -> Response:
    """Start the game in the current lobby.
    
    Returns:
        JSON response indicating success or error
    """
    lobby_code = session.get("LobbyCode")
    if not lobby_code:
        return jsonify({"ok": False, "error": "No lobby code in session!"})
    
    lobby = lobby_manager.get_lobby_by_code(lobby_code)
    if lobby is None:
        return jsonify({"ok": False, "error": "Lobby not found!"})
    
    player_name = session.get('playerName')
    if lobby.get_host() != player_name:
        return jsonify({"ok": False, "error": "You are not the host!"})
    
    lobby.start()
    socketio.emit("gameStart", room=lobby_code)

    return jsonify({"ok": True})


@api.route("/game/next")
def next_game() -> Response:
    """Move to the next game in the current lobby.
    
    Returns:
        JSON response indicating success or error
    """
    lobby_code = session.get("LobbyCode")
    if not lobby_code:
        return jsonify({"ok": False, "error": "No lobby code in session!"})
    
    lobby = lobby_manager.get_lobby_by_code(lobby_code)
    if lobby is None:
        return jsonify({"ok": False, "error": "Lobby not found!"})
    
    player_name = session.get('playerName')
    if lobby.get_host() != player_name:
        return jsonify({"ok": False, "error": "You are not the host!"})

    lobby.gen_new_seed()
    lobby.reset_tmp_value()

    return jsonify({"ok": True})


@api.route("/reload")
def reload_page() -> Response:
    """Reload the page for all players in the lobby.
    
    Returns:
        JSON response indicating success
    """
    lobby_code = session.get("LobbyCode")
    if not lobby_code:
        return jsonify({"ok": False, "error": "No lobby code in session!"})
    
    socketio.emit("reload", room=lobby_code)
    return jsonify({"ok": True})