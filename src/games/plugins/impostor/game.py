from manager import games_manager as gm
from games.GamesManager import Game
import requests

class impostor(Game):
    name = "impostor"
    weight = 0.1
    playerCount = 1

    def genWord(self):
        url = "https://www.parolecasuali.it/?fs=1&fs2=1&Submit=Nuova+parola"
        txt = requests.get(url).text
        return txt.split("https://it.wikipedia.org/wiki/")[1].split('"')[0]

    def play(self, lobby):
        with open(r"games/plugins/impostor/templates/index.html", "rb") as f:
            content = f.read().decode("utf-8")

        word = lobby.getTmpValue()
        if word == None or word["Type"] != "impostor":
            word = {"Word": self.genWord(), "Type": "impostor"}
            lobby.setTmpValue(word)   

        return {"template": content, "options": {"word": word["Word"]}}

gm.registerGame(impostor())