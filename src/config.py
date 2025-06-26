import os

DEBUG = int(os.getenv("DEBUG", 1))
INACTIVE_LOBBY_TIME = int(os.getenv("INACTIVE_LOBBY_TIME", 3600)) # 1 Hour
CODE_LEN = int(os.getenv("CODE_LEN", 5))
WEB_SOCKET_URL = os.getenv("WEB_SOCKET_URL", "http://192.168.91.200:5000/")