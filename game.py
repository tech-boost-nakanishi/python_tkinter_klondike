import tkinter as tk
from decimal import Decimal, ROUND_HALF_UP
from tkinter import messagebox
import warnings
warnings.simplefilter('ignore')

class Game(tk.Frame):
	def __init__(self, master):
		self.WIDTH = 800
		self.HEIGHT = 700
		self.bgcolor = 'forestgreen'
		tk.Frame.__init__(self, master, width = self.WIDTH, height = self.HEIGHT)
		self.pack()
		self.pack_propagate(0)

		self.reduction_ratio = 9  #縮小率
		self.imagewidth = int(Decimal(str(712 / self.reduction_ratio)).quantize(Decimal('0'), rounding=ROUND_HALF_UP))
		self.imageheight = int(Decimal(str(1008 / self.reduction_ratio)).quantize(Decimal('0'), rounding=ROUND_HALF_UP))

		self.highlighttags = []	# 選択中のタグを格納
		self.tempcards = []		# 選択中のカードを格納

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

		if tag == 'handcards':
			self.highlighttags = self.tempcards = []
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
				if self.tempcards[0].getColor() != tempcards[-1].getColor():
					if self.tempcards[0].getNum() + 1 == tempcards[-1].getNum():
						self.deleteCards(self.highlighttags)
						self.columndecks[pressindex].addCards(self.tempcards)

			elif pressdeck == self.SUITDECK:
				if len(self.tempcards) == 1 and len(tempcards) == 1:
					if self.tempcards[0].getSuit() == tempcards[0].getSuit():
						if self.tempcards[0].getNum() == tempcards[0].getNum() + 1:
							self.deleteCards(self.highlighttags)
							self.suitdecks[pressindex].addCards(self.tempcards)

			elif pressdeck == self.BLANK and 'suit' in tag:
				if len(self.tempcards) == 1:
					if self.tempcards[0].getNum() == 1:
						self.deleteCards(self.highlighttags)

						index = int(tag.replace('suit', ''))
						self.suitdecks[index].addCards(self.tempcards)

			elif pressdeck == self.BLANK and 'column' in tag:
				index = int(tag.replace('column', ''))
				if self.tempcards[0].getNum() == 13:
					self.deleteCards(self.highlighttags)
					self.columndecks[index].addCards(self.tempcards)

			self.highlighttags = self.tempcards = []

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

	def btnClicked(self):
		self.destroy()
		game = Game(master = root)

	def paint(self):
		# 最初からボタン
		restartbtn = tk.Button(self, text = '最初から', command = self.btnClicked, cursor = 'hand2', bg = self.bgcolor, highlightbackground = self.bgcolor)
		self.canvas.create_window(10, self.HEIGHT - 40, window = restartbtn, anchor='nw')

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