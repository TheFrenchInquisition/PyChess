def pieceCanMove(piece, newpos):
	if piece.name.endswith("_Rook"):
		return ((piece.pos[0] == newpos[0]) or (piece.pos[1] == newpos[1]))
	return True
