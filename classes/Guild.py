from classes.DiceController import DiceController
from library import handleArgs
from unidecode import unidecode
from classes.Config import Strings


class Guild:
    def __init__(self, key):
        self.key = key
        self.strings = Strings()
        self.dc = DiceController(self)

    async def run(self, context):
        for command, function in self.dc.commands.items():
            cmd = str.lower(unidecode(context.prefix+command))
            if context.message.content.startswith(cmd):
                args, message = handleArgs(
                    context.message.content[len(cmd):])
                context.setArgs(args, message)
                return await function(context)
