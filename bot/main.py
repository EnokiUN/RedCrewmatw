from dotenv import load_dotenv
import os
import voltage

from utils import unwrap, Command, CommandContext, Cog, CommandsClient

client = CommandsClient("-")

@client.error('message')
async def on_message_error(error: Exception, message: voltage.Message):
    await message.reply(f"An error has occured: {error}")

@client.command()
async def ping(ctx: CommandContext):
    await ctx.send("Pong!")

@client.command()
async def add(ctx: CommandContext, a: int, b: int):
    await ctx.send(str(a + b))

load_dotenv()
client.run(unwrap(os.getenv('TOKEN')))
