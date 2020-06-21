from classes.Database import Database
from json import loads
from discord import Embed
from unidecode import unidecode


class Item(dict):
    def __init__(self, *v, **kv):
        super().__init__(*v, **kv)

    async def send(self, context):
        meta = self['meta']
        data = self['data']
        tags = ", ".join(self['tags'])
        fields = context.strings["fields"]
        color = context.strings['colors'][meta['rarity']]
        embed = Embed(title=meta["name"],
                      description=meta['description'],
                      color=color)
        embed.add_field(name=fields['weight'], value=f"{meta['weight']}) Kg")

        for name, value in data:
            embed.add_field(name=name, value=value)

        embed.set_image(url=meta["image-url"])
        embed.set_footer(text=fields["tags"]+": "+tags)
        await context.channel.send(embed=embed)


class ItemList(Database):
    def __init__(self, *v, **kv):
        super().__init__(*v, **kv)

    def add(self, item):
        self.update(item)
        self.save()

    def remove(self, name):
        try:
            name = str.lower(unidecode(name))
            item = Item(self[name])
            del self[name]
            self.save()
            return item
        except Exception:
            return None

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
        self.strings = self.guild.strings.ic
        self.commands = {
            "add item": self.add,
            "show item": self.show,
            "remove item": self.remove,
            "give item": self.give
        }

    async def give(self, context):
        item = self.items.get(context.args[0])
        if not item:
            context.author.send(self.strings["error"]['item_not_found'])
            return False
        try:
            user = context.users[0]
            player = self.guild.pc.getPlayerManager(user)
        except Exception:
            context.author.send(self.strings["error"]['player_not_found'])
            return False
        player.inventory.addItem(item)
        await item.send(context)

    async def remove(self, context):
        item = self.items.remove(" ".join(context.args))
        await item.send(context)

    async def add(self, context):
        item = loads(context.msg, encoding="utf-8")
        name = str.lower(unidecode(item['meta']['name']))
        self.items.add({name: item})

    async def show(self, context):
        item = self.items.get(" ".join(context.args))
        await item.send(context)
