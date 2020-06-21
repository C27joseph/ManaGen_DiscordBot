from classes.Database import Database


class Binds(Database):
    def __init__(self, path):
        super().__init__(pathfile=path+"binds.json")
