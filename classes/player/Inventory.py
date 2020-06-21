from classes.Database import Database
from library import existKey, getCurrentTime
from unidecode import unidecode


class Inventory(Database):
    def __init__(self, path):
        super().__init__(pathfile=path+"inventory.json")

    def addItem(self, item):
        meta = item['meta']
        name = str.lower(unidecode(meta['name']))
        data = item['data']
        actions = item['actions']
        tags = item['tags']
        if meta['stack']:
            if not existKey(name, self):
                self[name] = {
                    "key": name,
                    "qtd": 1,
                    "tags": tags,
                    "actions": actions
                }
            else:
                self[name]['qtd'] += 1
        else:
            self.update({
                name+getCurrentTime(): {
                    "key": name,
                    "data": data,
                    "tags": tags,
                    "actions": actions
                }
            })
        self.save()
