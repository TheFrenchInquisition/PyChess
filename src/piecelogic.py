import math

piecelogic = {}

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
def collisionLogic(piece, newpos):
	print("I don't even care anymore")
def pawnLogic(piece, newpos):
	if piece.name == "W_Pawn":
		if abs(piece.pos[1]-newpos[1]) == 1 and piece.pos[0] != newpos[0] and board[newpos[0]][newpos[1]] != 0:
			return True
		elif board[newpos[0]][newpos[1]] != 0:
			return False
		elif piece.pos[1] == 6:
			return (piece.pos[1]-newpos[1] < 3 and piece.pos[0] == newpos[0])
		else:
			return (piece.pos[1]-newpos[1] == 1 and piece.pos[0] == newpos[0])
	if piece.name == "B_Pawn":
		if abs(piece.pos[1]-newpos[1]) == 1 and piece.pos[0] != newpos[0] and board[newpos[0]][newpos[1]] != 0:
			return True
		elif board[newpos[0]][newpos[1]] != 0:
			return False
		elif piece.pos[1] == 1:
			return (piece.pos[1]-newpos[1] > -3 and piece.pos[0] == newpos[0])
		else:
			return (piece.pos[1]-newpos[1] == -1 and piece.pos[0] == newpos[0])
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
	if queenLogic(piece, newpos):
		return(abs(piece.pos[0]-newpos[0]) == 1 or abs(piece.pos[1]-newpos[1]) == 1)

piecelogic["_King"]=kingLogic

#Pull from table of logics
def pieceCanMove(piece, newpos):
	for key in piecelogic:
		if piece.name.endswith(key):
			return piecelogic[key](piece, newpos)
	else:
		return True
