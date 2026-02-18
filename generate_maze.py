import random

DIRS = {
    'N': (0, -1),
    'S': (0, 1),
    'E': (1, 0),
    'W': (-1, 0)
}


class CellInfo:
    def __init__(self, cell):
        self.cell = cell
        self.is_visited = False
        self.walls = {
            'N': True,
            'S': True,
            'E': True,
            'W': True
        }

    @staticmethod
    def remove_wall(cell_a, cell_b):
        dx = cell_b.cell[0] - cell_a.cell[0]
        dy = cell_b.cell[1] - cell_a.cell[1]

        if dx == 1:
            cell_a.walls['E'] = False
            cell_b.walls['W'] = False
        elif dx == -1:
            cell_a.walls['W'] = False
            cell_b.walls['E'] = False
        elif dy == 1:
            cell_a.walls['S'] = False
            cell_b.walls['N'] = False
        elif dy == -1:
            cell_a.walls['N'] = False
            cell_b.walls['S'] = False


class MazeManager:
    def __init__(self):
        self.grid = {}
        self.frontier_edges = set()

    def initialise_grid(self, height, width):
        for x in range(height):
            for y in range(width):
                self.grid[(x, y)] = CellInfo((x, y))

    def add_frontier_from_cell(self, cell):
        x, y = cell.cell
        for dx, dy in DIRS.values():
            nx, ny = x + dx, y + dy
            if (nx, ny) in self.grid:
                neighbor = self.grid[(nx, ny)]
                if not neighbor.is_visited:
                    self.frontier_edges.add((cell, neighbor))

    def mark_start_cell(self, x, y):
        start = self.grid[(x, y)]
        start.is_visited = True
        self.add_frontier_from_cell(start)


def generate_maze_with_prim_algo(height=12, width=15, start=(2, 3)):
    maze = MazeManager()
    maze.initialise_grid(height, width)
    maze.mark_start_cell(*start)

    while maze.frontier_edges:
        cell_a, cell_b = random.choice(tuple(maze.frontier_edges))
        maze.frontier_edges.remove((cell_a, cell_b))

        if cell_b.is_visited:
            continue

        CellInfo.remove_wall(cell_a, cell_b)
        cell_b.is_visited = True
        maze.add_frontier_from_cell(cell_b)

    return maze


maze = generate_maze_with_prim_algo()

def print_maze(maze, height=12, width=15):
    grid = [['#' for _ in range(width*2+1)] for _ in range(height*2+1)]

    for x in range(height):
        for y in range(width):
            cx, cy = x*2+1, y*2+1
            grid[cx][cy] = ' '

            cell = maze.grid[(x, y)]

            if not cell.walls['N']:
                grid[cx-1][cy] = ' '
            if not cell.walls['S']:
                grid[cx+1][cy] = ' '
            if not cell.walls['W']:
                grid[cx][cy-1] = ' '
            if not cell.walls['E']:
                grid[cx][cy+1] = ' '

    for row in grid:
        print(''.join(row))


print_maze(maze)
