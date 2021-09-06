gameAnswers = [

    "classicGameWon": "Good job, you guessed all the letters and the word was:\n`{0}`", #format: word
    "classicLetterGuessed": "Letter **{0}** was guessed:\n`{1}`", #format: letter, word
    "classicLetterNotGuessed": "Incorrect guess **{0}**:\n{1}", #format letter, word
    "classicGameStarting": "Game has started, the word is:\n{0}" #format: word
]

class game:
	@staticmethod
	def getRandomWord(number=1):
		response = requests.get(
			"https://random-word-api.herokuapp.com/word?number="+number)
		text = response.text

		return text[2:-2]  #remove [""]

    @staticmethod
	def revealLetter(word, revealedWord, letter):
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

            #if letter was correctly guessed
			wasLetterGuessed = True
			newRevealed += letter

		return wasLetterGuessed, newRevealed

class classic(game):
	def __init__(self, channel):
		self.channel = channel
		self.word = super().getRandomWord()
		self.revealedWord = "-" * len(self.word)

	async def end(self):
	    await self.channel.send(
	        gameAnswers["classicGameWon"].format(self.word))

    async def makeGuess(self, msg):

        if self._is_whole_word_guessed(msg):
            return self.end()

        if not self._is_message_guess(msg):
            return False, "Message is not guess"

        wasLetterGuessed, newRevealedWord = super().revealLetter(
                                        self.word, self.revealedWord, msg)
        if wasLetterGuessed:
            self.revealedWord = newRevealedWord

            await self.channel.send(
                gameAnswers["classicLetterGuessed"].format(msg, self.revealedWord))
        else:
            await self.channel.send(
                gameAnswers["classicLetterNotGuessed"].format(msg, self.revealedWord))

    @staticmethod
    def _is_message_guess(msg):
        return len(msg) == 1

    def _is_whole_word_guessed(self, msg):
        return msg.lower == self.word
