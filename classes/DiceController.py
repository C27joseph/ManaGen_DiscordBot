import random
import discord
import re


class Dice:
    def __init__(self, total, dices, msg):
        self.total = total
        self.dices = dices
        self.message = msg


class DiceController:
    def __init__(self, guild):
        self.guild = guild
        self.strings = self.guild.strings.dc
        self.commands = {
            "r": self.r,
            "g": self.g
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
                expression = expression.replace(dice, r.message)
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

    def getMessage(self, message="", replaces=[]):
        for old, new in replaces:
            message = message.replace(old, new)
        return message

    def getEmbed(self, e, replaces=[]):
        embed = discord.Embed(
            title=self.getMessage(e['title'], replaces),
            description=self.getMessage(e['description'], replaces),
            color=e['color']
        )
        for field in e['fields']:
            if len(field) <= 3:
                field.append(True)
            embed.add_field(
                name=field[0],
                value=self.getMessage(field[1], replaces),
                inline=field[2])
        return embed

    async def g(self, context):
        try:
            nh, expression = self.getExpression(context.args)
        except Exception:
            await context.author.send(self.strings["error"]["expression"])
            return False
        dice = self.roll(3, 6)
        margin, result = self.getGurpsInfo(nh, dice.total)
        replaces = [
            ("<#author>", context.author.mention),
            ("<#expression>", expression),
            ("<#nh>", str(nh)),
            ("<#gdice>", dice.message),
            ("<#margin>", str(margin)),
            ("<#result>", result.capitalize()),
            ("<#message>", context.msg)
        ]
        message = self.strings['g'][result]['message']
        message = self.getMessage(message, replaces)
        embed = None
        if self.strings['g']['embed']:
            embed = self.strings['g'][result]["embed"]
            embed = self.getEmbed(embed, replaces)
        ctx = await context.channel.send(message, embed=embed)
        try:
            for react in self.strings['g'][result]['reactions']:
                await ctx.add_reaction(react)
        except Exception:
            pass
        return ctx

    async def r(self, context):
        try:
            total, expression = self.getExpression(context.args)
        except Exception:
            await context.author.send(self.strings["error"]["expression"])
            return False
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
        msg = msg[: -2]+"]"
        message = self.strings["dice"]
        replaces = [
            ("<#ndices>", str(num_dices)),
            ("<#nfaces>", str(num_faces)),
            ("<#dices>", msg),
            ("<#total>", str(total))
        ]
        message = self.getMessage(message, replaces)
        return Dice(total, dices, message)
