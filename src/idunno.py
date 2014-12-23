import pygame, sys
pygame.init()

size = [400, 400]
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("Chess")

#load images and stuff
wpawnimg = pygame.image.load("images\wpawn.png").convert_alpha()
wrookimg = pygame.image.load("images\wrook.png").convert_alpha()
wknightimg = pygame.image.load("images\wknight.png").convert_alpha()
wbishopimg = pygame.image.load("images\wbishop.png").convert_alpha()
wqueenimg = pygame.image.load("images\wqueen.png").convert_alpha()
wkingimg = pygame.image.load("images\wking.png").convert_alpha()
selectimg = pygame.image.load("images\select.png").convert_alpha()

somethingIsSelected = False
selected = (0, 0)
move = (0, 0)
flow = True
mpos = (0, 0)
alliedPiece = False
player1 = 'w'

board = [
    ['#', '#', '#', '#', '#', '#', '#', '#'],
    ['#', '#', '#', '#', '#', '#', '#', '#'],
    ['#', '#', '#', '#', '#', '#', '#', '#'],
    ['#', '#', '#', '#', '#', '#', '#', '#'],
    ['#', '#', '#', '#', '#', '#', '#', '#'],
    ['#', '#', '#', '#', '#', '#', '#', '#'],
    ['#', '#', '#', '#', '#', '#', '#', '#'],
    ['#', '#', '#', '#', '#', '#', '#', '#'],
    ]
#function getCPos takes a raw xy position on the board ex:(218, 129) and returns a chess position ex:(5, 6)
def getCPos(rpos):
    rxpos = rpos[0]-20
    if rxpos <= 45:
        nxpos = 1
    elif rxpos <=90:
        nxpos = 2
    elif rxpos <=135:
        nxpos = 3
    elif rxpos <=180:
        nxpos = 4
    elif rxpos <=225:
        nxpos = 5
    elif rxpos <=270:
        nxpos = 6
    elif rxpos <=315:
        nxpos = 7
    elif rxpos <=360:
        nxpos = 8
    rypos = rpos[1]-20
    if rypos <= 45:
        nypos = 8
    elif rypos <=90:
        nypos = 7
    elif rypos <=135:
        nypos = 6
    elif rypos <=180:
        nypos = 5
    elif rypos <=225:
        nypos = 4
    elif rypos <=270:
        nypos = 3
    elif rypos <=315:
        nypos = 2
    elif rypos <=360:
        nypos = 1
    return (nxpos, nypos)
#this does the opposite. will return value at top left corner of cpos
def getRPos(cpos):
    nxpos = cpos[0]*45-25
    nypos = cpos[1]*-45+380
    return (nxpos, nypos)
#function drawPieces takes characters from board[] and draws pieces to the screen depending upon their value
def drawPieces():
    global selected
    global somethingIsSelected
    global flow
    global mpos
    global selected
    for i in range(8):
        for k in range(8):
            ok = 7-k
            if board[i][k] == 'WP':
                screen.blit(wpawnimg, (i*45+20, ok*45+20))
            elif board[i][k] == 'WR':
                screen.blit(wrookimg, (i*45+20, ok*45+20))
            elif board[i][k] == 'WN':
                screen.blit(wknightimg, (i*45+20, ok*45+20))
            elif board[i][k] == 'WB':
                screen.blit(wbishopimg, (i*45+20, ok*45+20))
            elif board[i][k] == 'WQ':
                screen.blit(wqueenimg, (i*45+20, ok*45+20))
            elif board[i][k] == 'WK':
                screen.blit(wkingimg, (i*45+20, ok*45+20))
            if somethingIsSelected:
                if flow:   
                    flow = False
                screen.blit(selectimg, getRPos(selected))
            else:
                flow = True
#function cPiece takes a piece type and desired position ex:('WK', 5, 1) and sets position in board[]
def cPiece(piece, posl, posn):
    board[posl-1][posn-1] = piece
def checkIfAllied(cpos):
    checkpiece = board[cpos[0]-1][cpos[1]-1]
    whitepieces = ['WP', 'WR', 'WN', 'WB', 'WQ', 'WK']
    blackpieces = ['BP', 'BR', 'BN', 'BB', 'BQ', 'BK']
    if player1 == 'w':
        if checkpiece in whitepieces:
            return True
        else:
            return False
    else:
        if checkpiece == blackpieces:
            return True
        else:
            return False
def move(opos, npos):
    board[npos[0]-1][npos[1]-1] = board[opos[0]-1][opos[1]-1]
    board[opos[0]-1][opos[1]-1] = '#'
def select(pos):
    global somethingIsSelected
    global selected
    global move
    if somethingIsSelected and not checkIfAllied(pos):
        move(selected, pos)
        somethingIsSelected = False
    elif not somethingIsSelected and checkIfAllied(pos):
        selected = pos
        somethingIsSelected = True
screen.fill((102, 102, 102))

cPiece('WP', 1, 2)
cPiece('WR', 1, 1)
cPiece('WN', 2, 1)
cPiece('WB', 3, 1)
cPiece('WQ', 4, 1)
cPiece('WK', 5, 1)

clock = pygame.time.Clock()
#loopedy loop
while True:
    
    clock.tick(30)
    
    pygame.draw.rect(screen, (139, 125, 107), [20, 20, 360, 360])
    for i in range(4):
        for k in range(4):
            pygame.draw.rect(screen, (255, 228, 196), [i*90+20, k*90+20, 45, 45])
            pygame.draw.rect(screen, (255, 228, 196), [i*90+65, k*90+65, 45, 45])

    drawPieces()
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            select(getCPos(pygame.mouse.get_pos()))
    pygame.display.flip()
