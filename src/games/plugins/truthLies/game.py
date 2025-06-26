from manager import games_manager as gm
from games.GamesManager import Game

class truthLies(Game):
    name = "truthLies"
    weight = 0.1
    playerCount = 1

    def play(self, lobby):
        with open(r"games/plugins/truthLies/templates/index.html", "rb") as f:
            content = f.read().decode("utf-8")
        return {"template": content, "options": {}}

gm.registerGame(truthLies())