from discord import Embed
from library import existKey


class Context:
    def __init__(self, prefix, message, client):
        self.prefix = prefix
        self.message = message
        self.guild = message.guild
        self.channel = message.channel
        self.author = message.author
        self.client = client
        self.users = message.mentions

    def getMessage(self, message,
                   expression="", nh="", dlist="", margin="",
                   result="", total="", ndices="", nfaces=""):
        replaces = [
            ("<#author>", self.author.mention),
            ("<#message>", self.msg),
            ("<#expression>", expression),
            ("<#nh>", str(nh)),
            ("<#dlist>", dlist),
            ("<#margin>", str(margin)),
            ("<#result>", result),
            ("<#total>", str(total)),
            ("<#ndices>", str(ndices)),
            ("<#nfaces>", str(nfaces)),
        ]
        for old, new in replaces:
            message = message.replace(old, new)
        return message

    def getEmbed(self, embed, **kv):
        if len(list(embed.keys())) == 0:
            return None
        e = Embed(
            title=self.getMessage(embed['title'], **kv),
            description=self.getMessage(embed['description'], **kv),
            color=embed['color'])
        if existKey('fields', embed):
            for field in embed['fields']:
                inline = True
                if len(field) == 3:
                    inline = field[2]
                e.add_field(name=self.getMessage(field[0], **kv),
                            value=self.getMessage(field[1], **kv),
                            inline=inline)
        return e

    def setStrings(self, strings):
        self.strings = strings

    def setArgs(self, args, msg=""):
        self.args = args
        self.msg = msg

    def setPlayer(self, player):
        self.player = player

    def sendPv(self, msg):
        pass

    async def sendCh(self, msg, **kv):
        content = self.getMessage(msg['content'], **kv)
        embed = self.getEmbed(msg['embed'], **kv)
        return await self.channel.send(content, embed=embed)
