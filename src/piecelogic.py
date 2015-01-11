import math

pieceLogic = {}
EMPTY = 0
tempboard = False #2hacky5me
lastmove = False
playerTurn = True

def promote(pos):
	pass

def isFree(pos):
	global tempboard
	row, col = pos[0], pos[1]
	if ((row < 0) or (col < 0) or (row > len(tempboard)-1) or (col > len(tempboard)-1)): return
	return tempboard[row][col] == EMPTY

def CLogic(piece, newpos, key):
     global tempboard
     global playerTurn
   
     squareamountx = abs(piece.pos[0]-newpos[0])
     squareamounty = abs(piece.pos[1]-newpos[1])
	
     if key != "_Bishop" and key != "_Queen" and key != "_King":  #for knights
         if tempboard[newpos[0]][newpos[1]] == 0:
		return True
	 elif playerTurn == True and tempboard[newpos[0]][newpos[1]].name.startswith("B_"):
		return True
	 elif playerTurn == False and tempboard[newpos[0]][newpos[1]].name.startswith("W_"):
		return True
     else:			
	 if squareamountx == 0:  #for bishops, queen and no castling yet for king and rook 
		for i in range(1, squareamounty):
			mod = (piece.pos[1] > newpos[1]) and -i or i
			testpos = (piece.pos[0], piece.pos[1]+mod)
			if not isFree(testpos):
				return False
	 elif squareamounty == 0:
		for i in range(1, squareamountx):
			mod = (piece.pos[0] > newpos[0]) and -i or i
			testpos = (piece.pos[0]+mod, piece.pos[1])
			if not isFree(testpos):
				return False
 	 else:
		squareamount = abs(piece.pos[0]-newpos[0])
		for i in range(1, squareamount):
			mod = (piece.pos[0] > newpos[0]) and -i or i
			mod2 = (piece.pos[1] > newpos[1]) and -i or i
			testpos = (piece.pos[0]+mod, piece.pos[1]+mod2)
			if not isFree(testpos):
				return False
		return True
	 return True

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
        global tempboard
	squaresallowed = piece.hasMoved and 1 or 2 #piece.hasmoved and 1 or 2
	movedh = piece.name.startswith("W_") and (piece.pos[0] - newpos[0]) or (newpos[0] - piece.pos[0]) #Can't use abs like we would otherwise because pawns can't move backwards
	movedv = piece.name.startswith("W_") and (piece.pos[1] - newpos[1]) or (newpos[1] - piece.pos[1])
	if tempboard[newpos[0]][newpos[1]] != 0 and (bishopLogic(piece, newpos) and (abs(movedh) == 1 and movedv == 1)):
		return True
	elif tempboard[newpos[0]][newpos[1]] != 0 and movedh == 0:
		return False
	return ((piece.pos[0] == newpos[0]) and (movedv <= squaresallowed) and (movedv > 0))
pieceLogic["_Pawn"]=pawnLogic


#Pull from table of logics
def pieceCanMove(piece, newpos, newboard, bool, turn):
	global tempboard
        global playerTurn
   
        playerTurn = turn
	tempboard = newboard
	for key in pieceLogic:
		if piece.name.endswith(key):
			return (pieceLogic[key](piece, newpos) and CLogic(piece, newpos, key))

	return True
