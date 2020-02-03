import pygame, random, time, math


#Global Variables
ROWS = 125
COLS = 125
CELL_SIZE = 4
INITIAL_POP = 0.07

def placeIMG(IMG, x, y):
    screen.blit(IMG, (x*CELL_SIZE, y*CELL_SIZE))

def randMatrix():
        return [[random.random() < INITIAL_POP for j in range(COLS)] for i in range(ROWS)]

def getNeighbors(cellAlive,x,y):
    count = 0
    for j in range((y-1),(y+2)):
        for i in range((x-1),(x+2)):
            if not ((i == x) and (j == y)):
                if cellAlive[i%COLS][j%ROWS]:
                    count += 1
    return count

def getNeighborsNoWrap(cellAlive,x,y):
    count = 0
    minY=(y-1) if (y-1)>0 else 0
    maxY=(y+2) if (y+2)<ROWS else ROWS
    minX=(x-1) if (x-1)>0 else 0
    maxX=(x+2) if (x+2)<COLS else COLS

    for j in range(minY,maxY):
        for i in range(minX,maxX):
            if not ((i == x) and (j == y)):
                if cellAlive[i][j]:
                    count += 1
    return count

def checkForStateChange(cellAlive):
    for j in range(ROWS):
        for i in range(COLS):
            n = getNeighborsNoWrap(cellAlive,i,j)
            if cellAlive[i][j]:
                if not (2 <= n <= 3):
                    cellAlive[i][j] = False
            else:
                if n == 3:
                    cellAlive[i][j] = True


def drawCells():
    for y in range(0,ROWS,1):
        for x in range(0,COLS,1):
            if cellAlive[x][y]:
                placeIMG(aliveIMG, x, y)
            else:
                placeIMG(deadIMG, x, y)

#Initalize the pygame
pygame.init()

#Create the Screen
screen = pygame.display.set_mode((COLS*CELL_SIZE,ROWS*CELL_SIZE))

#Title and Icon
pygame.display.set_caption("Conway's Game of Life")
icon = pygame.image.load("res\\alive_8.png")

pygame.display.set_icon(icon)

#Sprites
aliveIMG = pygame.image.load('res\\alive_4.png')
deadIMG = pygame.image.load('res\\dead_4.png')

#Data Structures
cellAlive = randMatrix()

#Game Loop
running = True
while running:
    #QUIT
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #BACKGROUND COLOR
    screen.fill((50, 50, 50))
    #DRAW MATRIX
    drawCells()

    pygame.display.update()
    checkForStateChange(cellAlive)
 