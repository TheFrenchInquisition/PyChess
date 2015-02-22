import pygame, sys, os, math
sys.dont_write_bytecode = True
from piecelogic import *
from imagedefs import *
pygame.init()

tilew, tileh = 45, 45
height = tileh * 8
width = tilew * 8
'''
take board, and take all possible enemy moves
if piece is being attacked, set pieceisbeingattacked to True
'''
sbarw = 40
size = [width, height+sbarw]

os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.display.set_icon(iconimg)
pygame.display.set_caption("Chess")

screen = pygame.display.set_mode(size)

selected = False
pieces = []

playerIsWhite = True

class Piece():
	def __init__(self,name,startpos):
		global pieces
		self.name = name
		self.image = pieceimages[name]
		self.pos = startpos
		self.hasMoved = False
		self.beingAttacked = False
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
		print(self.beingAttacked)
		selected = self.pos

def initPieces():
	global pieces
	global board
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
	pieces = []
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

initPieces()

font = pygame.font.SysFont("monospace", 20)
def updateText():
	global turnindic, piecesleft
	turnindic = font.render("Turn: "+("white" if playerIsWhite == True else "black"), True, (139, 125, 107), (0, 0, 0, 0))
	piecesleft = font.render("Pieces: "+str(len(pieces)), True, (139, 125, 107), (0, 0, 0, 0))
updateText()

def contains(pos):
	boardpos = board[pos[0]][pos[1]]
	if boardpos == 0:
		return 0 #Returns 0 if specified position does not contain a piece
	if playerIsWhite == True:
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
				if pieceCanMove(board[selected[0]][selected[1]], (i, i2)) and selected != (i, i2) and contains((i, i2)) != 1:
					screen.blit(highlightimg, pixelpos((i, i2)))

					(mouseX, mouseY) = pygame.mouse.get_pos()
					curRow = int(math.ceil(mouseX/tilew) - 1)
					curCol = int(math.ceil(mouseY/tileh) - 1)
					if (curRow, curCol) == (i, i2):
						screen.blit(hhoverimg, pixelpos((i, i2)))
				else:
					pass
			if piece != EMPTY:
				screen.blit(piece.image, (i*45, i2*45))

def getAttacks():
	for piece in pieces:
		piece.beingAttacked = False
		for piece2 in pieces:
			enemyname = "B_" if piece.name.startswith("W_") else "W_"
			if piece != piece2 and piece2.name.startswith(enemyname) and pieceCanMove(piece2, piece.pos):
				piece.beingAttacked = True

clock = pygame.time.Clock()

darktan = pygame.Color(139, 125, 107)
lighttan = pygame.Color(255, 228, 196)
while True:
	clock.tick(30)

	pygame.draw.rect(screen, darktan, [0, 0, width, height])
	for row in range(4):
		for col in range(4):
			pygame.draw.rect(screen, lighttan, [row*90, col*90, tilew, tileh])
			pygame.draw.rect(screen, lighttan, [row*90+tilew, col*90+tileh, tilew, tileh])

	drawPieces()
	getAttacks()

	screen.blit(turnindic, (0, height+10))
	screen.blit(piecesleft, (width-140, height+10))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.event.post(pygame.event.Event(pygame.QUIT))
			elif event.key == pygame.K_r:
				initPieces()
		elif event.type == pygame.MOUSEBUTTONUP and pygame.mouse.get_pos()[1] <= height:
			(mouseX, mouseY) = pygame.mouse.get_pos()
			curCol = int(math.ceil(mouseY/tileh) - 1)
			curRow = int(math.ceil(mouseX/tilew) - 1)

			if selected == False:
				if contains((curRow, curCol)) == 1:
					board[curRow][curCol].select()
			else:
				if contains((curRow, curCol)) != 1:
					if pieceCanMove(board[selected[0]][selected[1]], (curRow, curCol)):
						playerIsWhite = not playerIsWhite
						updateText()
						board[selected[0]][selected[1]].move((curRow, curCol))
				else:
					board[curRow][curCol].select()

	pygame.display.update()