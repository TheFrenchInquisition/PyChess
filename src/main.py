import pygame, sys, os, math
sys.dont_write_bytecode = True
from piecelogic import *
from imagedefs import *
pygame.init()

tilew, tileh = 45, 45
height = tileh * 8
width = tilew * 8

size = [width, height+40]

os.environ["SDL_VIDEO_CENTERED"] = "1"

screen = pygame.display.set_mode(size)

pygame.display.set_caption("Chess")

selected = False
pieces = []

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
		board[startpos[0]][startpos[1]] = self
		pieces.append(self)
	def move(self,pos):
		global selected
		global pieces
		if containsEnemy((pos[0],pos[1])):
			pieces.remove(board[pos[0]][pos[1]])
		board[self.pos[0]][self.pos[1]] = EMPTY
		self.pos = pos
		board[self.pos[0]][self.pos[1]] = self
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

def containsEnemy(pos):
	row, col = pos[0], pos[1]
	if isFree(pos): return False
	if playerColor == WHITE:
		return (board[row][col].name.startswith("B_"))
	else:
		return (board[row][col].name.startswith("W_"))

def isFree(pos):
	row, col = pos[0], pos[1]
	if ((row < 0) or (col < 0) or (row > len(board)) or (col > len(board))): return
	return board[row][col] == EMPTY

#Returns top left pixel value of grid pos
def pixelpos(pos): return (pos[0] * tilew, pos[1] * tileh)

#Draws board pieces depending on value
def drawPieces():
	global selected
	for i in range(len(board)):
		row = board[i]
		for i2 in range(len(row)):
			piece = row[i2]
			if piece != EMPTY:
				screen.blit(piece.image, (i*45, i2*45))

			if selected != False:
				screen.blit(selectimg, pixelpos(selected))

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
		elif event.type == pygame.MOUSEBUTTONUP and pygame.mouse.get_pos()[1] < 361:
			(mouseX, mouseY) = pygame.mouse.get_pos()
			curCol = int(math.ceil(mouseY/tileh) - 1)
			curRow = int(math.ceil(mouseX/tilew) - 1)

			if selected == False:
				if not isFree((curRow, curCol)) and not containsEnemy((curRow, curCol)):
					board[curRow][curCol].select()
			else:
				if isFree((curRow, curCol)) or containsEnemy((curRow, curCol)):
					if pieceCanMove(board[selected[0]][selected[1]], (curRow, curCol)):
						playerColor = not playerColor
						updateText()
						board[selected[0]][selected[1]].move((curRow, curCol))
				else:
					board[curRow][curCol].select()

	pygame.display.update()
