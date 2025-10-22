"""I Know game plugin."""
import os
from typing import Dict, Any

from manager import games_manager
from games.GamesManager import Game
from lobby.lobby import Lobby


class IKnowGame(Game):
    """I Know trivia-style game."""
    
    name = "iKnow"
    weight = 0.1
    playerCount = 1

    def play(self, lobby: Lobby) -> Dict[str, Any]:
        """Start the I Know game.
        
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
        
        return {
            "template": template,
            "options": {}
        }


# Register the game
games_manager.register_game(IKnowGame())