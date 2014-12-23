def pieceCanMove(piece, newpos):
	if piece.name.endswith("_Rook"):
		print(piece.pos[0], piece.pos[1], newpos[0], newpos[1])
		print ((piece.pos[0] == newpos[0]) or (piece.pos[1] == newpos[1]))
		pass
	return True
