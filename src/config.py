import os

DEBUG = os.getenv("DEBUG", True)
INACTIVE_LOBBY_TIME = os.getenv("INACTIVE_LOBBY_TIME", 3600) # 1 Hour
CODE_LEN = os.getenv("CODE_LEN", 5)