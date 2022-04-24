import voltage
from voltage.ext import commands
import random

from utils import get_db, check_account, cooldown

# (name, multiplier)
people = [
    ("Enoki", 1),
    ("Insert", 1.2),
    ("NotJan", 0.9),
    ("Jan", 1),
    ("Delta", 1.2),
    ("z3", 0.1),
    ("atal", 1.5),
    ("Fatal", 1.2),
    ]

# (message, (min, max), weight)
scenarios = [
   ("{name} saw you begging and graciously gave you {amount} SusCoins.", (1, 100), 1),
   ("WOW, {name} gave you {amount} SusCoins for because they're like very kind and stuff.", (50, 100), 0.8),
    ]

def setup(client) -> commands.Cog:
    economy = commands.Cog("Economy", "Simple economy commands.")

    @check_account()
    @economy.command(aliases=['bal', 'b'])
    async def balance(ctx):
        """Check your balance."""
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT balance FROM economy WHERE user_id = ?", (ctx.author.id,))
        bal = cur.fetchone()[0]
        await ctx.reply(f"Your balance is **__{bal}__** SusCoins.")

    # @cooldown("beg", 20)
    @check_account()
    @economy.command()
    async def beg(ctx):
        """Beg for money."""
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT balance FROM economy WHERE user_id = ?", (ctx.author.id,))
        bal = cur.fetchone()[0]
        person = random.choice(people)
        scenario = random.choices(scenarios, weights=[x[2] for x in scenarios])[0]
        amount = int(random.randint(scenario[1][0], scenario[1][1]) * person[1])
        cur.execute("UPDATE economy SET balance = balance + ? WHERE user_id = ?", (amount, ctx.author.id))
        conn.commit()
        cur.close()
        conn.close()
        await ctx.reply(scenario[0].format(name=f"**{person[0]}**", amount=f"**__{amount}__**"))

    return economy
