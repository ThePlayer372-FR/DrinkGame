"""Main Flask application for DrinkGame."""
import os
import uuid
from typing import Optional

from flask import Flask, render_template, session, redirect, url_for, render_template_string, Response

from manager import lobby_manager, games_manager
from extensions import socketio
from config import DEBUG, WEB_SOCKET_URL
from utils import log
from api import api

# Initialize Flask app
app = Flask(__name__)
app.register_blueprint(api)
app.secret_key = os.urandom(32)
socketio.init_app(app)


@app.before_request
def before_request() -> None:
    """Ensure each user has a unique session ID."""
    if not session.get("user_id"):
        session["user_id"] = str(uuid.uuid4())


@app.route("/", methods=["GET"])
def index() -> str:
    """Render the home page."""
    return render_template("index.html")


@app.route("/game", methods=["GET"])
def game() -> Response | str:
    """Render the game or lobby page.
    
    Returns:
        Redirect to index if no valid lobby, lobby page if game not started,
        or game template if game is started
    """
    lobby_code: Optional[str] = session.get("LobbyCode")
    if not lobby_code:
        return redirect(url_for("index"))
    
    lobby = lobby_manager.get_lobby_by_code(lobby_code)
    if lobby is None:
        return redirect(url_for("index"))

    player_name = session.get("playerName", "")
    is_host = lobby.get_host() == player_name

    # Show lobby if game hasn't started
    if not lobby.is_started():
        return render_template(
            "lobby.html",
            lobbyCode=lobby_code,
            SOCKET_URL=WEB_SOCKET_URL,
            isHost=is_host
        )
    
    # Select and render game
    random_game = games_manager.choice_game(lobby.get_seed())
    if random_game is None:
        log("No game could be selected!")
        return redirect(url_for("index"))
    
    player_count = random_game.get_player_count()
    players = lobby.choice_players(player_count)
    game_options = random_game.play(lobby)
    is_selected = player_name in players

    return render_template_string(
        game_options["template"],
        players=players,
        lobbyCode=lobby_code,
        SOCKET_URL=WEB_SOCKET_URL,
        isHost=is_host,
        isSelected=is_selected,
        **game_options["options"]
    )


# Import socket handlers
import socket_handlers


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=DEBUG, use_reloader=False)