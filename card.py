class Card():

	def __init__(self, suit, num, color, state, tags, image):
		self.suit = suit       #マーク
		self.num = num		   #数字
		self.color = color     #カードの色
		self.state = state	   #状態 0=裏, 1=表
		self.tags = tags	   #キャンバスのタグ
		self.image = image	   #画像

	def getSuit(self):
		return self.suit

	def getNum(self):
		return self.num

	def getColor(self):
		return self.color

	def getState(self):
		return self.state

	def setState(self, state):
		self.state = state

	def getTags(self):
		return self.tags

	def getImage(self):
		return self.image
		