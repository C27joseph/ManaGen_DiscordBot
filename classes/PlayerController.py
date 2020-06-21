from classes.player.Inventory import Inventory
from classes.Database import Database
from classes.player.Binds import Binds
from library import existKey


class AcceptedPlayers(Database):
    def __init__(self, **kv):
        super().__init__(**kv)


class PlayerController(Database):
    def __init__(self, guild):
        self.guild = guild
        self.path = self.guild.path+"players/"
        self.acceptedPlayers = AcceptedPlayers(
            pathfile=self.guild.path+"acceptedPlayers.json")
        self.players = {}
        self.strings = self.guild.strings
        self.commands = {
            "add player": self.addPlayer,
            "items": self.items
        }

    async def items(self, context):
        try:
            # if is adm
            user = self.getPlayerManager(context.users[0])
        except Exception:
            user = self.getPlayerManager(context.author)
        await user.inventory.send(context)

    async def addPlayer(self, context):
        user = context.message.mentions[0]
        pKey = str(user.id)
        self.acceptedPlayers[pKey] = True
        self.acceptedPlayers.save()

    def getPlayerManager(self, user):
        key = str(user.id)
        if not existKey(key, self.acceptedPlayers):
            return None
        if not existKey(key, self.players):
            self.players[key] = PlayerManager(self, key)
        return self.players[key]


class PlayerManager:
    def __init__(self, controller, key):
        self.key = key
        self.controller = controller
        self.path = self.controller.path+key+"/"
        self.inventory = Inventory(self)
        self.binds = Binds(self.path)
