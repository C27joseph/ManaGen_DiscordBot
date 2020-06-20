from classes.Database import Database
from json import loads
from discord import Embed
from unidecode import unidecode
from string import capwords


class Item(dict):
    def __init__(self, _dct={}, **kv):
        super().__init__(_dct, **kv)
        
    async def send(self, context):
        meta = self['meta']
        data = self['data']
        if meta['hide']:
            return None
        embed = Embed(title=meta["name"], description=meta['description'])
        embed.set_image(url=meta["image-url"])
        for name, value in data.items():
            try:
                if isinstance(value, list):
                    value = capwords(", ".join(value))
                if len(value) > 0:
                    embed.add_field(name=name, value=value)

            except Exception:
                pass
        await context.channel.send(context.author.mention, embed=embed)


class ItemList(Database):
    def __init__(self, *v, **kv):
        super().__init__(*v, **kv)

    def add(self, item):
        self.update(item)
        self.save()

    def get(self, name):
        try:
            name = str.lower(unidecode(name))
            return Item(self[name])
        except Exception:
            return None


class ItemController:
    def __init__(self, guild):
        self.guild = guild
        self.items = ItemList(pathfile=self.guild.path+"items.json")
        self.commands = {
            "add item": self.addItem,
            "show item": self.showItem
        }

    async def addItem(self, context):
        item = loads(context.msg, encoding="utf-8")
        name = str.lower(unidecode(item['meta']['name']))
        self.items.add({name: item})

    async def showItem(self, context):
        item = self.items.get(" ".join(context.args))
        await item.send(context)
