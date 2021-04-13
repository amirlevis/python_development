import pygame, sys
from pygame.locals import *
from random import shuffle 


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
    'Cell': (200, 200, 200),
    'Square': (0, 0, 0),
    'Selected': (255,0,0)
}


ALLOWED_INPUTS = [1,2,3,4,5,6,7,8,9]

class Grid:
    def __init__(self, cells):
       
        self.grid = []
        for i in range(9):
            row = []
            for j in range(9):
                row.insert(0,cells.pop())
            self.grid.insert(0,row)

        #self.marked_cell_rect = None
       
    def draw_cell_grid(self):

        
        for x in range(0, WINDOW_WIDTH, CELL_SIZE[0]): # draw vertical lines
            pygame.draw.line(DISPLAYSURF, GRID_COLOR['Cell'], (x,0),(x,WINDOW_HEIGHT))
        
        for y in range (0, WINDOW_HEIGHT, CELL_SIZE[1]): # draw horizontal lines
            pygame.draw.line(DISPLAYSURF, GRID_COLOR['Cell'], (0,y), (WINDOW_WIDTH, y))
        

        ### Draw Major Lines
        for x in range(0, WINDOW_WIDTH, SQUARE_SIZE[0]): # draw vertical lines
            pygame.draw.line(DISPLAYSURF, GRID_COLOR['Square'], (x,0),(x,WINDOW_HEIGHT))
       
        for y in range (0, WINDOW_HEIGHT, SQUARE_SIZE[1]): # draw horizontal lines
            pygame.draw.line(DISPLAYSURF, GRID_COLOR['Square'], (0,y), (WINDOW_WIDTH, y))
    

    def draw_cells(self):
        for row in self.grid:
            for cell in row:
                cell.draw()
    

    def get_cell(self,coords):
        return self.grid[coords[1]][coords[0]]

    def get_rect(self, coords):
        rect = self.grid[coords[1]][coords[0]].rect
        return pygame.Rect(rect.x, rect.y, rect.width, rect.height)
      
    def get_clicked_cell(self, pos):
        for row in self.grid:
            for cell in row:
                if cell.in_boundries(pos):
                    return cell,[row.index(cell),self.grid.index(row)]

        return None

    
    def check_grid(self):
        for row in range(0,9):
            for col in range(0,9):
                if self.grid[row][col].value==0:
                    return False

        return True 

    def fill_grid(self):
        for i in range(81):
            row = int(i/9)
            col = int(i%9)

            if self.grid[row][col].value == 0:
                shuffle(ALLOWED_INPUTS)
                for value in ALLOWED_INPUTS: 
                    row_values = [cell.value for cell in self.grid[row]]
                    if not(value in row_values):
                        cell_column = [self.grid[0][col], self.grid[1][col],
                                  self.grid[2][col], self.grid[3][col], self.grid[4][col],
                                  self.grid[5][col], self.grid[6][col], self.grid[7][col],
                                  self.grid[8][col]]
                        
                        column_values = [cell.value for cell in cell_column]
                        if not value in column_values:
                            square=[]
                            if row<3:
                                if col<3:
                                    square=[self.grid[i][0:3] for i in range(0,3)]
                                elif col<6:
                                    square=[self.grid[i][3:6] for i in range(0,3)]
                                else:  
                                    square=[self.grid[i][6:9] for i in range(0,3)]
                            elif row<6:
                                if col<3:
                                    square=[self.grid[i][0:3] for i in range(3,6)]
                                elif col<6:
                                    square=[self.grid[i][3:6] for i in range(3,6)]
                                else:  
                                    square=[self.grid[i][6:9] for i in range(3,6)]
                            else:
                                if col<3:
                                    square=[self.grid[i][0:3] for i in range(6,9)]
                                elif col<6:
                                    square=[self.grid[i][3:6] for i in range(6,9)]
                                else:  
                                    square=[self.grid[i][6:9] for i in range(6,9)]
                            
                            if not value in ([cell.value for cell in square[0]] + [cell.value for cell in square[1]] + [cell.value for cell in square[2]]):
                                self.grid[row][col].clear()
                                self.grid[row][col].value=value
                                self.grid[row][col].draw()
                                if self.check_grid():
                                    return True
                                else:
                                    if self.fill_grid():
                                        return True
                break
        self.grid[row][col].value=0 

    

class Cell:
    def __init__(self, value, rect):
        self.value = value
        self.rect = rect
    

    def draw(self):
        self.cellSurf = BASICFONT.render('%s' %(self.value), True, GRID_COLOR['Square'])
        x = self.rect.x + self.rect.width/2
        y = self.rect.y + self.rect.height/2
        cellRect = self.cellSurf.get_rect(center = (x, y))
        pygame.draw.rect(DISPLAYSURF, GRID_COLOR['Cell'], self.rect, 2)
        DISPLAYSURF.blit(self.cellSurf, cellRect)


    def clear(self):
        self.cellSurf = BASICFONT.render('%s' %(''), True, BOARD_COLOR)
        DISPLAYSURF.fill(BOARD_COLOR, self.rect)
        DISPLAYSURF.blit(self.cellSurf, self.rect)


    def in_boundries(self, pos):
        x = self.rect.x
        y = self.rect.y
        z = x + self.rect.width
        w = y + self.rect.height
        if pos[0] >= x and pos[0] < z and pos[1] >= y and pos[1] < w:
            return True

        return False
    
    def __str__(self):
        return f'Value: {self.value} Rect: {self.rect}'


def create_cells():
    cells = []
    for x in range(1,10):
        for y in range(1,10):
            i = (y-1)*CELL_SIZE[1]
            j = (x-1)*CELL_SIZE[0]
            width = CELL_SIZE[0]
            height = CELL_SIZE[1]
            cell_rect = pygame.Rect(i,j,width,height)
            cells.append(Cell(0, cell_rect))
    
    return cells

def grid_navigation(event, grid, selected_cell, selected_cell_coords):
    if event.type == MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        pygame.draw.rect(DISPLAYSURF, GRID_COLOR['Cell'], selected_cell.rect, 3)
        selected_cell, selected_cell_coords = grid.get_clicked_cell(pos)
        if selected_cell is not None:
            print(selected_cell.value)
            
        else:
            print(f"Didnt found a cell in {pos} boundries")
    
    if event.type == KEYDOWN:
        if event.key == K_LEFT:
            if selected_cell_coords[0] - 1 >=0:
                selected_cell_coords[0] = selected_cell_coords[0] - 1
        if event.key == K_RIGHT:
            if selected_cell_coords[0] + 1 < 9:
                selected_cell_coords[0] = selected_cell_coords[0] + 1
        if event.key == K_UP:
            if selected_cell_coords[1] - 1 >= 0:
                selected_cell_coords[1] = selected_cell_coords[1] - 1
        if event.key == K_DOWN:
            if selected_cell_coords[1] + 1 < 9:
                selected_cell_coords[1] = selected_cell_coords[1] + 1
                        
        pygame.draw.rect(DISPLAYSURF, GRID_COLOR['Cell'], selected_cell.rect, 3)
        selected_cell = grid.get_cell(selected_cell_coords)
        print(selected_cell.value)


    return selected_cell, selected_cell_coords


def cell_value_change(event, cell, allowed_input = ALLOWED_INPUTS):
    if event.type == KEYDOWN:
        key = pygame.key.name(event.key)
        if key in allowed_input:
            cell.value = key
            cell.clear()
            cell.draw()
           


def generate_solved_grid():

    grid = Grid(create_cells())
    grid.draw_cell_grid()
    grid.fill_grid()
    return grid




def main():

    global FPSCLOCK, DISPLAYSURF
    global BASICFONT, BASICFONTSIZE
    BASICFONTSIZE = 25
    pygame.font.init()
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    DISPLAYSURF.fill(BOARD_COLOR)

    selected_cell_coords = [0,0]

    
    grid = generate_solved_grid()
    
    

    pygame.display.set_caption("Sudoku")

    selected_cell = grid.get_cell(selected_cell_coords)

    
    while True: #main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
           
            selected_cell, selected_cell_coords = grid_navigation(event, grid, selected_cell, selected_cell_coords)
            cell_value_change(event, selected_cell)
            pygame.draw.rect(DISPLAYSURF, (255,0,0), selected_cell.rect, 3)
            
            grid.draw_cell_grid()
                

        
        pygame.display.update()
        FPSCLOCK.tick(FPS)




if __name__=='__main__':
    main()