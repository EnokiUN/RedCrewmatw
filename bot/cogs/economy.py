import os
from dotenv import load_dotenv
import mariadb

import voltage
from voltage.ext import commands

def setup(client) -> commands.Cog:
    economy = commands.Cog("Economy", "Simple economy commands.")

    load_dotenv(".env")
    conn = mariadb.connect(
            username=os.getenv("DB_NAME"),
            password=os.getenv("DB_PASS"),
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT")),
            database=os.getenv("DB_NAME")
    )
    cur = conn.cursor()

    def check_account(command):
        func = command.func
        def wrapper(ctx, *args, **kwargs):
            cur.execute("SELECT * FROM economy WHERE user_id = ?", (ctx.author.id,))
            if cur.fetchone() is None:
                cur.execute("INSERT INTO economy (user_id) VALUES (?)", (ctx.author.id,))
                cur.execute("INSERT INTO cooldowns (user_id) VALUES (?)", (ctx.author.id,))
                conn.commit()
            return func(ctx, *args, **kwargs)
        command.func = wrapper
        return command

    @check_account
    @economy.command(aliases=['bal', 'b'])
    async def balance(ctx):
        """Check your balance."""
        cur.execute("SELECT * FROM economy")
        print(cur.fetchall())
        cur.execute("SELECT balance FROM economy WHERE user_id = ?", (ctx.author.id,))
        bal = cur.fetchone()[0]
        await ctx.send(f"Your balance is **__{bal}__** SusCoins.")

    return economy
