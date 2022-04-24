from __future__ import annotations
import os
import time
from dotenv import load_dotenv
from typing import Optional, TypeVar
from mariadb import connect, connection
from voltage.ext import commands

T = TypeVar('T')

def unwrap(x: Optional[T]) -> T:
    """
    A function inspired by Rust's Option::unwrap.

    If the argument is None, raise a ValueError else, returns the value.
    """
    if x is None:
        raise ValueError("Found None.")
    return x

def get_db() -> connection.Connection:
    """
    A fucntion that establishes a connection to the database.
    rhen returns that connection.
    """
    load_dotenv(".env")
    port = unwrap(os.getenv("DB_PORT"))
    if port.isdigit():
        port = int(port)
    else:
        raise ValueError("DB_PORT is not an integer.")
    conn = connect(
            username=os.getenv("DB_NAME"),
            password=os.getenv("DB_PASS"),
            host=os.getenv("DB_HOST"),
            port=port,
            database=os.getenv("DB_NAME")
    )
    return conn

@commands.check
async def check_account():
    """
    A check that checks if the user has an account and if not creates one for them.
    """
    async def check(ctx) -> bool:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM economy WHERE user_id = ?", (ctx.author.id,))
        if cur.fetchone() is None:
            cur.execute("INSERT INTO economy (user_id) VALUES (?)", (ctx.author.id,))
            cur.execute("INSERT INTO cooldowns (user_id) VALUES (?)", (ctx.author.id,))
            conn.commit()
        cur.close()
        conn.close()
        return True

    return check

@commands.check
async def cooldown(bucket: str, wait_time):
    """
    A simple check that handles cooldowns.
    """
    async def check(ctx):
        conn = get_db()
        cur = conn.cursor()
        wait = await wait_time(ctx) if callable(wait_time) else wait_time
        cur.execute(f"SELECT {bucket} FROM cooldowns WHERE user_id = ?", (ctx.author.id, ))
        last_use = cur.fetchone()[0]
        now = int(time.time())
        if now < last_use + wait:
            remaining = last_use + wait - now
            if remaining > 31536000:
                wait_str = f"{remaining // 31536000} years"
            if remaining > 2629743:
                wait_str = f"{remaining // 2629743} months"
            if remaining > 604800:
                wait_str = f"{remaining // 604800} weeks"
            if remaining > 86400:
                wait_str = f"{remaining // 86400} days"
            elif remaining > 3600:
                wait_str = f"{remaining // 3600} hours"
            elif remaining > 60:
                wait_str = f"{remaining // 60} minutes"
            else:
                wait_str = f"{remaining} seconds"
            await ctx.reply(f"You must wait **{wait_str}** before using this command again.")
            return False
        cur.execute(f"UPDATE cooldowns SET {bucket} = ? WHERE user_id = ?", (now, ctx.author.id))
        conn.commit()
        cur.close()
        conn.close()
        return True

    return check
