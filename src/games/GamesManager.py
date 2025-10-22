"""Game manager for registering and selecting games."""
import random
from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from lobby.lobby import Lobby
from utils import log


class Game(ABC):
    """Abstract base class for all games."""
    
    name: str
    weight: float
    playerCount: int

    def get_name(self) -> str:
        """Get the game name."""
        return self.name
    
    def get_weight(self) -> float:
        """Get the game selection weight."""
        return self.weight
    
    def get_player_count(self) -> int:
        """Get the number of players required for this game."""
        return self.playerCount
    
    @abstractmethod
    def play(self, lobby: Lobby) -> Dict[str, any]:
        """Execute the game logic.
        
        Args:
            lobby: The lobby instance
            
        Returns:
            Dictionary containing 'template' and 'options' keys
        """
        pass


class GamesManager:
    """Singleton manager for game registration and selection."""
    
    _instance: Optional['GamesManager'] = None

    def __new__(cls) -> 'GamesManager':
        """Ensure only one instance of GamesManager exists."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._games = {}
            cls._instance._whitelist = []
            cls._instance._initialize_dummy_lobby()
        return cls._instance

    def _initialize_dummy_lobby(self) -> None:
        """Initialize a dummy lobby for game validation."""
        lobby = Lobby()
        for x in range(10):
            lobby.add_player(f"Player-{x}")
        lobby.start()
        self._dummy_lobby = lobby

    def register_game(self, game: Game) -> bool:
        """Register a new game.
        
        Args:
            game: The game instance to register
            
        Returns:
            True if registration successful, False otherwise
        """
        game_name = game.get_name()

        if game_name in self._games:
            log(f"Game '{game_name}' already registered!")
            return False

        if self._whitelist and game_name not in self._whitelist:
            log(f"Game '{game_name}' not in whitelist!")
            return False

        game_weight = game.get_weight()
        if not isinstance(game_weight, (int, float)) or game_weight < 0:
            log(f"Invalid weight for game '{game_name}': {game_weight}")
            return False

        try:
            response = game.play(self._dummy_lobby)
        except Exception as e:
            log(f"Error testing game '{game_name}': {e}")
            return False

        if "template" not in response or "options" not in response:
            log(f"Game '{game_name}' missing 'template' or 'options' field!")
            return False
        
        self._games[game_name] = game
        log(f"Game '{game_name}' registered successfully!")
        return True

    def choice_game(self, seed: bytes) -> Optional[Game]:
        """Select a random game based on weights.
        
        Args:
            seed: Random seed for game selection
            
        Returns:
            Selected game instance or None if no games available
        """
        if not self._games:
            log("No games available!")
            return None
            
        random.seed(seed)
        games = list(self._games.keys())
        weights = [self._games[game].get_weight() for game in games]
        selected = random.choices(games, weights=weights, k=1)[0]
        return self._games[selected]
    
    def get_game_by_name(self, name: str) -> Optional[Game]:
        """Get a game by its name.
        
        Args:
            name: The game name
            
        Returns:
            The game instance or None if not found
        """
        return self._games.get(name)
    
    def get_all_games(self) -> Dict[str, Game]:
        """Get all registered games.
        
        Returns:
            Dictionary of all registered games
        """
        return self._games.copy()
    
    def set_whitelist(self, whitelist: List[str]) -> None:
        """Set the game whitelist.
        
        Args:
            whitelist: List of allowed game names
        """
        self._whitelist = whitelist