from classes.Database import Database
from library import existKey, getKey
from unidecode import unidecode


class Inventory(Database):
    def __init__(self, player):
        self.player = player
        super().__init__(pathfile=player.path+"inventory.json")

    async def send(self, context):
        text = "Lista: \n"
        for k, item in self.items():
            if existKey("key", item):
                text += f"**{item['meta']['name']}** > Item Único > Id: `{item['key']}`\n"
            else:
                text += f"**{item['name']}** x{item['qtd']}\n"
        await context.channel.send(text)

    def addItem(self, item, qtd=1):
        meta = item['meta']
        name = str.lower(unidecode(meta['name']))
        tags = item['tags']
        if meta['stack']:
            if not existKey(name, self):
                self[name] = {
                    "name": meta['name'],
                    "qtd": 1,
                    "tags": tags,
                }
            else:
                self[name]['qtd'] += qtd
        else:
            for i in range(qtd):
                time = name+getKey()+str(i)
                self.update({time: item})
                self[time]["key"] = time
        self.save()

    def getTags(self):
        tags = []
        for item, info in self.items():
            tags += info["tags"]
        return tags
