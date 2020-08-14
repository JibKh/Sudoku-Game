import pygame
from settings import *

class Button:
	def __init__(self, x, y, width, height, text, color, highlightedColor = (189,189,189), function = None, params = None):
		self.image = pygame.Surface((width, height)) #Create an image of specific height
		self.pos = [x, y]
		self.width = width
		self.height = height
		self.rect = self.image.get_rect() #You get the rectangular section of that image
		self.rect.topleft = self.pos #Set that rectangle where you need it to be
		self.text = text
		self.color = color
		self.highlightedColor = highlightedColor
		self.function = function
		self.params = params
		self.highlighted = False
		self.clicked = False
		self.timesClicked = -1

		self.font = pygame.font.SysFont("arial", int(20))

	def update(self, mouse):
		if self.rect.collidepoint(mouse):
			self.highlighted = True
		else:
			self.highlighted = False

		if self.clicked:
			self.timesClicked += 1
			#self.clicked = False
	
	def draw(self, window):
		if self.highlighted:
			self.image.fill(self.highlightedColor)
		else:
			self.image.fill(self.color)
			
		window.blit(self.image, self.pos) #Draw the image at that position

		self.drawText(window, deepcopy(self.pos))

		self.clicked = False


####### HELPER FUNCTIONS #######

	#Draws text on top of button
	def drawText(self, window, pos):
		font = self.font.render(self.text, False, WHITE)
		
		# Use to center the number
		fontHeight = font.get_height()
		fontWidth = font.get_width()

		pos[0] += (self.width - fontWidth) // 2
		pos[1] += (self.height - fontHeight) // 2

		#pos[0] += (pos[0] - fontWidth) // 2
		#pos[1] += 6
		#pos[1] += 2+(pos[1] - fontHeight) // 2

		window.blit(font, pos)

	#Checks if button has been clicked
	def buttonClicked(self, mouse):
		if (mouse[0] >= self.pos[0]) & (mouse[0] <= (self.pos[0]+self.width)) & (mouse[1] >= self.pos[1]) & (mouse[1] <= (self.pos[1]+self.height)):
			self.clicked = True
			return True
		return False

#You make an image of the button
#For highlight reasons, you create a rect of that button too
#In draw, you draw the image of the button
#In update, using the rect, check if you are hovering over it or not
#If you are, then in draw make the button highlighted