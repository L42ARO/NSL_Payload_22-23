import json
import mods.talking_heads as talking_heads
from signal import *
import sys

def cleanup(*args):
    talking_heads.talk(0,0)
    sys.exit(0)

def exitListen():
    try:
        for sig in (SIGABRT, SIGILL, SIGINT, SIGSEGV, SIGTERM):
            signal(sig, cleanup)
    except Exception as e:
        print(f'Error setting up signal handler: {e}')
        
        

class Database:
    def __init__(self, path):
        initdata=[]
        with open(path, 'w') as f:
            json.dump(initdata, f)

        self.path = path
        self.data = self._load_data()

    def add_entry(self, entry):
        self.data.append(entry)
        self._save_data()

    def remove_entry_by_name(self, name):
        for entry in self.data:
            if entry["name"] == name:
                self.data.remove(entry)
        self._save_data()

    def query_by_name(self, name):
        for entry in self.data:
            if entry["name"] == name:
                return entry
        return None

    def _load_data(self):
        try:
            with open(self.path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def _save_data(self):
        with open(self.path, 'w') as f:
            json.dump(self.data, f)
