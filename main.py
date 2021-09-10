import discord
from discord.ext import commands

from keepalive import keep_alive
from game_commands import start_commands
import os


client = discord.Client()
bot = commands.Bot(command_prefix="gb!")

games = {}

bot.add_cog(start_commands(bot, games))

@bot.command()
async def info(ctx):

	infoMessage = "This (a bit less) spaghetti nab of a bot was made by `lasadrinx#2517`,\n it's made with discord.py and hosted on replit.com"

	await ctx.send(infoMessage)

@bot.command()
async def updates(ctx):

	updateHeader = "guess bot updates:\n"
	updateMessage = "-Guessing the word in full will now win you the game\n-Capital letters will now also work"
	await ctx.send(updateHeader + updateMessage)

@bot.event
async def on_ready():
	print("readdy")

@bot.event
async def on_message(message):
	await bot.process_commands(message)

	if message.author.bot:
		return 

	channel = message.channel
	if not channel.id in games:
	    return

	if await games[channel.id].handle_message(message) == "end":
		del games[channel.id]
		
if __name__ == "__main__":
	keep_alive()
	bot.run(os.environ["token"])
