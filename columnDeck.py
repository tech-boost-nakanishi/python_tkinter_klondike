import tkinter as tk

class ColumnDeck():

	def __init__(self, x, y, index):
		self.cards = []
		self.x = x
		self.y = y
		self.index = index

	def getX(self):
		return self.x

	def getY(self):
		return self.y

	def getCards(self):
		return self.cards

	def addCard(self, card):
		self.cards.append(card)

	def addCards(self, cards):
		for card in cards:
			self.addCard(card)

	def deleteCards(self, highlighttags):
		dcards = []

		for card in self.cards:
			if card.getTags() not in highlighttags:
				dcards.append(card)

		self.cards.clear()
		self.addCards(dcards)

	def setFrontTopCard(self):
		if len(self.cards) > 0:
			self.cards[-1].setState(1)

	def paint(self, canvas, highlighttags, imagewidth, imageheight, bgcolor):
		self.setFrontTopCard()

		canvas.create_rectangle(self.x, self.y, self.x + imagewidth, self.y + imageheight, fill = bgcolor, width = 0, tags = 'column' + str(self.index))

		cy = self.y
		for i in range(len(self.cards)):
			if i > 0:
				if self.cards[i - 1].getState() == 0:
					cy += 5

				elif self.cards[i - 1].getState() == 1:
					cy += 15

			if self.cards[i].getState() == 0:
				canvas.create_rectangle(self.x, cy, self.x + imagewidth, cy + imageheight, fill = 'firebrick', outline = 'black', width = 1)

			elif self.cards[i].getState() == 1:
				canvas.create_image(self.x, cy, image = self.cards[i].getImage(), anchor = tk.NW, tags = self.cards[i].getTags())

				if self.cards[i].getTags() in highlighttags:
					canvas.create_line(self.x, cy, self.x, cy + imageheight, fill = 'cyan', width = 3, tags = self.cards[i].getTags() + 'line')
					canvas.create_line(self.x, cy, self.x + imagewidth, cy, fill = 'cyan', width = 3, tags = self.cards[i].getTags() + 'line')
					canvas.create_line(self.x + imagewidth, cy, self.x + imagewidth, cy + imageheight, fill = 'cyan', width = 3, tags = self.cards[i].getTags() + 'line')
					canvas.create_line(self.x, cy + imageheight, self.x + imagewidth, cy + imageheight, fill = 'cyan', width = 3, tags = self.cards[i].getTags() + 'line')