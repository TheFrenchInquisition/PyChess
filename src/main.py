import pygame, sys, os, math
pygame.init()

python_version_stupid = "Python3"
modifier = python_version_stupid == "Python3" and 1 or 0

tilew, tileh = 45, 45
height = tileh * 8
width = tilew * 8

size = [width, height]

os.environ["SDL_VIDEO_CENTERED"] = "1"

screen = pygame.display.set_mode(size)

pygame.display.set_caption("Chess")

#load images and stuff
selectimg = pygame.image.load("../images/select.png").convert_alpha()

selected = False

EMPTY = 0 #Even though 0 is shorter to type..
WPAWN = 1
WROOK = 2
WKNIG = 3
WBISH = 4
WQUEE = 5
WKING = 6

BPAWN = 11
BROOK = 12
BKNIG = 13
BBISH = 14
BQUEE = 15
BKING = 16

pieceimgs = {
	WPAWN: pygame.image.load("../images/wpawn.png").convert_alpha(),
	WROOK: pygame.image.load("../images/wrook.png").convert_alpha(),
	WKNIG: pygame.image.load("../images/wknight.png").convert_alpha(),
	WBISH: pygame.image.load("../images/wbishop.png").convert_alpha(),
	WQUEE: pygame.image.load("../images/wqueen.png").convert_alpha(),
	WKING: pygame.image.load("../images/wking.png").convert_alpha(),
	BPAWN: pygame.image.load("../images/bpawn.png").convert_alpha(),
	BROOK: pygame.image.load("../images/brook.png").convert_alpha(),
	BKNIG: pygame.image.load("../images/bknight.png").convert_alpha(),
	BBISH: pygame.image.load("../images/bbishop.png").convert_alpha(),
	BQUEE: pygame.image.load("../images/bqueen.png").convert_alpha(),
	BKING: pygame.image.load("../images/bking.png").convert_alpha(),
}

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

#Makes sure x is between min and max
def math_clamp(x, min, max): return x < min and min or (x > max and max or x)

def isFree(pos):
	row, col = pos[0], pos[1]
	if ((row < 0) or (col < 0) or (row > len(board)) or (col > len(board))): return

	return (board[row][col] == EMPTY)

#Returns top left pixel value of grid pos
def pixelpos(pos):
	return (pos[0] * tilew, pos[1] * tileh)

#Draws board pieces depending on value
def drawPieces():
	global selected
	for i in range(len(board)):
		row = board[i]
		for i2 in range(len(row)):
			square = row[i2]
			if square != EMPTY:
				screen.blit(pieceimgs[square], (i*45, i2*45))

			if selected != False:
				screen.blit(selectimg, pixelpos(selected))

def cPiece(piece, pos):
	board[pos[0]][pos[1]] = piece

def move(opos, npos):
	global selected
	board[npos[0]][npos[1]] = board[opos[0]][opos[1]]
	board[opos[0]][opos[1]] = 0
	selected = False

def select(pos):
	global selected
	selected = pos

screen.fill((102, 102, 102))

cPiece(WPAWN, (0, 6))
cPiece(WROOK, (0, 7))
cPiece(WKNIG, (1, 7))
cPiece(WBISH, (2, 7))
cPiece(WQUEE, (3, 7))
cPiece(WKING, (4, 7))

clock = pygame.time.Clock()

while True:
	clock.tick(30)

	pygame.draw.rect(screen, (139, 125, 107), [0, 0, width, height])
	for row in range(4):
		for col in range(4):
			pygame.draw.rect(screen, (255, 228, 196), [row*90, col*90, tilew, tileh])
			pygame.draw.rect(screen, (255, 228, 196), [row*90+tilew, col*90+tileh, tilew, tileh])

	drawPieces()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == pygame.MOUSEBUTTONUP:
			(mouseX, mouseY) = pygame.mouse.get_pos()
			curCol = int(math.ceil(mouseY/tileh) - modifier)
			curRow = int(math.ceil(mouseX/tilew) - modifier)

			if selected == False:
				if not isFree((curRow, curCol)):
					select((curRow, curCol))
			else:
				if isFree((curRow, curCol)):
					move(selected, (curRow, curCol))
				else:
					select((curRow, curCol))

	pygame.display.update()
