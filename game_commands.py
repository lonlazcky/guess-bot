from discord.ext import commands
import gametypes

class start_commands(commands.Cog):

	def __init__(self, bot, games_list):
		self.bot = bot
		self.games = games_list

	@commands.group(aliases=["s"])
	async def start(self, ctx):
		if ctx.invoked_subcommand:
				return

		await self.start_classic_game(ctx)

	@start.command(name="classic", aliases=["c", "cl", "cls"])
	async def start_classic_game(self, ctx):
		channel = ctx.message.channel

		if channel.id in self.games:
			return await channel.send(gametypes.gameAnswers["GameInProgress"].format(ctx.message.author.mention))

		self.games[channel.id] = gametypes.classic(channel)
		await channel.send(gametypes.gameAnswers["classicGameStarting"].format(
    		self.games[channel.id].revealedWord))

		print(self.games[channel.id].word)

