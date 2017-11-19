import sys, random, copy
from graphics import *

colors = ['black', 'white', 'red', 'blue', 'yellow', 'green','purple']

def tick(win, colored, old_colored, squares):
	#generate some random colors to make the game look interesting
	c1 = colors[random.randint(0,6)]
	c2 = colors[random.randint(0,6)]
	#c1 and c2 should not be the same color
	while c1 == c2:
		c2 = colors[random.randint(0,6)]
	#iterate through the cells in the game
	for i,r in enumerate(colored):
		for j,v in enumerate(r):
			#if the state of the cell has changed, recolor
			if colored[i][j] != old_colored[i][j]:
				rect = squares[i][j]
				color = c1 if colored[i][j] == 1 else c2
				rect.setFill(color)
				rect.setOutline(color)

def tick2(win, colored, old_colored, squares):
	#more pretty colors
	c1 = colors[random.randint(0,6)]
	c2 = colors[random.randint(0,6)]

	while c1 == c2:
		c2 = colors[random.randint(0,6)]
	#iterate over the cells from both x boundaries
	for i in range(len(colored)):
		#after iterating through half the cells the game has been redrawn
		#get new colored map
		if i == len(colored)/2:
			old_colored = copy.deepcopy(colored)
			colored = update(colored)
		for j in range(len(colored)):
			#act on the game from the left x boundary
			if colored[i][j] != old_colored[i][j]:
				rect = squares[i][j]
				color = c1 if colored[i][j] == 1 else c2
				rect.setFill(color)
				rect.setOutline(color)
			#act on the game from the right x boundary
			if colored[-i][-j] != old_colored[-i][-j] and i:
				rect = squares[-i][-j]
				color = c1 if colored[-i][-j] == 1 else c2
				rect.setFill(color)
				rect.setOutline(color)

def update(colored):
	#get the number of elements along a single axis
	num_elems = len(colored)
	#create the new colored array
	new_colored = [[0]*num_elems for i in range(num_elems)]
	for i,r in enumerate(colored):
		for j,v in enumerate(r):
			#get the state of the neighboring cells
			neighbors = get_neighbors(colored,i,j)
			#if the cell is alive
			if colored[i][j] == 1:
				#if the cell has less than 2 neighbors it dies
				if 0 in neighbors[-2:]:
					new_colored[i][j] = 0
				#if the cell has more than 3 neighbors it dies
				elif 1 in neighbors[:-3]:
					new_colored[i][j] = 0
				#otherwise it lives
				else:
					new_colored[i][j] = 1
			else:
				#if a dead cell has exactly 3 neighbors then it lives
				if 0 not in neighbors[-3:]:
					new_colored[i][j] = 1
				#otherwise its dead
				else:
					new_colored[i][j] = 0
	return new_colored	

def get_neighbors(colored, i, j):
	num_elems = len(colored)
	neighbors = []
	#check at each neighboring position
	for step in [[-1,-1],[1,1],[-1,0],[1,0],[0,-1],[0,1],[1,-1],[-1,1]]:
		i_s = i+step[0]
		j_s = j+step[1]
		#bounds check for border cells
		if i_s<num_elems and i_s>0 and j_s<num_elems and j_s>0:
			neighbors.append(colored[i_s][j_s])
	#sort the neighbors such that dead neighbors proceed living neighbors
	neighbors = sorted(neighbors)
	return neighbors

def generate_world(num_elems, num_colored):
	colored = [[0]*num_elems for i in range(num_elems)]
	#minimum boundary condition for the provided number of elements
 	cutoff = num_colored / float(num_elems**2)	
	#number of cells that are alive 
	have_color = 0
	for i,row in enumerate(colored):
		for j,val in enumerate(row):
			r = random.random()
			if r < cutoff and have_color < num_colored:
				colored[i][j] = 1
				have_color += 1
	return colored

def generate_grid(win, num_elems, elem_size):
	squares = [ [] for i in range(num_elems)]
	for i,r in enumerate(squares):
		for j in range(num_elems):
			x = i*elem_size
			y = j*elem_size
			rect = Rectangle(Point(x,y), Point(x+10, y+10))
			rect.setFill('white')
			rect.setOutline('white')
			r.append(rect)
			rect.draw(win)
	return squares

if __name__ == "__main__":
	num_elems = int(raw_input("Enter the number of elements along one axis of the grid: "))
	elem_size = int(raw_input("Enter the size of the elemt: "))
	grid_size = num_elems * elem_size

	num_colored = int(raw_input("Enter number of starting points: "))

	win = GraphWin("game_window", grid_size, grid_size)
	
	colored = generate_world(num_elems, num_colored)
	old_colored = [ [0]*num_elems for i in range(num_elems)]
	squares = generate_grid(win, num_elems, elem_size)

	
	while 1:
		tick2(win, colored, old_colored, squares)
		old_colored = copy.deepcopy(colored)
		colored = update(colored)

