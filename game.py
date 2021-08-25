import tkinter as tk
from decimal import Decimal, ROUND_HALF_UP
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
		self.deckobj = deck.Deck(self.imagewidth, self.imageheight)
		self.deckobj.shuffleCards()
		self.deckcards = self.deckobj.getCards()

		# カラムデッキのインスタンス生成
		import columnDeck
		self.columndecks = []
		for i in range(7):
			obj = columnDeck.ColumnDeck(i * self.imagewidth + (i + 1) * 30, self.imageheight * 1.5, self.imagewidth, self.imageheight)
			self.columndecks.append(obj)
			for j in range(i + 1):
				self.columndecks[i].addCard(self.deckcards[0])
				self.deckcards.pop(0)

		self.canvas = tk.Canvas(self, width = self.WIDTH, height = self.HEIGHT, bg = self.bgcolor, bd = 0, highlightthickness = 0)
		self.canvas.pack()

		self.paint()

	def mousePressed(self, event):
		tag = event.widget.gettags('current')[0]

		if tag in ['restartrect', 'restart']:
			self.destroy()
			game = Game(master = root)

		else:
			self.highlighttags.clear()
			self.getCardsWithTags(tag)
			self.repaint()

	def getCardsWithTags(self, tag):
		# カラムデッキを検索
		for i in range(len(self.columndecks)):
			for j in range(len(self.columndecks[i].getCards())):
				if self.columndecks[i].getCards()[j].getTags() == tag:
					while j < len(self.columndecks[i].getCards()):
						self.highlighttags.append(self.columndecks[i].getCards()[j].getTags())
						self.tempcards.append(self.columndecks[i].getCards()[j])
						j += 1
					break

	def repaint(self, event = None):
		self.canvas.delete('all')
		self.paint()

	def paint(self):
		# 最初からボタン
		self.canvas.create_rectangle(10, self.HEIGHT - 40, 100, self.HEIGHT - 10, fill = 'chocolate', outline = 'white', width = 1, tags = 'restartrect')
		self.canvas.create_text(55, self.HEIGHT - 25, fill = 'black', text = '最初から', font = ('Arial', 16), tags = 'restart')

		# カラムデッキの描画
		for i in range(len(self.columndecks)):
			self.columndecks[i].paint(self.canvas, self.highlighttags)

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