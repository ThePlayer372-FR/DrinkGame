"""Cards game plugin."""
import json
import os
import random
from typing import Dict, Any, List

from manager import games_manager
from games.GamesManager import Game
from lobby.lobby import Lobby


class CardsGame(Game):
    """Card selection game where players draw random cards."""
    
    name = "cards"
    weight = 1.0
    playerCount = 1

    def __init__(self) -> None:
        """Initialize the cards game and load card data."""
        cards_path = os.path.join(
            os.path.dirname(__file__),
            "cards.json"
        )
        
        with open(cards_path, "r", encoding="utf-8") as f:
            self.cards: List[Dict[str, Any]] = json.load(f)

    def play(self, lobby: Lobby) -> Dict[str, Any]:
        """Select and display a random card.
        
        Args:
            lobby: The game lobby
            
        Returns:
            Dictionary with template and options
        """
        template_path = os.path.join(
            os.path.dirname(__file__),
            "templates",
            "index.html"
        )
        
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()

        random.seed(lobby.get_seed())
        selected = random.choice(self.cards)

        return {
            "template": template,
            "options": {
                "card": selected["text"],
                "isSingle": selected["single"]
            }
        }


# Register the game
games_manager.register_game(CardsGame())