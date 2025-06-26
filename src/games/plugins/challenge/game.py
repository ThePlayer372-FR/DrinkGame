from manager import games_manager as gm
from games.GamesManager import Game

class challenge(Game):
    name = "challenge"
    weight = 0.1
    playerCount = 2

    def play(self, lobby):
        with open(r"games/plugins/challenge/templates/index.html", "rb") as f:
            content = f.read().decode("utf-8")
        return {"template": content, "options": {}}

gm.registerGame(challenge())