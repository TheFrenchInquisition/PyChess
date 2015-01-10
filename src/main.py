import pygame, sys, os, math
sys.dont_write_bytecode = True
from piecelogic import *
from imagedefs import *
pygame.init()

tilew, tileh = 45, 45
height = tileh * 8
width = tilew * 8

sbarw = 40
size = [width, height+sbarw]

os.environ["SDL_VIDEO_CENTERED"] = "1"

screen = pygame.display.set_mode(size)

pygame.display.set_caption("Chess")

selected = False
pieces = []
board = [
	[0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0],
]

WHITE = True
BLACK = False

playerColor = WHITE

EMPTY = 0 #Even though 0 is shorter to type..
class Piece():
	def __init__(self,name,startpos):
		global pieces
		self.name = name
		self.image = pieceimages[name]
		self.pos = startpos
		self.hasMoved = False
		board[startpos[0]][startpos[1]] = self
		pieces.append(self)
	def move(self,pos):
		global selected
		global pieces
		if contains((pos[0],pos[1])) == 2:
			pieces.remove(board[pos[0]][pos[1]])
		board[self.pos[0]][self.pos[1]] = EMPTY
		self.pos = pos
		board[self.pos[0]][self.pos[1]] = self
		self.hasMoved = True
		selected = False
	def select(self):
		global selected
		selected = self.pos

for i in range(0, 8):
	Piece("W_Pawn", (i, 6))
	Piece("B_Pawn", (i, 1))

Piece("W_Rook",   (0, 7))
Piece("W_Rook",   (7, 7))
Piece("W_Knight", (1, 7))
Piece("W_Knight", (6, 7))
Piece("W_Bishop", (2, 7))
Piece("W_Bishop", (5, 7))
Piece("W_Queen",  (3, 7))
Piece("W_King",   (4, 7))
Piece("B_Rook",   (0, 0))
Piece("B_Rook",   (7, 0))
Piece("B_Knight", (1, 0))
Piece("B_Knight", (6, 0))
Piece("B_Bishop", (2, 0))
Piece("B_Bishop", (5, 0))
Piece("B_Queen",  (3, 0))
Piece("B_King",   (4, 0))

font = pygame.font.SysFont("monospace", 20)
def updateText():
	global turnindic, piecesleft
	turnindic = font.render("Turn: "+(playerColor == WHITE and "white" or "black"), True, (139, 125, 107), (0, 0, 0, 0))
	piecesleft = font.render("Pieces: "+str(len(pieces)), True, (139, 125, 107), (0, 0, 0, 0))
updateText()

#Makes sure x is between min and max
def math_clamp(x, min, max): return x < min and min or (x > max and max or x)

def contains(pos):
	boardpos = board[pos[0]][pos[1]]
	if boardpos == 0:
		return 0 #Returns 0 if specified position does not contain a piece
	if playerColor == WHITE:
		if boardpos.name.startswith("W_"):
			return 1 #1 if it's an allied piece
		else:
			return 2 #2 if it's an enemy
	else:
		if boardpos.name.startswith("B_"):
			return 1
		else:
			return 2

#Returns top left pixel value of grid pos
def pixelpos(pos): return (pos[0] * tilew, pos[1] * tileh)

#Draws board pieces depending on value
def drawPieces():
	global selected
	for i in range(len(board)):
		row = board[i]
		for i2 in range(len(row)):
			piece = row[i2]
			
			if selected != False:
				if pieceCanMove(board[selected[0]][selected[1]], (i, i2), board, 1, playerColor) and selected != (i, i2) and contains((i, i2)) != 1:
					screen.blit(highlightimg, pixelpos((i, i2)))

					(mouseX, mouseY) = pygame.mouse.get_pos()
					curRow = int(math.ceil(mouseX/tilew))
					curCol = int(math.ceil(mouseY/tileh))
					if (curRow, curCol) == (i, i2):
						screen.blit(hhoverimg, pixelpos((i, i2)))
				else:
					pass
			if piece != EMPTY:
				screen.blit(piece.image, (i*45, i2*45))
				
clock = pygame.time.Clock()

while True:
	clock.tick(30)

	pygame.draw.rect(screen, (139, 125, 107), [0, 0, width, height])
	for row in range(4):
		for col in range(4):
			pygame.draw.rect(screen, (255, 228, 196), [row*90, col*90, tilew, tileh])
			pygame.draw.rect(screen, (255, 228, 196), [row*90+tilew, col*90+tileh, tilew, tileh])

	drawPieces()

	screen.blit(turnindic, (0, height+10))
	screen.blit(piecesleft, (width-140, height+10))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == pygame.MOUSEBUTTONUP and pygame.mouse.get_pos()[1] <= height:
			(mouseX, mouseY) = pygame.mouse.get_pos()
			curCol = int(math.ceil(mouseY/tileh))
			curRow = int(math.ceil(mouseX/tilew))

			if selected == False:
				if contains((curRow, curCol)) == 1:
					board[curRow][curCol].select()
			else:
				if contains((curRow, curCol)) != 1:
					if pieceCanMove(board[selected[0]][selected[1]], (curRow, curCol), board, 0, playerColor):
						playerColor = not playerColor
						updateText()
						board[selected[0]][selected[1]].move((curRow, curCol))
				else:
					board[curRow][curCol].select()

	pygame.display.update()
