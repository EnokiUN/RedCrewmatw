from dotenv import load_dotenv
import os
import json
import mariadb

import voltage
from voltage.ext import commands

from utils import unwrap

async def get_prefix(message, client):
    if message.server is None:
        return ['-', client.user.mention+' ', client.user.mention]
    try:
        with open ("prefixes.json", "r") as f:
            prefixes = json.load(f)
        return [prefixes.get(str(message.server.id), "-"), client.user.mention+' ', client.user.mention]
    except:
        return ['-', client.user.mention+' ', client.user.mention]

client = commands.CommandsClient(get_prefix)

@client.error('message')
async def on_message_error(error: Exception, message: voltage.Message):
    if isinstance(error, voltage.CommandNotFound):
        return
    await message.reply(f"An error has occured: {error}")

client.add_extension("cogs.misc")
client.add_extension("cogs.fun")
client.add_extension("cogs.economy")

@client.command()
async def prefix(ctx: commands.CommandContext, prefix):
    """Set the prefix for this server"""
    if ctx.server is None or isinstance(ctx.author, voltage.User):
        return await ctx.reply("Custom prefixes are only available in servers.")
    if not ctx.author.permissions.kick_members:
        return await ctx.reply("You don't have permission to change the prefix")
    with open ("prefixes.json", "r") as f:
        prefixes = json.load(f)
    prefixes[str(ctx.server.id)] = prefix
    with open ("prefixes.json", "w") as f:
        json.dump(prefixes, f)
    await ctx.reply(f"Prefix changed to `{prefix}`")

@client.command()
async def load(ctx, cog: str):
    """Load a cog"""
    if ctx.author.id != client.user.owner_id:
        return await ctx.send("You are not my owner, you do not own me, you cannot tell me what to do.\nNow shoo.")
    client.add_extension(f"cogs.{cog}")
    await ctx.reply(f"Cog `{cog}` loaded")

@client.command()
async def reload(ctx, cog: str):
    """Reload a cog"""
    if ctx.author.id != client.user.owner_id:
        return await ctx.send("You are not my owner, scram.")
    client.reload_extension(f"cogs.{cog}")
    await ctx.reply(f"Cog `{cog}` reloaded")

@client.command()
async def unload(ctx, cog: str):
    """Unload a cog"""
    if ctx.author.id != client.user.owner_id:
        return await ctx.send("You are not my owner, there's honestly nothing wrong with that but I won't let you do \
                that because you don't have a phd in being retarded.")
    client.remove_extension(f"cogs.{cog}")
    await ctx.reply(f"Cog `{cog}` unloaded")

load_dotenv()
client.run(unwrap(os.getenv('TOKEN')))
