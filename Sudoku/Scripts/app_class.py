import pygame
from settings import *
from buttonClass import *
from sudoku import *
import time

class App:
	def __init__(self):
		pygame.init() # Initialize
		self.window = pygame.display.set_mode((WIDTH, HEIGHT)) # Create Window
		
		self.running = True # Game is running
		self.finihed = False

		self.grid = testBoard # Make a testboard
		self.finalGrid = finalBoard

		self.incorrectCells = []
		self.hint = False
		self.hintCell = None
		self.starTime = None

		self.selected = None # Index i, j of what you have selected
		self.mousePos = None # (x,y) coordinates of where you clicked
		self.state = 'playing'
		self.cellChanged = False
		self.lockedCells = []

		self.playingButtons = []
		self.menuButtons = []
		self.endButtons = []

		self.finishGame = False
		self.finalShade = []
		self.finalWindow = False

		self.buttonClicked = None
		self.buttonActive = []

		self.font = pygame.font.SysFont("arial", int(cellSize/2))
		
		self.load() # Load everything. Buttons, board etc
	
	# We call this function in main.
	def run(self): 
		while self.running: # Becomes false if pygame.QUIT. 3 of these functions are called constantly.
			if self.state == 'playing':
				self.playing_events() 
				self.playing_update()
				self.playing_draw()
		pygame.QUIT
		sys.exit()
	
####### PLAYING STATE FUNCTIONS #######

	def playing_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False

			# User Clicks
			if event.type == pygame.MOUSEBUTTONDOWN: # If there was a mouse click in the window
				selected = self.mouseOnGrid() # Has index of which cell you clicked
				if selected: # Updates the self.selected to the cell clicked
					self.selected = selected
				else: #Checks if a button has been clicked. It puts the index of the button in buttonClicked
					self.buttonClicked = self.checkButtonClick()
					if self.buttonClicked == 1:
						pass
					else:
						self.selected = None
				"""else: # Unselects if no cell has been clicked
					self.selected = None"""
			
			# User Types
			if event.type == pygame.KEYDOWN:
				if self.selected != None and self.selected not in self.lockedCells:
					if self.isInt(event.unicode):
						self.grid[self.selected[0]][self.selected[1]] = int(event.unicode)
						self.cellChanged = True
					else:
						self.grid[self.selected[0]][self.selected[1]] = int(0)


	def playing_update(self):
		self.mousePos = pygame.mouse.get_pos()
		
		# Check buttons
		for button in self.playingButtons:
			button.update(self.mousePos)
			
		if self.finishGame == False:
			
			#If you've changed a cell value while 'Check' button is active, we +1 the Check button to ensure it works. And we clear out the incorrectCells
			if self.cellChanged:
				if self.buttonActive[0] == 1:
					self.playingButtons[0].timesClicked += 1
				self.incorrectCells = []
				#self.playingButtons[0].timesClicked += -1
			
			#Clicked the 'Check' button. If you've clicked it twice, the red goes away.
			if self.buttonClicked == 0:
				self.checkAllCells()
				if self.playingButtons[0].timesClicked % 2 == 0:
					self.buttonActive[0] = 1
					#self.checkAllCells()
				else:
					self.buttonActive[0] = 0
					self.incorrectCells = []
			"""if self.cellChanged:
				self.incorrectCells = []
				if self.allCellsDone():
					self.checkAllCells()
					print(self.incorrectCells)"""

			# Clicked the 'Hint button.
			if self.buttonClicked == 1:
				if self.selected: #If there was a selection then it will highlight it pink for 3 seconds.
					self.buttonActive[0] = 0
					self.incorrectCells = []
					self.playingButtons[0].timesClicked += 1
					#Green shade that one cell
					self.hint = True
					self.hintCell = self.selected
					self.buttonActive[1] = 1
					self.grid[self.selected[0]][self.selected[1]] = self.hintCellVal(self.hintCell)
					self.startTime = time.time()

		#Solve button clicked
		if self.buttonClicked == 2:
			for i, _ in enumerate(self.playingButtons):
				self.buttonActive[i] = 0
			self.buttonActive[2] = 1
			
			self.finishGame = True
			self.findFinalShadeCells()
			self.giveSolution()
			

		if self.allCellsDone():
			self.incorrectCells = []
			self.checkAllCells()
			if len(self.incorrectCells) == 0:
				self.finalWindow = True
		
		
	def playing_draw(self):
		self.window.fill(WHITE)

		# Draw Grid
		self.drawGrid(self.window)
		
		# Check buttons
		for i, button in enumerate(self.playingButtons):
			button.draw(self.window)

		# If we have selected something, we must draw on it.
		if self.selected: 
			self.drawSelection(self.window, self.selected)

		# Overdraws for specific cells. Hardcoded numbers basically
		self.shadeLockedCells(self.window, self.lockedCells)

		# Overdraws for the incorrect cells
		if self.buttonActive[0] == 1:
			self.shadeIncorrectCells(self.window, self.incorrectCells)
		self.buttonClicked = None

		# Hint cells highlighted
		if self.buttonActive[1] == 1:
			if (time.time() - self.startTime) <= 2.4:
				self.shadeHintCell(self.window, self.hintCell)
			else:
				self.buttonActive[1] = 0

		# Shade the final Cells
		if self.buttonActive[2] == 1:
			self.shadeFinalCells(self.window)

		# Final Window
		if self.finalWindow:
			self.drawFinalWindow(self.window)

		# Draw Numbers
		self.drawNumbers(self.window)

		self.cellChanged = False
		self.hint = False

		pygame.display.update()

		



####### HELPER FUNCTIONS #######

	# Load everything. Buttons and LockedCells.
	def load(self):
		self.loadButtons()
		
		# Setting locked cells from original board
		for yindx, row in enumerate(self.grid):
			for xindx, col in enumerate(row):
				if col != 0:
					self.lockedCells.append((yindx, xindx))

	# Loads all types of buttons
	def loadButtons(self):
		self.playingButtons.append(Button(gridStartPos[0], gridStartPos[1] - 60, 100, 40, 'Check', BUTTONCOLOR)) # Hardcoded Check button
		self.playingButtons.append(Button(WIDTH - gridStartPos[0] - 100, gridStartPos[1] - 60, 100, 40, 'Hint', BUTTONCOLOR)) #Hardcoded Hint button

		#Where 'Check' Ends. Where 'Hint starts'. The half of 'Solve'.
		halfPoint = ((WIDTH - gridStartPos[0] - 100) - (gridStartPos[0] + 100)) / 2
		lengthToHalf = gridStartPos[0] + 100 + halfPoint
		self.playingButtons.append(Button(lengthToHalf - 75, gridStartPos[1] - 60, 150, 40, 'Solve', GREEN))
		
		for _ in self.playingButtons:
			self.buttonActive.append(0)

	# Draw() calls this to draw the basic grid structure
	def drawGrid(self, window):
		pygame.draw.rect(window, BLACK, (gridStartPos[0], gridStartPos[1], WIDTH-150, HEIGHT - 150), 3) # Parameters are: x start, y start, the total width (removing 20 each side), total height (100 top and 20 bottom), 2 pixels thickness
		for x in range(9):
			# Parameters are: window, color, start position (x,y), end position (x,y). Every 3rd line must be bold
			pygame.draw.line(window, BLACK, (gridStartPos[0] + (x*cellSize), gridStartPos[1]), (gridStartPos[0] + (x*cellSize), gridStartPos[1] + 450), 2 if x % 3 == 0 else 1)
			pygame.draw.line(window, BLACK, (gridStartPos[0], gridStartPos[1] + (x*cellSize)), (gridStartPos[0] + 450, gridStartPos[1] + (x*cellSize)), 2 if x % 3 == 0 else 1)

	# Draws all the numbers by calling textToScreen for each number with its (i, j).
	def drawNumbers(self, window):
		for rindx, row in enumerate(self.grid):
			for cindx, col in enumerate(row):
				if col != 0:
					pos = [(cindx*cellSize) + gridStartPos[0], (rindx*cellSize) + gridStartPos[1]]
					self.textToScreen(window, str(col), pos)

	# Draws a single number. Center aligns it in the cell.
	def textToScreen(self, window, text, pos):
		font = self.font.render(text, False, BLACK)
		
		# Use to center the number
		fontHeight = font.get_height()
		fontWidth = font.get_width()

		pos[0] += (cellSize - fontWidth) // 2
		pos[1] += (cellSize - fontHeight) // 2

		window.blit(font, pos)
	
	# event() calls then when mouse clicks, checks if mouse was on grid or not. If it was then return index (i, j)
	def mouseOnGrid(self):
		if (self.mousePos[0] > gridStartPos[0]) & (self.mousePos[0] < gridStartPos[0] + gridSize) & (self.mousePos[1] > gridStartPos[1]) & (self.mousePos[1] < gridStartPos[1] + gridSize):
			return (int((self.mousePos[1] - gridStartPos[1]) / cellSize), int((self.mousePos[0] - gridStartPos[0]) / cellSize))
		return False

	# draw() calls this function when a cell has been clicked. It makes the cell blue.
	def drawSelection(self, window, pos):
		# Parameters are: window, color, (x start, y start, x size, y size)
		pygame.draw.rect(window, LIGHTBLUE, (gridStartPos[0] +1+  (pos[1]*cellSize), gridStartPos[1] +1+  (pos[0] * cellSize), cellSize-1, cellSize-1))
	
	# Grey color on lockedCells. Hardcoded numbers.		
	def shadeLockedCells(self, window, lockedCells):
		for cell in lockedCells:
			pygame.draw.rect(window, LOCKEDCELLCOLOR, (cell[1]*cellSize + 1+ gridStartPos[0], cell[0]*cellSize + 1+gridStartPos[1], cellSize-1, cellSize-1))

	# Grey color on incorrectCells.	
	def shadeIncorrectCells(self, window, incorrectCells):
		for cell in incorrectCells:
			pygame.draw.rect(window, RED, (cell[1]*cellSize + gridStartPos[0]+1, cell[0]*cellSize + gridStartPos[1]+1, cellSize-1, cellSize-1))

	# Checks if it is an int or not
	def isInt(self, stringVal):
		try:
			int(stringVal)
			return True
		except:
			return False

	# Checks if Cell is complete
	def allCellsDone(self):
		for row in self.grid:
			for number in row:
				if number == 0:
					return False

		return True

	# Finds all incorrect cells
	def checkAllCells(self):
		for rindx, row in enumerate(self.grid):
			for cindx, col in enumerate(row):
				if (self.finalGrid[rindx][cindx] != self.grid[rindx][cindx]) & (self.grid[rindx][cindx] != 0):
					self.incorrectCells.append((rindx, cindx))
	
	# Checks if it has clicked any button
	def checkButtonClick(self):
		for index, button in enumerate(self.playingButtons):
			if button.buttonClicked(self.mousePos):
				return index

	# Shade single cell
	def shadeHintCell(self, window, cell):
		if self.selected:
			pygame.draw.rect(window, PINK, (cell[1]*cellSize + gridStartPos[0]+1, cell[0]*cellSize + gridStartPos[1]+1, cellSize-1, cellSize-1))

	# Finds correct hint cell
	def hintCellVal(self, cell):
		return self.finalGrid[cell[0]][cell[1]]

	# Find all the wrong cells including 0's
	def findFinalShadeCells(self):
		for rindx, row in enumerate(self.grid):
			for cindx, col in enumerate(row):
				if (self.finalGrid[rindx][cindx] != self.grid[rindx][cindx]):
					self.finalShade.append((rindx, cindx))

	# Shade all the cells that have to be solved
	def shadeFinalCells(self, window):
		for cell in self.finalShade:
			pygame.draw.rect(window, PINK, (cell[1]*cellSize + gridStartPos[0]+1, cell[0]*cellSize + gridStartPos[1]+1, cellSize-1, cellSize-1))

	# Makes the grid the final solution
	def giveSolution(self):
		self.grid = self.finalGrid

	# Draw the final window
	def drawFinalWindow(self, window):
		pos = [50, 560]
		pygame.draw.rect(self.window, LIGHTBLUE, (pos[0], pos[1], 500, 30))
		text = 'Thank you for playing! Stay tuned for more updates such as random boards and more!'
		
		fontFinal = pygame.font.SysFont("arial", int(15))
		font = fontFinal.render(text, False, BLACK)
		
		# Use to center the number
		fontHeight = font.get_height()
		fontWidth = font.get_width()

		pos[0] += (500 - fontWidth) // 2
		pos[1] += (30 - fontHeight) // 2

		window.blit(font, pos)

"""
First the game is loaded. From the board the lockedCells are created. The buttons are loaded. All attributes are basically initially created.
The basic grid is then drawn and its numbers as well.
Then if there is a click event, retrieve where it was clicked, check if it was clicked inside the cell, if yes then highlight it.
Once highlighted, overdraw it with grey IF it is a lockedCell
If empty cell is selected, you can input an integer in it.
When you input an integer, it resets the incorrectCells variable. 
It checks if all cells are full. If they are then red highlight all incorrect cells

event() check if a button has been clicked. If it has, then return the index of which button. And tell the button it has been clicked
in update() call button update. Button update will add the number of clicks done (for 'Check' button)
the update() will check if a button has been clicked. And carry out the functions of that button
"""