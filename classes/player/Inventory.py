from classes.Database import Database


class Inventory(Database):
    def __init__(self, key):
        super().__init__(pathfile=f"{key}/inventory.json")
