from dotenv import load_dotenv
import os
import voltage
import json

from utils import unwrap, Command, CommandContext, Cog, CommandsClient, CommandNotFound

async def prefix(messsage):
    with open ("prefixes.json", "r") as f:
        prefixes = json.load(f)
    return prefixes.get(str(messsage.server.id), "-")

client = CommandsClient(prefix)

@client.error('message')
async def on_message_error(error: Exception, message: voltage.Message):
    if isinstance(error, CommandNotFound):
        return
    await message.reply(f"An error has occured: {error}")

client.add_extension("cogs.misc")
client.add_extension("cogs.fun")

@client.command()
async def prefix(ctx, prefix):
    perms = 0
    for i in ctx.author.roles:
        perms |= i.permissions.flags
    perms = voltage.ServerPermissions.new_with_flags(perms)
    if not perms.kick_members:
        return await ctx.reply("You don't have permission to change the prefix")
    with open ("prefixes.json", "r") as f:
        prefixes = json.load(f)
    prefixes[str(ctx.server.id)] = prefix
    with open ("prefixes.json", "w") as f:
        json.dump(prefixes, f)
    await ctx.reply(f"Prefix changed to `{prefix}`")

@client.command()
async def reload(ctx, cog: str):
    if ctx.author.id != client.user.owner_id:
        return await ctx.send("You are not my owner, scram.")
    client.reload_extension(f"cogs.{cog}")
    await ctx.reply("Reloaded")

load_dotenv()
client.run(unwrap(os.getenv('TOKEN')))
