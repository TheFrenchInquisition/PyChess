import pygame, sys, os, math
pygame.init()

tilew, tileh = 45, 45
height = tileh * 8
width = tilew * 8

size = [width, height+40]

os.environ["SDL_VIDEO_CENTERED"] = "1"

screen = pygame.display.set_mode(size)

pygame.display.set_caption("Chess")

#load images and stuff
selectimg = pygame.image.load("../images/select.png").convert_alpha()

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
	def __init__(self,name,image,startpos):
		global pieces
		self.name = name
		self.image = image
		self.x = startpos[0]
		self.y = startpos[1]
		board[startpos[0]][startpos[1]] = self
		pieces.append(self)
	def move(self,pos):
		global selected
		board[self.x][self.y] = EMPTY
		self.x = pos[0]
		self.y = pos[1]
		board[self.x][self.y] = self
		selected = False
	def attack(self,enemy):
		global pieces
		self.move((enemy.x, enemy.y))
		pieces.remove(enemy)
	def select(self):
		global selected
		selected = (self.x, self.y)

for i in range(0, 8):
	Piece("W_Pawn", pygame.image.load("../images/wpawn.png").convert_alpha(), (i, 6))
	Piece("B_Pawn", pygame.image.load("../images/bpawn.png").convert_alpha(), (i, 1))

Piece("W_Rook", pygame.image.load("../images/wrook.png").convert_alpha(), (0, 7))
Piece("W_Rook", pygame.image.load("../images/wrook.png").convert_alpha(), (7, 7))
Piece("W_Knight", pygame.image.load("../images/wknight.png").convert_alpha(), (1, 7))
Piece("W_Knight", pygame.image.load("../images/wknight.png").convert_alpha(), (6, 7))
Piece("W_Bishop", pygame.image.load("../images/wbishop.png").convert_alpha(), (2, 7))
Piece("W_Bishop", pygame.image.load("../images/wbishop.png").convert_alpha(), (5, 7))
Piece("W_Queen", pygame.image.load("../images/wqueen.png").convert_alpha(), (3, 7))
Piece("W_King", pygame.image.load("../images/wking.png").convert_alpha(), (4, 7))
Piece("B_Rook", pygame.image.load("../images/brook.png").convert_alpha(), (0, 0))
Piece("B_Rook", pygame.image.load("../images/brook.png").convert_alpha(), (7, 0))
Piece("B_Knight", pygame.image.load("../images/bknight.png").convert_alpha(), (1, 0))
Piece("B_Knight", pygame.image.load("../images/bknight.png").convert_alpha(), (6, 0))
Piece("B_Bishop", pygame.image.load("../images/bbishop.png").convert_alpha(), (2, 0))
Piece("B_Bishop", pygame.image.load("../images/bbishop.png").convert_alpha(), (5, 0))
Piece("B_Queen", pygame.image.load("../images/bqueen.png").convert_alpha(), (3, 0))
Piece("B_King", pygame.image.load("../images/bking.png").convert_alpha(), (4, 0))

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
def pixelpos(pos):
	return (pos[0] * tilew, pos[1] * tileh)

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
		elif event.type == pygame.MOUSEBUTTONUP:
			(mouseX, mouseY) = pygame.mouse.get_pos()
			curCol = int(math.ceil(mouseY/tileh) - 1)
			curRow = int(math.ceil(mouseX/tilew) - 1)

			if selected == False:
				if not isFree((curRow, curCol)) and not containsEnemy((curRow, curCol)):
					board[curRow][curCol].select()
			else:
				if isFree((curRow, curCol)):
					board[selected[0]][selected[1]].move((curRow, curCol))
					playerColor = not playerColor
					updateText()
				elif containsEnemy((curRow, curCol)):
					board[selected[0]][selected[1]].attack(board[curRow][curCol])
					playerColor = not playerColor
					updateText()
				else:
					board[curRow][curCol].select()

	pygame.display.update()
