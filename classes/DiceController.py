from library import handleExpression
import random


class Dice:
    def __init__(self, total, dices, msg):
        self.total = total
        self.dices = dices
        self.message = msg


class DiceController:
    def __init__(self, guild):
        self.guild = guild
        self.commands = {
            "r": self.r,
            "g": self.g
        }
        self.strings = self.guild.strings["DiceController"]

    def getExpression(self, args):
        expression = handleExpression(args)
        expression = expression.replace(" d", " 1d")
        total_expression = []
        args_message = []
        for v in expression.split():
            if v.find("d") != -1:
                try:
                    num_dices, num_faces = v.split("d")
                    r = self.roll(int(num_dices), int(num_faces))
                    total_expression.append(str(r.total))
                    args_message.append(r.message)
                except Exception:
                    return False
            else:
                total_expression.append(v)
                args_message.append(v)
        total = " ".join(total_expression)
        total = eval(total)
        args_message = " ".join(args_message)
        return total, args_message

    def getGurpsInfo(self, nh, total):
        margin = nh - total
        if total <= 4:
            result = "decisive"
        elif total >= 17:
            result = "critic"
        elif margin >= 10:
            result = "decisive"
        elif margin <= -10:
            result = "critic"
        elif margin >= 0:
            result = "success"
        else:
            result = "fail"
        return margin, result

    def getMessage(self, message="", replaces=[]):
        for old, new in replaces:
            message = message.replace(old, new)
        return message

    async def g(self, context):
        nh, expression = self.getExpression(context.args)
        dice = self.roll(3, 6)
        margin, result = self.getGurpsInfo(nh, dice.total)
        replaces = [
            ("<#author>", context.author.mention),
            ("<#expression>", expression),
            ("<#nh>", str(nh)),
            ("<#gdice>", dice.message),
            ("<#margin>", str(margin))
        ]
        message = self.strings['g']['message']
        message = self.getMessage(message, replaces)
        return await context.channel.send(message)

    async def r(self, context):
        total, expression = self.getExpression(context.args)
        replaces = [
            ("<#author>", context.author.mention),
            ("<#expression>", expression),
            ("<#total>", str(total))
        ]
        message = self.strings['r']['message']
        message = self.getMessage(message, replaces)
        return await context.channel.send(message)

    def roll(self, num_dices, num_faces):
        dices = []
        msg = "["
        total = 0
        for i in range(num_dices):
            v = random.randrange(1, num_faces+1)
            msg += str(v)+", "
            total += v
            dices.append(v)
        msg = f"{num_dices}d{num_faces}: {total} "+msg[:-2]+"]"
        return Dice(total, dices, msg)
