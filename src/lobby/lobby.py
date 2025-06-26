import random, os
from config import *

class Lobby:

    PLAYERS: dict
    SEED: bytes
    LastUpdate: float
    STARTED: bool
    HOST: str

    def __init__(self):
        self.PLAYERS = {}
        self.SEED = os.urandom(10)
        self.STARTED = False
        self.HOST = None
        self.TMP = None

    def isStarted(self):
        return self.STARTED
    
    def start(self):
        self.STARTED = True
    
    def getSeed(self):
        return self.SEED
    
    def genNewSeed(self):
        self.SEED = os.urandom(10)

    def addPlayer(self, name):
        if self.HOST == None:
            self.setHost(name)
        self.PLAYERS[name] = 0

    def getPlayers(self):
        return self.PLAYERS

    def selectPlayer(self, name):
        self.PLAYERS[name] += 1
    
    def getHost(self):
        return self.HOST

    def setHost(self, name):
        self.HOST = name

    def setTmpValue(self, value):
        self.TMP = value

    def getTmpValue(self):
        return self.TMP
    
    def resetTmpValue(self):
        self.TMP = None

    def choicePlayers(self, n):
        players = list(self.PLAYERS.keys())
        if n > len(players):
            n = len(players)
        weights = [1 / (self.PLAYERS[user] + 1) for user in players]
        player_weights = list(zip(players, weights))
        selPlayers = []
        for _ in range(n):
            total_weight = sum(w for _, w in player_weights)
            if total_weight == 0:
                break
            r = random.uniform(0, total_weight)
            upto = 0
            for i, (p, w) in enumerate(player_weights):
                upto += w
                if upto >= r:
                    selPlayers.append(p)
                    self.selectPlayer(p)
                    player_weights.pop(i)
                    break

        return selPlayers
