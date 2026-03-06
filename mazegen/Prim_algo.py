import random
from .Cell import Cell
from typing import Dict, Set, List, Tuple

DIRS: Dict[str, Tuple[int, int]] = {
    "N": (0, -1),
    "S": (0, 1),
    "E": (1, 0),
    "W": (-1, 0),
}

CELLS_42_offset: List[Tuple[int, int]] = [
    (0, -1), (0, -2), (0, -3), (0, 1), (0, 2), (0, 3),
    (-1, 3), (-1, -3),
    (-2, -3), (-2, 1), (-2, 2), (-2, 3),
    (1, -1), (1, 1),
    (2, -1), (2, 1), (2, 2), (2, 3)
]


class PrimeGenerator:
    """
    Maze generator based on Prim's algorithm.

    This class builds a maze grid, carves passages between cells,
    and optionally introduces loops to create non-perfect mazes.
    """

    def __init__(self, configuration: Dict) -> None:
        """
        Initialize the maze generator.

        Args:
            configuration: Dictionary containing maze configuration
                parameters such as HEIGHT, WIDTH, ENTRY, EXIT, SEED,
                and PERFECT.
        """
        self.configuration: Dict = configuration
        self.height: int = configuration["HEIGHT"]
        self.width: int = configuration["WIDTH"]
        self.entry: Tuple[int, int] = configuration["ENTRY"]
        self.exit: Tuple[int, int] = configuration["EXIT"]
        self.seed: int | None = configuration.get("SEED", None)
        self.perfect: bool = configuration.get("PERFECT", True)

        self.grid: List[List[Cell]] = [
            [Cell(row, col) for col in range(self.width)]
            for row in range(self.height)
        ]

        self.frontier: Set[Cell] = set()

    def in_bounds(self, row: int, col: int) -> bool:
        """
        Check if a coordinate is inside the maze boundaries.

        Args:
            row: Row index.
            col: Column index.

        Returns:
            True if the coordinate is inside the maze, False otherwise.
        """
        return 0 <= row < self.height and 0 <= col < self.width

    def mark_42_cell(self) -> None:
        """
        Mark special '42 cells' near the center of the maze.

        These cells are marked as visited so the generator
        avoids carving paths through them.
        """
        mid_h = self.height // 2
        mid_w = self.width // 2

        for dx, dy in CELLS_42_offset:
            nx = mid_h + dx
            ny = mid_w + dy

            if self.in_bounds(nx, ny):
                cell = self.grid[nx][ny]
                cell.is_cell_42 = True
                cell.is_visited = True

    def add_frontier(self, cell: Cell) -> None:
        """
        Add all unvisited neighbors of a cell to the frontier set.

        Args:
            cell: The current cell whose neighbors will be inspected.
        """
        for dx, dy in DIRS.values():
            nx, ny = cell.x + dx, cell.y + dy

            if self.in_bounds(nx, ny):
                neighbor = self.grid[nx][ny]

                if not neighbor.is_visited and not neighbor.is_cell_42:
                    self.frontier.add(neighbor)

    def remove_wall_between(self, cell_a: Cell, cell_b: Cell) -> None:
        """
        Remove the wall between two adjacent cells.

        Args:
            cell_a: First cell.
            cell_b: Second cell.
        """
        dx = cell_b.x - cell_a.x
        dy = cell_b.y - cell_a.y

        if dx == 1:
            cell_a.walls["S"] = False
            cell_b.walls["N"] = False
        elif dx == -1:
            cell_a.walls["N"] = False
            cell_b.walls["S"] = False
        elif dy == 1:
            cell_a.walls["E"] = False
            cell_b.walls["W"] = False
        elif dy == -1:
            cell_a.walls["W"] = False
            cell_b.walls["E"] = False

    def add_loops(self, loop_percent: float) -> None:
        """
        Add loops to the maze by randomly removing additional walls.

        Args:
            loop_percent: Percentage of cells used to determine
                          how many extra walls will be removed.
        """
        total_cells = self.height * self.width
        walls_to_remove = int(total_cells * loop_percent)

        for _ in range(walls_to_remove):

            row = random.randint(0, self.height - 1)
            col = random.randint(0, self.width - 1)

            cell = self.grid[row][col]

            dx, dy = random.choice(list(DIRS.values()))
            nx, ny = row + dx, col + dy

            if (
                self.in_bounds(nx, ny)
                and not self.grid[nx][ny].is_cell_42
                and not cell.is_cell_42
            ):
                neighbor = self.grid[nx][ny]
                self.remove_wall_between(cell, neighbor)

    def generate_grid_walls_for_solver(self) -> List[List[List[int]]]:
        """
        Convert the maze grid into a wall structure usable by the solver.

        Returns:
            A 3D list representing the walls of each cell
            in the order [N, E, S, W].
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

    def generate(self, start_x: int = 0, start_y: int = 0) -> None:
        """
        Generate the maze using Prim's algorithm.

        Args:
            start_x: Starting row position.
            start_y: Starting column position.
        """
        if self.seed is not None:
            random.seed(self.seed)

        x, y = self.entry
        i, j = self.exit

        self.mark_42_cell()

        if self.grid[x][y].is_cell_42 or self.grid[i][j].is_cell_42:
            raise ValueError("Entry and exit should be outside 42")

        start = self.grid[start_x][start_y]
        start.is_visited = True
        self.add_frontier(start)

        while self.frontier:
            cell_b = random.choice(
                sorted(self.frontier, key=lambda c: (c.x, c.y))
            )
            self.frontier.remove(cell_b)

            visited_neighbors: List[Cell] = []

            for dx, dy in DIRS.values():
                nx, ny = cell_b.x + dx, cell_b.y + dy

                if self.in_bounds(nx, ny):
                    neighbor = self.grid[nx][ny]

                    if neighbor.is_visited and not neighbor.is_cell_42:
                        visited_neighbors.append(neighbor)

            if visited_neighbors:
                cell_a = random.choice(visited_neighbors)
                self.remove_wall_between(cell_a, cell_b)

            cell_b.is_visited = True
            self.add_frontier(cell_b)

        if not self.perfect:
            self.add_loops(0.1)
