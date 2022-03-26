from dotenv import load_dotenv
import os
import voltage

from utils import unwrap, Command, CommandContext, Cog, CommandsClient

client = CommandsClient("-")

@client.error('message')
async def on_message_error(error: Exception, message: voltage.Message):
    await message.reply(f"An error has occured: {error}")
    raise error

client.add_extension("cogs.misc")
client.add_extension("cogs.fun")

@client.command()
async def reload(ctx, cog: str):
    if ctx.author.id != client.user.owner_id:
        return await ctx.send("You are not my owner, scram.")
    client.reload_extension(f"cogs.{cog}")
    await ctx.reply("Reloaded")

load_dotenv()
client.run(unwrap(os.getenv('TOKEN')))
