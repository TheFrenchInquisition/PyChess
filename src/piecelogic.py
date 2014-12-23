import math

piecelogic = {}

def rookLogic(piece, newpos):
	return ((piece.pos[0] == newpos[0]) or (piece.pos[1] == newpos[1]))
piecelogic["_Rook"]=rookLogic

def bishopLogic(piece, newpos):
	return (abs(piece.pos[1]-newpos[1]) == abs(piece.pos[0]-newpos[0]))
piecelogic["_Bishop"]=bishopLogic

def queenLogic(piece, newpos):
	return (rookLogic(piece, newpos) or bishopLogic(piece, newpos))

piecelogic["_Queen"]=queenLogic

#Pull from table of logics
def pieceCanMove(piece, newpos):
	for key in piecelogic:
		if piece.name.endswith(key):
			return piecelogic[key](piece, newpos)
	else:
		return True
