import random
from typing import Dict
from .Cell import Cell


class DFSGenerator:

    def __init__(self, configuration: Dict):

        self.configuration = configuration
        self.height = configuration["HEIGHT"]
        self.width = configuration["WIDTH"]
        self.entry = configuration["ENTRY"]
        self.exit = configuration["EXIT"]
        self.seed = configuration.get("SEED", None)

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
                row.append(Cell(i, j))
            self.grid.append(row)


    def remove_current_wall(self, row, col, new_row, new_col):

        current = self.grid[row][col]
        neighbor = self.grid[new_row][new_col]

        if row > new_row:  # move up
            current.walls['N'] = False
            neighbor.walls['S'] = False

        elif row < new_row:  # move down
            current.walls['S'] = False
            neighbor.walls['N'] = False

        elif new_col > col:  # move right
            current.walls['E'] = False
            neighbor.walls['W'] = False

        elif new_col < col:  # move left
            current.walls['W'] = False
            neighbor.walls['E'] = False

        return 1


    def visited_before_42(self):

        pattern_42 = [
            [1, 0, 0, 0, 1, 1, 1],
            [1, 0, 1, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 1],
        ]

        pattern_rows = len(pattern_42)
        pattern_cols = len(pattern_42[0])

        if pattern_rows > self.height or pattern_cols > self.width:
            print("Pattern too big for the grid!")
            return

        start_row = (self.height - pattern_rows) // 2
        start_col = (self.width - pattern_cols) // 2

        for i in range(pattern_rows):
            for j in range(pattern_cols):
                if pattern_42[i][j] == 1:
                    cell = self.grid[start_row + i][start_col + j]
                    cell.is_visited = True
                    cell.is_cell_42 = True

    def ft_algo(self):

        # Find start cell
        start_row, start_col = self.start
        start_cell = self.grid[start_row][start_col]
        start_cell.is_visited = True
        self.stack.append((start_row, start_col))

        while self.stack:

            row, col = self.stack[-1]

            neighbors = [
                (row + 1, col),
                (row - 1, col),
                (row, col + 1),
                (row, col - 1)
            ]

            random.shuffle(neighbors)

            moved = False

            for new_row, new_col in neighbors:

                if 0 <= new_row < self.height and 0 <= new_col < self.width:

                    neighbor = self.grid[new_row][new_col]

                    if not neighbor.is_visited:
                        neighbor.is_visited = True
                        self.stack.append((new_row, new_col))

                        self.remove_current_wall(row, col, new_row, new_col)

                        moved = True
                        break

                    elif random.random() < 0.1 and not neighbor.is_cell_42 and not self.configuration["PERFECT"]:
                        self.remove_current_wall(row, col, new_row, new_col)

            if not moved:
                self.stack.pop()
    def generate_grid_walls_for_solver(self):
        grid_walls = []
        for row in self.grid:
            row_walls = []
            for cell in row:
                cell_walls = [
                    1 if cell.walls['N'] else 0,
                    1 if cell.walls['E'] else 0,
                    1 if cell.walls['S'] else 0,
                    1 if cell.walls['W'] else 0,
                ]
                cell.solver_walls = cell_walls
                row_walls.append(cell.solver_walls)
            grid_walls.append(row_walls)
        return grid_walls

    def ft_show(self):

        for row in self.grid:

            # Top walls
            for cell in row:
                top = "-----" if cell.walls['N'] else "     "
                print(f"+{top}", end="")
            print("+")

            # Left walls + content
            for cell in row:
                left = "|" if cell.walls['W'] else " "
                content = " 42 " if cell.is_cell_42 else "    "
                print(f"{left}{content}", end="")
            print("|")

        # Bottom border
        for cell in self.grid[-1]:
            print("+-----", end="")
        print("+")


    def generate(self):
        self.visited_before_42()
        self.ft_algo()
        # self.ft_show()