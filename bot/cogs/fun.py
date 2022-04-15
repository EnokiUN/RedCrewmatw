from typing import Optional
import PIL # type: ignore
from PIL import Image, ImageOps
from io import BytesIO
import random
import asyncio
import math

import voltage
from voltage.file import get_file_from_url
from voltage.ext import commands

class TickTackToeGame:
    """A simple class which represents and handles a game of tick tack toe"""
    def __init__(self, player1: voltage.Member, player2: voltage.Member):
        self.player = player1
        self.players = [player1, player2]
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.turn = 0
        self.winner = None
        self.draw = False

    def render_board(self):
        """Renders the board as a string"""
        board = str()
        symbols = ["$\\textcolor{red}{\\textsf{X}}$", "$\\textcolor{yellow}{\\textsf{O}}$"]
        for i, row in enumerate(self.board):
            board += "|"
            if i == 1:
                board += "---|---|---|\n"
            for j, cell in enumerate(row):
                if cell == 1:
                    symbol = symbols[0]
                elif cell == -1:
                    symbol = symbols[1]
                else:
                    symbol = str(i*3+j+1)
                board += f" {symbol} |"
            board += "\n"
        return board

    def check_winner(self):
        for i in self.board:
            if i[0] == i[1] == i[2] != 0:
                self.winner = self.player
                return True
        for i in range(3):
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != 0:
                self.winner = self.player
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != 0:
            self.winner = self.player
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != 0:
            self.winner = self.player
            return True
        if 0 not in self.board[0] and 0 not in self.board[1] and 0 not in self.board[2]:
            self.draw = True
            return True
        return False

    def make_move(self, place: int):
        """Makes a move on the board"""
        x, y = math.ceil(place/3), (place-1)%3
        x -= 1
        self.board[x][y] = 1 if self.turn%2 == 0 else -1
        self.turn += 1
        self.player = self.players[self.turn%2]

    def __str__(self):
        return f"{self.player}'s turn\n{self.render_board()}"

    @property
    def available(self):
        """Returns a list of available moves"""
        available = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    available.append(i*3+j+1)
        return available

    @property
    def is_over(self):
        """Returns whether the game is over"""
        self.check_winner()
        return self.winner is not None or self.draw

def setup(client) -> commands.Cog:

    fun = commands.Cog("Fun", "Some commands that you can use to mess around with people.")

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

    @fun.command()
    async def tto(ctx, member: voltage.Member):
        """Face someone in the ultimate game of skill, Tic-Tac-Toe."""
        msg = await ctx.send(f"{ctx.author.display_name} challenged {member.display_name} to an epic game of Tic-Tac-Toe")
        game = TickTackToeGame(ctx.author, member)
        while not game.is_over:
            await asyncio.sleep(1)
            await msg.edit(game)
            try:
                place = int((await client.wait_for("message", timeout=60, check=lambda m: m.author == game.player and m.channel == ctx.channel and m.content in ''.join([str(i) for i in game.available]))).content)
            except asyncio.TimeoutError:
                await ctx.send(f"{ctx.author.display_name} forfeited!")
                break
            game.make_move(place)
        await msg.edit(game)
        if game.draw:
            await ctx.send(f"{ctx.author.display_name} and {member.display_name} tied!")
        elif game.winner == ctx.author:
            await ctx.send(f"{ctx.author.display_name} won!")
        else:
            await ctx.send(f"{member.display_name} won!")

    return fun
