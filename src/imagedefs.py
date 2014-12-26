import pygame
#load images and stuff
selectimg = pygame.image.load("../images/select.png")
hightlightimg = pygame.image.load("../images/highlight.png")

pieceimages = {}
pieceimages["W_Pawn"] = pygame.image.load("../images/wpawn.png")
pieceimages["W_Rook"] = pygame.image.load("../images/wrook.png")
pieceimages["W_Knight"] = pygame.image.load("../images/wknight.png")
pieceimages["W_Bishop"] = pygame.image.load("../images/wbishop.png")
pieceimages["W_Queen"] = pygame.image.load("../images/wqueen.png")
pieceimages["W_King"] = pygame.image.load("../images/wking.png")

pieceimages["B_Pawn"] = pygame.image.load("../images/bpawn.png")
pieceimages["B_Rook"] = pygame.image.load("../images/brook.png")
pieceimages["B_Knight"] = pygame.image.load("../images/bknight.png")
pieceimages["B_Bishop"] = pygame.image.load("../images/bbishop.png")
pieceimages["B_Queen"] = pygame.image.load("../images/bqueen.png")
pieceimages["B_King"] = pygame.image.load("../images/bking.png")
