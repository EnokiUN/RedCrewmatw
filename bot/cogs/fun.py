import PIL # type: ignore
from PIL import Image, ImageOps
from io import BytesIO
import random
import asyncio

import voltage
from voltage.file import get_file_from_url
from utils import Cog

def setup(client) -> Cog:

    fun = Cog("Fun", "Some commands that you can use to mess around with people.")

    @fun.command()
    async def imposter(ctx, member: voltage.Member, *, content = None):
        """Impersonate a user."""
        if content is None:
            return await ctx.send("You need to provide a message to send.")
        await ctx.send(content, masquerade = voltage.MessageMasquerade(name = member.display_name, avatar = member.display_avatar.url))

    @fun.command()
    async def sus(ctx, member: voltage.Member):
        """Make a user sus."""
        base = Image.open("assets/sus.jpg")
        pfp = Image.open(BytesIO(await member.display_avatar.get_binary())).resize((175, 175))
        base.paste(pfp, (115, 90))
        with BytesIO() as data:
            base.save(data, "PNG")
            data.seek(0)
            return await ctx.reply("sus", attachment=voltage.File(data.read(), filename="sus.png"))

    @fun.command()
    async def arch(ctx, member: voltage.Member):
        """Arch my beloved."""
        mask = Image.open("assets/arch.png").convert("L")
        pfp = Image.open(BytesIO(await member.display_avatar.get_binary())).convert("RGBA")
        
        output = ImageOps.fit(pfp, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)

        with BytesIO() as data:
            output.save(data, "PNG")
            data.seek(0)
            return await ctx.reply("arch", attachment=voltage.File(data.read(), filename="arch.png"))

    @fun.command()
    async def gentoo(ctx, member: voltage.Member):
        """Gentoo also my beloved."""
        mask = Image.open("assets/gentoo.png").convert("L")
        pfp = Image.open(BytesIO(await member.display_avatar.get_binary())).convert("RGBA")
        
        output = ImageOps.fit(pfp, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)

        with BytesIO() as data:
            output.save(data, "PNG")
            data.seek(0)
            return await ctx.reply("gentoo", attachment=voltage.File(data.read(), filename="gentoo.png"))

    @fun.command()
    async def debian(ctx, member: voltage.Member):
        """Debian more like decent amirite?"""
        mask = Image.open("assets/debian.png").convert("L")
        pfp = Image.open(BytesIO(await member.display_avatar.get_binary())).convert("RGBA")
        
        output = ImageOps.fit(pfp, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)

        with BytesIO() as data:
            output.save(data, "PNG")
            data.seek(0)
            return await ctx.reply("debian", attachment=voltage.File(data.read(), filename="debian.png"))

    @fun.command()
    async def windows(ctx, member: voltage.Member):
        """CringeOS"""
        mask = Image.open("assets/windows.png").convert("L")
        pfp = Image.open(BytesIO(await member.display_avatar.get_binary())).convert("RGBA")
        
        output = ImageOps.fit(pfp, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)

        with BytesIO() as data:
            output.save(data, "PNG")
            data.seek(0)
            return await ctx.reply("windows", attachment=voltage.File(data.read(), filename="windows.png"))

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

    @fun.command()
    async def fight(ctx, member: voltage.Member):
        """Fight someone."""
        msg = await ctx.reply(f"{ctx.author.display_name} is fighting {member.display_name}")
        await asyncio.sleep(3)
        await msg.edit("3")
        await asyncio.sleep(1)
        await msg.edit("2")
        await asyncio.sleep(1)
        await msg.edit("1")
        await asyncio.sleep(1)
        await msg.edit("FIGHT")
        await asyncio.sleep(1)
        hp1 = hp2 = 100
        while hp1 > 0 and hp2 > 0:
            dmg = random.randint(0, 10)
            hp1 = max(hp1 - dmg, 0)
            await msg.edit(f"{member.display_name} hit {ctx.author.display_name} for {dmg} damage. {ctx.author.display_name} has {hp1} HP left.")
            if hp1 <= 0:
                break
            await asyncio.sleep(1)
            dmg = random.randint(0, 10)
            hp2 = max(hp2-dmg, 0)
            await msg.edit(f"{ctx.author.display_name} hit {member.display_name} for {dmg} damage. {member.display_name} has {hp2} HP left.")
            if hp2 <= 0:
                break
            await asyncio.sleep(1)
        if hp1 > 0:
            await ctx.send(f"{ctx.author.display_name} won!")
        else:
            await ctx.send(f"{member.display_name} won!")

    return fun
