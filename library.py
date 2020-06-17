from json import load, dump
import os, sys
import datetime

def existKey(_key, _dict):
	try:
		if _key in list(_dict.keys()):
			return True
	except:
		pass
	return False

def getCurrentTime():
	currentDT = datetime.datetime.now()
	return currentDT.strftime("date: %d/%m/%Y, %H:%M:%S")
	
class Json:
	def load(pathfile=""):
		try:
			with open(pathfile, "r") as f:
				data = load(f)
				return data
		except IOError:
			print(f"cannot load {pathfile}")
			return False
	def loadWrite(pathfile="", default={}, encoding="utf-8"):
		try:
			with open(pathfile, "r", encoding=encoding) as f:
				data = load(f)
				return data
		except IOError:
			cur_path = ""
			for path in pathfile.split("/")[:-1]:
				cur_path += path+"/"
				os.mkdir(cur_path)
			with open(pathfile, 'w') as f:
				dump(default, f, indent = 4, ensure_ascii = False)
				return default
	def write(pathfile="", default={}, encoding="utf-8"):
		try:
			cur_path = ""
			for path in pathfile.split("/")[:-1]:
				cur_path += path+"/"
				os.mkdir(cur_path)
			with open(pathfile, 'w') as f:
				dump(default, f, indent = 4, ensure_ascii = False)
				return True
		except IOError:
			print(f"cannot write {pathfile}")
