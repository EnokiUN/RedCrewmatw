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
async def add(ctx: CommandContext, a: int, b: int = 10):
    await ctx.reply(a+b)

@client.command()
async def echo(ctx: CommandContext, *, args: str = "supply something u idot"):
    await ctx.reply(args)

load_dotenv()
client.run(unwrap(os.getenv('TOKEN')))
