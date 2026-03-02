import random
from Cell import Cell
from typing import Dict, Set, List

DIRS = {
    'N': (0, -1),
    'S': (0, 1),
    'E': (1, 0),
    'W': (-1, 0)
}

CELLS_42_offset = [
    (0, -1), (0, -2), (0, -3), (0, 1), (0, 2), (0, 3),
    (-1, 3), (-1, -3),
    (-2, -3), (-2, 1), (-2, 2), (-2, 3),
    (1, -1), (1, 1),
    (2, -1), (2, 1), (2, 2), (2, 3)
]

#add generate grid walls for solver 

class PrimeGenerator:
    def __init__(self, configuration: Dict):
        self.configuration = configuration
        self.height = configuration["HEIGHT"]
        self.width = configuration["WIDTH"]
        self.entry = configuration["ENTRY"]
        self.exit = configuration["EXIT"]
        self.seed = configuration.get("SEED", None)
        self.perfect = configuration.get("PERFECT", True)
        self.grid = [[Cell(row, col) for col in range(configuration["WIDTH"])] for row in range(configuration["HEIGHT"])]
        self.frontier: Set = set()
        

    def in_bounds(self, row, col):
        return 0 <= row < self.height and 0 <= col < self.width

    def mark_42_cell(self):
        mid_h = self.height // 2
        mid_w = self.width // 2

        for dx, dy in CELLS_42_offset:
            nx = mid_h + dx
            ny = mid_w + dy

            if self.in_bounds(nx, ny):
                cell = self.grid[nx][ny]
                cell.is_cell_42 = True
                cell.is_visited = True


    def add_frontier(self, cell):
        for dx, dy in DIRS.values():
            nx, ny = cell.x + dx, cell.y + dy

            if self.in_bounds(nx, ny):
                neighbor = self.grid[nx][ny]

                if not neighbor.is_visited and not neighbor.is_cell_42:
                    self.frontier.add(neighbor)


    def remove_wall_between(self, cell_a, cell_b):
        dx = cell_b.x - cell_a.x
        dy = cell_b.y - cell_a.y

        if dx == 1:
            cell_a.walls['S'] = False
            cell_b.walls['N'] = False
        elif dx == -1:
            cell_a.walls['N'] = False
            cell_b.walls['S'] = False
        elif dy == 1:
            cell_a.walls['E'] = False
            cell_b.walls['W'] = False
        elif dy == -1:
            cell_a.walls['W'] = False
            cell_b.walls['E'] = False


    def add_loops(self, loop_percent):
        total_cells = self.height * self.width
        walls_to_remove = int(total_cells * loop_percent)

        for _ in range(walls_to_remove):
            
            row = random.randint(0, self.height - 1)
            col = random.randint(0, self.width - 1)
            
            cell = self.grid[row][col]
            
            dx, dy = random.choice(list(DIRS.values()))
            nx, ny = row + dx, col + dy

            if self.in_bounds(nx, ny) and not self.grid[nx][ny].is_cell_42:
                neighbor = self.grid[nx][ny]
                self.remove_wall_between(cell, neighbor)

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

    def generate(self, start_x=0, start_y=0):
        if self.seed is not None:
            random.seed(self.seed)


        self.mark_42_cell()
        start = self.grid[start_x][start_y]
        start.is_visited = True
        self.add_frontier(start)

        while self.frontier:
            cell_b = random.choice(sorted(self.frontier, key=lambda c: (c.x, c.y)))
            self.frontier.remove(cell_b)

            visited_neighbors = []

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

