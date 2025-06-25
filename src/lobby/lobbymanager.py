from .lobby import Lobby
import random, string
from config import CODE_LEN

class LobbyManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    LOBBY = {}

    def createLobby(self) -> str:
        code = "".join(random.choices(string.digits, k=CODE_LEN))
        self.LOBBY[code] = Lobby()
        return code
    
    def getLobbyByCode(self, code) -> Lobby:
        return self.LOBBY.get(code)