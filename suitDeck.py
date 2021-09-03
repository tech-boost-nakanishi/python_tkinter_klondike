import tkinter as tk

class SuitDeck():

	def __init__(self, x, y, index):
		self.cards = []
		self.x = x
		self.y = y
		self.index = index
		self.padding = 8

	def getX(self):
		return self.x

	def getY(self):
		return self.y

	def getPadding(self):
		return self.padding

	def addCard(self, card):
		self.cards.append(card)

	def addCards(self, cards):
		for card in cards:
			self.addCard(card)

	def getCards(self):
		return self.cards

	def deleteCards(self, highlighttags):
		dcards = []

		for card in self.cards:
			if card.getTags() not in highlighttags:
				dcards.append(card)

		self.cards.clear()
		self.addCards(dcards)

	def paint(self, canvas, highlighttags, imagewidth, imageheight, bgcolor):
		# スーツデッキの白枠表示
		canvas.create_rectangle(self.x - self.padding, self.y - self.padding, self.x + imagewidth + self.padding, self.y + imageheight + self.padding, outline = 'white', fill = bgcolor, width = 2, tags = 'suit' + str(self.index))

		# カードの表示
		if len(self.cards) > 0:
			canvas.create_image(self.x, self.y, image = self.cards[-1].getImage(), anchor = tk.NW, tags = self.cards[-1].getTags())

			if self.cards[-1].getTags() in highlighttags:
				canvas.create_line(self.x, self.y, self.x, self.y + imageheight, fill = 'cyan', width = 3, tags = self.cards[-1].getTags() + 'line')
				canvas.create_line(self.x, self.y, self.x + imagewidth, self.y, fill = 'cyan', width = 3, tags = self.cards[-1].getTags() + 'line')
				canvas.create_line(self.x + imagewidth, self.y, self.x + imagewidth, self.y + imageheight, fill = 'cyan', width = 3, tags = self.cards[-1].getTags() + 'line')
				canvas.create_line(self.x, self.y + imageheight, self.x + imagewidth, self.y + imageheight, fill = 'cyan', width = 3, tags = self.cards[-1].getTags() + 'line')