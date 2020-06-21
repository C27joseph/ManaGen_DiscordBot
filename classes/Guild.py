from classes.DiceController import DiceController
from classes.ItemController import ItemController
from classes.PlayerController import PlayerController
from library import handleArgs
from unidecode import unidecode
from classes.Config import Strings


class GuildManager:
    def __init__(self, key):
        self.key = key
        self.path = f"guilds/{self.key}/"
        self.strings = Strings()
        self.dc = DiceController(self)
        self.ic = ItemController(self)
        self.pc = PlayerController(self)
        self.playerManagers = {}

    async def run(self, context):
        where = [self.dc, self.ic, self.pc]
        for place in where:
            for command, function in place.commands.items():
                cmd = str.lower(unidecode(context.prefix+command+' '))
                if context.message.content.startswith(cmd):
                    args, msg = handleArgs(
                        context.message.content[len(cmd):])
                    player = self.pc.getPlayerManager(context.author)
                    if player:
                        context.setPlayer(player)
                    context.setArgs(args, msg)
                    context.setStrings(place.strings)
                    return await function(context)
