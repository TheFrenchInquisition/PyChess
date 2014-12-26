import math

piecelogic = {}
tempboard = False #2hacky5me

def collisionLogic(piece, newpos):
	return True

def rookLogic(piece, newpos):
	return ((piece.pos[0] == newpos[0]) or (piece.pos[1] == newpos[1]))
piecelogic["_Rook"]=rookLogic

def knightLogic(piece, newpos):
	diffx = abs(piece.pos[0]-newpos[0])
	diffy = abs(piece.pos[1]-newpos[1])
	return (diffx <= 2 and diffy <= 2 and diffx != 0 and diffy != 0 and diffx != diffy)
piecelogic["_Knight"]=knightLogic

def bishopLogic(piece, newpos):
	return (abs(piece.pos[1]-newpos[1]) == abs(piece.pos[0]-newpos[0]))
piecelogic["_Bishop"]=bishopLogic

def queenLogic(piece, newpos):
	return (rookLogic(piece, newpos) or bishopLogic(piece, newpos))
piecelogic["_Queen"]=queenLogic

def kingLogic(piece, newpos):
	return (queenLogic(piece, newpos) and (abs(piece.pos[0]-newpos[0]) <= 1 and abs(piece.pos[1]-newpos[1]) <= 1))
piecelogic["_King"]=kingLogic

def pawnLogic(piece, newpos):
	squaresallowed = piece.hasMoved and 1 or 2 #piece.hasmoved and 1 or 2
	movedh = piece.name.startswith("W_") and (piece.pos[0] - newpos[0]) or (newpos[0] - piece.pos[0]) #Can't use abs like we would otherwise because pawns can't move backwards
	movedv = piece.name.startswith("W_") and (piece.pos[1] - newpos[1]) or (newpos[1] - piece.pos[1])
	if tempboard[newpos[0]][newpos[1]] != 0 and (bishopLogic(piece, newpos) and (abs(movedh) == 1 and movedv == 1)):
		return True
	return ((piece.pos[0] == newpos[0]) and (movedv <= squaresallowed) and (movedv > 0))
piecelogic["_Pawn"]=pawnLogic

#Pull from table of logics
def pieceCanMove(piece, newpos, newboard):
	global tempboard
	tempboard = newboard
	for key in piecelogic:
		if piece.name.endswith(key):
			return (collisionLogic(piece, newpos) and piecelogic[key](piece, newpos))

	return True
