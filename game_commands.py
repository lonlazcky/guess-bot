from discord.ext import commands
import gametypes

class start_commands(commands.Cog):
	GameInProgress = "{0} Wait for the game to finish smh" #format mention

	def __init__(self, bot, games_list):
		self.bot = bot
		self.games = games_list

	async def game_exists(self, ctx):
		channel = ctx.message.channel
		return channel.id in self.games and await channel.send(
			self.GameInProgress.format(ctx.message.author.mention)
		)


	@commands.group(aliases=["s"])
	async def start(self, ctx):
		if ctx.invoked_subcommand:
			return

		await self.start_classic_game(ctx)


	@start.command(name="classic", aliases=["c", "cl", "cls"])
	async def start_classic_game(self, ctx):
		if await self.game_exists(ctx):
			return
		
		channel = ctx.message.channel
		game = gametypes.classic(channel)
		self.games[channel.id] = game
		await channel.send(game.gameAnswers["GameStarting"].format(
    		game.revealedWord))

		print(game.word)


	@start.command(name="hangman", aliases=["h", "hm", "hang"])
	async def start_hangman_game(self, ctx, lives=8):
		if await self.game_exists(ctx):
			return
		
		channel = ctx.message.channel
		game = gametypes.hangman(channel, ctx.message.author, lives)
		self.games[channel.id] = game
		await channel.send(game.gameAnswers["GameStarting"].format(
    		game.revealedWord, str(game.lives)
		))

