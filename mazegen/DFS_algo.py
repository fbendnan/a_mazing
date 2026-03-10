import random
from typing import Dict, List, Tuple
from .Cell import Cell


class DFSGenerator:
    """
    Maze generator using the Depth-First Search (DFS) backtracking algorithm.

    This generator creates a maze by exploring cells recursively and
    backtracking when no unvisited neighbors remain.
    """

    def __init__(self, configuration: Dict) -> None:
        """
        Initialize the DFS maze generator.

        Args:
            configuration: Dictionary containing maze configuration
                parameters such as HEIGHT, WIDTH, ENTRY, EXIT,
                SEED, and PERFECT.
        """

        self.configuration: Dict = configuration
        self.height: int = configuration["HEIGHT"]
        self.width: int = configuration["WIDTH"]
        self.entry: Tuple[int, int] = configuration["ENTRY"]
        self.exit: Tuple[int, int] = configuration["EXIT"]
        self.seed: int | None = configuration.get("SEED", None)
        self.perfect: bool = configuration.get("PERFECT", True)

        if self.seed is not None:
            random.seed(self.seed)

        self.start: Tuple[int, int] = self.entry
        self.stack: List[Tuple[int, int]] = []
        self.grid: List[List[Cell]] = []

        self._init_grid()

    def _init_grid(self) -> None:
        """
        Initialize the maze grid with Cell objects.
        """
        for i in range(self.height):
            row: List[Cell] = []
            for j in range(self.width):
                row.append(Cell(i, j))
            self.grid.append(row)

    def remove_current_wall(
        self, row: int, col: int, new_row: int, new_col: int
    ) -> int:
        """
        Remove the wall between the current cell and its neighbor.

        Args:
            row: Current cell row.
            col: Current cell column.
            new_row: Neighbor cell row.
            new_col: Neighbor cell column.

        Returns:
            1 when the wall is successfully removed.
        """

        current = self.grid[row][col]
        neighbor = self.grid[new_row][new_col]

        if row > new_row:
            current.walls["N"] = False
            neighbor.walls["S"] = False

        elif row < new_row:
            current.walls["S"] = False
            neighbor.walls["N"] = False

        elif new_col > col:
            current.walls["E"] = False
            neighbor.walls["W"] = False

        elif new_col < col:
            current.walls["W"] = False
            neighbor.walls["E"] = False

        return 1

    def visited_before_42(self) -> None:
        """
        Mark a predefined '42 pattern' in the maze as visited cells.

        These cells are protected so the generator avoids modifying them.
        """

        pattern_42 = [
            [1, 0, 0, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
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

    def ft_algo(self) -> None:
        """
        Core DFS maze generation algorithm using a stack.
        """

        start_row, start_col = self.start
        start_cell = self.grid[start_row][start_col]
        start_cell.is_visited = True
        self.stack.append((start_row, start_col))

        while self.stack:

            row, col = self.stack[-1]

            neighbors: List[Tuple[int, int]] = [
                (row + 1, col),
                (row - 1, col),
                (row, col + 1),
                (row, col - 1),
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

                    elif (
                        random.random() < 0.1
                        and not neighbor.is_cell_42
                        and not self.configuration["PERFECT"]
                    ):
                        self.remove_current_wall(row, col, new_row, new_col)

            if not moved:
                self.stack.pop()

    def generate_grid_walls_for_solver(self) -> List[List[List[int]]]:
        """
        Convert the maze grid into a wall representation for the solver.

        Returns:
            A 3D list where each cell contains walls in the
            order [N, E, S, W].
        """

        grid_walls: List[List[List[int]]] = []

        for row in self.grid:
            row_walls: List[List[int]] = []

            for cell in row:
                cell_walls = [
                    1 if cell.walls["N"] else 0,
                    1 if cell.walls["E"] else 0,
                    1 if cell.walls["S"] else 0,
                    1 if cell.walls["W"] else 0,
                ]

                cell.solver_walls = cell_walls
                row_walls.append(cell.solver_walls)

            grid_walls.append(row_walls)

        return grid_walls

    def generate(self) -> None:
        """
        Generate the maze using the DFS algorithm.
        """

        self.visited_before_42()

        x, y = self.entry
        i, j = self.exit

        if self.grid[y][x].is_cell_42 or self.grid[j][i].is_cell_42:
            raise ValueError("Entry and exit should be outside 42")

        self.ft_algo()
