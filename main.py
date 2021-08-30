import discord
from discord.ext import commands
from keepalive import keep_alive
import os
import requests

client = discord.Client()
bot = commands.Bot(command_prefix="-guess ")

games = {}

class game:
	def __init__(self, channel):
		self.channel = channel
		self.word = self.getRandomWord()
		self.revealedWord = "_" * len(self.word)
		print(self.word)
	
	@staticmethod
	def getRandomWord():
		response = requests.get(
			"https://random-word-api.herokuapp.com/word?number=1")
		text = response.text

		return text[2:-2]  #remove [""]
	
	def revealLetter(self, letter):
		word = self.word
		revealedWord = self.revealedWord
		newRevealed = ""
		wasLetterGuessed = False
		
		letter = letter.lower()

		for i in range(0, len(word)):
			wordLetter = word[i]
			revealedWordLetter = revealedWord[i]

			if wordLetter != letter:
				newRevealed += revealedWordLetter
				continue
			if wordLetter == revealedWordLetter:
				newRevealed += revealedWordLetter
				continue
			
			wasLetterGuessed = True
			newRevealed += letter

		self.revealedWord = newRevealed
		return wasLetterGuessed, newRevealed	

	def checkForWin(self):
		return self.word == self.revealedWord
	
	def win(self, message):
		del games[message.channel.id]

		return responses["WordGuessed"].format(
			message.author.mention, self.word)


responses = {

	"StartingGame": "ok ur game has started, the word is: \n`{0}`",

	"GameAlreadyStarted": "Wait for the game to finish nab",
	
	"WordGuessed": "Great job {0} you guessed the word: \n `{1}`", #format: name, word

	"LetterGuessed": "Correct guess **{0}**:\n `{1}`", #format: letter, word

	"LetterNotGuessed": "Incorrect guess **{0}**:\n `{1}`", #format: letter, word
}

@bot.command()
async def start(ctx): 
	channel = ctx.message.channel
	
	if channel.id in games:
		await channel.send(responses["GameAlreadyStarted"])
		return
	
	games[channel.id] = game(channel)
	await channel.send(responses["StartingGame"].format(
		games[channel.id].revealedWord))

@bot.command()
async def info(ctx):
	
	infoMessage = "This (a bit less) spaghetti nab of a bot was made by `lasadrinx:2517`,\n it's made with discord.py and hosted on replit.com"

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

	if message.author == client:
		return
	
	channel = message.channel
	msg = message.content

	if channel.id not in games:
		return
	game = games[channel.id]
	
	if msg.lower() == game.word:
		await channel.send(game.win(message))
		return
	if len(msg) != 1:
		return

	wasLetterCorrect, revealedWord = game.revealLetter(msg)
	
	if game.checkForWin():
		await channel.send(game.win(message))
		return

	if wasLetterCorrect:
		await channel.send(responses["LetterGuessed"].format(msg, revealedWord))
		return

	await channel.send(responses["LetterNotGuessed"].format(msg, revealedWord))
	
keep_alive()
bot.run(os.environ["TOKEN"])
