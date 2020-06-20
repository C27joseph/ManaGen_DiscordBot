from classes.player.Inventory import Inventory
from classes.Database import Database
from classes.player.Binds import Binds
from library import existKey


class PlayerList(Database):
    def __init__(self, **kv):
        super().__init__(**kv)


class PlayerController(Database):
    def __init__(self, guild):
        self.guild = guild
        self.path = self.guild.path+"players/"
        self.players = PlayerList(pathfile=self.guild.path+"players.json")
        self.commands = {
            "addplayer":self.addPlayer
        }

    async def addPlayer(self, context):
        # O ideal é aqui adicionar mais informações da criação do personagem, um acesso rápido a configurações dos players como elementos e outras questões, e é claro se o player esta ativo.
        user = context.message.mentions[0]
        pKey = str(user.id)
        self.players[pKey] = True
        self.players.save()

    def getPlayerManager(self, key):
        if not existKey(key, self.players):
            return None
        if not existKey(key, self.playerManagers):
            pKey = self.path+key
            self.playerManagers[key] = PlayerManager(pKey)


class PlayerManager:
    def __init__(self, key):
        self.key = key
        self.inventory = Inventory(key)
        self.binds = Binds(key)
