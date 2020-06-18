import discord
from library import Json, existKey, getCurrentTime
from classes.Guild import Guild


class Context:
    def __init__(self, prefix, message, client):
        self.prefix = prefix
        self.message = message
        self.guild = message.guild
        self.channel = message.channel
        self.author = message.author
        self.client = client

    def setArgs(self, args, msg=""):
        self.args = args
        self.msg = msg


class Application:
    def __init__(self):
        self.token = Json.loadWrite(pathfile='private/token.json')
        self.server = "dev"
        self.version = "0.001"
        self.name = "ManaGens"
        self.guilds = {}
        self.prefixes = Json.loadWrite(pathfile='private/prefixes.json')

    def getPrefix(self, key):
        if not existKey(key, self.prefixes):
            return '/'
        return self.prefixes[key]

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
    gKey = str(message.guild.id)
    prefix = app.getPrefix(gKey)
    context = Context(prefix, message, client)
    gm = app.getGuild(gKey)
    await gm.run(context)


@client.event
async def on_ready():
    print(f"{app.name} init at {getCurrentTime()}")
    for guild in client.guilds:
        print(f"\t{guild.name}:{guild.id} connected")


client.run(app.token[app.server])
