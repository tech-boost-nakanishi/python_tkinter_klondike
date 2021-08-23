import tkinter as tk
import random
from PIL import Image, ImageTk

class Deck():

	def __init__(self, imagewidth, imageheight):
		self.cards = []
		self.suits = ['diamond', 'club', 'heart', 'spade']
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