import random
from Cell import Cell


DIRS = {
    'N': (0, -1),
    'S': (0, 1),
    'E': (1, 0),
    'W': (-1, 0)
}

CELLS_42_offset = [
    (0, -1), (0, -2), (0, -3), (0, 1), (0, 2), (0, 3),
    (1, 3), (1, -3),
    (2, -3), (2, 1), (2, 2), (2, 3),
    (-1, -1), (-1, 1),
    (-2, -1), (-2, 1), (-2, 2), (-2, 3)
]

class Maze:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.grid = [[Cell(x, y) for y in range(width)] for x in range(height)]
        self.frontier = set()

    def in_bounds(self, x, y):
        return 0 <= x < self.height and 0 <= y < self.width

    def add_frontier(self, cell):
        x, y = cell.x, cell.y
        for dir, (dx, dy) in DIRS.items():
            nx, ny = x + dx, y + dy
            if self.in_bounds(nx, ny):
                neighbor = self.grid[nx][ny]
                if not neighbor.is_visited:
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

    def mark_42_cell(self):
        mid_h = int(self.height/2)
        mid_w = int(self.width/2)

        for dx, dy in CELLS_42_offset:
            cell = self.grid[mid_h+dx-1][mid_w+dy-1]
            # print(f"{cell.x}, {cell.y}")
            # cell.is_visited = True
            cell.walls = {'N': False, 'S': False, 'E': False, 'W': False}
            self.is_cell_42 = True



    def generate(self, start_x=0, start_y=0):
        random.seed(42)
        start = self.grid[start_x][start_y]
        start.is_visited = True
        self.add_frontier(start)
        self.mark_42_cell()
        while self.frontier:
            cell_b = random.choice(tuple(self.frontier))
            self.frontier.remove(cell_b)

            visited_neighbors = []
            for dir, (dx, dy) in DIRS.items():
                nx, ny = cell_b.x + dx, cell_b.y + dy
                if self.in_bounds(nx, ny):
                    neighbor = self.grid[nx][ny]
                    if neighbor.is_visited:
                        visited_neighbors.append(neighbor)

            if visited_neighbors:
                cell_a = random.choice(visited_neighbors)
                self.remove_wall_between(cell_a, cell_b)

            cell_b.is_visited = True
            self.add_frontier(cell_b)
        

# maze = Maze(height=5, width=9)
# maze.generate(start_x=0, start_y=0)