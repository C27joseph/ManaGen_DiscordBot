from classes.player.Inventory import Inventory
from classes.Database import Database
from classes.player.Binds import Binds


class PlayerList(Database):
    def __init__(self, **kv):
        super().__init__(**kv)


class PlayerManager:
    def __init__(self, key):
        self.key = key
        self.inventory = Inventory(key)
        self.binds = Binds(key)
