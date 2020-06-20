from classes.Database import Database

class ItemList(Database):
    pass

class ItemController:
    def __init__(self, guild):
        self.guild = guild
        self.commands = add
        self.items = ItemList(self.guild.key)
