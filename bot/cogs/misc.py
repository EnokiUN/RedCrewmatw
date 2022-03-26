from time import time

import voltage
from utils import Cog

def setup(client: voltage.Client) -> Cog:
    misc = Cog("Misc", "A collection of miscellaneous commands.")

    @misc.command()
    async def ping(ctx) -> None:
        """Pong!"""
        start = time()
        msg = await ctx.send(f"Pong! :ping_pong:")
        await msg.edit(content=f"Pong! :ping_pong: ({time() - start:2f}s)")

    return misc

