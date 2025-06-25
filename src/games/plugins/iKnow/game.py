from manager import games_manager as gm
from games.GamesManager import Game

class iKnow(Game):
    name = "iKnow"
    weight = 1
    playerCount = 1

    def play(self, lobby):
        with open(r"games/plugins/iKnow/templates/index.html", "rb") as f:
            content = f.read().decode("utf-8")
        return {"template": content, "options": {}}

gm.registerGame(iKnow())