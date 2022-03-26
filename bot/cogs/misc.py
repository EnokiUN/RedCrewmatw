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

    @misc.command()
    async def imposter(ctx, member: voltage.Member, *, content = None):
        """Impostor command.

        This command is used to impersonate a user.
        """
        if member is None:
            return await ctx.send("couldn't find that user")
        if content is None:
            return await ctx.send("You need to provide a message to send.")
        await ctx.send(content, masquerade = voltage.MessageMasquerade(name = member.display_name, avatar = member.display_avatar.url))

    return misc

