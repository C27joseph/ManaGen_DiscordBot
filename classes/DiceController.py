from library import *
import random
        
class Roll:
    def __init__(self, total, dices, msg):
        self.total = total
        self.dices = dices
        self.message = msg
        
class DiceController:
    def __init__(self):
        self.commands = {
            "r":self.r
        }
    async def r(self, context):
        expression = handleExpression(context.args)
        expression = expression.replace(" d", " 1d")
        total_expression = []
        args_message = []
        for v in expression.split():
            if v.find("d")!=-1:
                try:
                    num_dices, num_faces = v.split("d")
                    r = self.roll(int(num_dices), int(num_faces))
                    total_expression.append(str(r.total))
                    args_message.append(r.message)
                except:
                    return False
            else:
                total_expression.append(v)
                args_message.append(v)
        total = " ".join(total_expression)
        total = eval(total)
        args_message = " ".join(args_message)
        final_message = f"{context.author.mention} rolou {args_message}, Total = {total}"
        await context.channel.send(final_message)
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
        return Roll(total, dices, msg)
