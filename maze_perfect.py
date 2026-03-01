import random
from typing import Dict

class PrimeGenerator:

    def __init__(self, configuration: Dict):

        self.configuration = configuration
        self.height = configuration["HEIGHT"]
        self.width = configuration["WIDTH"]
        self.entry = configuration["ENTRY"]
        self.exit = configuration["EXIT"]
        self.seed = configuration.get("SEED", None)
        self.perfect = configuration.get("PERFECT", True)

        if self.seed is not None:
            random.seed(self.seed)

        self.start = self.entry
        self.stack = []
        self.grid = []

        self._init_grid()

    def _init_grid(self):
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append({
                    "wall": [1,1,1,1],   # Top Right Bottom Left
                    "visit": False,
                    "pos": (i,j),
                    "is_42": False
                })
            self.grid.append(row)

    def ft_show(self, grid):

        for x in grid:

            for arr in x:
                top = "-----" if arr["wall"][0] == 1 else "     "
                print(f"+{top}", end="")
            print("+")

            for arr in x:
                left = "|" if arr["wall"][3] == 1 else " "
                content = " 42 " if arr["is_42"] else "    "
                print(f"{left}{content}", end="")
            print("|")

        for arr in grid[-1]:
            print("+-----", end="")
        print("+")


    def remove_current_wall(self, row , col , new_row ,new_col, grid):

        if row > new_row:
            grid[row][col]["wall"][0] = 0
            grid[new_row][new_col]["wall"][2] = 0

        elif row < new_row:
            grid[row][col]["wall"][2] = 0
            grid[new_row][new_col]["wall"][0] = 0

        elif new_col > col:
            grid[row][col]["wall"][1] = 0
            grid[new_row][new_col]["wall"][3] = 0

        elif new_col < col:
            grid[row][col]["wall"][3] = 0
            grid[new_row][new_col]["wall"][1] = 0

        return 1

    def visited_befor_42(self, grid, width, heigh):

        pattern_42 = [
            [1,0,0,0,1,1,1],
            [1,0,1,0,0,0,1],
            [1,1,1,0,1,1,1],
            [0,0,1,0,1,0,0],
            [0,0,1,0,1,1,1]
        ]

        pattern_rows = len(pattern_42)
        pattern_cols = len(pattern_42[0])

        start_row = (heigh - pattern_rows) // 2
        start_col = (width - pattern_cols) // 2

        if pattern_rows > heigh or pattern_cols > width:
            print("Pattern too big for the grid!")
            return

        for x in range(pattern_rows):
            for y in range(pattern_cols):
                if pattern_42[x][y] == 1:
                    grid[start_row + x][start_col + y]["visit"] = True
                    grid[start_row + x][start_col + y]["is_42"] = True
    def ft_algo(self, grid, width, heigh):

        for i in grid:
            for j in i:
                if j["pos"] == self.start:
                    j["visit"] = True
                    self.stack = [j["pos"]]

        while self.stack:

            row, col = self.stack[-1]

            neighbors = [
                (row+1,col),
                (row-1,col),
                (row,col+1),
                (row,col-1)
            ]

            random.shuffle(neighbors)

            check = 0

            for new_row, new_col in neighbors:

                if 0 <= new_row < heigh and 0 <= new_col < width:

                    if grid[new_row][new_col]["visit"] == False:

                        grid[new_row][new_col]["visit"] = True
                        self.stack.append((new_row,new_col))

                        check += self.remove_current_wall(row,col,new_row,new_col,grid)
                        break
       
            if check == 0:
                self.stack.pop()


    def main(self):
        self.visited_befor_42(self.grid, self.width, self.height)
        self.ft_algo(self.grid, self.width, self.height)
        self.ft_show(self.grid)


maze = PrimeGenerator(config)
maze.main()
