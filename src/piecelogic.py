import math

def pieceCanMove(piece, newpos):
	if piece.name.endswith("_Rook"):
		return ((piece.pos[0] == newpos[0]) or (piece.pos[1] == newpos[1]))
	if piece.name.endswith("_Queen"):
		if piece.pos[0] == newpos[0]:
			return (abs(piece.pos[1]-newpos[1]) == 1)
		elif piece.pos[1] == newpos[1]:
			return (abs(piece.pos[0]-newpos[0]) == 1)
		else:
			if abs(piece.pos[1]-newpos[1]) == abs(piece.pos[0]-newpos[0]):
				return True
			else:
				return False
	return True
