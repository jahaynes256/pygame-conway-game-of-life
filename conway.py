import pygame, random, time, math, copy


#Global Variables
ROWS = 125
COLS = 125
CELL_SIZE = 4
INITIAL_POP = 0.20

# ---Debug Functions---
def matrixCheckSum(matrix):
    """
    Creates a unique (rare more accurately) ID to compare two 2D boolean lists.
    Unlikely to be different and return the same ID, but possible. Good enough.
    """
    checksum = 0
    for j in range(ROWS):
        for i in range(COLS):
            if matrix[i][j]:
                checksum+=i+j
    return checksum

def matrixComp(matrix,otherMatrix):
    """
    Compare two matrix checksums see previous function.
    """
    return matrixCheckSum(matrix) == matrixCheckSum(otherMatrix)
# ---End Debug Functions---

def placeIMG(IMG, x, y):
    """
    Display cell[x][y] with a rectangle with the top left being at (x*CELL_SIZE,y*CELL_SIZE)
    """
    screen.blit(IMG, (x*CELL_SIZE, y*CELL_SIZE))

def randMatrix():
    """
    Return a 2D List of True and False values with a INITIAL_POP chance to be true.
    Ex. If INITIAL_POP = 0.20 then 20% of values in the matrix will be True
    """
    return [[random.random() < INITIAL_POP for j in range(COLS)] for i in range(ROWS)]

def getNeighbors(cellAlive,x,y):
    """
    Uses torus topology, going left at (0,0) goes to right most value (MAX, 0)
    Return a count of cells adjacent to current cell. Ignore self.
    """
    count = 0
    for j in range((y-1),(y+2)):
        for i in range((x-1),(x+2)):
            if not ((i == x) and (j == y)):
                if cellAlive[i%COLS][j%ROWS]:
                    count += 1
    return count

def getNeighborsNoWrap(cellAlive,x,y):
    """
    Uses rectangular topology. Can't go beyond borders.
    Return a count of cells adjacent to current cell. Ignore self.
    """
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
    """
    The core logic of the Game of Life.

    Checks each cell for it neighbors and depending on the number of neighbors, kills it
    or resurects it. 
    
    Old version changed the matrix each iteration while checking it for
    the animation frame. This gives interesting cellular automata, but is not Conway's Game
    of Life. Fixed in latest version.
    """
    newCellAlive = copy.deepcopy(cellAlive)
    for j in range(ROWS):
        for i in range(COLS):
            n = getNeighborsNoWrap(cellAlive,i,j)
            if cellAlive[i][j]:
                if not (2 <= n <= 3):
                    newCellAlive[i][j] = False
            else:
                if n == 3:
                    newCellAlive[i][j] = True
    return newCellAlive
    

def drawCells(cellAlive):
    """
    Places the images that make up the graphics for the game.
    """
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
cAlive = randMatrix()

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
    drawCells(cAlive)
    pygame.display.update()
    cAlive = checkForStateChange(cAlive)
 