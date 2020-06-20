from classes.DiceController import DiceController
from classes.ItemController import ItemController
from library import handleArgs
from unidecode import unidecode
from classes.Config import Strings
from classes.Player import PlayerController


class GuildManager:
    def __init__(self, key):
        self.key = key
        self.path = f"guilds/{self.key}/"
        self.strings = Strings()
        self.dc = DiceController(self)
        self.ic = ItemController(self)
        self.pc = PlayerController(self)
        self.playerManagers = {}
        self.commands = {
            "addplayer": self.addPlayer
        }

    async def run(self, context):
        where = [self.dc, self.ic, self.pc]
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