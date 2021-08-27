import tkinter as tk
import random
from PIL import Image, ImageTk

class Deck():

	def __init__(self, x, y, fcx, imagewidth, imageheight):
		self.cards = []			# 全手札
		self.fieldcards = []	# オープンになった手札
		self.opencardscount = 0	# オープンになったばかりのカード枚数
		self.suits = ['diamond', 'club', 'heart', 'spade']
		self.x = x
		self.y = y
		self.fieldcardsX = fcx
		self.imagewidth = imagewidth
		self.imageheight = imageheight

		import card
		for suit in self.suits:
			if suit in ['diamond', 'heart']:
				color = 'red'
			elif suit in ['club', 'spade']:
				color = 'black'
			for num in range(1, 14):
				img=ImageTk.PhotoImage(Image.open('images/' + suit + '/' + str(num) + '.png').convert('RGB').resize(size=(self.imagewidth, self.imageheight)))

				obj = card.Card(
					suit = suit,
					num = num,
					color = color,
					state = 0,
					tags = suit + str(num),
					image = img
				)
				self.cards.append(obj)

	def shuffleCards(self):
		random.shuffle(self.cards)

	def getCards(self):
		return self.cards

	def getFieldCards(self):
		return self.fieldcards

	def addFieldCard(self, card):
		self.fieldcards.append(card)

	def addFieldCards(self, cards):
		for card in cards:
			self.addFieldCard(card)

	def getX(self):
		return self.x

	def getY(self):
		return self.y

	def getFieldcardsX(self):
		return self.fieldcardsX

	def setX(self, x):
		self.x = x

	def setY(self, y):
		self.y = y

	def setFieldcardsX(self, fcx):
		self.fieldcardsX = fcx

	def deleteFieldCards(self, highlighttags):
		dcards = []

		for card in self.fieldcards:
			if card.getTags() not in highlighttags:
				dcards.append(card)
			else:
				self.opencardscount -= 1
				if self.opencardscount < 0:
					self.opencardscount = 0

		self.fieldcards.clear()
		self.addFieldCards(dcards)

	def drawCard(self):
		if len(self.cards) == 0 and len(self.fieldcards) == 0:
			return

		if len(self.cards) == 0:
			self.cards.extend(self.fieldcards)
			self.fieldcards.clear()
			self.opencardscount = 0

		elif len(self.cards) >= 3:
			for i in range(3):
				self.fieldcards.append(self.cards[0])
				self.cards.pop(0)
			self.opencardscount = 3

		else:
			self.opencardscount = len(self.cards)
			for i in range(len(self.cards)):
				self.fieldcards.append(self.cards[0])
				self.cards.pop(0)

	def paint(self, canvas, bgcolor, highlighttags):
		diff = 3
		canvas.create_rectangle(self.x - diff, self.y - diff, self.x + self.imagewidth + diff, self.y + self.imageheight + diff, fill = bgcolor, outline = 'white', width = 2, tags = 'handcards')
		if len(self.cards) > 0:
			canvas.create_rectangle(self.x, self.y, self.x + self.imagewidth, self.y + self.imageheight, fill = 'firebrick', outline = 'black', width = 1, tags = 'handcards')

		cx = self.fieldcardsX
		for i in range(len(self.fieldcards)):
			if self.opencardscount == 0:
				canvas.create_image(cx, self.y, image = self.fieldcards[-1].getImage(), anchor = tk.NW, tags = self.fieldcards[-1].getTags())
				if self.fieldcards[-1].getTags() in highlighttags:
					canvas.create_line(cx, self.y, cx, self.y + self.imageheight, fill = 'cyan', width = 3, tags = self.fieldcards[-1].getTags() + 'line')
					canvas.create_line(cx, self.y, cx + self.imagewidth, self.y, fill = 'cyan', width = 3, tags = self.fieldcards[-1].getTags() + 'line')
					canvas.create_line(cx + self.imagewidth, self.y, cx + self.imagewidth, self.y + self.imageheight, fill = 'cyan', width = 3, tags = self.fieldcards[-1].getTags() + 'line')
					canvas.create_line(cx, self.y + self.imageheight, cx + self.imagewidth, self.y + self.imageheight, fill = 'cyan', width = 3, tags = self.fieldcards[-1].getTags() + 'line')
			elif i < len(self.fieldcards) - self.opencardscount:
				canvas.create_image(cx, self.y, image = self.fieldcards[i].getImage(), anchor = tk.NW)
			else:
				if i > len(self.fieldcards) - self.opencardscount:
					cx += 15
				if i != len(self.fieldcards) - 1:
					canvas.create_image(cx, self.y, image = self.fieldcards[i].getImage(), anchor = tk.NW)
				else:
					canvas.create_image(cx, self.y, image = self.fieldcards[i].getImage(), anchor = tk.NW, tags = self.fieldcards[i].getTags())
					if self.fieldcards[-1].getTags() in highlighttags:
						canvas.create_line(cx, self.y, cx, self.y + self.imageheight, fill = 'cyan', width = 3, tags = self.fieldcards[-1].getTags() + 'line')
						canvas.create_line(cx, self.y, cx + self.imagewidth, self.y, fill = 'cyan', width = 3, tags = self.fieldcards[-1].getTags() + 'line')
						canvas.create_line(cx + self.imagewidth, self.y, cx + self.imagewidth, self.y + self.imageheight, fill = 'cyan', width = 3, tags = self.fieldcards[-1].getTags() + 'line')
						canvas.create_line(cx, self.y + self.imageheight, cx + self.imagewidth, self.y + self.imageheight, fill = 'cyan', width = 3, tags = self.fieldcards[-1].getTags() + 'line')