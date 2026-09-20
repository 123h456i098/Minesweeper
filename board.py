import random

class Board:
    def __init__(self, width: int, height: int, num_mines: int, num_non_mines: int):
        self.width = width
        self.height = height
        self.set_mines(num_mines, num_non_mines)
        self.make_board()
        # self.print_board()
    
    def set_mines(self, num_mines: int, num_non_mines: int):
        self.mines = ["💣" for _ in range(num_mines)] + [0 for _ in range(num_non_mines)]
        random.shuffle(self.mines)

    def make_board(self):
        self.board = []
        for y in range(self.height):
            self.board.append(self.mines[y*self.width:(y+1)*self.width])        
        self.set_numbers()
        
    def set_numbers(self):
        for y, row in enumerate(self.board):
            for x, tile in enumerate(row):
                if tile == 0:
                    self.board[y][x] = self.find_surrounding_mines(x, y)

    def find_surrounding_mines(self, x: int, y: int):
        mines = 0
        for i in range(y - 1, y + 2):
            for j in range(x - 1, x + 2):
                if i >= 0 and j >= 0 and i < self.height and j < self.width:
                    if self.board[i][j] == "💣":
                        mines += 1
        return mines

    def print_board(self):
        for row in self.board:
            print(*row)

