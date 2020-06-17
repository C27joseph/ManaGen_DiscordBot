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

def handleArgs(content):
    args = []
    message = ""
    found_message = False
    for word in content.split():
        if word.startswith("#"):
            found_message = True
        if found_message:
            message += word+" "
        else:
            args.append(word)
    return args, message.rstrip()
    

def getCurrentTime():
    currentDT = datetime.datetime.now()
    return currentDT.strftime("date: %d/%m/%Y, %H:%M:%S")


def handleExpression(args):
    expression = " ".join(args)
    ops = ["/", "*", "+", "-"]
    for op in ops:
        expression = expression.replace(op, " "+op+" ")
    expression = expression.strip().replace("  ", " ")
    return expression

    
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
                try:
                    os.mkdir(cur_path)
                except:
                    pass
            with open(pathfile, 'w') as f:
                dump(default, f, indent = 4, ensure_ascii = False)
                return default
    def write(pathfile="", default={}, encoding="utf-8"):
        try:
            cur_path = ""
            for path in pathfile.split("/")[:-1]:
                cur_path += path+"/"
                try:
                    os.mkdir(cur_path)
                except:
                    pass
            with open(pathfile, 'w') as f:
                dump(default, f, indent = 4, ensure_ascii = False)
                return True
        except IOError:
            print(f"cannot write {pathfile}")