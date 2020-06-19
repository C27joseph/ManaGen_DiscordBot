from classes.DiceController import DiceController
from library import handleArgs, existKey
from unidecode import unidecode
from classes.Config import Strings
from classes.Player import PlayerManager, PlayerList


class GuildManager:
    def __init__(self, key):
        self.key = key
        self.strings = Strings()
        self.dc = DiceController(self)
        self.players = PlayerList(pathfile=f'guilds/{self.key}/players.json')
        self.playerManagers = {}
        self.commands = {
            "addplayer": self.addPlayer
        }

    async def run(self, context):
        where = [self.dc, self]
        for place in where:
            for command, function in place.commands.items():
                cmd = str.lower(unidecode(context.prefix+command))
                if context.message.content.startswith(cmd):
                    args, message = handleArgs(
                        context.message.content[len(cmd):])
                    pKey = str(context.author.id)
                    player = self.getPlayerManager(pKey)
                    if player:
                        context.setPlayer(player)
                    context.setArgs(args, message)
                    return await function(context)

    async def addPlayer(self, context):
        user = context.message.mentions[0]
        pKey = str(user.id)
        self.players[pKey] = True
        self.players.save()

    def getPlayerManager(self, key):
        if not existKey(key, self.players):
            return None
        if not existKey(key, self.playerManagers):
            pKey = f"guilds/{self.key}/players/{key}/"
            self.playerManagers[key] = PlayerManager(pKey)
