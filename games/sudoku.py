import pygame, sys
from pygame.locals import *


WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
SCREEN_ASPECT_RATIO = WINDOW_WIDTH//WINDOW_HEIGHT
FPS = 30
WINDOW_MULTIPLIER = 5 
WINDOW_SIZE = 90 * SCREEN_ASPECT_RATIO
SQUARE_SIZE = [WINDOW_WIDTH // 3 * SCREEN_ASPECT_RATIO, WINDOW_HEIGHT // 3 * SCREEN_ASPECT_RATIO ] #(WINDOW_SIZE * WINDOW_MULTIPLIER) // 3 // SCREEN_ASPECT_RATIO
CELL_SIZE = [SQUARE_SIZE[0] // 3 * SCREEN_ASPECT_RATIO, SQUARE_SIZE[1] // 3 * SCREEN_ASPECT_RATIO ]#SQUARE_SIZE // 3 // SCREEN_ASPECT_RATIO
NUMBER_SIZE = [CELL_SIZE[0] /3,CELL_SIZE[1] /3]

BOARD_COLOR = (255,255,255)
GRID_COLOR = {
    'LIGHT_GRAY': (200, 200, 200),
    'Black': (0, 0, 0)
}


def draw_grid():
    
    for x in range(0, WINDOW_WIDTH, CELL_SIZE[0]): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, GRID_COLOR['LIGHT_GRAY'], (x,0),(x,WINDOW_HEIGHT))
    for y in range (0, WINDOW_HEIGHT, CELL_SIZE[1]): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, GRID_COLOR['LIGHT_GRAY'], (0,y), (WINDOW_WIDTH, y))
        
    
    
    ### Draw Major Lines
    for x in range(0, WINDOW_WIDTH, SQUARE_SIZE[0]): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, GRID_COLOR['Black'], (x,0),(x,WINDOW_HEIGHT))
    for y in range (0, WINDOW_HEIGHT, SQUARE_SIZE[1]): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, GRID_COLOR['Black'], (0,y), (WINDOW_WIDTH, y))


def initiateCells():
    currentGrid = {}
    fullCell = [1,2,3,4,5,6,7,8,9]
    for xCoord in range(0,9):
        for yCoord in range(0,9):
            currentGrid[xCoord,yCoord] = list(fullCell) # Copies List
    return currentGrid


def displayCells(grid):
    # Create offset factors to display numbers in right location in cells.
    xFactor = 0
    yFactor = 0
    for item in grid: # item is x,y co-ordinate from 0 - 8
        cellData = grid[item] # isolates the numbers still available for that cell
        for number in cellData: #iterates through each number
            if number != ' ': # ignores those already dismissed
                xFactor = ((number-1)%3) # 1/4/7 = 0 2/5/8 = 1 3/6/9 =2
                if number <= 3:
                    yFactor = 0
                elif number <=6:
                    yFactor = 1
                else:
                    yFactor = 2
                #(item[0] * CELLSIZE) Positions in the right Cell
                #(xFactor*NUMBERSIZE) Offsets to position number    
                populateCells(number,(item[0]*CELL_SIZE[0])+(xFactor*NUMBER_SIZE[0]),(item[1]*CELL_SIZE[1])+(yFactor*NUMBER_SIZE[1]))


def populateCells(cellData, x, y):
    cellSurf = BASICFONT.render('%s' %(cellData), True, GRID_COLOR[''])
    cellRect = cellSurf.get_rect()
    cellRect.topleft = (x, y)
    DISPLAYSURF.blit(cellSurf, cellRect)


def main():

    global FPSCLOCK, DISPLAYSURF
    global BASICFONT, BASICFONTSIZE
    BASICFONTSIZE = 15
    pygame.font.init()
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
   

   
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    DISPLAYSURF.fill(BOARD_COLOR)
    grid = initiateCells()
    displayCells(grid)
    draw_grid()
    pygame.display.set_caption("Sudoku")
    

    while True: #main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        FPSCLOCK.tick(FPS)




if __name__=='__main__':
    main()