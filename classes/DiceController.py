from library import handleExpression
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
        self.commands = {
            "r": self.r,
            "g": self.g
        }
        self.strings = self.guild.strings["DiceController"]

    def getExpression(self, args):
        try:
            expression = handleExpression(args)
            pattern = re.compile(r"\d*d\d+")
            total_expression = []
            for v in expression.split():
                dices = pattern.findall(repr(v))
                for dice in dices:
                    n_dices, n_faces = dice.split("d")
                    if len(n_dices) <= 0:
                        n_dices = 1
                    r = self.roll(int(n_dices), int(n_faces))
                    v = v.replace(dice, str(r.total))
                    expression = expression.replace(dice, r.message)
                total_expression.append(v)
            total = " ".join(total_expression)
            total = eval(total)
            return total, expression
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
        nh, expression = self.getExpression(context.args)
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
