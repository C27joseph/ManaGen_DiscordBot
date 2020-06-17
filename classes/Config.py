from library import *
from classes.Database import *

class Strings(Database):
	def __init__(self, lenguage="portuguese"):
		super().__init__(pathfile=f"lenguages/{lenguage}.json")