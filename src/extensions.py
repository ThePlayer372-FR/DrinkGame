"""Flask extensions and plugin loading."""
import os
import importlib
from glob import glob

from flask_socketio import SocketIO

from utils import log

# Initialize SocketIO with CORS support
socketio = SocketIO(cors_allowed_origins="*")


def load_game_plugins() -> None:
    """Load all game plugins from the games/plugins directory.
    
    Dynamically imports all game.py files from plugin directories
    to register games with the GamesManager.
    """
    plugins_path = "games/plugins/*/game.py"
    paths = glob(plugins_path)
    
    log(f"Loading game plugins from: {plugins_path}")
    
    for path in paths:
        plugin_folder = os.path.basename(os.path.dirname(path))
        module_name = f"games.plugins.{plugin_folder}.game"
        
        try:
            importlib.import_module(module_name)
            log(f"Successfully loaded plugin: {plugin_folder}")
        except Exception as e:
            log(f"Error loading plugin '{plugin_folder}': {e}")


# Load all game plugins on module import
load_game_plugins()