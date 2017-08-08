import random
import pygame, sys
from pygame.locals import *

boardwidth = 4
boardheight = 4
tilesize = 80
windowwidth = 640
windowheight = 480
fps = 30
blank = None

black = (0,0,0)
white = (255,255,255)
brightblue = (0,50,255)
darkturqoise = (3,54,73)
green = (0,204,0)

bgcolor = darkturqoise
tilecolor = green
textcolor = white
boardercolor = brightblue
basicfontsize = 20

buttoncolor = white
buttontextcolor = white
messagecolor = white

xmargin= int((windowwidth- (boardwidth*tilesize))/2)
ymargin = int((windowheight - (boardheight*tilesize))/2)

def main():
	global displaysurf,fpslock

	fpslock = pygame.time.Clock()
	pygame.init()	
	displaysurf = pygame.display.set_mode((windowwidth,windowheight))
	displaysurf.fill(bgcolor)
	mainBoard = getRandomizeBoard()

	startAnimation(mainBoard)

	while True:

		for event in pygame.event.get():
			options(20,white)
			
			if event.type==QUIT:
				terminate()
			if event.type == KEYUP:
				key = event.key
				if isValidMove(key,mainBoard):
					move(key,mainBoard)	
					if hasWon(mainBoard):
						wonAnimation(mainBoard)
					
			if event.type == MOUSEMOTION:
				mousex, mousey= event.pos
				if hoverOption(mousex,mousey,20):
					options(20,black)

			if event.type == MOUSEBUTTONUP:
				mousex,mousey = event.pos
				if hoverOption(mousex, mousey,20):
					mainBoard = getRandomizeBoard()
					startAnimation(mainBoard)
					pygame.display.update()
					continue

				boxx, boxy = getBoxAtpixet(mousex, mousey)
				if boxx==None or boxy==None:
					continue
				elif boxx+1<boardheight and mainBoard[boxx+1][boxy]==0:
					move(274,mainBoard)	
				elif boxx-1>=0 and mainBoard[boxx-1][boxy]==0:
					move(273,mainBoard)	
				elif boxy+1<boardwidth and mainBoard[boxx][boxy+1]==0:
					move(275,mainBoard)	
				elif boxy-1>=0 and mainBoard[boxx][boxy-1]==0:
					move(276,mainBoard)			
				if hasWon(mainBoard):
					wonAnimation(mainBoard)

def moveAnimation(x1,y1,x2,y2,digit,key,coverage):
	if key == 273:
		left,top = topCoordinates(x2,y2)
		top+=tilesize
		left1,top1 = topCoordinates(x1,y1)
		for i in range(0,tilesize+coverage,coverage):
			pygame.draw.rect(displaysurf,bgcolor,(left1,top1,tilesize,tilesize*2))
			pygame.draw.rect(displaysurf,tilecolor,(left,top-tilesize-i,tilesize-2,tilesize-2))
			displayDigit(left,top-tilesize-i,digit)
			pygame.display.update()
			fpslock.tick(fps)
	elif key == 274:
		left,top = topCoordinates(x2,y2)
		left1,top1 = topCoordinates(x1,y1)
		top1+=tilesize
		for i in range(0,tilesize+coverage,coverage):
			pygame.draw.rect(displaysurf,bgcolor,(left,top,tilesize,tilesize*2))
			pygame.draw.rect(displaysurf,tilecolor,(left,top+i,tilesize-2,tilesize-2))
			displayDigit(left,top+i,digit)
			pygame.display.update()
			fpslock.tick(fps)	
	elif key == 275:
		left,top = topCoordinates(x2,y2)
		left1,top1 = topCoordinates(x1,y1)
		left1+=tilesize
		for i in range(0,tilesize+coverage,coverage):
			pygame.draw.rect(displaysurf,bgcolor,(left,top,tilesize*2,tilesize))
			pygame.draw.rect(displaysurf,tilecolor,(left+i,top,tilesize-2,tilesize-2))
			displayDigit(left+i,top,digit)
			pygame.display.update()
			fpslock.tick(fps)	
	elif key == 276:
		left,top = topCoordinates(x2,y2)
		left1,top1 = topCoordinates(x1,y1)
		left+=tilesize
		for i in range(0,tilesize+coverage,coverage):
			pygame.draw.rect(displaysurf,bgcolor,(left1,top1,tilesize*2,tilesize))
			pygame.draw.rect(displaysurf,tilecolor,(left-tilesize-i,top,tilesize-2,tilesize-2))
			displayDigit(left-tilesize-i,top,digit)
			pygame.display.update()
			fpslock.tick(fps)			

def move(key,board):
	for i in range(boardheight):
		for j in range(boardwidth):
			if board[i][j] == 0:
				x,y=i,j
				if key == 273:
					x+=1
				elif key == 274:
					x-=1
				elif key == 275:
					y-=1
				elif key == 276:
					y+=1
				moveAnimation(i,j,x,y,board[x][y],key,8)
				board[i][j],board[x][y] = board[x][y], board[i][j] 				
				return	

def isValidMove(move,board):
	if move == 273:
		for i in board[boardheight-1]:
			if i == 0:
				print i
				return False
		return True	

	elif move==274:
		for i in board[0]:
			if i==0:
				return False
		return True

	elif move == 275:
		for i in range(boardheight):
			if board[i][0] == 0:
				return False
		return True
	elif move == 276:
		for i in range(boardheight):
			if board[i][boardwidth-1] == 0:
				return False
		return True
				
def terminate():
	pygame.quit()
	sys.exit()

def getRandomizeBoard():
	a=[[i+j*boardwidth for i in range(boardwidth)] for j in range(boardheight)]
	for i in a:
		random.shuffle(i)
	random.shuffle(a)
	return a

def topCoordinates(x,y):
	left,top = xmargin + y*tilesize,ymargin + x*tilesize
	return left,top

def drawBoarder():
	left,top = topCoordinates(0,0)
	boardersize=4
	pygame.draw.rect(displaysurf,boardercolor,(left-boardersize,top-boardersize,boardwidth*tilesize+boardersize*2,boardheight*tilesize+boardersize*2))
	pygame.draw.rect(displaysurf,bgcolor,(left,top,boardwidth*tilesize,boardheight*tilesize))

def displayDigit(left,top,digit):
	fontObj = pygame.font.Font('freesansbold.ttf', basicfontsize)
	textSurfaceObj = fontObj.render(str(digit), True, textcolor,tilecolor)
	textRecteObj = textSurfaceObj.get_rect()
	textRecteObj.center = (left+tilesize/2,top+tilesize/2)
	displaysurf.blit(textSurfaceObj, textRecteObj)
	pygame.display.update()

def startAnimation(board):
	drawBoarder()
	showText()
	options(20, white)
	for i in range(boardheight):
		for j in range(boardwidth):
			if board[i][j] == 0:
				continue
			left,top = topCoordinates(i,j)
			pygame.draw.rect(displaysurf,tilecolor,(left,top,tilesize-2,tilesize-2))
			displayDigit(left,top,board[i][j])
	pygame.display.update()					

def hasWon(board):

	flag=0
	for i in range(boardheight):
		for j in range(boardwidth):
			if j == boardwidth-1 and i == boardheight-1:
				continue
			if board[i][j]!=(i*boardwidth+j+1):
				flag = 1
	if not flag:
		return True

	flag=0
	for i in range(boardwidth):
		for j in range(boardheight):
			if j == boardwidth-1 and i == boardheight-1:
				continue
			if board[j][i]!=(i*boardheight+j+1):
				flag = 1
	if not flag:
		return True		

	return False				
def getBoxAtpixet(x, y):
	for boxx in range(boardwidth):
		for boxy in range(boardheight):
			left,top = topCoordinates(boxx,boxy)
			boxRect= pygame.Rect(left,top,tilesize-2,tilesize-2)
			if boxRect.collidepoint(x,y):
				return (boxx,boxy)
	return (None,None)			

def hoverOption(x,y,size):
	boxRect= pygame.Rect(510,430,size*6,size+2)
	if boxRect.collidepoint(x,y):
		return True
	return False
		
def options(size,color):
	fontObj = pygame.font.Font('freesansbold.ttf', size)
	textSurfaceObj = fontObj.render('New Game', True, color,bgcolor)
	textRecteObj = textSurfaceObj.get_rect()
	textRecteObj.center = (560, 440)
	displaysurf.blit(textSurfaceObj,textRecteObj)
	pygame.display.update()	

def showText():
	fontObj = pygame.font.Font('freesansbold.ttf', 20)
	textSurfaceObj = fontObj.render('Click tile ot press arrow key to slide.', True, white,bgcolor)
	textRecteObj = textSurfaceObj.get_rect()
	textRecteObj.center = (180,20)
	displaysurf.blit(textSurfaceObj,textRecteObj)
	pygame.display.update()

def wonAnimation(board):
	color1 = brightblue
	color2 = bgcolor

	for i in range(13):
		color1,color2 = color2, color1
		displaysurf.fill(color1)
		startAnimation(board)
		pygame.display.update()
		pygame.time.wait(300)


if __name__ == '__main__':
	main()			
