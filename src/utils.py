from config import *
from googletrans import Translator
import asyncio, traceback

def log(*args, **kargs):
    if DEBUG:
        print("[LOG]", *args, **kargs)

def traduci(word):
    try:
        translator = Translator()
        translated = asyncio.run(translator.translate(word.strip(), src='auto', dest='it'))
        output = translated.text
    except:
        output = word
        traceback.print_exc()
    output = " ".join([w.capitalize() for w in output.split()])
    return output