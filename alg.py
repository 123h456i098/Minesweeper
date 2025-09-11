import random

class Algorithm:
    def __init__(self, board: list, height: int, width: int):
        self.board = board
        self.height = height
        self.width = width
    
    def display_results(self, constraints):
        new_constraints = list(filter(lambda x: x[1] > 0, constraints))
        print("=== MINES ===")
        return_mines = self.find_mines(new_constraints)
        safe_tiles = list(filter(lambda x: x[1] == 0, constraints))
        print("=== SAFE ===")
        return_safe = []
        for row in safe_tiles:
            print(f"{row[1]} = " + " + ".join(map(str, row[2:])))
            return_safe.extend(row[2:])
        return_safe = set(return_safe)
        wrongly_flagged = list(filter(lambda x: x[1] < 0, constraints))
        print("=== WRONG ===")
        return_wrong = set()
        for row in wrongly_flagged:
            print(row[0])
            return_wrong.add(row[0])
        return return_mines, return_safe, return_wrong

    def find_move(self, board_state: list):
        constraints = []
        for y in range(self.height):
            for x in range(self.width):
                if board_state[y][x] == "U" and self.board[y][x] > 0:
                    # For each uncovered tile
                    constraints.append([(x, y), self.board[y][x]])
                    for i in range(y - 1, y + 2):
                        for j in range(x - 1, x + 2):
                            if i >= 0 and j >= 0 and i < self.height and j < self.width:
                                if board_state[i][j] == "C":
                                    # Add any surrounding covered (unflagged) tiles to possibly add to the number on the uncovered tile
                                    constraints[-1].append((j, i))
                                elif board_state[i][j] == "F":
                                    # For each flagged tile, subtract from the number of possibly mines around the uncovered tile
                                    constraints[-1][1] -= 1
                                    # print(constraints[-1])
        # list(filter(lambda x: x != [0], constraints))
        return self.display_results(constraints)
        
        # mines = set()
        # for row in constraints:
        #     if len(row[1:]) == row[0]:
        #         for tile in row[1:]:
        #             mines.add(tile)
        # print(mines)
        # print(set(mines))
    
    def find_mines(self, constraints):
        mines = []
        change_occured = True
        while change_occured:
            change_occured = False
            to_delete = []
            for i, row in enumerate(constraints):
                if row[1] == len(row[2:]):
                    mines.extend(row[2:])
                    to_delete.append(i)
            print(mines)
            print(constraints)
            for each in reversed(to_delete):
                del(constraints[each])
            print(mines)
            print(constraints)
            for constraint_index, row in enumerate(constraints):
                for coords in mines:
                    if coords in row[2:]:
                        constraints[constraint_index].remove(coords)
                        constraints[constraint_index][1] -= 1
                        change_occured = True
            print(mines)
            print(constraints)
            print("=========")

        print(set(mines))
        return set(mines)

        
