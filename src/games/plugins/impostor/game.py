"""Impostor game plugin."""
import os
from typing import Dict, Any, Optional

import requests

from manager import games_manager
from games.GamesManager import Game
from lobby.lobby import Lobby
from utils import log


class ImpostorGame(Game):
    """Impostor game where one player gets a different word."""
    
    name = "impostor"
    weight = 0.1
    playerCount = 1

    def _generate_word(self) -> str:
        """Generate a random word from an external API.
        
        Returns:
            A random Italian word
        """
        try:
            url = "https://www.parolecasuali.it/?fs=1&fs2=1&Submit=Nuova+parola"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            # Extract word from Wikipedia link
            text = response.text
            if "https://it.wikipedia.org/wiki/" in text:
                word = text.split("https://it.wikipedia.org/wiki/")[1].split('"')[0]
                return word
            else:
                log("Could not extract word from response")
                return "Parola"
        except Exception as e:
            log(f"Error generating word: {e}")
            return "Parola"

    def play(self, lobby: Lobby) -> Dict[str, Any]:
        """Start the impostor game with a random word.
        
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

        # Check if word is already generated for this round
        tmp_value = lobby.get_tmp_value()
        if tmp_value is None or not isinstance(tmp_value, dict) or tmp_value.get("Type") != "impostor":
            word = self._generate_word()
            lobby.set_tmp_value({"Word": word, "Type": "impostor"})
        else:
            word = tmp_value["Word"]

        return {
            "template": template,
            "options": {"word": word}
        }


# Register the game
games_manager.register_game(ImpostorGame())