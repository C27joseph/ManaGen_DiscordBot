from classes.Database import *
from classes.DiceController import *
from library import *
from unidecode import unidecode

class Guild:
	def __init__(self, key):
		self.key = key
		self.dc = DiceController()
	async def run(self, context):
		for command, function in self.dc.commands.items():
			if context.message.content.startswith(str.lower(unidecode(context.prefix+command))):
				args, message = handleArgs(context.message.content[len(context.prefix+command):])
				context.setArgs(args, message)
				return await function(context)
