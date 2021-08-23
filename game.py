import tkinter as tk
import random

class Game(tk.Frame):
	def __init__(self, master):
		self.WIDTH = 640
		self.HEIGHT = 700
		self.bgcolor = 'forestgreen'
		tk.Frame.__init__(self, master, width = self.WIDTH, height = self.HEIGHT, bg = self.bgcolor)
		self.pack()
		self.pack_propagate(0)

		tk.Label(self, text = str(random.randint(0,10))).pack()

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
