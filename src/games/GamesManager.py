from lobby.lobby import Lobby
from utils import log
import random

class Game:
    name: str
    weight: int
    playerCount: int

    def getName(self) -> str: return self.name
    def getWeight(self) -> int: return self.weight
    def getPlayerCount(self) -> int: return self.playerCount
    def play(self, lobby: Lobby) -> dict: ... 

class GamesManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    GAMES: dict[str, Game] = {}
    _dummyLobby: Lobby
    whitelist = []

    def __init__(self):
        lobby = Lobby()
        for x in range(10):
            lobby.addPlayer(f"Player-{x}")
        lobby.start()
        self._dummyLobby = lobby 

    def registerGame(self, game: Game):
        gameName = game.getName()

        if self.GAMES.get(gameName) != None:
            log(f"Gioco già caricato!")
            return

        if len(self.whitelist) != 0 and gameName not in self.whitelist:
            log(f"Gioco {gameName} non in whitelist!")
            return


        gameWeight = game.getWeight()

        if not type(gameWeight) in [int, float]:
            log(f"Peso del gioco {gameName} errato!")
            return

        response = game.play(self._dummyLobby)

        if "template" not in response or "options" not in response:
            log(f"Campo template o options non trovato!")
            return
        
        self.GAMES[gameName] = game
        log(f"Gioco {gameName} registrato!")

    def choiceGame(self, seed):
        random.seed(seed)
        games = list(self.GAMES.keys())
        weight = [self.GAMES[game].getWeight() for game in games]
        return self.GAMES[random.choices(games, weights=weight, k=1)[0]]