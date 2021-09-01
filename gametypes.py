class game:
	@staticmethod
	def getRandomWord(number=1):
		response = requests.get(
			"https://random-word-api.herokuapp.com/word?number="+number)
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

class classic(game):
	def __init__(self, channel):
		self.channel = channel
		self.word = super().getRandomWord()
		self.revealedWord = "-" * len(self.word)
