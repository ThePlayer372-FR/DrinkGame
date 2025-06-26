from manager import games_manager as gm
from games.GamesManager import Game
import random, json

class cards(Game):
    name = "cards"
    weight = 1
    playerCount = 1

    cards = []
    
    def __init__(self):
        with open(r"games/plugins/cards/cards.json", "rb") as f:
            content = f.read()
        self.cards = json.loads(content)

    def play(self, lobby):
        with open(r"games/plugins/cards/templates/index.html", "rb") as f:
            content = f.read().decode("utf-8")

        random.seed(lobby.getSeed())
        selected = random.choice(self.cards)

        return {"template": content, "options": {"card": selected["text"], "isSingle": selected["single"]}}

gm.registerGame(cards())