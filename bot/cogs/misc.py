from time import time

import voltage
from voltage.ext import commands

def setup(client: voltage.Client) -> commands.Cog:
    misc = commands.Cog("Misc", "A collection of miscellaneous commands.")

    @misc.listen("message")
    async def on_message(message: voltage.Message):
        if "/shrug" in message.content:
            await message.channel.send(message.content.replace("/shrug", r"¯\\_(ツ)_/¯"), masquerade=voltage.MessageMasquerade(message.author.display_name, message.author.display_avatar.url))

    @misc.command()
    async def ping(ctx) -> None:
        """Pong!"""
        start = time()
        msg = await ctx.send(f"Pong! :ping_pong:")
        await msg.edit(content=f"Pong! :ping_pong: ({time() - start:2f}s)")

    @misc.command()
    async def test(ctx) -> None:
        """Test command that changes functionality every time I need to test something."""
        await ctx.send(ctx.message.url)

    @misc.command()
    async def purge(ctx, amount: int) -> None:
        """Purge a number of messages from the channel."""
        if not ctx.author.channel_permissions.manage_messages:
            return await ctx.send("You don't have permission to do that.")
        start = time()
        await ctx.channel.purge(amount)
        await ctx.send(f"Purged {amount} messages in {time() - start:2f}s.")


    return misc

