"""Central manager instances for games and lobbies."""
from games.GamesManager import GamesManager
from lobby.lobbymanager import LobbyManager

games_manager = GamesManager()
lobby_manager = LobbyManager()