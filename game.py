import tkinter as tk
from decimal import Decimal, ROUND_HALF_UP
import warnings
warnings.simplefilter('ignore')

class Game(tk.Frame):
	def __init__(self, master):
		self.WIDTH = 800
		self.HEIGHT = 700
		self.bgcolor = 'forestgreen'
		tk.Frame.__init__(self, master, width = self.WIDTH, height = self.HEIGHT, bg = self.bgcolor)
		self.pack()
		self.pack_propagate(0)

		self.reduction_ratio = 9  #縮小率
		self.imagewidth = int(Decimal(str(712 / self.reduction_ratio)).quantize(Decimal('0'), rounding=ROUND_HALF_UP))
		self.imageheight = int(Decimal(str(1008 / self.reduction_ratio)).quantize(Decimal('0'), rounding=ROUND_HALF_UP))

		# 52枚のカードを生成
		import deck
		self.deckobj = deck.Deck(self.imagewidth, self.imageheight)
		self.deckobj.shuffleCards()
		self.deckcards = self.deckobj.getCards()

		tk.Button(self, text = '最初から', command = self.btnClicked).pack()

	def btnClicked(self):
		self.destroy()
		game = Game(master = root)

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
