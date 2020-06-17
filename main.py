import discord
from library import *
from classes.Config import *
from classes.Guild import *

class Application:
	def __init__(self):
		self.token = Json.load(pathfile="token.json")
		self.server = "dev"
		self.version = "0.001"
		self.name = "ManaGens"
		self.guilds = {}
	def getGuild(self, key):
		if not existKey(key, self.guilds):
			self.guilds[key] = Guild(key)
		return self.guilds[key]

app = Application()

client = discord.Client()
@client.event
async def on_message(message):
	if message.author == client.user:
		return
	if not message.guild:
		return
	gm = app.getGuild(str(message.id))
	gm.message = message
	

@client.event
async def on_ready():
	print(f"{app.name} init at {getCurrentTime()}")
	for guild in client.guilds:
		print(f"\t{guild.name}:{guild.id} connected")





client.run(app.token[app.server])