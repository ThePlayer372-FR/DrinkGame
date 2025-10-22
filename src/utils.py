"""Utility functions for the DrinkGame application."""
import traceback
from typing import Any

from config import DEBUG


def log(*args: Any, **kwargs: Any) -> None:
    """Log messages when DEBUG mode is enabled.
    
    Args:
        *args: Positional arguments to print
        **kwargs: Keyword arguments to pass to print
    """
    if DEBUG:
        print("[LOG]", *args, **kwargs)


def traduci(word: str) -> str:
    """Translate a word to Italian and capitalize each word.
    
    Args:
        word: The word to translate
        
    Returns:
        The translated and capitalized word
        
    Note:
        This function is currently disabled and returns the input word capitalized.
        The async translation caused issues and has been simplified.
    """
    try:
        # Translation disabled due to async issues with googletrans
        # Consider using a proper translation API if needed
        output = word.strip()
    except Exception as e:
        log(f"Translation error: {e}")
        output = word
        traceback.print_exc()
    
    # Capitalize each word
    output = " ".join([w.capitalize() for w in output.split()])
    return output