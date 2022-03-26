from dotenv import load_dotenv
import os
import voltage

from utils import unwrap, Command, CommandContext, Cog, CommandsClient

client = CommandsClient("-")

@client.error('message')
async def on_message_error(error: Exception, message: voltage.Message):
    await message.reply(f"An error has occured: {error}")

client.add_extension("cogs.misc")

@client.command()
async def reload(ctx):
    client.reload_extension("cogs.misc")
    await ctx.reply("Reloaded")

load_dotenv()
client.run(unwrap(os.getenv('TOKEN')))
