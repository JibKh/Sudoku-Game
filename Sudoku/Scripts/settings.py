from sudoku import solve
from copy import deepcopy

WIDTH = 600
HEIGHT = 600

#Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
LIGHTBLUE = (96, 216, 232)
LOCKEDCELLCOLOR = (189, 189, 189)
RED = (255, 0, 0)
PINK = (255, 192, 203)
GREEN = (0, 128, 0)
BUTTONCOLOR = (73,73,73)


#Boards
#testBoard = [[0 for x in range(9)] for x in range(9)]

testBoard = [
	[0,6,0,2,0,0,8,3,1],
	[0,0,0,0,8,4,0,0,0],
	[0,0,7,6,0,3,0,4,9],
	[0,4,6,8,0,2,1,0,0],
	[0,0,3,0,9,6,0,0,0],
	[1,2,0,7,0,5,0,0,6],
	[7,3,0,0,0,1,0,2,0],
	[8,1,5,0,2,9,7,0,0],
	[0,0,0,0,7,0,0,1,5]
]

finalBoard = deepcopy(testBoard)
solve(finalBoard)

#Positions and Sizes
gridStartPos = (75,100) #Top left of our grid
cellSize = 50
gridSize = cellSize * 9