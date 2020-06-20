from library import Json


class Strings:
    def __init__(self, lenguage="portuguese"):
        self.path = f"lenguages/{lenguage}/"
        self.dc = Json.loadWrite(self.path+"DiceController.json")
        self.ic = Json.loadWrite(self.path+"ItemController.json")
