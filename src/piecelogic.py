import math

piecelogic = {}

def collisionLogic(piece, newpos):
	return True

def pawnLogic(piece, newpos):
	squaresallowed = 1 #piece.hasmoved and 1 or 2
	return ((piece.pos[0] == newpos[0]) and (abs(piece.pos[1] - newpos[1]) <= squaresallowed))
piecelogic["_Pawn"]=pawnLogic

def rookLogic(piece, newpos):
	return ((piece.pos[0] == newpos[0]) or (piece.pos[1] == newpos[1]))
piecelogic["_Rook"]=rookLogic

def bishopLogic(piece, newpos):
	return (abs(piece.pos[1]-newpos[1]) == abs(piece.pos[0]-newpos[0]))
piecelogic["_Bishop"]=bishopLogic

def queenLogic(piece, newpos):
	return (rookLogic(piece, newpos) or bishopLogic(piece, newpos))
piecelogic["_Queen"]=queenLogic

def kingLogic(piece, newpos):
	return (queenLogic(piece, newpos) and (abs(piece.pos[0]-newpos[0]) <= 1 and abs(piece.pos[1]-newpos[1]) <= 1))
piecelogic["_King"]=kingLogic

#Pull from table of logics
def pieceCanMove(piece, newpos):
	for key in piecelogic:
		if piece.name.endswith(key):
			return (collisionLogic(piece, newpos) and piecelogic[key](piece, newpos))

	return True
