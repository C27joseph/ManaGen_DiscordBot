from library import *

class Database(dict):
	def __init__(self,pathfile="", **kv):
		self.pathfile = pathfile
		super().__init__(Json.loadWrite(pathfile=pathfile, **kv))
	def save(self):
		Json.write(pathfile=self.pathfile, default=self)