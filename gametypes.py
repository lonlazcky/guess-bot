import requests

class game:
	@staticmethod
	def getRandomWord(number=1):
		response = requests.get(
			"https://random-word-api.herokuapp.com/word?number="+ str(number))
		text = response.text

		return text[2:-2]  #remove [""]


	@staticmethod
	def revealLetter(letter, word, revealedWord):
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

		return wasLetterGuessed, newRevealed


	@staticmethod
	def _is_message_guess(msg):
		return len(msg) == 1


	@staticmethod
	def _is_whole_word_guessed(msg, word, revealedWord):
		return msg.lower() == word or revealedWord == word


	def _makeGuess(self, guess, word, revealed_word):
		"""returns True if guess is correct, False if its not
			also returns all if whole word is guesed
			revealed word is its second return value"""

		if self._is_whole_word_guessed(guess, word, revealed_word):
			return "ALL", word
		if not self._is_message_guess(guess):
			return None, revealed_word
		return self.revealLetter(guess, word, revealed_word)


class classic(game):
	gameAnswers = {
		"GameWon": "Good job, you guessed all the letters and the word was:\n`{0}`", #format: word
		"LetterGuessed": "Letter **{0}** was guessed:\n`{1}`", #format: letter, word
		"LetterNotGuessed": "Incorrect guess **{0}**:\n`{1}`", #format letter, word
		"GameStarting": "The game has started and your word is:\n`{0}`" #format: word
    }

	def __init__(self, channel):
		self.channel = channel
		self.word = self.getRandomWord()
		self.revealedWord = "-" * len(self.word)


	async def end(self):
		await self.channel.send(
			self.gameAnswers["GameWon"].format(self.word))
		return "END"

	
	def makeGuess(self, msg):
		return self._makeGuess(msg, self.word, self.revealedWord)
	

	async def send_message(self, msg):
		await self.channel.send(msg)
	

	async def handle_message(self, message):
		msg = message.content
		msg_to_send = None
		guess, newRevealed = self.makeGuess(msg)

		self.revealedWord = newRevealed
		if guess is not None:
			if guess:
				msg_to_send = self.gameAnswers["LetterGuessed"].format(msg, self.revealedWord)
			else:
				msg_to_send = self.gameAnswers["LetterNotGuessed"].format(msg, self.revealedWord)
			
		if guess == "ALL" or self._is_whole_word_guessed(msg, self.word, self.revealedWord):
			return await self.end()

		return msg_to_send

	

class hangman(classic):
	gameAnswers = {
		"GameWon": "Good job {0}, you guessed all the letters in the word:\n`{1}`.\nyou had **{2}** lives left", 
		"LetterGuessed": "Letter **{0}** was guessed:\n`{1}`\nyou have **{2}** lives left",
		"LetterNotGuessed": "Incorrect guess **{0}**:\n`{1}`\nyou have **{2}** lives left",
		"GameStarting": "The game has started and your word is:\n`{0}`\nyou have {1} lives",
		"GameLost": "{0} you lost! the word was:\n`{1}`"
	}

	def __init__(self, channel, user, lives=8):
		super().__init__(channel)
		self.lives = lives
		self.user = user
	

	async def end(self):
		msg_to_send = None

		if not self.lives:
			msg_to_send = self.gameAnswers["GameLost"].format(
				self.user.mention, self.word
			)
		else:
			msg_to_send = self.gameAnswers["GameWon"].format(
				self.user.mention, self.word, self.lives
			)

		await self.channel.send(msg_to_send)
		return "END"


	def makeGuess(self, msg):
		guess, revealed_word = self._makeGuess(msg, self.word, self.revealedWord)
		self.lives -= guess is not None and not guess
		return guess, revealed_word
	

	#i literally just copy pasted this from classic
	#because of the different formatting :/
	async def handle_message(self, message):
		if message.author != self.user:
			return
		
		msg = message.content
		msg_to_send = None
		guess, newRevealed = self.makeGuess(msg)

		self.revealedWord = newRevealed
		if guess is not None:
			if guess:
				msg_to_send = self.gameAnswers["LetterGuessed"].format(
					msg, self.revealedWord, str(self.lives)
					)
			else:
				msg_to_send = self.gameAnswers["LetterNotGuessed"].format(
					msg, self.revealedWord, str(self.lives)
				)
			
		if guess == "ALL" or self._is_whole_word_guessed(msg, self.word, self.revealedWord) or not self.lives:
			return await self.end()

		return msg_to_send

