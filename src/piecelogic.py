import math

pieceLogic = {}
collisionLogic = {}
EMPTY = 0
tempboard = False #2hacky5me

def isFree(pos):
	row, col = pos[0], pos[1]
	if ((row < 0) or (col < 0) or (row > len(tempboard)-1) or (col > len(tempboard)-1)): return
	return tempboard[row][col] == EMPTY

def bishopCLogic(piece, newpos):
	squareamount = abs(piece.pos[0]-newpos[0])
	print(squareamount)
	for i in range(1, squareamount):
		mod = (piece.pos[0] > newpos[0]) and -i or i
		mod2 = (piece.pos[1] > newpos[1]) and -i or i
		testpos = (piece.pos[0]+mod, piece.pos[1]+mod2)
		if not isFree(testpos):
			return False
	return True
collisionLogic["_Bishop"]=bishopCLogic

def rookCLogic(piece, newpos): #broken kinda
	diffx = (piece.pos[0] - newpos[0])
	diffy = (piece.pos[1] - newpos[1])
	squareamount = diffx == 0 and abs(diffy) or abs(diffx)
	for i in range(1, squareamount):
		mod = (piece.pos[1] > newpos[1]) and -i or i
		testpos1 = diffx == 0 and piece.pos[0] or piece.pos[0] + mod
		print(testpos1)
		testpos2 = diffx == 0 and piece.pos[1] + mod or piece.pos[1]
		testpos = (testpos1, testpos2)
		if testpos1 == -1:
			testpos = (0, testpos2)
		print(testpos)
		if not isFree(testpos):
			return False
	return True
collisionLogic["_Rook"]=rookCLogic

def queenCLogic(piece, newpos):
	return (bishopCLogic(piece, newpos) and rookCLogic(piece, newpos))
collisionLogic["_Queen"]=queenCLogic

def pawnCLogic(piece, newpos):
	return (rookCLogic(piece, newpos))
collisionLogic["_Pawn"]=pawnCLogic

def returntrue(doop, dipp):
	return True
collisionLogic["_Knight"]=returntrue
collisionLogic["_King"]=returntrue

def rookLogic(piece, newpos):
	return ((piece.pos[0] == newpos[0]) or (piece.pos[1] == newpos[1]))
pieceLogic["_Rook"]=rookLogic

def knightLogic(piece, newpos):
	diffx = abs(piece.pos[0]-newpos[0])
	diffy = abs(piece.pos[1]-newpos[1])
	return (diffx <= 2 and diffy <= 2 and diffx != 0 and diffy != 0 and diffx != diffy)
pieceLogic["_Knight"]=knightLogic

def bishopLogic(piece, newpos):
	return (abs(piece.pos[1]-newpos[1]) == abs(piece.pos[0]-newpos[0]))
pieceLogic["_Bishop"]=bishopLogic

def queenLogic(piece, newpos):
	return (rookLogic(piece, newpos) or bishopLogic(piece, newpos))
pieceLogic["_Queen"]=queenLogic

def kingLogic(piece, newpos):
	return (queenLogic(piece, newpos) and (abs(piece.pos[0]-newpos[0]) <= 1 and abs(piece.pos[1]-newpos[1]) <= 1))
pieceLogic["_King"]=kingLogic

def pawnLogic(piece, newpos):
	squaresallowed = piece.hasMoved and 1 or 2 #piece.hasmoved and 1 or 2
	movedh = piece.name.startswith("W_") and (piece.pos[0] - newpos[0]) or (newpos[0] - piece.pos[0]) #Can't use abs like we would otherwise because pawns can't move backwards
	movedv = piece.name.startswith("W_") and (piece.pos[1] - newpos[1]) or (newpos[1] - piece.pos[1])
	if tempboard[newpos[0]][newpos[1]] != 0 and (bishopLogic(piece, newpos) and (abs(movedh) == 1 and movedv == 1)):
		return True
	return ((piece.pos[0] == newpos[0]) and (movedv <= squaresallowed) and (movedv > 0))
pieceLogic["_Pawn"]=pawnLogic

#Pull from table of logics
def pieceCanMove(piece, newpos, newboard):
	global tempboard
	tempboard = newboard
	for key in pieceLogic:
		if piece.name.endswith(key):
			return (pieceLogic[key](piece, newpos) and collisionLogic[key](piece, newpos))

	return True
