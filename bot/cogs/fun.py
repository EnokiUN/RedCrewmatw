import PIL # type: ignore
from PIL import Image
from io import BytesIO
import random

import voltage
from voltage.file import get_file_from_url
from utils import Cog

def setup(client) -> Cog:

    fun = Cog("Fun", "Some commands that you can use to mess around with people.")

    @fun.command()
    async def imposter(ctx, member: voltage.Member, *, content = None):
        """Impersonate a user."""
        if member is None:
            return await ctx.send("couldn't find that user")
        if content is None:
            return await ctx.send("You need to provide a message to send.")
        await ctx.send(content, masquerade = voltage.MessageMasquerade(name = member.display_name, avatar = member.display_avatar.url))

    @fun.command()
    async def sus(ctx, member: voltage.Member):
        if member is None:
            return await ctx.send("couldn't find that user")
        base = Image.open("assets/sus.jpg")
        pfp = Image.open(BytesIO(await member.display_avatar.get_binary())).resize((175, 175))
        base.paste(pfp, (115, 90))
        with BytesIO() as data:
            base.save(data, "PNG")
            data.seek(0)
            return await ctx.reply("sus", attachment=voltage.File(data.read(), filename="sus.png"))

    @fun.command()
    async def sex(ctx):
        """Sex command :lenny:"""
        file = await get_file_from_url(client.http, "https://autumn.revolt.chat/attachments/rRBCDm2VSn8UJKLuxtEcVa9ZE2uStNp7hXgCR8Idw5/h.mp4")
        await ctx.reply("Here :lenny:", attachment=file)

    @fun.command()
    async def howsus(ctx, member: voltage.Member = None):
        """Show's how sus a person is."""
        if member is None:
            member = ctx.author
        await ctx.reply(f"{member.display_name} is **{random.randint(0, 100)}%** sus :amogus:")

    return fun
