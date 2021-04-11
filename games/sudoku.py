import pygame, sys
from pygame.locals import *


WINDOW_WIDTH = 900
WINDOW_HEIGHT = 900
SCREEN_ASPECT_RATIO = WINDOW_WIDTH//WINDOW_HEIGHT
FPS = 30
WINDOW_MULTIPLIER = 5
SQUARE_MULTIPLIER = 3
CELL_MUTLTIPLIER = 3
#WINDOW_SIZE = 90 * SCREEN_ASPECT_RATIO
SQUARE_SIZE = [WINDOW_WIDTH // SQUARE_MULTIPLIER * SCREEN_ASPECT_RATIO, WINDOW_HEIGHT // SQUARE_MULTIPLIER * SCREEN_ASPECT_RATIO ]
CELL_SIZE = [SQUARE_SIZE[0] // CELL_MUTLTIPLIER , SQUARE_SIZE[1] // CELL_MUTLTIPLIER  ]#SQUARE_SIZE // 3 // SCREEN_ASPECT_RATIO
NUMBER_SIZE = [CELL_SIZE[0] /CELL_MUTLTIPLIER,CELL_SIZE[1] /CELL_MUTLTIPLIER]

BOARD_COLOR = (255,255,255)
GRID_COLOR = {
    'LIGHT_GRAY': (200, 200, 200),
    'Black': (0, 0, 0)
}


class Grid:
    def __init__(self, cells):
        self.cells = cells
       
    def draw_grid(self):
        for x in range(0, WINDOW_WIDTH, CELL_SIZE[0]): # draw vertical lines
            pygame.draw.line(DISPLAYSURF, GRID_COLOR['LIGHT_GRAY'], (x,0),(x,WINDOW_HEIGHT))
        
        for y in range (0, WINDOW_HEIGHT, CELL_SIZE[1]): # draw horizontal lines
            pygame.draw.line(DISPLAYSURF, GRID_COLOR['LIGHT_GRAY'], (0,y), (WINDOW_WIDTH, y))
        

        ### Draw Major Lines
        for x in range(0, WINDOW_WIDTH, SQUARE_SIZE[0]): # draw vertical lines
            pygame.draw.line(DISPLAYSURF, GRID_COLOR['Black'], (x,0),(x,WINDOW_HEIGHT))
       
        for y in range (0, WINDOW_HEIGHT, SQUARE_SIZE[1]): # draw horizontal lines
            pygame.draw.line(DISPLAYSURF, GRID_COLOR['Black'], (0,y), (WINDOW_WIDTH, y))
    

    def draw_cells(self):
        for cell in self.cells:
            cell.display()
            print(cell)
    
    def get_clicked_cell(self, pos):
        for cell in self.cells:
            print(f'cell: {cell} pos: {pos}')
            if cell.in_boundries(pos):
                return cell

        return None

    def shuffle(self):
        pass


class Cell:
    def __init__(self, coords, value, rect):
        self.coords = coords
        self.value = value
        self.rect = rect
    

    def display(self):
        cellSurf = BASICFONT.render('%s' %(self.value), True, GRID_COLOR['Black'])
        x = self.rect.x + self.rect.width/2
        y = self.rect.y + self.rect.height/2
        cellRect = cellSurf.get_rect(center = (x, y))
        #cellRect.topleft = (self.rect[0], self.rect[1])
        DISPLAYSURF.blit(cellSurf, cellRect)


    def in_boundries(self, pos):
        x = self.rect.x
        y = self.rect.y
        z = x + self.rect.width
        w = y + self.rect.height
        if pos[0] >= x and pos[0] < z and pos[1] >= y and pos[1] < w:
            return True

        return False
    
    def __str__(self):
        return f'Coords: {self.coords} -> Value: {self.value} Rect: {self.rect}'



class CellRect:
    def __init__(self,x ,y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __str__(self) -> str:
        return f'Rect x: {self.x} y: {self.y} width: {self.width} height: {self.height}'


def create_cells():
    cells = []
    for x in range(1,10):
        for y in range(1,10):
            #cell_rect = [ (y-1)*CELL_SIZE[1] + CELL_SIZE[1]//2 , (x-1)*CELL_SIZE[0] + CELL_SIZE[0]//2 ]
            i = (y-1)*CELL_SIZE[1]
            j = (x-1)*CELL_SIZE[0]
            width = CELL_SIZE[0]
            height = CELL_SIZE[1]
            cell_rect = CellRect(i,j,width,height)
            cells.append(Cell([x,y], (x+y - 2)%9 + 1, cell_rect))
    
    return cells


def main():

    global FPSCLOCK, DISPLAYSURF
    global BASICFONT, BASICFONTSIZE
    BASICFONTSIZE = 25
    pygame.font.init()
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    DISPLAYSURF.fill(BOARD_COLOR)

    
    grid = Grid(create_cells())
    grid.draw_grid()
    grid.draw_cells()

    pygame.mouse.get_pos()

    pygame.display.set_caption("Sudoku")
    
    while True: #main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                selected_cell = grid.get_clicked_cell(pos)

                if selected_cell is not None:
                    print(selected_cell.value)
                else:
                    print(f"Didnt found a cell in {pos} boundries")
        pygame.display.update()
        FPSCLOCK.tick(FPS)




if __name__=='__main__':
    main()