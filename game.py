import tkinter as tk
from decimal import Decimal, ROUND_HALF_UP
from tkinter import messagebox
import threading
import time
import warnings
warnings.simplefilter('ignore')

class Game(tk.Frame):
	def __init__(self, master):
		self.WIDTH = 800
		self.HEIGHT = 560
		self.bgcolor = 'forestgreen'
		tk.Frame.__init__(self, master, width = self.WIDTH, height = self.HEIGHT)
		self.pack()
		self.pack_propagate(0)

		self.reduction_ratio = 9  #縮小率
		self.imagewidth = int(Decimal(str(712 / self.reduction_ratio)).quantize(Decimal('0'), rounding=ROUND_HALF_UP))
		self.imageheight = int(Decimal(str(1008 / self.reduction_ratio)).quantize(Decimal('0'), rounding=ROUND_HALF_UP))

		self.highlighttags = []	# 選択中のタグを格納
		self.tempcards = []		# 選択中のカードを格納
		self.isCardMove = False
		self.isDoubleClicked = False

		# 52枚のカードを生成
		import deck
		self.deckobj = deck.Deck(0, 0, 0, self.imagewidth, self.imageheight)
		self.deckobj.shuffleCards()

		# カラムデッキのインスタンス生成
		import columnDeck
		self.columndecks = []
		for i in range(7):
			obj = columnDeck.ColumnDeck(i * self.imagewidth + (i + 1) * 30, self.imageheight * 1.5, i)
			self.columndecks.append(obj)
			for j in range(i + 1):
				self.columndecks[i].addCard(self.deckobj.getCards()[0])
				self.deckobj.getCards().pop(0)

		# デッキクラスのx,y,fcx変更
		self.deckobj.setX(self.columndecks[0].getX())
		self.deckobj.setY(30)
		self.deckobj.setFieldcardsX(self.columndecks[1].getX())

		# スーツデッキのインスタンス生成
		import suitDeck
		self.suitdecks = []
		i = 3
		for j in range(4):
			obj = suitDeck.SuitDeck(self.columndecks[i].getX(), 30, j)
			self.suitdecks.append(obj)
			i += 1

		self.BLANK = 0
		self.COLUMNDECK = 1
		self.SUITDECK = 2
		self.HANDDECK = 3
		self.pressdeck = self.BLANK
		self.pressindex = -1

		self.canvas = tk.Canvas(self, width = self.WIDTH, height = self.HEIGHT, bg = self.bgcolor, bd = 0, highlightthickness = 0)
		self.canvas.pack()

		self.paint()

	def mousePressed(self, event):
		tag = event.widget.gettags('current')[0]

		if tag in ['restart', 'restartarrow', 'restartoval']:
			self.destroy()
			game = Game(master = root)
			return

		if tag == 'handcards':
			self.highlighttags = self.tempcards = []
			self.isCardMove = self.isDoubleClicked = False
			self.deckobj.drawCard()
			self.repaint()
			return

		if len(self.tempcards) == 0:
			# 1回目の選択
			self.tempcards, self.pressindex, self.pressdeck = self.getCardsInfosWithTags(tag)
			for card in self.tempcards:
				self.highlighttags.append(card.getTags())

		else:
			# 2回目の選択
			tempcards, pressindex, pressdeck = self.getCardsInfosWithTags(tag)
			if pressdeck == self.COLUMNDECK:
				if self.tempcards[0].getColor() != tempcards[-1].getColor() and self.tempcards[0].getNum() + 1 == tempcards[-1].getNum():
					self.isCardMove = True
					self.startCardAnimThread(tag, tempcards, pressindex, pressdeck, self.canvas.coords(self.highlighttags[0]))
				else:
					self.highlighttags = self.tempcards = []
					self.tempcards, self.pressindex, self.pressdeck = self.getCardsInfosWithTags(tag)
					for card in self.tempcards:
						self.highlighttags.append(card.getTags())

			elif pressdeck == self.SUITDECK:
				if len(self.tempcards) == 1 and len(tempcards) == 1:
					if self.tempcards[0].getSuit() == tempcards[0].getSuit() and self.tempcards[0].getNum() == tempcards[0].getNum() + 1:
						self.isCardMove = True
						self.startCardAnimThread(tag, tempcards, pressindex, pressdeck, self.canvas.coords(self.highlighttags[0]))
					else:
						self.highlighttags = self.tempcards = []
						self.tempcards, self.pressindex, self.pressdeck = self.getCardsInfosWithTags(tag)
						for card in self.tempcards:
							self.highlighttags.append(card.getTags())

			elif pressdeck == self.BLANK and 'suit' in tag:
				if len(self.tempcards) == 1:
					if self.tempcards[0].getNum() == 1:
						index = int(tag.replace('suit', ''))
						self.isCardMove = True
						self.startCardAnimThread(tag, tempcards, index, pressdeck, self.canvas.coords(self.highlighttags[0]))

			elif pressdeck == self.BLANK and 'column' in tag:
				index = int(tag.replace('column', ''))
				if self.tempcards[0].getNum() == 13:
					self.isCardMove = True
					self.startCardAnimThread(tag, tempcards, index, pressdeck, self.canvas.coords(self.highlighttags[0]))

			elif pressdeck == self.HANDDECK:
				self.highlighttags = self.tempcards = []
				self.tempcards, self.pressindex, self.pressdeck = self.getCardsInfosWithTags(tag)
				for card in self.tempcards:
					self.highlighttags.append(card.getTags())

		self.repaint()

	def doubleClicked(self, event):
		self.isDoubleClicked = True
		tag = event.widget.gettags('current')[0]

		self.tempcards, self.pressindex, self.pressdeck = self.getCardsInfosWithTags(tag)
		for card in self.tempcards:
			self.highlighttags.append(card.getTags())

		if len(self.tempcards) == 0:
			return

		if self.tempcards[0].getNum() == 1:
			for index in range(len(self.suitdecks)):
				if len(self.suitdecks[index].getCards()) == 0:
					break
			if index < len(self.suitdecks):
				self.isCardMove = True
				self.startCardAnimThread(tag, self.tempcards, index, self.pressdeck, self.canvas.coords(self.highlighttags[0]))
		else:
			for index in range(len(self.suitdecks)):
				if len(self.suitdecks[index].getCards()) > 0:
					if self.suitdecks[index].getCards()[0].getSuit() == self.tempcards[0].getSuit():
						break
			if index < len(self.suitdecks):
				if self.tempcards[0].getSuit() == self.suitdecks[index].getCards()[-1].getSuit() and self.tempcards[0].getNum() == self.suitdecks[index].getCards()[-1].getNum() + 1:
					self.isCardMove = True
					self.startCardAnimThread(tag, self.tempcards, index, self.pressdeck, self.canvas.coords(self.highlighttags[0]))

		self.repaint()

	def mouseEnter(self, event):
		tag = event.widget.gettags('current')[0]

		if tag in ['restart', 'restartarrow', 'restartoval']:
			event.widget.itemconfig('restartarrow', fill = 'black')
			event.widget.itemconfig('restartoval', outline = 'black')

	def startCardAnimThread(self, tag, tempcards, pressindex, pressdeck, start):
		temppositions = []
		for i in range(len(self.highlighttags)):
			temppositions.append(self.canvas.coords(self.highlighttags[i]))

		cardanimthread = threading.Thread(target=self.addCardAnim, args=(tag, tempcards, pressindex, pressdeck, start, temppositions,))
		cardanimthread.setDaemon(True)

		if self.isCardMove == True and cardanimthread.is_alive() == False:
			cardanimthread.start()

	def addCardAnim(self, tag, tempcards, pressindex, pressdeck, start, temppositions):
		self.deleteCards(self.highlighttags)
		for i in range(len(self.tempcards)):
			self.canvas.create_image(temppositions[i][0], temppositions[i][1], image = self.tempcards[i].getImage(), anchor = tk.NW, tags = self.tempcards[i].getTags())
		splitcount = 3
		if self.tempcards[0].getNum() == 1 and len(self.tempcards) == 1 and 'suit' in tag:
			goal = self.canvas.coords(tag)
			goal[0] += self.suitdecks[0].getPadding()
			goal[1] += self.suitdecks[0].getPadding()
		elif self.tempcards[0].getNum() == 13 and 'column' in tag:
			goal = self.canvas.coords(tag)
		else:
			goal = self.canvas.coords(tempcards[0].getTags())
			goal[1] += self.columndecks[0].getShiftX()
		if self.isDoubleClicked == True:
			start = self.canvas.coords(tempcards[0].getTags())
			if len(self.suitdecks[pressindex].getCards()) > 0:
				goal = self.canvas.coords(self.suitdecks[pressindex].getCards()[-1].getTags())
			else:
				goal = self.canvas.coords('suit' + str(pressindex))
				goal[0] += self.suitdecks[0].getPadding()
				goal[1] += self.suitdecks[0].getPadding()
		mx = (goal[0] - start[0]) / splitcount
		my = (goal[1] - start[1]) / splitcount
		for i in range(splitcount):
			for j in range(len(self.tempcards)):
				self.canvas.move(self.tempcards[j].getTags(), mx, my)
			time.sleep(0.05)

		if self.isDoubleClicked == True or pressdeck == self.SUITDECK:
			self.suitdecks[pressindex].addCards(self.tempcards)
		elif pressdeck == self.COLUMNDECK:
			self.columndecks[pressindex].addCards(self.tempcards)
		else:
			if self.tempcards[0].getNum() == 1 and len(self.tempcards) == 1 and 'suit' in tag:
				self.suitdecks[pressindex].addCards(self.tempcards)
			elif self.tempcards[0].getNum() == 13 and 'column' in tag:
				self.columndecks[pressindex].addCards(self.tempcards)
		self.highlighttags = self.tempcards = []
		self.isCardMove = self.isDoubleClicked = False
		self.repaint()
		if self.gameComplete() == True:
			messagebox.showinfo('メッセージ', '成功です。')

	def getCardsInfosWithTags(self, tag):
		cards = []
		# カラムデッキを検索
		for i in range(len(self.columndecks)):
			for j in range(len(self.columndecks[i].getCards())):
				if self.columndecks[i].getCards()[j].getTags() == tag:
					while j < len(self.columndecks[i].getCards()):
						cards.append(self.columndecks[i].getCards()[j])
						j += 1
					return cards, i, self.COLUMNDECK

		# スーツデッキを検索
		for i in range(len(self.suitdecks)):
			if len(self.suitdecks[i].getCards()) > 0:
				if self.suitdecks[i].getCards()[-1].getTags() == tag:
					cards.append(self.suitdecks[i].getCards()[-1])
					return cards, i, self.SUITDECK

		# 手札を検索
		if len(self.deckobj.getFieldCards()) > 0:
			if tag == self.deckobj.getFieldCards()[-1].getTags():
				cards.append(self.deckobj.getFieldCards()[-1])
				return cards, -1, self.HANDDECK

		return [], -1, self.BLANK

	def deleteCards(self, highlighttags):
		for i in range(len(self.columndecks)):
			self.columndecks[i].deleteCards(highlighttags)
		for i in range(len(self.suitdecks)):
			self.suitdecks[i].deleteCards(highlighttags)
		self.deckobj.deleteFieldCards(highlighttags)

	def gameComplete(self):
		count = 0
		for i in range(len(self.suitdecks)):
			count += len(self.suitdecks[i].getCards())

		if count == 52:
			return True

		return False

	def repaint(self, event = None):
		self.canvas.delete('all')
		self.paint()

	def paint(self):
		# 最初からボタン
		self.canvas.create_oval(10, self.HEIGHT - 60, 60, self.HEIGHT - 10, fill = 'red', tags = 'restart')
		self.canvas.create_oval(22, self.HEIGHT - 46, 48, self.HEIGHT - 20, fill = 'red', outline = 'white', width = 3, tags = 'restartoval')
		self.canvas.create_rectangle(42, self.HEIGHT - 52, 52, self.HEIGHT - 32, fill = 'red', width = 0, tags = 'restart')
		self.canvas.create_line(34, self.HEIGHT - 52, 42, self.HEIGHT - 45, fill = 'white', width = 3, tags = 'restartarrow')
		self.canvas.create_line(34, self.HEIGHT - 39, 42, self.HEIGHT - 46, fill = 'white', width = 3, tags = 'restartarrow')

		# 手札の描画
		self.deckobj.paint(self.canvas, self.bgcolor, self.highlighttags)

		# カラムデッキの描画
		for i in range(len(self.columndecks)):
			self.columndecks[i].paint(self.canvas, self.highlighttags, self.imagewidth, self.imageheight, self.bgcolor)

		# スーツデッキの描画
		for i in range(len(self.suitdecks)):
			self.suitdecks[i].paint(self.canvas, self.highlighttags, self.imagewidth, self.imageheight, self.bgcolor)

		# マウスイベント
		self.canvas.tag_bind('current', '<ButtonPress-1>', self.mousePressed)
		self.canvas.tag_bind('current', '<Double-1>', self.doubleClicked)
		self.canvas.tag_bind('current', '<Enter>', self.mouseEnter)
		self.canvas.tag_bind('current', '<Leave>', self.repaint)

if __name__ == '__main__':
	root = tk.Tk()
	game = Game(master = root)
	root.update_idletasks()
	x = (root.winfo_screenwidth() // 2) - (game.WIDTH // 2)
	y = (root.winfo_screenheight() // 2) - (game.HEIGHT // 2)
	root.geometry('{}x{}+{}+{}'.format(game.WIDTH, game.HEIGHT, x, y))
	root.title('ソリティアゲーム')
	root.resizable(False, False)
	game.mainloop()