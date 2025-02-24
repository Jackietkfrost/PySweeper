import random
from enum import Enum
class Difficulty(Enum):
    BEGINNER = (9, 9, 10)
    INTERMEDIATE = (16, 16, 40)
    EXPERT = (30, 16, 99)
    def __init__(self, width, height, num_mines):
        self.width = width
        self.height = height
        self.num_mines = num_mines

class Minesweeper:
    def __init__(self, difficulty=Difficulty.BEGINNER):
        """
        Initialize the Minesweeper game board.

        Sets up the game with a predetermined board size and number of mines. 
        Randomly places mines on the board and calculates numbers for non-mine cells, 
        indicating how many adjacent mines each cell has.

        Attributes:
            width (int): The width of the game board.
            height (int): The height of the game board.
            num_mines (int): The number of mines to place on the board.
            grid (list of list of int): 2D list representing the game board, 
                where -1 indicates a mine and other numbers indicate the count 
                of adjacent mines.
            revealed (list of list of bool): 2D list indicating whether each cell 
                has been revealed.
            game_over (bool): Flag indicating if the game is over.
        """

        self.difficulty = difficulty
        self.width = difficulty.width
        self.height = difficulty.height
        self.num_mines = difficulty.num_mines
        self.flags_remaining = self.num_mines
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.revealed = [[False for _ in range(self.width)] for _ in range(self.height)]
        self.game_over = False
        self.game_win = False

        # Randomly place mines
        mines_placed = 0
        while mines_placed < self.num_mines:
            x, y = random.randint(0, self.width-1), random.randint(0, self.height-1)
            if self.grid[y][x] == 0:
                self.grid[y][x] = -1
                mines_placed += 1

        # Calculate numbers for non-mine cells
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == -1:
                    continue
                count = 0
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if 0 <= x+dx < self.width and 0 <= y+dy < self.height:
                            if self.grid[y+dy][x+dx] == -1:
                                count += 1
                self.grid[y][x] = count

    def click(self, x, y):
        """
        Handle a click event at the specified coordinates (x, y).
        
        Reveals the cell at the given coordinates. If the cell contains a mine,
        sets the game as over. If the cell is empty, recursively reveals all 
        adjacent cells. Otherwise, reveals the number of adjacent mines.
        
        :param x: The x-coordinate of the clicked cell.
        :param y: The y-coordinate of the clicked cell.
        """

        if self.revealed[y][x]:
            return
        self.revealed[y][x] = True
        if self.grid[y][x] == -1:
            self.game_over = True
        elif self.grid[y][x] == 0:
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if 0 <= x+dx < self.width and 0 <= y+dy < self.height:
                        self.click(x+dx, y+dy)
    
    def check_win(self):
        unrevealed_tiles = sum(1 for row in self.revealed for cell in row if not cell)
        if unrevealed_tiles == self.num_mines:
            self.game_win = True
        return self.game_win