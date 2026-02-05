
import sys

DEBUG = 0
SEED = 1234


def is_debug_mode():
    """Return whether debug mode is enabled."""
    global DEBUG 
    return DEBUG == 1

def activate_debug():
    """Set the DEBUG flag from command-line arguments when provided."""
    global DEBUG
    if (len(sys.argv)) > 2:
        DEBUG = int(sys.argv[2])

def activate_seed():
    """Set the random SEED from command-line arguments or fall back to default value shown on top."""
    global SEED, DEBUG
    if (len(sys.argv)) > 1:
        SEED = sys.argv[1]
