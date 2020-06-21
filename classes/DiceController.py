import random
import re


class Dice:
    def __init__(self, total, dices, dlist, ndices, nfaces):
        self.total = total
        self.dices = dices
        self.dlist = dlist
        self.ndices = ndices
        self.nfaces = nfaces


class DiceController:
    def __init__(self, guild):
        self.guild = guild
        self.strings = self.guild.strings.dc
        self.commands = {
            "r ": self.r,
            "g ": self.g
        }

    def getExpression(self, args):
        try:
            expression = " ".join(args)
            total = expression
            pattern = re.compile(r"\d*d\d+")
            dices = pattern.findall(repr(expression))
            for dice in dices:
                n_dices, n_faces = dice.split("d")
                if len(n_dices) <= 0:
                    n_dices = 1
                r = self.roll(int(n_dices), int(n_faces))
                total = total.replace(dice, str(r.total))
                expression = expression.replace(dice, f"{dice}={r.total}")
            total = eval(total)
            return total, expression.replace("*", "\\*")
        except Exception:
            return False

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

    async def g(self, context):
        try:
            nh, expression = self.getExpression(context.args)
        except Exception:
            await context.sendPv(self.strings["error"]["expression"])
            return False
        dice = self.roll(3, 6)
        margin, result = self.getGurpsInfo(nh, dice.total)
        return await context.sendCh(
            self.strings['g'][result], result=result,
            nh=nh, expression=expression, margin=margin,
            ndices=dice.ndices, nfaces=dice.nfaces,
            total=dice.total, dlist=dice.dlist,
        )

    async def r(self, context):
        try:
            total, expression = self.getExpression(context.args)
        except Exception:
            await context.author.send(self.strings["error"]["expression"])
            return False
        await context.sendCh(
            self.strings["r"],
            total=total, expression=expression)

    def roll(self, num_dices, num_faces):
        dices = []
        msg = "["
        total = 0
        for i in range(num_dices):
            v = random.randrange(1, num_faces+1)
            msg += str(v)+", "
            total += v
            dices.append(v)
        msg = msg[: -2]+"]"
        return Dice(total, dices, msg, num_dices, num_faces)
