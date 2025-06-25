from flask_socketio import SocketIO
from glob import glob
import os, importlib

socketio = SocketIO(cors_allowed_origins="*")

paths = glob("games/plugins/*/game.py")
for path in paths:
    plugin_folder = os.path.basename(os.path.dirname(path))
    module_name = f"games.plugins.{plugin_folder}.game"
    module = importlib.import_module(module_name)