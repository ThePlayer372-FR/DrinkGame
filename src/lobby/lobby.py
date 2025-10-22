"""Lobby management for game sessions."""
import os
import random
from typing import Any, Dict, List, Optional


class Lobby:
    """Represents a game lobby with players and game state."""

    def __init__(self) -> None:
        """Initialize a new lobby."""
        self._players: Dict[str, int] = {}
        self._seed: bytes = os.urandom(10)
        self._started: bool = False
        self._host: Optional[str] = None
        self._tmp_value: Optional[Any] = None

    def is_started(self) -> bool:
        """Check if the game has started.
        
        Returns:
            True if the game has started, False otherwise
        """
        return self._started
    
    def start(self) -> None:
        """Mark the game as started."""
        self._started = True
    
    def get_seed(self) -> bytes:
        """Get the random seed for this lobby.
        
        Returns:
            The random seed bytes
        """
        return self._seed
    
    def gen_new_seed(self) -> None:
        """Generate a new random seed for the lobby."""
        self._seed = os.urandom(10)

    def add_player(self, name: str) -> None:
        """Add a player to the lobby.
        
        Args:
            name: The player's name
        """
        if self._host is None:
            self.set_host(name)
        self._players[name] = 0

    def get_players(self) -> Dict[str, int]:
        """Get all players and their selection counts.
        
        Returns:
            Dictionary mapping player names to selection counts
        """
        return self._players

    def select_player(self, name: str) -> None:
        """Increment the selection count for a player.
        
        Args:
            name: The player's name
        """
        if name in self._players:
            self._players[name] += 1
    
    def get_host(self) -> Optional[str]:
        """Get the lobby host's name.
        
        Returns:
            The host's name or None if no host
        """
        return self._host

    def set_host(self, name: str) -> None:
        """Set the lobby host.
        
        Args:
            name: The player's name to set as host
        """
        self._host = name

    def set_tmp_value(self, value: Any) -> None:
        """Set a temporary value for game state.
        
        Args:
            value: Any value to store temporarily
        """
        self._tmp_value = value

    def get_tmp_value(self) -> Optional[Any]:
        """Get the temporary value.
        
        Returns:
            The stored temporary value or None
        """
        return self._tmp_value
    
    def reset_tmp_value(self) -> None:
        """Reset the temporary value to None."""
        self._tmp_value = None

    def choice_players(self, n: int) -> List[str]:
        """Select players using weighted random selection.
        
        Players who have been selected less often have higher probability
        of being selected.
        
        Args:
            n: Number of players to select
            
        Returns:
            List of selected player names
        """
        players = list(self._players.keys())
        n = min(n, len(players))
        
        # Calculate weights: players selected less often have higher weight
        weights = [1.0 / (self._players[player] + 1) for player in players]
        player_weights = list(zip(players, weights))
        selected_players: List[str] = []
        random.seed(self.get_seed())
        
        for _ in range(n):
            total_weight = sum(w for _, w in player_weights)
            if total_weight == 0:
                break
                
            r = random.uniform(0, total_weight)
            cumulative = 0.0
            
            for i, (player, weight) in enumerate(player_weights):
                cumulative += weight
                if cumulative >= r:
                    selected_players.append(player)
                    self.select_player(player)
                    player_weights.pop(i)
                    break

        return selected_players