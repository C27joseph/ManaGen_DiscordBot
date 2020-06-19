from classes.Database import Database


class Binds(Database):
    def __init__(self, key):
        super().__init__(pathfile=f"{key}/binds.json")
