"""Lobby manager for creating and managing game lobbies."""
import random
import string
from typing import Dict, Optional

from config import CODE_LEN
from .lobby import Lobby


class LobbyManager:
    """Singleton manager for creating and accessing game lobbies."""
    
    _instance: Optional['LobbyManager'] = None

    def __new__(cls) -> 'LobbyManager':
        """Ensure only one instance of LobbyManager exists."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._lobbies = {}
        return cls._instance

    def create_lobby(self) -> str:
        """Create a new lobby with a unique code.
        
        Returns:
            The generated lobby code
        """
        code = "".join(random.choices(string.digits, k=CODE_LEN))
        self._lobbies[code] = Lobby()
        return code
    
    def get_lobby_by_code(self, code: str) -> Optional[Lobby]:
        """Get a lobby by its code.
        
        Args:
            code: The lobby code
            
        Returns:
            The Lobby object if found, None otherwise
        """
        return self._lobbies.get(code)
    
    def remove_lobby(self, code: str) -> bool:
        """Remove a lobby by its code.
        
        Args:
            code: The lobby code
            
        Returns:
            True if lobby was removed, False if not found
        """
        if code in self._lobbies:
            del self._lobbies[code]
            return True
        return False
    
    def get_active_lobbies_count(self) -> int:
        """Get the number of active lobbies.
        
        Returns:
            Number of active lobbies
        """
        return len(self._lobbies)