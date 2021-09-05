gameAnswers = [

    "classicGameWon": "Good job, you guessed all the letters and the word was:\n`{0}`" #format: word

]

class game:
	@staticmethod
	def getRandomWord(number=1):
		response = requests.get(
			"https://random-word-api.herokuapp.com/word?number="+number)
		text = response.text

		return text[2:-2]  #remove [""]

	def revealLetter(word, word_guessed_so_far, letter):
		revealedWord = word_guessed_so_far
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

    async def makeGuess(letter):
        wasLetterGuessed, newRevealedWord = super().revealLetter(
                                        self.word, self.revealedWord, letter)
        if wasLetterGuessed:
            self.revealedWord = newRevealedWord
            await self.channel.send(
                gameAnswers["classicLetterGuessed"].format())

    def _is_message_guess():
        pass
