import discord
from library import Json, existKey, getCurrentTime
from classes.Guild import GuildManager
from context import Context


class Client(discord.Client):
    def __init__(self):
        super().__init__()
        self.tokens = Json.loadWrite(pathfile='private/token.json')
        self.bot = "dev"
        self.version = "0.001"
        self.name = "ManaGens"
        self.guildManagers = {}
        self.prefixes = Json.loadWrite(pathfile='private/prefixes.json')
        self.run(self.tokens[self.bot])

    async def on_ready(self):
        cur_time = getCurrentTime()
        print(f"{self.name} [{self.bot}] - {self.version} init at {cur_time}")
        for guild in self.guilds:
            print(f"\t{guild.name}:{guild.id} connected")

    async def on_message(self, message):
        if message.author == self.user:
            return
        if not message.guild:
            return
        gKey = str(message.guild.id)
        gm, prefix = self.getGuildManager(gKey)
        context = Context(prefix, message, self)
        await gm.run(context)

    def getGuildManager(self, key):
        if not existKey(key, self.guilds):
            self.guildManagers[key] = GuildManager(key)
        if not existKey(key, self.prefixes):
            prefix = '/'
        else:
            prefix = self.prefixes[key]
        return self.guildManagers[key], prefix


client = Client()
