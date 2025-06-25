from config import *

def log(*args, **kargs):
    if DEBUG:
        print("[LOG]", *args, **kargs)