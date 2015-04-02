import os
import sys
import random
import time

difficulty = 2
s = 10
if len(sys.argv) > 0:
	try:
		if sys.argv[1]:
			difficulty = int(sys.argv[1])
	except:
		pass
	try:
		if sys.argv[2]:
			s = int(sys.argv[2])
	except:
		pass

class Field:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.total_cells = width * height
		self.field_data = []
		self.corners = []

		self.field_data = [0 for i in range(self.total_cells)]

	def Draw(self, show = False):
		for y in range(0, self.height):
			o = "|"
			for x in range(0, self.width):
				index = y * self.height + x
				o += " " + str(self.DrawCharacter( index ))
			o += " |"
			print o

	def DrawCharacter(self, index, show = False):
		cell = self.field_data[ index ]
		val = self.IterateField(cell, index)
		if cell == -1:
			return "\033[91m@\033[0m"
		elif val and cell == 0 and bool(show):
			return str(val)
		else:
			return "."

	def PopulateField(self):
		# Take 20% of the total field
		total_mines = round(self.total_cells / 100.0 * (10 * difficulty))

		while total_mines != 0:
			random.seed(int(round(time.time() * 1000.0)))
			randnum = random.randrange(1, self.total_cells*2)
			index = int(round(randnum/2))

			if self.field_data[index] == 0 and randnum % 2 == 0:
				total_mines = total_mines - 1
				self.field_data[index] = -1
		random.shuffle(self.field_data)

	def getNeighbours(self, index):
		f = self.field_data
		def set_location(index):
			try:
				n = f[index]
			except:
				return 0
			return n

		row = self.width
		col = self.height
		left = set_location(index - 1)
		right = set_location(index + 1)
		top = set_location(index - row)
		topright = set_location(index - row + 1)
		topleft = set_location(index - row - 1)
		bottom = set_location(index + row)
		bottomright = set_location(index + row + 1)
		bottomleft = set_location(index + row - 1)
		new_range = [left, topleft, top, topright, right, bottomright, bottom, bottomleft]
		
		# Top left corner
		if index == 0:
			new_range = [right, bottomright, bottom]

		# top row
		elif index < row-1 and index > 0:
			new_range = [left, bottomleft, bottom, bottomright, right]
		
		# top right corner
		elif index == row-1:
			new_range = [left, bottomleft, bottom]
		
		# left-hand column
		elif index % row == 0:
			new_range = [top, topright, right, bottomright, bottom]

		# right-hand column
		elif index-1 % row == 0:
			new_range = [top, topleft, left, bottomleft, bottom]

		# bottom left corner
		elif index == col-1 * row :
			new_range = [top, topright, right]
		
		# bottom right corner
		elif index == row * col:
			new_range = [left, topleft, top]
		
		# bottom row
		elif index > row * (col-1):
			new_range = [left, topleft, top, topright, right]

		return new_range

	def IterateField(self, cell, index):
		new_range = self.getNeighbours(cell, index)

		for neighbour in new_range:
			if neighbour == -1:
				cell += 1
			else:
				cell += 0
		return cell

os.system("clear")


def select(cell):
	if field.field_data[cell] < 0:
		return True
	else:
		empty_neighbour = True
		empty_cells = []
		leaf = 0
		while(empty_neighbour):
			for tree in field.getNeighbours(cell):
				for branch in field.getNeighbours(tree):
					for twig in field.getNeighbours(branch):
						if twig == 0:
							leaf += 1
						else:
							empty_neighbour = False

field = Field(s,s)

field.PopulateField()
print "+-" + ((field.width) * "--") + "+"
if select(int((field.width/2)*(field.height/2))):
	field.Draw(True)
else:
	field.Draw(False)

print "+-" + ((field.width) * "--") + "+"
print
print "Syntax: python mine.py \033[93mdifficulty \033[96mrow-length\033[0m"
print "Eg.: python mine.py \033[93m1 \033[96m20\033[0m"