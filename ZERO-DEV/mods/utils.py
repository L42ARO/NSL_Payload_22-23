import mods.talking_heads as talking_heads
from signal import *
import sys

def cleanup(*args):
    talking_heads.talk('0-0')
    sys.exit(0)

def exitListen():
    try:
        for sig in (SIGABRT, SIGILL, SIGINT, SIGSEGV, SIGTERM):
            signal(sig, cleanup)
    except Exception as e:
        print(f'Error setting up signal handler: {e}')